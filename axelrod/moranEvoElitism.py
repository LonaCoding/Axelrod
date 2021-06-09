"""Implementation of the Moran process on Graphs, with elitist evolutionary rules."""

from collections import Counter
from typing import Callable, List, Optional, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
import math #needed for floor()
from axelrod import DEFAULT_TURNS, EvolvablePlayer, Game, Player
from axelrod.deterministic_cache import DeterministicCache
from axelrod.graph import Graph, complete_graph
from axelrod.match import Match
from axelrod.random_ import BulkRandomGenerator, RandomGenerator

#unless indicated, majority of this code was not created by me
#The only functions I modified and renamed:
#splitPlayersByScore: copied, then modified and renamed from fitness_proportionate_selection

class MainEvoEliteMoranProcess(object):
    def __init__( #with additional comments made by J Candra for reference
        self,
        players: List[Player],
        turns: int = DEFAULT_TURNS,
        prob_end: float = None,
        noise: float = 0,
        game: Game = None,
        deterministic_cache: DeterministicCache = None,
        mutation_rate: float = 0.0, #no mutation by default
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

    #The function below is no longer used, but kept here for reference for splitPlayersByScore
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
        r = self._random.random() * total

        for i, x in enumerate(csums):
            if x >= r:
                break
        return i

    #The function below is a version of fitness_proportionate_selection
    #adapted for Elitist Evolution and renamed for distinction.
    #Parts of this code are copied from fitness_proportionate_selection,
    #while others are written by J Candra
    def splitPlayersByScore(
        self, scores: List, fitness_transformation: Callable = None,splitThresholdPercentile=50
    ) -> int: #added input param argument for splitThresholdPercentile, which give nth-percentile
        """Divides the players based on their scores, 
        according to median (half) or nth-percentile
        as threshold

        This function is adapted from fitness_proportionate_selection for Elitist Evolution.
        Elitist Selection method is implemented.

        Parameters
        ----------
        scores: Any sequence of real numbers
        fitness_transformation: A function mapping a score to a (non-negative) float

        Returns
        -------
        2 lists of indexes derived from the above list, split according to fitness/score
        low: List of indices belonging to lower bound that will be eliminated
        upp: List of indices belonging to upper bound that will be cloned

        """
        #perc=50 #50 for median/half. 25 for quarter
        dispOutput=True #determines whether output will be printed to terminal or not

        if dispOutput:    
            print("~~~ Scores: ~~~")

        if fitness_transformation is None:
            #scores is list of scores
            llim=np.percentile(scores,splitThresholdPercentile)
            ulim=np.percentile(scores,100-splitThresholdPercentile)
            if dispOutput:
                print(scores)

        else:
            array=[fitness_transformation(s) for s in scores]            
            llim=np.percentile(array,splitThresholdPercentile)
            ulim=np.percentile(array,100-splitThresholdPercentile)
            if dispOutput:
                print(array)
        if dispOutput:    
            print("*** Thresholds: ***")
            print("+++ lower: +++")
            print(llim)
            print("+++ upper: +++")
            print(ulim)
            print("===========")
            
        #initialize list of indices
        upp=[] #upper: List of indices slected for cloning
        low=[] #lower: List of indices slected for culling/elimiation/replacement
        uppLim=[]
        lowLim=[]

        for n,m in enumerate(scores):
            if m>ulim: #if score exceeeds the upper threshold
                upp.append(n) #assign for cloning
            elif m<llim: #if score is below the lower threshold
                low.append(n) #assign for culling
            elif m==ulim: #if score matches the upper threshold
                uppLim.append(n)
            elif m==llim: #if score matches the lower threshold
                lowLim.append(n)

        PopulationSize=len(self.players)

        #implement list length checks. All list must be half of total population, 
        # unless population number is odd
        
        halfPop=math.floor(0.5*PopulationSize) #have it round down to floor value in case odd number. find the right function
        #alt: if value exceeds 0.5, reduce by 0.5
        #get someone from uppLim. use while loop

        while len(low)<halfPop: #loop does not trigger if length of low is eaqual or greater
            rand=self._random.randrange(0, len(lowLim))
            low.append(lowLim.pop(rand))
        while len(upp)<halfPop: #loop does not trigger if length of low is eaqual or greater
            rand=self._random.randrange(0, len(uppLim))
            upp.append(uppLim.pop(rand))

#        if low==[]:
#            print("empty lower")
            #to implement:
            #select half of total population 
            
#        if upp==[]:
#            print("empty upper")
            #to implement:
            #select half of total population at random, provided they have not been selected by low
            
        
        if low==[] & upp==[]:#if all score values are the same (thus both low and upp is empty)
            #create sequence of values of lenth equal to total players
            fullIndexList=list(range(PopulationSize)) #inspired by https://note.nkmk.me/en/python-range-usage/
            p=0
            while len(low)<halfPop:
                randLow = self._random.randrange(0, len(fullIndexList))
                #add to low the value that was popped from fullIndexList
                low.append(fullIndexList.pop(randLow))
                #randUpp = self._random.randrange(0, len(fullIndexList))
                #add to low the value that was popped from fullIndexList
                #upp.append(fullIndexList.pop(randUpp))
            
            upp=fullIndexList #copy the remaining list as upp
            if PopulationSize%2==1: #if PopulationSize is odd-number
                randPop = self._random.randrange(0, len(upp))
                midVal=upp.pop(randPop)





        if dispOutput:
            print("*** Split into lower and upper: ***")
            print("+++ lower: +++")     
            print(low)
            print("+++ lower threshold: +++")     
            print(lowLim)
            print("+++ upper: +++")
            print(upp)
            print("+++ upper threshold: +++")     
            print(uppLim)
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

    #The function below is no longer used, but kept here for reference for getCulledandCloneList
    def birth(self, index: int = None) -> int:
        """The birth event.

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
            j = self.fitness_proportionate_selection(
                scores, fitness_transformation=self.fitness_transformation
            )
            if j >= index:
                j += 1
        else:
            j = self.fitness_proportionate_selection(
                scores, fitness_transformation=self.fitness_transformation
            )
        return j

    #The function below is a slightly modified and renamed version
    #of birth(self, index: int = None).
    #Part of the function is still copied from birth().
    #Some parts were removed because unused and redundant

    def getCulledandCloneList(self, index: int = None) -> int: #add count input arg/param
        """Produce the 2 list of indices that determines
        which player will be cloned and which one will
        be replaced with new clone
        

        Parameters
        ----------
        index:
            The index of the player to be copied

        Returns
        -------
        2 lists of indexes derived from the above list, split according to fitness/score
        lowerList:
            List of indices belonging to lower bound that will be eliminated
        upperList:
            List of indices belonging to upper bound that will be cloned
        """
        # Compute necessary fitnesses.
        scores = self.score_all()
        if index is not None:
            # Death has already occurred, so remove the dead player from the
            # possible choices
            scores.pop(index)
            # Make sure to get the correct index post-pop
        
        lowerList, upperList = self.splitPlayersByScore( #this part is modified by J Candra
            scores, fitness_transformation=self.fitness_transformation #add percentile input arg here!
        )

        return lowerList, upperList #this part is modified by J Candra

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

    #Modified by J Candra from the function of same name, without renaming function. 
    # Original cannot be retained due to possible namespace clash
    #Original version can be found in moran.py under MoranProcess class
    def __next__(self) -> object:
        """
        Iterate the population:

        - play the round's matches
        - chooses a player proportionally to fitness (total score) to reproduce
        (change this part)
        - mutate, if appropriate
        - choose half of all the players to be replaced with copies of the other half
        - update the population

        Returns
        -------
        MainEvoEliteMoranProcess:
            Returns itself with a new population
        """
        # Check the exit condition, that all players are of the same type.
        if self.stop_on_fixation and self.fixation_check():
            raise StopIteration

        #Perform score calculation and
        #get 2 list of indices, one of which whose scores are 
        #under lower bounds and represents players to be culled,
        #and the other are above upper bounds and represents players 
        #to be cloned and/or mutated    
        cullList, cloneList=self.getCulledandCloneList()

        #Mutate and/or replace player pCull from cullList 
        #with clone or mutated clone of player pClone from cloneList
        counter=0        

        for pClone in cloneList: #cloneList is list of integers
            #implement error handling or preventative measure
            #when pCull is list index value that is out of range
            #due to counter exceeding list length
            if counter>=len(cullList):
                break #stop the replacement process
            print("j is {}".format(pClone))
            pCull=cullList[counter] #cullList is list of integers
            print("k is {}".format(pCull))
            self.players[pCull]=self.mutate(pClone)
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

    #minor modifications to docs
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
