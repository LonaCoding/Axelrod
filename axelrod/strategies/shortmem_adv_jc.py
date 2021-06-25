#This file is a modified version of shortmem.py
from axelrod import Player
from axelrod.action import Action
import random
import math

C, D = Action.C, Action.D


class ShortMemDynamicThreshold(Player):
    """
    (From the original:)　
    A player starts by always cooperating for the first 10 moves.
    
    From the tenth round on, the player analyzes the last ten actions, and
    compare the number of defects and cooperates of the opponent.

    (Writen by J Candra:)
    Then, the difference between the number of
    defects and cooperates was calculated and compared with
    a threshold value.
    The threshold for the comparison oscillates as the turn goes,
    according to sine wave with minimum value of 1 and 
    maximum value of 9.
    If it the difference between the number of
    defects and cooperates exceeds the threshold,
    it chooses the most frequent action.

    From the original:
    Otherwise, the program follows the TitForTat algorithm.

    Inspired by:

    - ShortMem: [Andre2013]_
    - Rapoport's strategy: [Axelrod1980]_
    - TitForTat: [Axelrod1980]_
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

        #everything below this line until specified otherwise within this function is created by J Candra


        #threshold changes between 1 and 9
        
        #offset=0 #30 if want to start halfway to max (7), 90 if want to start high (9), 270 if want to start low (1). have this parameter adjustable, if possible, from outside (as input argument)

        if self.uniform:        
            #The uniform method. Median is exactly in middle
            count=(len(opponent.history)+self.offset-10)%16
            if count>=8:
                threshold=(16-count)+1
            else:
                threshold=count+1
        else:    
            #the sine method. Value changes are not uniform. Median is not exactly in middle
            threshold=(4*round(math.sin(math.radians((len(opponent.history)-10)*22.5)+self.offset),1))+5

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
        
        #everything below this line within this function is not created by J Candra, but was copied from original shortmem.py
        #except for "threshold" variable, which replaces the original's static variable
        if C_counts - D_counts >= threshold:
            return C
        elif D_counts - C_counts >= threshold:
            return D
        else:
            return opponent.history[-1]


class ShortMemFuzzy(Player):
    """
    (From the original:)　
    A player starts by always cooperating for the first 10 moves.

    From the tenth round on, the player analyzes the last ten actions, 

    (Written J Candra:)
    counts the number of defections, counts the longest action streak the 
    opponent made and gets the last move the opponent made.

    Then, it uses those information and fuzzy logic 
    to calculate the fuzzy value of belief that
    the opponent would defect or to cooperate.
    If the fuzzy belief value is greater than 0,
    it will assume that the opponent will defect next turn
    and thus respond with defection.
    If the fuzzy belief value is smaller than 0,
    it will assume that the opponent will cooperate next turn
    and thus respond with cooperation. 

    This simulates simplified version of fuzzy logic, where 
    the player does not decide to absolutely defect or cooperate,
    but to factor in belief/doubt as well, which is where probability came in.
    e.g. The player is 90% sure that it should choose to defect, 
    because its opponent defects during 90% of the 10 last matches^, which
    if rounded, meant that the player would defect. HOwever, this is not
    true implementation of fuzzy logic, as to do so requires overhauling
    significant portions of the actual Axelrod Python Library itself.

    ^According to payoff matrix, if player A is relatively sure that player B
    will defect, the choice player A can make with the least losses
    is to defect, rather than cooperate and end up being the sucker.

    Inspired by:

    - ShortMem: [Andre2013]_
    - Rapoport's strategy: [Axelrod1980]_
    - TitForTat: [Axelrod1980]_
    """

    name = "ShortMemFuzzy"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
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

        #everything below this line within this function is created by J Candra
        #the higher the D_counts (opponent defect), the more likely it will defect
        
        #3 factors that determine fuzzy rating (scale: -1 (C) to 1 (D)):
        #1. number of total defections
        defectProb=D_counts/10 #the higher it is, the more likely to defect
        coopProb=C_counts/10 #the higher it is, the more likely to cooperate
        if D_counts>C_counts:
            fuzzy=defectProb/2
        elif D_counts<C_counts:
            fuzzy=-coopProb/2
        else: #if both number of defections and cooperations are equal
            fuzzy=0

        #2. longest streak (check length of currentBestList)

        current=None
        mCount=0
        currBestCount=0
        currentBestList=[]
        for m in array:
            if current!=m:
                if mCount>currBestCount: #check wether it beats the current maximum streak
                    currBestCount=mCount
                    currBestMove=current
                    currentBestList=[] #reset
                    currentBestList.append([current,mCount])
                elif mCount==currBestCount:
                    currentBestList.append([current,mCount])
                current=m
                mCount=1 #reset move count
            else:
                mCount=mCount+1
        if mCount>currBestCount: #FInal check. check wether it beats the current maximum streak
            currBestCount=mCount
            currBestMove=current
            currentBestList=[] #reset
            currentBestList.append([current,mCount])
        elif mCount==currBestCount:
            currentBestList.append([current,mCount])

        streakToConsider=0
        streakC=0
        if len(currentBestList)>1 and len(currentBestList)<4: #if there is more than 1 and less than 4 maxima means that each maxima is 3 at least, the smallest possible streak
            n=0
            while n<len(currentBestList):
                if currentBestList[n][1]<=2:
                    currentBestList.pop(n)
                else:    
                    n=n+1
            streakDcount=currentBestList.count(D)
            streakCcount=currentBestList.count(C)
            if streakDcount>streakCcount:
                streakM=D
                streakC=0.05*(streakDcount-streakCcount)*currentBestList[0][1]
            elif streakDcount<streakCcount:
                streakM=C
                streakC=-0.05*(streakCcount-streakDcount)*currentBestList[0][1]
            else:
                streakM=D #default
                streakC=0 #set to none
        elif len(currentBestList)==1:
            streakM=currentBestList[0][0]
            if currentBestList[0][0]==D:#if longest streak is defect
                streakC=0.05*currentBestList[0][1]
            else: #if longest streak is cooperate
                streakC=-0.05*currentBestList[0][1]
        
        fuzzy=fuzzy+streakC #add streak modifier value to current fuzzy value


        #3. last move (Influenced by Tit-For-Tat)
        lastMove=opponent.history[-1]
        lastMoveDefect=lastMove.count(D)
        if lastMoveDefect==1: #if opponent defected last turn
            fuzzy=fuzzy+0.25
        else:
            fuzzy=fuzzy-0.25
        
        print("New strategy")

        #Determines next action based on fuzzy value
        if fuzzy>0:
            return D
        elif fuzzy<0:
            return C
        else: #if fuzzy=0, do Tit-For-Tat
            return opponent.history[-1]


class ShortMemProbabilistic(Player):
    """
    (From the original:)　
    A player starts by always cooperating for the first 10 moves.

    From the tenth round on, the player analyzes the last ten actions, 

    (Written by J Candra:)
    counts the number of defections and randomly decides wether to defect or cooperate, but
    with the likelihood to defect increasing the more often
    the opponent defects

    This strategy is similar to Tit-For-Tat wrapped in Joss-Ann Transformer 
    but instead of using a fixed, manually-specified probability,
    this strategy relies on the dynamically changing number of 
    opponent's defections to set its probability.


    Inspired by:

    - ShortMem: [Andre2013]_
    - JossAnnTransformer: [Ashlock2008]_
    - Rapoport's strategy: [Axelrod1980]_
    - TitForTat: [Axelrod1980]_
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


        #everything below this line within this function is created by J Candra
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
            generousToleranceProb=self.generousTolerance/100
            if randCoop2>=generousToleranceProb:
                return C
            else:
                return opponent.history[-1] #play Tit-for-Tat





