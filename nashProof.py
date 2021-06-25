#This file is created by J Candra
import axelrod as axl
import pprint #for formatting output lists
import sys #outout terminal result to file

#print("Start")
#axl.all_strategies

#TFT starting with d vs TFT starting with c
#normal match
#check score each round and cumulatove score

def TournamentWithNashEq(players,turns,repetitions,newFileNameNumber):

    csv=False

    ##tournament
    tournament = axl.Tournament(players, turns=turns, repetitions=repetitions) #orig turn=10
    TourRes = tournament.play() #tournament results
    #find way to write these to file
    win=TourRes.wins
    score=TourRes.scores
    rank=TourRes.ranking
    rankName=TourRes.ranked_names
    CoopCount=TourRes.cooperation
    diff=TourRes.score_diffs

    orig_stdOut=sys.stdout

    if csv==True: #Choose file type of output
        fileType=".csv"
    else:
        fileType=".txt"

        

        FileName="NashEqOutputTour{newFileNameNumber}{fileType}".format(newFileNameNumber=newFileNameNumber,fileType=fileType)#If want to modify naming format, replace the "NashEqOutputTour" part. DO NOT MODIFY ANYTHING ELSE, including bracket and .format() content. 

        with open(FileName,'w') as outFile:
            sys.stdout=outFile
            print("Nash Equilibrium Tournament:")
            print("Trial run {numTrial}:".format(numTrial=n))
            print("..................................................")
            print("Ranking (Names):")
            pprint.pprint(rankName)
            print("==================================================")
            print("List of players:")
            for s in players: #list of strategies in play
                print(s)
            print("==================================================")
            print("Ranking (position):")
            pprint.pprint(rank)
            print("--------------------------------------------------")
            print("Score:")
            pprint.pprint(score)
            print("--------------------------------------------------")
            print("Wins:")
            pprint.pprint(win)
            print("--------------------------------------------------")
            print("Score difference:")
            pprint.pprint(diff)
            print("***************************************************")
            sys.stdout=orig_stdOut #change standard output back to default/normal
            n=n+1

def MatchWithNashEq(players,turns,iterations,newFileNameNumber):

    csv=False
    n=1

    while n<=iterations:

        ##single match:
        match = axl.Match(players, turns=turns)
        match.play() 
        res=match.result

        #print(rankName)
        #pprint.pprint(win)
        #output to file
        #print("Writing to file")

        orig_stdOut=sys.stdout

        if csv==True: #Choose file type of output
            fileType=".csv"
        else:
            fileType=".txt"

        FileName="NashEqOutputMatch{newFileNameNumber}{iteration}{fileType}".format(newFileNameNumber=newFileNameNumber,iteration=n,fileType=fileType)#If want to modify naming format, replace the "NashEqOutputMatch" part. DO NOT MODIFY ANYTHING ELSE, including bracket and .format() content. 
        with open(FileName,'w') as outFile:
            sys.stdout=outFile
            print("Nash Equilibrium Single Match:")
            print("Trial run {numTrial}:".format(numTrial=n))
            print("==================================================")
            print("List of players:")
            for s in players: #list of strategies in play
                print(s)
            print("==================================================")
            print("Result:")
            print(res)
            print("***************************************************")
            sys.stdout=orig_stdOut #change standard output back to default/normal
        n=n+1


TFT2players = [axl.TitForTat(), axl.SuspiciousTitForTat()]

#Both are TFT, but the difference is which first move
#attempt to make alternating round

#def TournamentWithResultFile(players,turns,repetitions,iterations,newFileNameNumber):
#TournamentWithNashEq(TFT2players,10,1,1,3)
MatchWithNashEq(TFT2players,10,1,4)


#use modified moran process, moranEvolution.py
#population pool selected from other best