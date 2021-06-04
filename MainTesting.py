import axelrod as axl
from axelrod.strategies import TitForTat,grudger
from axelrod import Match
import pprint #for formatting output lists

print("testing start")


#works
#players = [axl.TitForTat(), axl.TitForTat()]
#match2 = axl.Match(players, turns=3)
#match2.play() 
#res=match2.result
#print(res)




#strategies = [s() for s in axl.demo_strategies]
#for s in strategies:
#    print(s)
#match = axl.Match(strategies, turns=3)
#match.play() 
#match.result
#print(match.result)
#out=match.result
#out


#fail:
players = [TitForTat(), grudger()]
match = Match(players, turns=3)


match.play() 
pprint.pprint(match.result)

#players = [axelrod.TitForTat(), axelrod.forgiver()]
#match = axelrod.Match(players, turns=3)
#match.play() 

#axl.TitForTat()
print("testing okay1")