class ShortMemProbPreferences(Player):
    """
        (From the original:)　
        A player starts by always cooperating for the first 10 moves.

        From the tenth round on, the player analyzes the last ten actions, 

        (Written by J Candra:)
        counts the number of defections and
        randomly decides wether to defect or cooperate, but
        with the likelihood to defect increasing the more often
        the opponent defects and taking into account
        doubt/belief by using 2 tiers of checks, the first being
        boolean based and the second relying on roulette selection. 

        Inspired by:

        - ShortMem: [Andre2013]_
        - Rapoport's strategy: [Axelrod1980]_
        - TitForTat: [Axelrod1980]_
        """

    name = "ShortMemProbPreferences"
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
        TFTbias, int (Range of values: -33 to 66, on a scale of 100 (Default: 10))
            Probability of choosing to TFT, that is, copy opponent's previous move rather than choosing its
            own move without taking into account opponent's previous move
            Range of values: -33 to 66, on a scale of 100 (Default: 10)
            If set to -33, it will never do TFT and will instead ignore opponent's previous move. 
            From here on out, only MajorityBias affects the move choice.
            If set to 66, it will always do TFT or copy opponent's previous move.
        
        MajorityBias, int (Range of values: -((1-((1/3)+TFTbias))/2) to (1-((1/3)+TFTbias))/2, on a scale of 100 (Default: 5))
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
            TFTprob=(1/3)+(self.TFTbias/100) #Calculate TFT first because it should be greater than or equal to pure defect or cooperate
            MajorityProb=((1-TFTprob)/2)+(self.MajorityBias/100)
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
