from typing import List
import random
import math
from controller import controller

class card:
    suit: int
    value: int
    is_ace: bool

    def __init__(self, suit: int, value: int):
        self.suit = suit
        if value == 1:
            self.is_ace = True
        else:
            self.is_ace = False
        self.value = value

    def print(self):
        value = ""
        if self.is_ace:
            value = "A"
        elif self.value < 11:
            value = str(self.value)
        elif self.value == 11:
            value = "J"
        elif self.value == 12:
            value = "Q"
        elif self.value == 13:
            value = "K"
        
        if self.suit == 1:
            print(value + "♧")
        elif self.suit == 2:
            print(value + "♢")
        elif self.suit == 3:
            print(value + "♡")
        elif self.suit == 4:
            print(value + "♤")

class deck:
    cards_in: List[card]
    cards_out: List[card]

    def __init__(self, num_decks):
        self.cards_in = []
        self.cards_out = []
        suits = [1, 2, 3, 4]
        for _ in range(num_decks):
            for suit in suits:
                for i in range(13):
                    new_card = card(suit, i+1)
                    self.cards_in.append(new_card)
                
        assert(len(self.cards_in) == 52*num_decks)
        assert(len(self.cards_out) == 0)

    def shuffle(self):
        self.cards_in.extend(self.cards_out)
        self.cards_out = []
        random.shuffle(self.cards_in)

    def deal(self, n=1) -> List[card]:
        dealt = []
        for i in range(n):
            self.cards_out.append(self.cards_in[0])
            dealt.append(self.cards_in[0])
            self.cards_in.remove(self.cards_in[0])
        return dealt
    
def get_hand_value(cards: List[card]) -> int:
    value = 0
    num_aces = 0
    for card in cards:
        if card.is_ace:
            num_aces += 1
            value += 11
        elif card.value > 10:
            value += 10
        else:
            value += card.value
    while value > 21 and num_aces > 0:
        value -= 10
        num_aces -= 1
    return value
    
class dealer:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.shoe = deck(num_decks)
        self.shuffle_point = math.floor(0.75 * num_decks * 52)
        self.hand = []
        self.name = "dealer"
        self.split_hand = []
        self.splitted = False

    def get_num_decks(self) -> int:
        return self.num_decks

    def deal(self, n=1) -> List[card]:
        return self.shoe.deal(n=n)
    
    def split_debug_deal(self) -> List[card]:
        two = card(1, 2)
        return [two]
    
    def shuffle(self):
        self.shoe.shuffle()

    def play(self):
        self.print_dealer_hand(initial=False)
        while get_hand_value(self.hand) < 17:
            print(self.name + " hits")
            self.hand.extend(self.shoe.deal())
            self.print_dealer_hand(initial=False)
            if self.bust(verbose=True):
                return


    def bust(self, verbose=False) -> bool:
        if get_hand_value(self.hand) > 21:
            if verbose:
                print("dealer bust with hand:")
                for c in self.hand:
                    c.print()
            return True
        else:
            return False
    
    def print_dealer_hand(self, initial=True):
        print(self.name + "'s hand:")
        if initial:
            self.hand[0].print()
        else:
            for c in self.hand:
                c.print()

    def hit(self):
        self.hand.extend(self.deal())

    def print_win(self):
        print(self.name + " wins")
    
    def get_up_card(self) -> str:
        return self.hand[0]

    def clear_hand(self):
        self.hand = []

    def shuffle_check(self):
        if len(self.shoe.cards_out) > self.shuffle_point:
            self.shoe.shuffle()
            print("Shuffling Deck")

class player:
    def __init__(self, dealer: dealer, name: str, ai=False, method="chart"):
        self.hand = []
        self.dealer = dealer
        self.name = name
        self.splitted = False
        self.split_hand = []
        self.winnings = 0
        self.bet = 0
        self.split_bet = 0
        self.ai = ai
        self.controller = None
        if self.ai:
            self.controller = controller(method)

    def query_controller(self, options: List[str], split=False):
        if not split:
            return self.controller.decide(options, self.hand, self.dealer.get_up_card(), self.dealer.get_num_decks(), get_hand_value(self.hand))
        else:
            return self.controller.decide(options, self.split_hand, self.dealer.get_up_card(), self.dealer.get_num_decks(), get_hand_value(self.split_hand))

    def hit(self, split=False):
        if split:
            self.split_hand.extend(self.dealer.deal())
        else:
            self.hand.extend(self.dealer.deal())

    def print_hand(self, split=False):
        if split:
            print(self.name + "'s split hand:")
            for c in self.split_hand:
                c.print()
        else:
            print(self.name + "'s hand:")
            for c in self.hand:
                c.print()

    def bust(self, verbose=False, split=False) -> bool:
        if split:
            if get_hand_value(self.split_hand) > 21:
                if verbose:
                    print("bust with hand:")
                    for c in self.split_hand:
                        c.print()
                return True
            else:
                return False
        else:
            if get_hand_value(self.hand) > 21:
                if verbose:
                    print("bust with hand:")
                    for c in self.hand:
                        c.print()
                return True
            else:
                return False
        
    def print_win(self):
        print(self.name + " wins")

    def print_loss(self):
        print(self.name + " loses")

    def print_push(self):
        print(self.name + " pushes")

    def print_winnings(self):
        print(self.name + " winnings: " + str(self.winnings))

    def splittable(self):
        if len(self.hand) == 2:
            return self.hand[0].value == self.hand[1].value
        else:
            return False
        
    def split(self):
        self.splitted = True
        self.split_hand.append(self.hand[1])
        self.split_bet = self.bet
        self.hand.remove(self.hand[1])

    def play(self, split=False):
        done = False
        while not done:
            self.print_hand(split=split)
            can_double = (split and len(self.split_hand) == 2) or (not split and len(self.hand) == 2)
            if can_double:
                h_or_s = input("hit, stand, or double?")
            else:
                h_or_s = input("hit or stand?")
            if h_or_s.startswith("h"):
                self.hit(split=split)
            elif h_or_s.startswith("st"):
                done = True
            elif h_or_s.startswith("d") and can_double:
                if split:
                    self.split_bet *= 2
                else:
                    self.bet *= 2
                self.hit(split=split)
                done = True
            if self.bust(verbose=True, split=split):
                done = True

    def play_robot(self, split=False):
        done = False
        while not done:
            self.print_hand(split=split)
            can_double = (split and len(self.split_hand) == 2) or (not split and len(self.hand) == 2)
            if can_double:
                decision = self.query_controller(["h", "st", "d"], split)
            else:
                decision = self.query_controller(["h", "st"], split)
            if decision.startswith("h"):
                self.hit(split=split)
            elif decision.startswith("st"):
                done = True
            elif decision.startswith("d") and can_double:
                if split:
                    self.split_bet *= 2
                else:
                    self.bet *= 2
                self.hit(split=split)
                done = True
            if self.bust(verbose=True, split=split):
                done = True

    def clear_hand(self):
        self.hand = []
        self.split_hand = []

