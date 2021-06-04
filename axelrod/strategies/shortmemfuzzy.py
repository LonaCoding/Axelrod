from axelrod import Player
from axelrod.action import Action

C, D = Action.C, Action.D


class ShortMemFuzzy(Player):
    """
    A player starts by always cooperating for the first 10 moves.

    From the tenth round on, the player analyzes the last ten actions, and
    compare the number of defects and cooperates of the opponent, based in
    percentage. 
    
    Then, apply fuzzy logic or probabilistic decision-making.

    If cooperation occurs 30% more than defection, it will
    cooperate.
    If defection occurs 30% more than cooperation, the program will defect.
    Otherwise, the program follows the TitForTat algorithm.


    Names:

    - ShortMem: [Andre2013]_
    """

    name = "ShortMemFuzzy"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""

        threshold=3

        if len(opponent.history) <= 10:
            return C

        array = opponent.history[-10:] #fetch the last 10 moves of the opponent and out into array
        C_counts = array.count(C)
        D_counts = array.count(D)

        CtoDdiff=C_counts - D_counts

        if opponent.defections > len(opponent.history) / 10.0:
            return D
        return C

        if C_counts - D_counts >= threshold:
            #add fuzzy probabilistic

            return C
        elif D_counts - C_counts >= threshold:
            #add fuzzy probabilistic

            return D
        else:
            return opponent.history[-1]