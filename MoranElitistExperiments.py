import random
import math
import matplotlib.pyplot as mplot
import axelrod as axl
import pprint #for formatting output lists
import sys #outout terminal result to file
import shutil #for moving files

def MoranProcTour(
    agents,
    newFileNameNumber,
    turns=10,
    firstSeed=1,
    iterations=1,
    splitThresholdPercentile=50, 
    displayOutput=False,
    createPlot=False,
    PlotFileType="PNG",
    csv=False
    ):

    #print test parameters information
    print(">>> Output of Elitist Selection (Modified) Moran Process <<<")
    print("------------------------------------------------------------")
    print("Output")
    print("Experiment parameters:")
    print("1. Player Agents: {}".format(len(agents)))
    for a in agents: #list of strategies in play
        print(a)
    print("2. newFileNameNumber for plot:           {}".format(newFileNameNumber))    
    print("3. (Number of) turns:                    {}".format(turns))
    print("4. Starting seed (firstSeed):            {}".format(firstSeed))
    print("5. splitThresholdPercentile:             {}%".format(splitThresholdPercentile))
    print("6. displayOutput:                        {}".format(displayOutput))    
    print("7. createPlot:                           {}".format(createPlot))
    print("8. PlotFileType:                         {}".format(PlotFileType))    
    print("9. (use) csv (as output's file format):  {}".format(csv))
    print("------------------------------------------------------------")
    
    #Initialize
    n=1 #counter for interation loop
    seed=firstSeed #set first seed

    while n<iterations+1: #iteration loop for repeating tests
        #AllStratPlayers = [s() for s in axl.all_strategies]
        #for s in AllStratPlayers: #list of strategies in play
        #    pprint.pprint(s)

        ##single match:
        #match = axl.Match(AllStratPlayers, turns=3)
        #match.play() 
        #res=match.result

        if csv==True: #Choose file type of output
            fileType=".csv"
        else:
            fileType=".txt"

        #PlotFileType="png"
        #options: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff
        PlotFileTypeExt=PlotFileType.lower()
        #print(PlotFileTypeExt) #testing
        plotFileName="EliteMoranProcPlot{newFileNameNumber}_{iterNum}.{PlotFileTypeExt}".format(newFileNameNumber=newFileNameNumber,iterNum=n,PlotFileTypeExt=PlotFileTypeExt)#If want to modify naming format, replace the "ScrListBrandModel" part. DO NOT MODIFY ANYTHING ELSE, including bracket and .format() content. 

        ##tournament
        #tournament = axl.MoranProcess(players=players, turns=200, seed=2)
        tournament = axl.MainEvoEliteMoranProcess(
            agents,turns=turns, 
            seed=seed,
            splitThresholdPercentile=splitThresholdPercentile,
            dispOutput=displayOutput
            )
        TourRes = tournament.play() #tournament results
        if createPlot:
            plot = tournament.populations_plot() #created the plot
            mplot.savefig(plotFileName,format=PlotFileType, dpi=100) #saves the plot as image
            targetOutFolder = "MoranElitistExperiments_Output/Plots"
            outputNewPath = shutil.move(plotFileName, targetOutFolder) #move the saved image plot to output folder
        win=tournament.winning_strategy_name
        score=tournament.score_history

        #FileName="AllTournamentOutput{newFileNameNumber}{fileType}".format(newFileNameNumber=newFileNameNumber,fileType=fileType)#If want to modify naming format, replace the "ScrListBrandModel" part. DO NOT MODIFY ANYTHING ELSE, including bracket and .format() content. 

        #with open(FileName,'w') as outFile:
            #sys.stdout=outFile

        print("Trial run {numTrial}/seed {seedNum}:".format(numTrial=n,seedNum=seed))
        print("..................................................")
        print("winner: {}".format(win))
        print("==================================================")
        print("List of players:")
        for a in agents: #list of strategies in play
            print(a)
        print("==================================================")
        print("Results:")
        pprint.pprint(TourRes)
        print("--------------------------------------------------")
        print("Score:")
        pprint.pprint(score)
        print("***************************************************")
        print("***************************************************")
            #sys.stdout=orig_stdOut #change standard output back to default/normal
        n=n+1
        seed=seed+1

#Initialize population of player agents
player3=[axl.TitForTat(), axl.Random(), axl.Negation()]

player6=[axl.TitForTat(), axl.Random(), axl.Negation(),
        axl.CyclerCCD(), axl.MemoryOnePlayer(), axl.Inverse()]

#add players that were selected from 20-,50- and 200-turn tournaments' winners
playerBest=[axl.EvolvedFSM6(), axl.SecondByRichardHufford(), axl.TitForTat(), 
            axl.EvolvedFSM16(), axl.EvolvedHMM5(), axl.EvolvedLookerUp2_2_2(), 
            axl.Michaelos(), axl.Defector(),axl.Cooperator(),axl.Random(),
            axl.WinStayLoseShift(),axl.Grudger(),axl.Prober(), axl.TitFor2Tats()]

#winners of tournaments:
#'Evolved FSM 6': 50-turn 1st
#'Evolved HMM 5': 50-turn 2nd
#'EvolvedLookerUp2_2_2': 50-turn 3rd
#'Second by RichardHufford': 20-turn 1st
#'Evolved FSM 16': 20-turn 2nd
#'Michaelos: (D,)': 20-turn 3rd


#example from github
players = [axl.Defector(), axl.Defector(), axl.Defector(),
       axl.Cooperator(), axl.Cooperator(), axl.Cooperator(),
       axl.TitForTat(), axl.TitForTat(), axl.TitForTat(),
       axl.Random()]

AllStratPlayers = [s() for s in axl.all_strategies]

#generating random values for seed
#randPow=random.randint(0,10)
#RandFloat=random.random()
initSeed=math.floor(random.random()*(10**random.randint(0,10))) #generate random starting seed

#convertor
desiredClonedPopSize=5 #sets the number of player agents that will be cloned and the ones that will be culled
agentPlayers=playerBest #total number of player agents
percentile=desiredClonedPopSize/len(agentPlayers) #convertor
#put percentile in splitThresholdPercentile (splitThresholdPercentile=percentile)


#Additional input parameters for MoranProcTour: 
#PlotFileType options (,PlotFileType=".____"): 
#"EPS", "JPEG", ".jpg", ".pdf", ".pgf", ".png", ".ps", ".raw," ".rgba", ".svg", ".svgz", ".tif", ".tiff"

#MoranProcTour(players,newFileNameNumber,turns=10,seedOffset=1,iterations=1,splitThresholdPercentile=50,displayOutput=False,createPlot=False,PlotFileType=".png",csv=False)
#MoranProcTour(AllStratPlayers,13,200,initSeed,10,50,True) #all strategies
MoranProcTour(playerBest,19,200,initSeed,20,50,True,True) #real
#MoranProcTour(playerBest,18,5,initSeed,2,50,True,True) #testing

#next test do perc=25