class Blackjack:
    def __init__(self, num_players: int, num_ai: int):
        self.dealer = dealer(2)
        self.players = [player(self.dealer, str(i)) for i in range(num_players)]
        self.players += [player(self.dealer, str(i+num_players), ai=True) for i in range(num_ai)]

    def deal_initial_cards(self):
        self.dealer.shuffle()
        for _ in range(2):
            for play in [self.dealer] + self.players:
                play.hit()

    def winner(self) -> []:
        best = get_hand_value(self.dealer.hand)
        winners = []
        pushers = []
        losers = []
        split_winners = []
        split_pushers = []
        split_losers = []
        for player in self.players:
            value = get_hand_value(player.hand)
            if not player.bust() and (value > best or best > 21):
                winners.append(player)
            elif not player.bust() and value == best:
                pushers.append(player)
            elif player.bust() and best > 21:
                pushers.append(player)
            else:
                losers.append(player)
            if player.splitted:
                split_value = get_hand_value(player.split_hand)
                if not player.bust(split=True) and (split_value > best or best > 21):
                    split_winners.append(player)
                elif not player.bust(split=True) and split_value == best:
                    split_pushers.append(player)
                elif player.bust(split=True) and best > 21:
                    split_pushers.append(player)
                else:
                    split_losers.append(player)
        for winner in winners:
            if len(winner.hand) == 2 and get_hand_value(winner.hand) == 21:
                winner.winnings += winner.bet * 1.5
            else:
                winner.winnings += winner.bet
            winner.bet = 0
            winner.print_win()
        for pusher in pushers:
            pusher.bet = 0
        for loser in losers:
            loser.winnings -= loser.bet
            loser.bet = 0
        for s_winner in split_winners:
            if len(s_winner.hand) == 2 and get_hand_value(s_winner.hand) == 21:
                s_winner.winnings += s_winner.split_bet * 1.5
            else:
                s_winner.winnings += s_winner.split_bet
            s_winner.split_bet = 0
            winner.print_win()
        for s_pusher in split_pushers:
            s_pusher.split_bet = 0
        for s_loser in split_losers:
            s_loser.winnings -= s_loser.split_bet
            s_loser.split_bet = 0

    def play(self):
        while True:
            self.deal_initial_cards()
            for player in self.players:
                if not player.ai:
                    player.print_winnings()
                    bet = input("Enter bet")
                    player.bet = int(bet)
                    self.dealer.print_dealer_hand()
                    if player.splittable():
                        player.print_hand()
                        h_s_or_split = input("hit, stand, split, or double? ")
                        if h_s_or_split.startswith("sp"):
                            player.split()
                            player.hit()
                            player.play()
                            player.hit(split=True)
                            player.play(split=True)
                        elif h_s_or_split.startswith("h"):
                            player.hit()
                            player.play()
                        elif h_s_or_split.startswith("st"):
                            continue
                        elif h_s_or_split.startswith("d"):
                            player.bet *= 2
                            player.hit()
                            continue
                        if player.bust():
                            continue
                    else:
                        player.play()
                else:
                    player.print_winnings()
                    player.bet = 100
                    if player.splittable():
                        player.print_hand()
                        h_s_or_split = player.query_controller(["h", "st", "sp", "d"])
                        if h_s_or_split.startswith("sp"):
                            player.split()
                            player.hit()
                            player.play_robot()
                            player.hit(split=True)
                            player.play_robot(split=True)
                        elif h_s_or_split.startswith("h"):
                            player.hit()
                            player.play_robot()
                        elif h_s_or_split.startswith("st"):
                            continue
                        elif h_s_or_split.startswith("d"):
                            player.bet *= 2
                            player.hit()
                            continue
                        if player.bust():
                            continue
                    else:
                        player.play_robot()
            self.dealer.play()
            self.winner()
            for player in self.players + [self.dealer]:
                player.clear_hand()
            self.dealer.shuffle_check()

    