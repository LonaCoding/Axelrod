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

        #0  10  -   10
        #1  9   -   8
        #2  8   -   6
        #3  7   -   4
        #4  6   -   2
        #5  5       0
        #6  4       2
        #7  3       4
        #8  2       6
        #9  1       8
        #10 0       10

        #threshold changes between 10 and 0


        if C_counts - D_counts >= threshold:
            return C
        elif D_counts - C_counts >= threshold:
            return D
        else:
            return opponent.history[-1]


class ShortMemProbabilistic(Player):
    """
    A player starts by always cooperating for the first 10 moves.

    From the tenth round on, the player analyzes the last ten actions, 
    counts the number of defections
    and
    randomly decides wether to defect or cooperate, but
    with the likelihood to defect increasing the more often
    the opponent defects

    
    
    Then, apply fuzzy logic or probabilistic decision-making.


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
        cooperateProb=C_counts/10 #the higher it is, the more likely to cooperate

        #self._random.random_choice(self.cooperateProb) #example reference taken from random.py
        randDefect1=random.random() #1 is not included
        if randDefect1<=defectProb:
            return D
        else: #50-50 chance of being cooperative or mimicking opponent's previous move (Tit-for-Tat)
            randCoop2=random.random()
            generousTolerance=50 #Probability to choose to tolerate opponent and shows that willing to cooperate on their own volition instead of TFT
            generousToleranceProb=generousTolerance/100
            if randCoop2>=generousToleranceProb:
                return C
            else:
                return opponent.history[-1] #play Tit-for-Tat


        #if opponent defected all the time

class ShortMemProbabilisticFuzzy(Player):
    """
    A player starts by always cooperating for the first 10 moves.

    From the tenth round on, the player analyzes the last ten actions, 
    counts the number of defections
    and
    randomly decides wether to defect or cooperate, but
    with the likelihood to defect increasing the more often
    the opponent defects

    This simulates simplified version of fuzzy logic, where 
    the player does not decide to absolutely defect or cooperate,
    but to consider doubt as well
    e.g. I am 90% sure that I should choose to defect, 
    because my opponent defects during 90% of the 10 last matches

    According to payoff matrix, if player A is sure that player B
    will defect, the choice player A can make with the least losses
    is to defect, rather than cooperate and end up being the sucker.
    If player A is sure that player B
    will defect, the choice player A can make with the least losses
    is to defect
    
    
    Then, attempt to simulate fuzzy logic or probabilistic decision-making
    using several random numbers generated by random.random()
    and thresholding.


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

        if len(opponent.history) <= 10:
            return C

        array = opponent.history[-10:] #fetch the last 10 moves of the opponent and out into array
        C_counts = array.count(C)
        D_counts = array.count(D)

        CtoDdiff=C_counts - D_counts


        #use C_counts and D_counts to adjust probability
        #the higher the D_counts (opponent defect), the more likely it will defect
        
        defectProb=D_counts/10 #the higher it is, the more likely to defect
        coopProb=C_counts/10 #the higher it is, the more likely to cooperate

        randDefect=random.random() #1 is not included
        if randDefect<=defectProb: #if random value does not pass threshold (more likeely as defection increases), consider defecting
            preferDefect=1
        else: #if random value passes threshold (less likely as defection increases), consider not defecting
            preferDefect=0
            
        randCoop=random.random() #1 is not included
        if randCoop<=coopProb: #if random value does not pass threshold (more likeely as defection increases), consider defecting
            preferCoop=1
        else: #if random value passes threshold (less likely as defection increases), consider not defecting    
            preferCoop=0

        if preferDefect==1 and  preferCoop==0: #situation = d x d (defect)
            return D
        elif preferDefect==0 and  preferCoop==1: #situation = 10-d x 10-d (cooperate)
            return C
        else: #situation = 10-d x d or d x 10-d (uncertain)
            #do second check 
            #defect should be greater than cooperate 
            #40:30:30
            TFTbias=10 #scale: 1 to 100
            MajorityBias=5 #Dominant's bias. Apply to which one matches the opponent's move
            TFTprob=(1/3)+(TFTbias/100) #Calculate TFT first because it should be greater than or equal to pure defect or cooperate
            MajorityProb=((1-TFTprob)/2)+(MajorityBias/100)
            #SubProb=1-TFTprob-DomProb
            randUncertain=random.random()
            if randUncertain<=TFTprob:
                return opponent.history[-1] #play Tit-for-Tat
            elif randUncertain<=MajorityProb:
                if C_counts>D_counts:
                    return C
                elif D_counts<C_counts:
                    return D
                else:
                    # do random
                    MajorityTiebreakerRand=random.random()
                    if MajorityTiebreakerRand<0.5:
                        return C
                    else: 
                        return D
            else: #SubProb=1-TFTprob-DomProb
                if C_counts>D_counts:
                    return D
                elif D_counts<C_counts:
                    return C
                else:
                    # do random
                    MinorityTiebreakerRand=random.random()
                    if MinorityTiebreakerRand<0.5:
                        return C
                    else: 
                        return D

        #make fuzzy logic:
        #                                           probability tables
        #   d                           0   1   2   3   4   5   6   7   8   9   10 
        #situation = d x d              0   1   4   9   16  25  36  49  64  81  100
        #situation = d x (10-d)         0   9   16  21  24  25  24  21  16  9   0
        #situation = (10-d) x d         0   9   16  21  24  25  24  21  16  9   0
        #situation = (10-d) x (10-d)    100 81  64  49  36  25  16  9   4   1   0                                                                      1
        #                                                  (n/2)^

            #50-50 chance of being cooperative or mimicking opponent's previous move (Tit-for-Tat)
            #randCoop2=random.random()
            #if randCoop2>=0.5:
            #    return C
            #else:
            #    return opponent.history[-1] #play Tit-for-Tat


        #if opponent defected all the time
