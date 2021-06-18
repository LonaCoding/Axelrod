import random
import math
import matplotlib.pyplot as mplot
from matplotlib.gridspec import SubplotSpec
import axelrod as axl
import pprint #for formatting output lists
import sys #outout terminal result to file
import shutil #for moving files

def largestFactor(inputValue):
    n=1
    a=1
    b=1
    while n <=math.sqrt(inputValue): #only look for factors up to square root
        if inputValue%n==0: #if factor found    
            a=n #current biggest factor
        n=n+1
    b=int(inputValue/a) #find other compliemntary factor

    return a, b

def MoranProcTour(
    agents,
    newFileNameNumber,
    turns=10,
    firstSeed=1,
    iterations=1,
    splitThresholdPercentile=50,
    ConvergeScoreGenLimit=5,
    displayOutput=False,
    createPlot=0,
    PlotFileType="PNG",
    csv=False,
    testing=False
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
    print("5. iterations:                           {}".format(iterations))
    print("6. splitThresholdPercentile:             {}%".format(splitThresholdPercentile))
    print("7. ConvergeScoreGenLimit:                {}".format(ConvergeScoreGenLimit))
    print("8. displayOutput:                        {}".format(displayOutput))    
    print("9. createPlot:                           {}".format(createPlot))
    print("10.PlotFileType:                         {}".format(PlotFileType))    
    print("11.(use) csv (as output's file format):  {}".format(csv))
    print("12.testing (mode):                       {}".format(testing))#determines file path to send plot images to 
    print("------------------------------------------------------------")
    
    #Initialize
    n=1 #counter for interation loop
    seed=firstSeed #set first seed

    
    if createPlot>=2:
        row,col=largestFactor(iterations) #find largest factor of iterations to determine subplot grid dimensions
        subplotMain, subplotAxes = mplot.subplots(row,col,sharey='row',figsize=(14, 14))#,tight_layout=False #13 inches = 1024
        #sharey=row: everything on a single row shares the same y-axis

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
        subplotFileName="EliteMoranProcSubplot{newFileNameNumber}_{iterNum}.{PlotFileTypeExt}".format(newFileNameNumber=newFileNameNumber,iterNum=n,PlotFileTypeExt=PlotFileTypeExt)#If want to modify naming format, replace the "ScrListBrandModel" part. DO NOT MODIFY ANYTHING ELSE, including bracket and .format() content. 
        
        if testing:
            targetOutFolder = "MoranElitistExperiments_Output/testPlots"
        else:
            targetOutFolder = "MoranElitistExperiments_Output/Plots"

        ##tournament
        #tournament = axl.MoranProcess(players=players, turns=200, seed=2)
        tournament = axl.MainEvoEliteMoranProcess(
            agents,turns=turns, 
            seed=seed,
            splitThresholdPercentile=splitThresholdPercentile,
            dispOutput=displayOutput,
            ConvergeScoreLimit=ConvergeScoreGenLimit
            )
        TourRes = tournament.play() #tournament results

        if createPlot>=2: #create subplot
            #finds quotient and remainder of upcoming iteration after division with column size, 
            #to determine position of next subplot, outputs quotient row and remainder collumn
            r, c = divmod(n,col) # r=row position for subplot
            if c==0: #if n%col=0,
                r=r-1 #ensure the row does not follow quotient
                c=col #subplot is at rightmost end
            c=c-1 #c=column position for subplot. Transpose to index notation

            subplotAxes[r][c]=tournament.populations_plot(iter=n,ax=subplotAxes[r][c]) #do subplot
            

        if createPlot==1 or createPlot==3: #create seperate plots
            plotAxis=tournament.populations_plot() #created the plot

            #final touches. Have to do it here because tournament.populations_plot could be used for subplots
            #plotAxis.set_title("Iteration: {iter} || Threshold: {Threshold}% || Players: {numPlayers}".format(iter=n, Threshold=splitThresholdPercentile,numPlayers=len(agents)), loc='center') #Modified by J Candra: Iteration replaced by generation                    
            #plotAxis.set_xlabel("Generation") #Modified by J Candra: Iteration replaced by generation
            #plotAxis.set_ylabel("Number of Individuals")
            #plotAxis.legend(title="Player Agent Types",loc='upper right', borderaxespad=0.)

            mplot.savefig(plotFileName,format=PlotFileType, dpi=100) #saves the plot as image
            outputNewPath=shutil.move(plotFileName, targetOutFolder) #move the saved image plot to output folder
        
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


    #shift iteration top axis title to the right
    
    tightLayout=False
    

    if createPlot>=2: #end of loop, aggregate and create main plot #\nIteration
        subplotMain.suptitle("Moran Process Population by Generation in Different Iterations\nThreshold: {Threshold}% || Players: {numPlayers}".format(Threshold=splitThresholdPercentile,numPlayers=len(agents)), fontweight='black',fontsize='18')
        subplotMain.supxlabel('Generation',fontweight='bold',fontsize='16',ha='center')
        subplotMain.supylabel('Number of Individuals',fontweight='bold',fontsize='16',ha='center')

        #subplotMain.legend(title="Player Agent Types",loc='upper right', borderaxespad=0.) #duplicated legend labels
        PlayerAgentColor,PlayerAgentLabel=subplotAxes[0][0].get_legend_handles_labels() #get legend from first plot #modified from https://www.delftstack.com/howto/matplotlib/how-to-make-a-single-legend-for-all-subplots-in-matplotlib/
        subplotMain.legend(reversed(PlayerAgentColor), reversed(PlayerAgentLabel),title="Player Agent Types",loc='upper right', borderaxespad=0.) #,bbox_to_anchor=(0.8, 0.8) #apply first plot's legend as legend for entire figure
        #reverse order of legend keys

        #Make top axis title/label "Iteration"
        grid=mplot.GridSpec(r+1,c+1)
        topAxis=subplotMain.add_subplot(grid[0,0:c], frameon=False) #make frame invisible
        topAxis.set_frame_on(False) #make frame invisible
        topAxis.axis('off') #make axis invisible

        #create 2 modes, depends on wether to use tight layout or not
        if tightLayout:
            offset=0.6 #re-adjust
            subplotMain.tight_layout(pad=0.5)
        else:
            offset=0.7 #re-adjust
            subplotMain.subplots_adjust(left=0.05,hspace=0.2,bottom=0.05,wspace=0.001,right=0.825) #offset between plot and legend

        topAxis.set_title("Iteration\n",fontweight='heavy',fontsize='16', color='#1c2e4a',x=offset) #loc='center'

        #subplotAxes[0][1].set_title
        #subplotMain.text(0.5,0.8,"Iteration",fontweight='bold',fontsize='14',ha='center')





        #save plot as image and move the image to output folder
        mplot.savefig(subplotFileName,format=PlotFileType, dpi=300) #, bbox_inches='tight'#saves the plot as image
        outputNewPath=shutil.move(subplotFileName, targetOutFolder) #move the saved image plot to output folder
        

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

myPlayersAgainstTFT=[axl.ShortMemDynamicThreshold(),axl.ShortMemProbabilistic(),axl.ShortMemProbabilisticFuzzy(),axl.TitForTat()]            

myPlayersAgainstplayerBest1=[axl.ShortMemDynamicThreshold(),axl.ShortMemProbabilistic(),axl.ShortMemProbabilisticFuzzy(),
                            axl.EvolvedFSM6(), axl.SecondByRichardHufford(), axl.TitForTat(), 
                            axl.EvolvedFSM16(), axl.EvolvedHMM5(), axl.EvolvedLookerUp2_2_2(), 
                            axl.Michaelos(), axl.Defector(),axl.Cooperator(),axl.Random(),
                            axl.WinStayLoseShift(),axl.Grudger(),axl.Prober(), axl.TitFor2Tats()]            


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

playerTest=[axl.Defector(),axl.Cooperator(),axl.Random(),
            axl.Defector(),axl.Cooperator(),axl.Random(),
            axl.Defector(),axl.Cooperator(),axl.Random(),]

AllStratPlayers = [s() for s in axl.all_strategies]

#generating random values for seed
#Seed value must be between 0 and 2**32 - 1, else trigger ValueError
#randPow=random.randint(1,9) #9 is maximum, because 10**9<2**32<10**10 and else will trigger ValueError
#RandFloat=random.random()
initSeed=math.floor(random.random()*(10**random.randint(1,9))) #generate random starting seed

#convertor
desiredClonedPopSize=5 #sets the number of player agents that will be cloned and the ones that will be culled
agentPlayers=playerBest1 #all player agents
percentile=desiredClonedPopSize/len(agentPlayers) #convertor
#put percentile in splitThresholdPercentile (splitThresholdPercentile=percentile)


#Additional input parameters for MoranProcTour: 
#PlotFileType options (,PlotFileType=".____"): 
#"EPS", "JPEG", ".jpg", ".pdf", ".pgf", ".png", ".ps", ".raw," ".rgba", ".svg", ".svgz", ".tif", ".tiff"
#createPlot options (,createPlot="_"):
# 0: No plot
# 1: Individual seperate plots, 1 for each iteration
# 2: A single plot of combined subplots. where 1 subplot represents 1 iteration
# 3: Plots from both options 1 and 2 (still buggy)

#MoranProcTour(players,newFileNameNumber,turns=10,seedOffset=1,iterations=1,splitThresholdPercentile=50,ConvergeScoreGenLimit=5,displayOutput=False,createPlot=0,PlotFileType=".png",csv=False,testing=False)
#MoranProcTour(AllStratPlayers,13,200,initSeed,10,50,True) #all strategies
#MoranProcTour(playerBest1,20,200,initSeed,20,25,True,True) #real v1.0
#MoranProcTour(playerTest,74,10,initSeed,20,50,50,False,3,True) #testing
#                     pop|fn|turn|seed|iter|st|cgl|do|cp|pft|csv|testing
#MoranProcTour(playerBest1,94,200,306,20,50,100,True,2,testing=False) #

#MoranProcTour(myPlayersAgainstTFT,101,200,initSeed,20,50,100,True,2,testing=False) #my strategies vs TFT

MoranProcTour(myPlayersAgainstplayerBest1,102,200,initSeed,20,50,100,True,2,testing=False) #my strategies vs playerBest1




#combination to test
#   perc    p1      p2
#    50            
#    25            

#MoranProcTour(playerBest1,41,200,42634304,20,25,50,True,1) #real v2.0

#vary the st=splitThresholdPercentile between 50 & 25

#raise ConvergeScoreGenLimit to 100?

#next test do perc=25
#try reducing population? or enlarging?

#p1, 12901, 50%: done

#TO DO:
#move testing input param to middle
#change plot save file path once everything's correct





