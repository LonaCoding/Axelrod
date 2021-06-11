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
    ConvergeScoreLimit=5,
    displayOutput=False,
    createPlot=False,
    PlotFileType="PNG",
    csv=False
    ):

    #print test parameters information
    print(">>> Output of Elitist Selection (Modified) Moran Process <<<")
    print("------------------------------------------------------------")
    print("Experiment parameters:")
    print("1. Player Agents: {}".format(len(agents)))
    for a in agents: #list of strategies in play
        print(a)
    print("2. newFileNameNumber for plot:           {}".format(newFileNameNumber))    
    print("3. (Number of) turns:                    {}".format(turns))
    print("4. Starting seed (firstSeed):            {}".format(firstSeed))
    print("5. iterations:                           {}%".format(iterations))
    print("6. splitThresholdPercentile:             {}%".format(splitThresholdPercentile))
    print("7. ConvergeScoreLimit:                   {}%".format(ConvergeScoreLimit))
    print("8. displayOutput:                        {}".format(displayOutput))    
    print("9. createPlot:                           {}".format(createPlot))
    print("10. PlotFileType:                         {}".format(PlotFileType))    
    print("11.(use) csv (as output's file format):  {}".format(csv))
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
            dispOutput=displayOutput,
            ConvergeScoreLimit=ConvergeScoreLimit
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
playerBest1=[axl.EvolvedFSM6(), axl.SecondByRichardHufford(), axl.TitForTat(), 
            axl.EvolvedFSM16(), axl.EvolvedHMM5(), axl.EvolvedLookerUp2_2_2(), 
            axl.Michaelos(), axl.Defector(),axl.Cooperator(),axl.Random(),
            axl.WinStayLoseShift(),axl.Grudger(),axl.Prober(), axl.TitFor2Tats()]

#add players that were selected from 20-,50- and 200-turn tournaments' winners
#as well as those according to results from drvinceknight's tournament repository
playerBest2=[axl.EvolvedFSM6(), axl.SecondByRichardHufford(), axl.TitForTat(), 
            axl.EvolvedFSM16(), axl.EvolvedHMM5(), axl.EvolvedLookerUp2_2_2(), 
            axl.Michaelos(), axl.Defector(),axl.Cooperator(),axl.Random(),
            axl.WinStayLoseShift(),axl.Grudger(),axl.Prober(), axl.TitFor2Tats(),
            axl.EvolvedANNNoise05(),axl.Aggravater(),axl.RevisedDowning(),axl.Raider(),
            axl.Prober3(),axl.FirstByDowning(),axl.Fortress3(),axl.EvolvedANN5(),axl.DBS()
            ]



#playerBestDouble=[axl.EvolvedFSM6()*2, axl.SecondByRichardHufford()*2, axl.TitForTat()*2,
#                    axl.EvolvedFSM16()*2, axl.EvolvedHMM5()*2, axl.EvolvedLookerUp2_2_2()*2, 
#                    axl.Michaelos()*2, axl.Defector()*2,axl.Cooperator()*2,axl.Random()*2,
#                    axl.WinStayLoseShift()*2,axl.Grudger()*2,axl.Prober()*2, axl.TitFor2Tats()*2]

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
#Seed value must be between 0 and 2**32 - 1, else trigger ValueError
#randPow=random.randint(1,9) #9 is maximum, because 10**9<2**32<10**10 and else will trigger ValueError
#RandFloat=random.random()
initSeed=math.floor(random.random()*(10**random.randint(1,9))) #generate random starting seed

#convertor
desiredClonedPopSize=5 #sets the number of player agents that will be cloned and the ones that will be culled
agentPlayers=playerBest1 #total number of player agents
percentile=desiredClonedPopSize/len(agentPlayers) #convertor
#put percentile in splitThresholdPercentile (splitThresholdPercentile=percentile)


#Additional input parameters for MoranProcTour: 
#PlotFileType options (,PlotFileType=".____"): 
#"EPS", "JPEG", ".jpg", ".pdf", ".pgf", ".png", ".ps", ".raw," ".rgba", ".svg", ".svgz", ".tif", ".tiff"

#MoranProcTour(players,newFileNameNumber,turns=10,seedOffset=1,iterations=1,splitThresholdPercentile=50,ConvergeScoreLimit=5,displayOutput=False,createPlot=False,PlotFileType=".png",csv=False)
#MoranProcTour(AllStratPlayers,13,200,initSeed,10,50,True) #all strategies
#MoranProcTour(playerBest1,20,200,initSeed,20,25,True,True) #real v1.0
#MoranProcTour(playerBest1,18,5,initSeed,2,50,True,True) #testing


MoranProcTour(playerBest2,37,200,12901,20,25,50,True,True) #real v2.0


#next test do perc=25
#try reducing population? or enlarging?




