"""Implementation of the Moran process on Graphs, with evolutionary rules."""

from collections import Counter
from typing import Callable, List, Optional, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
from axelrod import DEFAULT_TURNS, EvolvablePlayer, Game, Player
from axelrod.deterministic_cache import DeterministicCache
from axelrod.graph import Graph, complete_graph
from axelrod.match import Match
from axelrod.random_ import BulkRandomGenerator, RandomGenerator

class MainEvoEliteMoranProcess(object):
    def __init__(
        self,
        players: List[Player],
        turns: int = DEFAULT_TURNS,
        prob_end: float = None,
        noise: float = 0,
        game: Game = None,
        deterministic_cache: DeterministicCache = None,
        mutation_rate: float = 0.0,
        mode: str = "bd", #other option: "db"
        interaction_graph: Graph = None,
        reproduction_graph: Graph = None,
        fitness_transformation: Callable = None,
        mutation_method="transition", #other option: atomic (only for EvolvablePlayers)
        stop_on_fixation=True,
        seed=None,
    ) -> None:
        """
        An agent based Moran process class. In each round, each player plays a
        Match with each other player. Players are assigned a fitness score by
        their total score from all matches in the round. A player is chosen to
        reproduce 
        --proportionally to fitness--
        based on their fitness, where the best are first to be chosen

        , possibly mutated, and is cloned.
        The clone replaces the worst player.
        
        --The clone replaces a randomly chosen player.--

        If the mutation_rate is 0, the population will eventually fixate on
        exactly one player type. In this case a StopIteration exception is
        raised and the play stops. If the mutation_rate is not zero, then the
        process will iterate indefinitely, so mp.play() will never exit, and
        you should use the class as an iterator instead.

        When a player mutates it chooses a random player type from the initial
        population. This is not the only method yet emulates the common method
        in the literature.

        It is possible to pass interaction graphs and reproduction graphs to the
        Moran process. In this case, in each round, each player plays a
        Match with each neighboring player according to the interaction graph.
        Players are assigned a fitness score by their total score from all
        matches in the round. A player is chosen to reproduce proportionally to
        fitness, possibly mutated, and is cloned. The clone replaces a randomly
        chosen neighboring player according to the reproduction graph.

        Parameters
        ----------
        players
        turns:
            The number of turns in each pairwise interaction
        prob_end :
            The probability of a given turn ending a match
        noise:
            The background noise, if any. Randomly flips plays with probability
            `noise`.
        game: axelrod.Game
            The game object used to score matches.
        deterministic_cache:
            A optional prebuilt deterministic cache
        mutation_rate:
            The rate of mutation. Replicating players are mutated with
            probability `mutation_rate`
        mode:
            Birth-Death (bd) or Death-Birth (db)
        interaction_graph: Axelrod.graph.Graph
            The graph in which the replicators are arranged
        reproduction_graph: Axelrod.graph.Graph
            The reproduction graph, set equal to the interaction graph if not
            given
        fitness_transformation:
            A function mapping a score to a (non-negative) float
        mutation_method:
            A string indicating if the mutation method should be between original types ("transition")
            or based on the player's mutation method, if present ("atomic").
        stop_on_fixation:
            A bool indicating if the process should stop on fixation
        seed: int
            A random seed for reproducibility
        """
        m = mutation_method.lower()
        if m in ["atomic", "transition"]:
            self.mutation_method = m
        else:
            raise ValueError(
                "Invalid mutation method {}".format(mutation_method)
            )
        assert (mutation_rate >= 0) and (mutation_rate <= 1)
        assert (noise >= 0) and (noise <= 1)
        mode = mode.lower()
        assert mode in ["bd", "db"]
        self.mode = mode
        if deterministic_cache is not None:
            self.deterministic_cache = deterministic_cache
        else:
            self.deterministic_cache = DeterministicCache()
        self.turns = turns
        self.prob_end = prob_end
        self.game = game
        self.noise = noise
        self.initial_players = players  # save initial population
        self.players = []  # type: List
        self.populations = []  # type: List
        self.score_history = []  # type: List
        self.winning_strategy_name = None  # type: Optional[str]
        self.mutation_rate = mutation_rate
        self.stop_on_fixation = stop_on_fixation
        self._random = RandomGenerator(seed=seed)
        self._bulk_random = BulkRandomGenerator(self._random.random_seed_int())
        self.set_players()
        # Build the set of mutation targets
        # Determine the number of unique types (players)
        keys = set([str(p) for p in players])
        # Create a dictionary mapping each type to a set of representatives
        # of the other types
        d = dict()
        for p in players:
            d[str(p)] = p
        mutation_targets = dict()
        for key in sorted(keys):
            mutation_targets[key] = [
                v for (k, v) in sorted(d.items()) if k != key
            ]
        self.mutation_targets = mutation_targets

        if interaction_graph is None:
            interaction_graph = complete_graph(len(players), loops=False)
        if reproduction_graph is None:
            reproduction_graph = Graph(
                interaction_graph.edges, directed=interaction_graph.directed
            )
            reproduction_graph.add_loops()
        # Check equal vertices
        v1 = interaction_graph.vertices
        v2 = reproduction_graph.vertices
        assert list(v1) == list(v2)
        self.interaction_graph = interaction_graph
        self.reproduction_graph = reproduction_graph
        self.fitness_transformation = fitness_transformation
        # Map players to graph vertices
        self.locations = sorted(interaction_graph.vertices)
        self.index = dict(
            zip(sorted(interaction_graph.vertices), range(len(players)))
        )
        self.fixated = self.fixation_check()

    def set_players(self) -> None:
        """Copy the initial players into the first population, setting seeds as needed."""
        self.players = []
        for player in self.initial_players:
            if (self.mutation_method == "atomic") and issubclass(
                player.__class__, EvolvablePlayer
            ):
                # For reproducibility, we generate random seeds for evolvable players.
                seed = next(self._bulk_random)
                new_player = player.create_new(seed=seed)
                self.players.append(new_player)
            else:
                player.reset()
                self.players.append(player)
        self.populations = [self.population_distribution()]

    def fitness_proportionate_selection(
        self, scores: List, fitness_transformation: Callable = None
    ) -> int:
        """Randomly selects an individual proportionally to score.

        Parameters
        ----------
        scores: Any sequence of real numbers
        fitness_transformation: A function mapping a score to a (non-negative) float

        Returns
        -------
        An index of the above list selected at random proportionally to the list
        element divided by the total.

        """
        if fitness_transformation is None:
            csums = np.cumsum(scores) 
        else:
            csums = np.cumsum([fitness_transformation(s) for s in scores])
        total = csums[-1]

        #randomity
        r = self._random.random() * total



        for i, x in enumerate(csums): 
            if x >= r:
                break
        return i #an index that is located at location r

    def splitPlayersByScore(
        self, scores: List, fitness_transformation: Callable = None
    ) -> int:
        """Divides the players based on their scores, 
        according to median (half) or nth-percentile
        as threshold

        Parameters
        ----------
        scores: Any sequence of real numbers
        fitness_transformation: A function mapping a score to a (non-negative) float

        Returns
        -------
        2 lists of indexes derived from the above list, split according to fitness/score
        The first list is indices belonging to lower bound that will be eliminated
        The first list is indices belonging to upper bound that will be cloned

        """
        perc=25 #50 for median/half
        if fitness_transformation is None:
            #csums = np.cumsum(scores) #csums is ndarray list of dim 1
            print(scores)
            #scores is list of scores
            llim=np.percentile(scores,perc)
            ulim=np.percentile(scores,100-perc)
            print(llim)
            print("+++++++++++++++++")
            print(ulim)
            print("===========")

        else:
            array=[fitness_transformation(s) for s in scores]
            #csums = np.cumsum(array)
            print(array)
            llim=np.percentile(array,perc)
            ulim=np.percentile(array,100-perc)
            print(llim)
            print("+++++++++++++++++")
            print(ulim)
            print("===========")
            

        upp=[]
        low=[]
        for n,m in enumerate(scores):
            if m>ulim:
                upp.append(n)
            elif m<llim:
                low.append(n)
        if low==[]:
            print("empty lower")
            rl = self._random.randrange(0, len(self.players))
            low.append(rl)
        if upp==[]:
            print("empty upper")
            ru = self._random.randrange(0, len(self.players))
            upp.append(ru)
        print(low)
        print("***********************")
        print(upp)
        print("/////////////////////////")

            
        #total = csums[-1] #cumulative sum of scores #csums will be a list of cimulative sums
        #randomity
        #r = self._random.random() * total #r is fitness threshold


        #for i, x in enumerate(csums): #i is index of list
        #    if x >= r:#x is cumulative sum
        #        break
        return low,upp #2 lists of indices, one for culling and another for cloning

    def mutate(self, index: int) -> Player:
        """Mutate the player at index.

        Parameters
        ----------
        index:
            The index of the player to be mutated
        """

        if self.mutation_method == "atomic":
            if not issubclass(self.players[index].__class__, EvolvablePlayer):
                raise TypeError(
                    "Player is not evolvable. Use a subclass of EvolvablePlayer."
                )
            return self.players[index].mutate()

        # Assuming mutation_method == "transition"
        if self.mutation_rate > 0:
            # Choose another strategy at random from the initial population
            r = self._random.random()
            if r < self.mutation_rate:
                s = str(self.players[index])
                j = self._random.randrange(0, len(self.mutation_targets[s]))
                p = self.mutation_targets[s][j]
                return p.clone()
        # Just clone the player
        return self.players[index].clone()

    def getCulledandCloneList(self, index: int = None) -> int: #add count input arg/param
        """Produce the 2 list of indices that determines
        which player will be cloned and which one will
        be replaced with new clone
        

        Parameters
        ----------
        index:
            The index of the player to be copied
        """
        # Compute necessary fitnesses.
        scores = self.score_all()
        if index is not None:
            # Death has already occurred, so remove the dead player from the
            # possible choices
            scores.pop(index)
            # Make sure to get the correct index post-pop
        
        lowerList, upperList = self.splitPlayersByScore(
            scores, fitness_transformation=self.fitness_transformation
        )

        #get list of rank index
        #j=rankIndex[1]         #j= index of best player

        return lowerList, upperList

    def fixation_check(self) -> bool:
        """
        Checks if the population is all of a single type

        Returns
        -------
        Boolean:
            True if fixation has occurred (population all of a single type)
        """
        classes = set(str(p) for p in self.players)
        self.fixated = False
        if len(classes) == 1:
            # Set the winning strategy name variable
            self.winning_strategy_name = str(self.players[0])
            self.fixated = True
        return self.fixated

    def __next__(self) -> object:
        """
        Iterate the population:

        - play the round's matches
        - chooses a player proportionally to fitness (total score) to reproduce
        (change this part)
        - mutate, if appropriate
        - choose a player to be replaced
        (change this part)
        - update the population

        Returns
        -------
        MoranEvoEliteProcess:
            Returns itself with a new population
        """
        # Check the exit condition, that all players are of the same type.
        if self.stop_on_fixation and self.fixation_check():
            raise StopIteration

        #get 2 list of indices, one of which whose scores are 
        #under lower bounds and the other are above upper bounds    
        cullList, cloneList=self.getCulledandCloneList()

        # Mutate and/or replace player culled from cullList 
        # #with clone of player clone from cloneList
        counter=0
        for clone in cloneList: #cloneList is list of integers
            print("j is {}".format(clone))
            culled=cullList[counter] #cullList is list of integers
            print("k is {}".format(culled))
            self.players[culled]=self.mutate(clone)
            counter=counter+1

        # Record population.
        self.populations.append(self.population_distribution())
        return self

    def _matchup_indices(self) -> Set[Tuple[int, int]]:
        """
        Generate the matchup pairs.

        Returns
        -------
        indices:
            A set of 2 tuples of matchup pairs: the collection of all players
            who play each other.
        """
        indices = set()  # type: Set
        # For death-birth we only want the neighbors of the dead node
        # The other calculations are unnecessary
        if self.mode == "db":
            source = self.index[self.dead]
            self.dead = None
            sources = sorted(self.interaction_graph.out_vertices(source))
        else:
            # birth-death is global
            sources = sorted(self.locations)
        for i, source in enumerate(sources):
            for target in sorted(self.interaction_graph.out_vertices(source)):
                j = self.index[target]
                if (self.players[i] is None) or (self.players[j] is None):
                    continue
                # Don't duplicate matches
                if ((i, j) in indices) or ((j, i) in indices):
                    continue
                indices.add((i, j))
        return indices

    def score_all(self) -> List:
        """Plays the next round of the process. Every player is paired up
        against every other player and the total scores are recorded.

        Returns
        -------
        scores:
            List of scores for each player
        """
        N = len(self.players)
        scores = [0] * N
        for i, j in self._matchup_indices():
            player1 = self.players[i]
            player2 = self.players[j]
            match = Match(
                (player1, player2),
                turns=self.turns,
                prob_end=self.prob_end,
                noise=self.noise,
                game=self.game,
                deterministic_cache=self.deterministic_cache,
                seed=next(self._bulk_random),
            )
            match.play()
            match_scores = match.final_score_per_turn()
            scores[i] += match_scores[0]
            scores[j] += match_scores[1]
        self.score_history.append(scores)
        return scores

    def population_distribution(self) -> Counter:
        """Returns the population distribution of the last iteration.

        Returns
        -------
        counter:
            The counts of each strategy in the population of the last iteration
        """
        player_names = [str(player) for player in self.players]
        counter = Counter(player_names)
        return counter

    def __iter__(self) -> object:
        """
        Returns
        -------
        self
        """
        return self

    def reset(self) -> None:
        """Reset the process to replay."""
        self.winning_strategy_name = None
        self.score_history = []
        # Reset all the players
        self.set_players()

    def play(self) -> List[Counter]:
        """
        Play the process out to completion. If played with mutation this will
        not terminate.

        Returns
        -------
         populations:
            Returns a list of all the populations
        """
        if not self.stop_on_fixation or self.mutation_rate != 0:
            raise ValueError(
                "MoranEvoEliteProcess.play() will never exit if mutation_rate is"
                "nonzero or stop_on_fixation is False. Use iteration instead."
            )
        while True:
            try:
                self.__next__()
            except StopIteration:
                break
        return self.populations

    def __len__(self) -> int:
        """
        Returns
        -------
            The length of the Moran process: the number of populations
        """
        return len(self.populations)

    def populations_plot(self, ax=None):
        """
        Create a stackplot of the population distributions at each iteration of
        the Moran process.

        Parameters
        ----------------
        ax: matplotlib axis
            Allows the plot to be written to a given matplotlib axis.
            Default is None.

        Returns
        -----------
        A matplotlib axis object

        """
        player_names = self.populations[0].keys()
        if ax is None:
            _, ax = plt.subplots()
        else:
            ax = ax

        plot_data = []
        labels = []
        for name in player_names:
            labels.append(name)
            values = [counter[name] for counter in self.populations]
            plot_data.append(values)
            domain = range(len(values))

        ax.stackplot(domain, plot_data, labels=labels)
        ax.set_title("Moran Process Population by Iteration")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Number of Individuals")
        ax.legend()
        return ax
