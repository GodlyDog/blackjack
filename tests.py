from blackjack import card, get_hand_value, deck

ace = card(1, 1)
two = card(1, 2)
three = card(1, 3)
four = card(1, 4)
five = card(1, 5)
six = card(1, 6)
seven = card(1, 7)
eight = card(1, 8)
nine = card(1, 9)
ten = card(1, 10)
jack = card(1, 11)
queen = card(1, 12)
king = card(1, 13)
def test_hand_value_player():
    blackjack = [ace, king]
    assert(get_hand_value(blackjack) == 21)
    kings = [king, king]
    assert(get_hand_value(kings) == 20)
    three_aces = [ace, ace, ace]
    assert(get_hand_value(three_aces) == 13)

test_hand_value_player()