import random
import csv

class Deck():
    def __init__(self):
        #init 52 card deck
        unique_cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
        self.cards = []
        for _ in range(0,4):
            self.cards.extend(unique_cards)

        #defining high and low cards
        self.high_cards = ["A", "K", "Q", "J", "T"]
        self.low_cards = ["6", "5", "4", "3", "2"]

        #deck shuffle
        random.shuffle(self.cards)

        #init count
        self.update_count()

    def force_count(self, count):
        #forces count by removing cards
        #negative/positive counts: choose random high/low card, check if its removable, update current counter
        current_count = 0
        while current_count != count:
            if count < 0:
                to_remove = random.choice(self.high_cards)
                if to_remove in self.cards:
                    self.cards.remove(to_remove)
                    current_count -= 1
            elif count > 0:
                to_remove = random.choice(self.low_cards)
                if to_remove in self.cards:
                    self.cards.remove(to_remove)
                    current_count += 1
        self.update_count()

    def update_count(self):
        #loops through deck and updates count with higher/lower appearances
        self.count = 0
        for card in self.cards:
            if card in self.high_cards:
                self.count += 1
            elif card in self.low_cards:
                self.count -= 1
    
    def draw_card(self):
        #removes and returns random card from deck
        drawed = random.choice(self.cards)
        self.cards.remove(drawed)
        self.update_count()
        return drawed

class Hand():
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        #add card to hand
        self.cards.append(card)
        self.update_value()

    def update_value(self):
        #updates hand value. pushes aces to the end of the list and later decides their value
        self.value = 0
        sorted_hand = sorted(self.cards, key=lambda x: x == 'A')
        for card in sorted_hand:
            if card in ["9", "8", "7", "6", "5", "4", "3", "2"]:
                self.value += int(card)
            elif card in ["K", "Q", "J", "T"]:
                self.value += 10
            elif card == "A" and self.value < 11:
                self.value += 11
            elif card == "A" and self.value >= 11:
                self.value += 1

class Game():
    def __init__(self, player_info, dealer_info, deck_info, decision):
        #info arguments in the form [instance of respective class, value]
        combinations = {
            #combinations are merely a visual add on while debugging. these must not have impact in the result
            #pair combinations
            "AA" : [["A", "A"]],
            "22" : [["2", "2"]],
            "33" : [["3", "3"]],
            "44" : [["4", "4"]],
            "55" : [["5", "5"]],
            "66" : [["6", "6"]],
            "77" : [["7", "7"]],
            "88" : [["8", "8"]],
            "99" : [["9", "9"]],
            "TT" : [["T", "T"], ["Q", "Q"], ["J", "J"], ["K", "K"]],

            #soft combinations
            "A2" : [["A", "2"], ["2", "A"]],
            "A3" : [["A", "3"], ["3", "A"]],
            "A4" : [["A", "4"], ["4", "A"]],
            "A5" : [["A", "5"], ["5", "A"]],
            "A6" : [["A", "6"], ["6", "A"]],
            "A7" : [["A", "7"], ["7", "A"]],
            "A8" : [["A", "8"], ["8", "A"]],
            "A9" : [["A", "9"], ["9", "A"]],
            
            #hard combinations
            "5"  : [["3", "2"]],
            "6"  : [["4", "2"]],
            "7"  : [["5", "2"], ["4", "3"]],
            "8"  : [["6", "2"], ["5", "3"]],
            "9"  : [["7", "2"], ["6", "3"], ["5", "4"]],
            "10" : [["8", "2"], ["7", "3"], ["6", "4"]],
            "11" : [["9", "2"], ["8", "3"], ["7", "4"], ["6", "5"]],
            "12" : [["K", "2"], ["Q", "2"], ["J", "2"], ["T", "2"], ["9", "3"], ["8", "4"], ["7", "5"]],
            "13" : [["K", "3"], ["Q", "3"], ["J", "3"], ["T", "3"], ["9", "4"], ["8", "5"], ["7", "6"]],
            "14" : [["K", "4"], ["Q", "4"], ["J", "4"], ["T", "4"], ["9", "5"], ["8", "6"]],
            "15" : [["K", "5"], ["Q", "5"], ["J", "5"], ["T", "5"], ["9", "6"], ["8", "7"]],
            "16" : [["K", "6"], ["Q", "6"], ["J", "6"], ["T", "6"], ["9", "7"]],
            "17" : [["K", "7"], ["Q", "7"], ["J", "7"], ["T", "7"], ["9", "8"]],
            "18" : [["K", "8"], ["Q", "8"], ["J", "8"], ["T", "8"]],
            "19" : [["K", "9"], ["Q", "9"], ["J", "9"], ["T", "9"]],
            "20" : [["T", "T"], ["Q", "Q"], ["J", "J"], ["K", "K"]],
            "21" : [["A", "K"], ["A", "Q"], ["A", "J"], ["A", "T"]]
            }

        #init player
        self.player = player_info[0]
        to_player = random.choice(combinations[player_info[1]])
        random.shuffle(to_player)
        for card in to_player:
            self.player.add_card(card)

        #init deck
        self.deck = deck_info[0]
        self.deck.force_count(deck_info[1])

        #init dealer, draws second card based on deck state. doesnt influence its count
        self.dealer = dealer_info[0]
        self.dealer.add_card(dealer_info[1])
        self.dealer.add_card(random.choice(self.deck.cards))

        #init game status
        self.decision = decision
        self.on = True

    def peak(self):
        if self.dealer.value == 21 and len(self.dealer.cards) == 2:
            self.on = False

    def update_result(self):
        #dealer has blackjack, either draw player blackjack or player loses
        if self.dealer.value == 21 and len(self.dealer.cards) == 2:
            if self.player.value == 21 and len(self.player.value) == 2:
                self.result = 0
            else:
                self.result = -1
        #player busts
        elif self.player.value > 21:
            self.result = -1
        #dealer busts
        elif self.dealer.value > 21:
            self.result = 1
        #dealer > player
        elif self.dealer.value > self.player.value:
            self.result = - 1
        #player > dealer
        elif self.player.value > self.dealer.value:
            self.result = 1
        #player = value
        elif self.player.value == self.dealer.value:
            self.result = 0

    def read_decision(self):
        #opens deck count table file and returns a decision
        with open(f"./tables/{self.deck.count}.csv", "r") as f:
            table = list(csv.reader(f))

        table_j = table[0].index(self.dealer.cards[0])
        for line in table:
            if line[0] == str(self.player.value):
                table_i = table.index(line)
        self.decision = table[table_i][table_j]

    def do_player(self):
        #border checkpoint. papers, please
        if self.decision == "H":
            self.hit()
        elif self.decision == "S":
            self.stand()
        elif self.decision == "D":
            self.double()
        else:
            print("Missing decision")

    def hit(self):
        #draws card, checks if player busted, else fetch another decision
        self.player.add_card(self.deck.draw_card())
        if self.player.value < 21:
            self.read_decision()
            self.do_player()
        else:
            self.on = False

    def stand(self):
        #status off
        self.on = False

    def double(self):
        #draws card, status off
        self.player.add_card(self.deck.draw_card())
        self.on = False

    def do_dealer(self):
        #draws cards till dealer hits 17 or higher
        while self.dealer.value < 17:
            self.dealer.add_card(self.deck.draw_card())