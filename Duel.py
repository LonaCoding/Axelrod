#This file is created by J Candra
import axelrod as axl
import pprint #for formatting output lists
import sys #outout terminal result to file

def DuelMatch(initPlayers,testPlayer,turns,iterations,match_attributes):
    players=[]
    fullPlayers=initPlayers #initialize as to preserve the original population
    #players.append(fullPlayers[-1]) #add first player
    
    fpc=1
    for p in testPlayer:
        players.append(p)
        pc=1
        for fp in fullPlayers:
            players.append(fp) #add next player
            sumFSt0=0 #reset
            sumFSt1=0 #reset
            i=0
            while i<=iterations:
                ##single match:
                match = axl.Match(players, turns=turns,match_attributes=match_attributes) #Do the match
                match.play() 
                res=match.result #only history of moves
                fs=match.final_score()
                fst=match.final_score_per_turn()
                w=match.winner()
                #print(rankName)
                #pprint.pprint(win)
                #output to file
                #print("Writing to file")
                #orig_stdOut=sys.stdout

                sumFSt0=sumFSt0+fst[0]
                sumFSt1=sumFSt1+fst[1]

                print("Nash Equilibrium Single Match {iter} of ({firstPC}) {testPlayer} vs ({PC}) {player}):".format(iter=i,firstPC=fpc,PC=pc, testPlayer=str(p),player=str(fp)))
                print("==================================================")
                print("List of players:")
                for s in players: #list of strategies in play
                    print(s)
                print("==================================================")
                #print("Result:")
                #pprint.pprint(res)
                #print("--------------------------------------------------")
                print("Final Scores: {}".format(fs))
                #pprint.pprint(fs)
                #print("--------------------------------------------------")
                print("Final Scores per Turn: {}".format(fst))
                #pprint.pprint(fst)
                #print("--------------------------------------------------")
                print("Winner: {}".format(w))
                #print(w)
                print("--------------------------------------------------")
                #print("++++++++++++++++++++++++++++++++++++++++++++++++++")
                #sys.stdout=orig_stdOut #change standard output back to default/normal
                i=i+1
            average0=sumFSt0/iterations
            average1=sumFSt1/iterations
            if average0>average1:
                averageWinner=players[0]
            elif average0<average1:
                averageWinner=players[1]
            else: #if tied
                averageWinner="None (Tie)"
            print("++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Average final winner and score: {} ({}, {})".format(averageWinner, average0, average1))
            print("***************************************************")
            players.pop()
            pc=pc+1
        players.pop()
        fpc=fpc+1



def DuelExperiment(playerKnowsTurnLim):
    if playerKnowsTurnLim:
        match_attrLen=None #default settings. {"length": self.turns}. players know how manybturns there is in a match
    else:
        match_attrLen={"length": float('inf')} #players do not know how many turns tehre wil be, so assumes it is infinite

    AllStratPlayers = [s() for s in axl.all_strategies]
    shortMemOnly=[axl.ShortMem()] #control/predecessor
    playerToTest=[axl.ShortMemDynamicThreshold(),axl.ShortMemFuzzy(),axl.ShortMemProbabilistic(),axl.ShortMemProbPreferences()]
    myPlayersAgainstTFT=[axl.ShortMemDynamicThreshold(),axl.ShortMemFuzzy(),axl.ShortMemProbabilistic(),axl.ShortMemProbPreferences(),axl.TitForTat()]            

    TFT2players = [axl.TitForTat(), axl.SuspiciousTitForTat()]

    #Both are TFT, but the difference is which first move
    #attempt to make alternating round

    #def TournamentWithResultFile(players,turns,repetitions,iterations,newFileNameNumber):
    DuelMatch(AllStratPlayers,playerToTest,200,10,match_attributes=match_attrLen)


    #use modified moran process, moranEvolution.py
    #population pool selected from other best

DuelExperiment(True)