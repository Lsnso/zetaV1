from lib import *

def hit_script(pv, dv, count, decision):
    if decision == "P":
        player1, dealer1, deck1 = Hand(), Hand(), Deck()
        game1 = Game([player1, pv], [dealer1, dv], [deck1, count], "H")
        while game1.on:
            game1.do_player()
        game1.do_dealer()
        game1.update_result()

        player2, dealer2, deck2 = Hand(), Hand(), Deck()
        game2 = Game([player2, pv], [dealer2, dv], [deck2, count], "H")
        game2.dealer = game1.dealer
        while game2.on:
            game2.do_player()
        game2.do_dealer()
        game2.update_result()

    else:
        player, dealer, deck = Hand(), Hand(), Deck()
        game = Game([player, pv], [dealer, dv], [deck, count], decision)
        while game.on:
            game.do_player()
        game.do_dealer()
        game.update_result()