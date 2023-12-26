from lib import *

def hit_script(pv, dv, count):
    player, dealer, deck, decision = Hand(), Hand(), Deck(), "S"
    game = Game([player, pv], [dealer, dv], [deck, count], decision)
    
    if dv == "A":
        game.peak()
    while game.on:
        game.do_player()
        game.do_dealer()
    game.update_result()

hit_script("20", "A", 0)