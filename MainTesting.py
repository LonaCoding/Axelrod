import axelrod as axl
#from axelrod.strategies import TitForTat,forgiver
#from axelrod import Match

players = [axl.TitForTat(), axl.TitForTat()]
match = axl.Match(players, turns=3)
match.play() 

#players = [TitForTat(), forgiver()]
#match = Match(players, turns=3)
#match.play() 

#players = [axelrod.TitForTat(), axelrod.forgiver()]
#match = axelrod.Match(players, turns=3)
#match.play() 

#axl.TitForTat()