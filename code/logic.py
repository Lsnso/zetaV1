from lib import *

def logic(pv, dv, count, decision):
    player, dealer, deck = Hand(), Hand(), Deck()
    if decision == "P": decision, split = "H", True
    else: split = False
    game = Game([player, pv], [dealer, dv], [deck, count], decision)
    while game.on:
        game.do_player()
    game.do_dealer()
    result = game.update_result()

    if split: 
        player2, dealer2, deck2 = Hand(), Hand(), Deck()
        game2 = Game([player2, pv], [dealer2, dv], [deck2, count], "H")
        game2.dealer = game.dealer
        while game2.on:
            game2.do_player()
        game2.do_dealer()
        result += game2.update_result()

    return result