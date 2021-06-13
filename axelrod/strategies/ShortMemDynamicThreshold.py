from axelrod import Player
from axelrod.action import Action
import random

C, D = Action.C, Action.D


class ShortMemDynamicThreshold(Player):
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

    name = "ShortMemDynamicThreshold"
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

        threshold=3 #have this parameter adjustable, if possible, from outside (as input argument)

        if len(opponent.history) <= 10:
            return C

        array = opponent.history[-10:] #fetch the last 10 moves of the opponent and out into array
        C_counts = array.count(C)
        D_counts = array.count(D)

        CtoDdiff=C_counts - D_counts

        if C_counts - D_counts >= threshold:
            return C
        elif D_counts - C_counts >= threshold:
            return D
        else:
            return opponent.history[-1]

        #use C_counts and D_counts to adjust probability
        #the higher the D_counts (opponent defect), the more likely it will defect
        
        defectProb=D_counts/10 #the higher it is, the more likely to defect

        randDefect1=random.random() #1 is not included
        if randDefect1<=defectProb:
            return D
        else: #50-50 chance of being cooperative or mimicking opponent's previous move (Tit-for-Tat)
            randCoop2=random.random()
            if randCoop2>=0.5:
                return C
            else:
                return opponent.history[-1] #play Tit-for-Tat


        #if opponent defected all the time


class ShortMemProbabilistic(Player):
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

    name = "ShortMemDynamicThreshold"
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

        threshold=3 #have this parameter adjustable, if possible, from outside (as input argument)

        if len(opponent.history) <= 10:
            return C

        array = opponent.history[-10:] #fetch the last 10 moves of the opponent and out into array
        C_counts = array.count(C)
        D_counts = array.count(D)

        CtoDdiff=C_counts - D_counts

        #use C_counts and D_counts to adjust probability
        #the higher the D_counts (opponent defect), the more likely it will defect
        
        defectProb=D_counts/10 #the higher it is, the more likely to defect

        randDefect1=random.random() #1 is not included
        if randDefect1<=defectProb:
            return D
        else: #50-50 chance of being cooperative or mimicking opponent's previous move (Tit-for-Tat)
            randCoop2=random.random()
            if randCoop2>=0.5:
                return C
            else:
                return opponent.history[-1] #play Tit-for-Tat


        #if opponent defected all the time
