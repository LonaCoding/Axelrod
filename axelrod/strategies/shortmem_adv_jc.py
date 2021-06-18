from axelrod import Player
from axelrod.action import Action
import random
import math

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
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    #copied and adapted from rand.py
    def __init__(self, offset: int = 0, uniform = False) -> None:
        """
        Parameters
        ----------
        offset, int
            How far should the starting value be.
            If uniform is set to false, use radians or degree values (e.g. 30, 210)
            Else, values starting from 16 will start to repeat the first 16 values
            Modulus 16 is used in this case.

        uniform, boolean
            Whether to use the uniform-increase-and-decrease method, where values increment and decrement by 1 all the time,
            or to use the non-uniform sine method, where values are determined by sine function and median is  not exactly in the middle

        """
        super().__init__()
        assert uniform in [True, False]
        self.offset = offset
        self.uniform = uniform


    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""

        #threshold=3 #have this parameter adjustable, if possible, from outside (as input argument)

        if len(opponent.history) <= 10:
            return C

        array = opponent.history[-10:] #fetch the last 10 moves of the opponent and out into array
        C_counts = array.count(C)
        D_counts = array.count(D)

        CtoDdiff=C_counts - D_counts
        # 10(-) =    0    -    10     
        # 8 (-) =    1    -    9      
        # 6 (-) =    2    -    8      
        # 4 (-) =    3    -    7      
        # 2 (-) =    4    -    6      
        # 0     =    5    -    5       
        # 2     =    6    -    4       
        # 4     =    7    -    3       
        # 6     =    8    -    2       
        # 8     =    9    -    1       
        # 10    =    10   -    0       

        #threshold changes between 1 and 9
        
        #offset=0 #30 if want to start halfway to max (7), 90 if want to start high (9), 270 if want to start low (1). have this parameter adjustable, if possible, from outside (as input argument)

        if uniform:        
            #The uniform method. Median is exactly in middle
            count=(len(opponent.history)+offset-10)%16
            if count>=8:
                threshold=(16-count)+1
            else:
                threshold=count+1
        else:    
            #the sine method. Value changes are not uniform. Median is not exactly in middle
            threshold=(4*round(math.sin(math.radians((len(opponent.history)-10)*22.5)+offset),1))+5

            #        threshold   sine     offset=0    offset value in order to start there               
            #minimum:   1        (-1)    -     22          270
            #q1:        3        (-0.5)  -   20  24        210/330
            #median/q2: 5        (0)     10  18  26        0
            #q3:        7        (0.5)   12  16            30/150
            #maximum:   9        (1)       14              90  

            #oscillate between these numbers using sine function, so that no counters were needed
            #use length of opponent history as x but convert to radian
            #new threshold= 4sin(x)+5
            #x=length_opponenthistory-10)*22.5 in radians
        

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


    Inspired by:

    - ShortMem: [Andre2013]_
    """

    name = "ShortMemProbabilistic"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    
    def __init__(self, generousTolerance: int = 50) -> None:
        """
        Parameters
        ----------
        generousTolerance, int
            Probability of choosing to cooperate irather than TFT, once it decided it does not want to defect,
            or to choose to tolerate opponent and shows that it is willing to cooperate on their own volition instead of TFT
            The higher it is, the more often it cooperates and the more generous it is
            even if opponent defects, which could invite mutual cooperation with certain strategies.
            Range of values: 0 to 100, on a scale of 100
            If set to 0, it will always TFT.
            If set to 100, it will always Cooperate.

        """
        super().__init__()
        assert (generousTolerance>=0) and (generousTolerance<=100)
        self.generousTolerance = generousTolerance

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""

        if len(opponent.history) <= 10:
            return C

        array = opponent.history[-10:] #fetch the last 10 moves of the opponent and out into array
        C_counts = array.count(C)
        D_counts = array.count(D)


        #use C_counts and D_counts to adjust probability
        #the higher the D_counts (opponent defect), the more likely it will defect
        
        defectProb=D_counts/10 #the higher it is, the more likely to defect
        cooperateProb=C_counts/10 #the higher it is, the more likely to cooperate

        #self._random.random_choice(self.cooperateProb) #example reference taken from random.py
        randDefect1=random.random() #1 is not included
        if randDefect1<=defectProb:
            return D
            #when opponent constantly defects for the last 10 moves, this strategy becomes grim trigger starting from the 11th move
        else: #chance of being cooperative or mimicking opponent's previous move (Tit-for-Tat)
            randCoop2=random.random()
            #generousTolerance=50 #Probability to choose to tolerate opponent and shows that willing to cooperate on their own volition instead of TFT
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

    Then, attempt to simulate fuzzy logic or probabilistic decision-making
    using several random numbers generated by random.random()
    and thresholding.

    This simulates simplified version of fuzzy logic, where 
    the player does not decide to absolutely defect or cooperate,
    but to factor in doubt as well, which is where probability came in.
    e.g. I am 90% sure that I should choose to defect, 
    because my opponent defects during 90% of the 10 last matches

    According to payoff matrix, if player A is sure that player B
    will defect, the choice player A can make with the least losses
    is to defect, rather than cooperate and end up being the sucker.

    Inspired by:

    - ShortMem: [Andre2013]_
    """

    name = "ShortMemProbabilisticFuzzy"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, TFTbias: int = 10, MajorityBias: int = 5) -> None:
        """
        Parameters
        ----------
        TFTbias, int
            Probability of choosing to TFT, that is, copy opponent's previous move rather than choosing its
            own move without taking into account opponent's previous move
            Range of values: -33 to 66, on a scale of 100
            If set to -33, it will never do TFT and will instead ignore opponent's previous move. 
            From here on out, only MajorityBias affects the move choice.
            If set to 66, it will always do TFT or copy opponent's previous move.
        
        MajorityBias, int
            Probability of choosing the majority, that is, which move that the opponent made the most within the last 10 turns,
            over the minority, which is the least move made by the opponent within the last 10 turns. 
            Range of values: -((1-((1/3)+TFTbias))/2) to (1-((1/3)+TFTbias))/2, on a scale of 100
            Limits varies depending on the value of TFTbias, where they can only go as far as half of the remaining
            portion after TFT's limits has been set.
            For example, assuming it's extreme case of no TFT or TFTbias = 0, it would be -50 to 50 
            If set to -50 and TFTbias is 0, it will always make the move that the opponent made the least within the last 10 turns
            If set to 50 and TFTbias is 0, it will always make the move that the opponent made the most within the last 10 turns

        """
        super().__init__()
        assert (TFTbias>=-33) and (TFTbias<=66)
        majminsplit=((1-((1/3)+(TFTbias/100)))/2)*100
        assert (MajorityBias>=-majminsplit) and (MajorityBias<=majminsplit)
        self.TFTbias = TFTbias
        self.MajorityBias = MajorityBias

    def strategy(self, opponent: Player) -> Action:
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
            #possible actions: TFT, majority or minority
            #defect should be greater than cooperate 
            #40:30:30
            #TFTbias=10 #scale: 1 to 100. range: -33 (no TFT) to 66 (always TFT)
            #MajorityBias=5 #Dominant's bias. Apply to which one matches the opponent's move. range: (depending on TFTbias, but assume it's extreme case of no TFT or TFTbias = 0) -50 to 50
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
                    # if tied
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
                    # if tied
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
