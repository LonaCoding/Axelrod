import axelrod as axl
import pprint #for formatting output lists
import sys #outout terminal result to file

#print("Start")
#axl.all_strategies

#TFT starting with d vs TFT starting with c
#normal match
#check score each round and cumulatove score

def TournamentWithNashEq(players,turns,repetitions,iterations,newFileNameNumber):

    csv=False
    n=1

    while n<iterations+1:
        #AllStratPlayers = [s() for s in axl.all_strategies]
        #for s in AllStratPlayers: #list of strategies in play
        #    print(s)

        ##single match:
        #match = axl.Match(AllStratPlayers, turns=3)
        #match.play() 
        #res=match.result

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

        #print(rankName)
        #pprint.pprint(win)

        #output to file
        #print("Writing to file")
        orig_stdOut=sys.stdout


        if csv==True: #Choose file type of output
            fileType=".csv"
        else:
            fileType=".txt"

        

        FileName="NashEqOutput{newFileNameNumber}{fileType}".format(newFileNameNumber=newFileNameNumber,fileType=fileType)#If want to modify naming format, replace the "ScrListBrandModel" part. DO NOT MODIFY ANYTHING ELSE, including bracket and .format() content. 

        with open(FileName,'w') as outFile:
            sys.stdout=outFile
            print("Trial run {numTrial}:".format(numTrial=n))
            print("..................................................")
            print("Ranking (Names):")
            print(rankName)
            print("==================================================")
            print("List of players:")
            for s in players: #list of strategies in play
                print(s)
            print("==================================================")
            print("Ranking (position):")
            print(rank)
            print("--------------------------------------------------")
            print("Score:")
            print(score)
            print("--------------------------------------------------")
            print("Wins:")
            print(win)
            print("--------------------------------------------------")
            print("Score difference:")
            print(diff)
            print("***************************************************")
            sys.stdout=orig_stdOut #change standard output back to default/normal
            n=n+1

players = [axl.TitForTat(), axl.SuspiciousTitForTat()]

#Both are TFT, but the difference is which first move
#attempt to make alternating round

#def TournamentWithResultFile(players,turns,repetitions,iterations,newFileNameNumber):
TournamentWithNashEq(players,21,3,2,2)


#use modified moran process, moranEvolution.py
#population pool selected from other best