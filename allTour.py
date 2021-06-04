import axelrod as axl
import pprint #for formatting output lists


#axl.all_strategies

AllStratPlayers = [s() for s in axl.all_strategies]
#for s in AllStratPlayers: #list of strategies in play
#    print(s)

##single match:
#match = axl.Match(AllStratPlayers, turns=3)
#match.play() 
#res=match.result

##tournament
tournament = axl.Tournament(AllStratPlayers, turns=10, repetitions=3)
TourRes = tournament.play() #tournament results
win=TourRes.wins
score=TourRes.scores
rank=TourRes.ranking
rankName=TourRes.ranked_names
CoopCount=TourRes.cooperation

print(win)
#pprint.pprint(win)

