import axelrod as axl
import pprint #for formatting output lists
import sys #outout terminal result to file

#pprint.pprint("Start")
#axl.all_strategies

def TournamentWithResultFile(players,turns,repetitions,iterations,newFileNameNumber):

    csv=False
    n=1

    while n<iterations+1:
        #AllStratPlayers = [s() for s in axl.all_strategies]
        #for s in AllStratPlayers: #list of strategies in play
        #    pprint.pprint(s)

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

        #pprint.pprint(rankName)
        #ppprint.pprint.ppprint.pprint(win)

        #output to file
        #pprint.pprint("Writing to file")
        orig_stdOut=sys.stdout


        if csv==True: #Choose file type of output
            fileType=".csv"
        else:
            fileType=".txt"

        

        FileName="AllTournamentOutput{newFileNameNumber}{fileType}".format(newFileNameNumber=newFileNameNumber,fileType=fileType)#If want to modify naming format, replace the "ScrListBrandModel" part. DO NOT MODIFY ANYTHING ELSE, including bracket and .format() content. 

        with open(FileName,'w') as outFile:
            sys.stdout=outFile
            pprint.pprint("Trial run {numTrial}:".format(numTrial=n))
            pprint.pprint("..................................................")
            pprint.pprint("Ranking (Names):")
            pprint.pprint(rankName)
            pprint.pprint("==================================================")
            pprint.pprint("List of players:")
            for s in AllStratPlayers: #list of strategies in play
                pprint.pprint(s)
            pprint.pprint("==================================================")
            pprint.pprint("Ranking (position):")
            pprint.pprint(rank)
            pprint.pprint("--------------------------------------------------")
            pprint.pprint("Score:")
            pprint.pprint(score)
            pprint.pprint("--------------------------------------------------")
            pprint.pprint("Wins:")
            pprint.pprint(win)
            pprint.pprint("--------------------------------------------------")
            pprint.pprint("Cooperation Count:")
            pprint.pprint(CoopCount)
            pprint.pprint("***************************************************")
            sys.stdout=orig_stdOut #change standard output back to default/normal
            n=n+1


def TournamentWithResult(players,turns,repetitions,iterations):

    csv=False
    n=1

    while n<iterations+1:
        #AllStratPlayers = [s() for s in axl.all_strategies]
        #for s in AllStratPlayers: #list of strategies in play
        #    pprint.pprint(s)

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

        #pprint.pprint(rankName)
        #ppprint.pprint.ppprint.pprint(win)

        #output to file
        #pprint.pprint("Writing to file")
        #orig_stdOut=sys.stdout


        if csv==True: #Choose file type of output
            fileType=".csv"
        else:
            fileType=".txt"

        

        #FileName="AllTournamentOutput{newFileNameNumber}{fileType}".format(newFileNameNumber=newFileNameNumber,fileType=fileType)#If want to modify naming format, replace the "ScrListBrandModel" part. DO NOT MODIFY ANYTHING ELSE, including bracket and .format() content. 

        #with open(FileName,'w') as outFile:
            #sys.stdout=outFile
        print("Trial run {numTrial}:".format(numTrial=n))
        print("..................................................")
        print("Ranking (Names):")
        pprint.pprint(rankName)
        print("==================================================")
        print("List of players:")
        for s in AllStratPlayers: #list of strategies in play
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
        print("Cooperation Count:")
        pprint.pprint(CoopCount)
        print("***************************************************")
        print("***************************************************")
            #sys.stdout=orig_stdOut #change standard output back to default/normal
        n=n+1

AllStratPlayers = [s() for s in axl.all_strategies]
    #for s in AllStratPlayers: #list of strategies in play
    #    pprint.pprint(s)

#def TournamentWithResultFile(players,turns,repetitions,iterations,newFileNameNumber):
#TournamentWithResultFile(AllStratPlayers,20,3,2,3)
TournamentWithResult(AllStratPlayers,50,3,5)