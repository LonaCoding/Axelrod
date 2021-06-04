import axelrod as axl
import pprint #for formatting output lists
import sys #outout terminal result to file

print("Start")
#axl.all_strategies

csv=False

AllStratPlayers = [s() for s in axl.all_strategies]
#for s in AllStratPlayers: #list of strategies in play
#    print(s)

##single match:
#match = axl.Match(AllStratPlayers, turns=3)
#match.play() 
#res=match.result

##tournament
tournament = axl.Tournament(AllStratPlayers, turns=20, repetitions=3) #orig turn=10
TourRes = tournament.play() #tournament results
#find way to write these to file
win=TourRes.wins
score=TourRes.scores
rank=TourRes.ranking
rankName=TourRes.ranked_names
CoopCount=TourRes.cooperation

#print(rankName)
#pprint.pprint(win)

#output to file
print("Writing to file")
orig_stdOut=sys.stdout


if csv==True: #Choose file type of output
    fileType=".csv"
else:
    fileType=".txt"

newFileNameNumber = 1

FileName="AllTournamentOutput{newFileNameNumber}{fileType}".format(newFileNameNumber=newFileNameNumber,fileType=fileType)#If want to modify naming format, replace the "ScrListBrandModel" part. DO NOT MODIFY ANYTHING ELSE, including bracket and .format() content. 

with open(FileName,'w') as outFile:
    sys.stdout=outFile
    #print("Trial run {num}:".format(num=newFileNameNumber))
    print("Ranking (Names):")
    print(rankName)
    print("--------------------------------------------------")
    print("Ranking (position):")
    print(rank)
    print("--------------------------------------------------")
    print("Score:")
    print(score)
    print("--------------------------------------------------")
    print("Wins:")
    print(win)
    print("--------------------------------------------------")
    print("Cooperation Count:")
    print(CoopCount)
    print("***************************************************")
    sys.stdout=orig_stdOut #change standard output back to default/normal

