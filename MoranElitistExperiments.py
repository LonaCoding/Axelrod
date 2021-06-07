import random
import matplotlib.pyplot as plt
import axelrod as axl
import pprint #for formatting output lists
import sys #outout terminal result to file

def MoranTour(players,turns,seed=1,iterations):

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
        #tournament = axl.Tournament(players, turns=turns, repetitions=repetitions) #orig turn=10
        #tournament = axl.MoranProcess(players=players, turns=200, seed=2)
        tournament = axl.MainEvoEliteMoranProcess(players,turns=turns, seed=seed)
        TourRes = tournament.play() #tournament results
        #find way to write these to file
        win=tournament.winning_strategy_name
        score=tournament.score_history
        

        #pprint.pprint(rankName)
        #ppprint.pprint.ppprint.pprint(win)

        #output to file
        #pprint.pprint("Writing to file")
        #orig_stdOut=sys.stdout


        if csv==True: #Choose file type of output
            fileType=".csv"
        else:
            fileType=".txt"

        ax = tournament.populations_plot()
        plt.show() 

        #FileName="AllTournamentOutput{newFileNameNumber}{fileType}".format(newFileNameNumber=newFileNameNumber,fileType=fileType)#If want to modify naming format, replace the "ScrListBrandModel" part. DO NOT MODIFY ANYTHING ELSE, including bracket and .format() content. 

        #with open(FileName,'w') as outFile:
            #sys.stdout=outFile
        print("Trial run {numTrial}:".format(numTrial=n))
        print("..................................................")
        print("winner:")
        print(win)
        print("==================================================")
        print("List of players:")
        for s in players: #list of strategies in play
            print(s)
        print("==================================================")
        print("Results:")
        pprint.pprint(TourRes)
        print("--------------------------------------------------")
        print("Score:")
        print(score)
        print("***************************************************")
        print("***************************************************")
            #sys.stdout=orig_stdOut #change standard output back to default/normal
        n=n+1

#AllStratPlayers = [s() for s in axl.all_strategies]
    #for s in AllStratPlayers: #list of strategies in play
    #    pprint.pprint(s)

player3=[axl.TitForTat(), axl.Random(), axl.Negation()]

player6=[axl.TitForTat(), axl.Random(), axl.Negation(),axl.CyclerCCD(), axl.MemoryOnePlayer(), axl.Inverse()]

playerBest=[axl.TitForTat(), axl.Random(), axl.Negation(),axl.CyclerCCD(), axl.MemoryOnePlayer(), axl.Inverse()]

players = [axl.Defector(), axl.Defector(), axl.Defector(),
       axl.Cooperator(), axl.Cooperator(), axl.Cooperator(),
       axl.TitForTat(), axl.TitForTat(), axl.TitForTat(),
       axl.Random()]

#def TournamentWithResultFile(players,turns,repetitions,iterations,newFileNameNumber):
#TournamentWithResultFile(AllStratPlayers,20,3,2,3)
#TournamentWithResult(AllStratPlayers,50,3,5)
MoranTour(player6,5,1,2)



