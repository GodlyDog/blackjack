from typing import List
from collections import Counter

class controller:
    def __init__(self, method: str):
        self.method = method

    def decide(self, options: List[str], hand, up_card, num_decks, hand_total) -> str:
        if self.method == "hitter":
            return self.hitter(options)
        if self.method == "chart":
            return self.chart(options, hand, up_card, num_decks, hand_total)

    def hitter(self, options: List[str]) -> str:
        if "h" in options:
            return "h"
        else:
            return "st"
        
    # charts are formatted as chart[hand value or tuple][up card]
    global two_deck_chart
    two_deck_chart = {
        2: {2: "h", 3: "h", 4: "h", 5: "h", 6: "h", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        3: {2: "h", 3: "h", 4: "h", 5: "h", 6: "h", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        4: {2: "h", 3: "h", 4: "h", 5: "h", 6: "h", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        5: {2: "h", 3: "h", 4: "h", 5: "h", 6: "h", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        6: {2: "h", 3: "h", 4: "h", 5: "h", 6: "h", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        7: {2: "h", 3: "h", 4: "h", 5: "h", 6: "h", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        8: {2: "h", 3: "h", 4: "h", 5: "h", 6: "h", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        9: {2: "Dh", 3: "Dh", 4: "Dh", 5: "Dh", 6: "Dh", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        10: {2: "Dh", 3: "Dh", 4: "Dh", 5: "Dh", 6: "Dh", 7: "Dh", 8: "Dh", 9: "Dh", 10: "h", "A": "h"},
        11: {2: "Dh", 3: "Dh", 4: "Dh", 5: "Dh", 6: "Dh", 7: "Dh", 8: "Dh", 9: "Dh", 10: "Dh", "A": "Dh"},
        12: {2: "h", 3: "h", 4: "st", 5: "st", 6: "st", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        13: {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        14: {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        15: {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        16: {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        17: {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "st", 8: "st", 9: "st", 10: "st", "A": "st"},
        18: {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "st", 8: "st", 9: "st", 10: "st", "A": "st"},
        19: {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "st", 8: "st", 9: "st", 10: "st", "A": "st"},
        20: {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "st", 8: "st", 9: "st", 10: "st", "A": "st"},
        21: {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "st", 8: "st", 9: "st", 10: "st", "A": "st"},
        ("A", 2): {2: "h", 3: "h", 4: "h", 5: "Dh", 6: "Dh", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        ("A", 3): {2: "h", 3: "h", 4: "h", 5: "Dh", 6: "Dh", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        ("A", 4): {2: "h", 3: "h", 4: "Dh", 5: "Dh", 6: "Dh", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        ("A", 5): {2: "h", 3: "h", 4: "Dh", 5: "Dh", 6: "Dh", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        ("A", 6): {2: "h", 3: "Dh", 4: "Dh", 5: "Dh", 6: "Dh", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        ("A", 7): {2: "st", 3: "Ds", 4: "Ds", 5: "Ds", 6: "Ds", 7: "st", 8: "st", 9: "h", 10: "h", "A": "h"},
        ("A", 8): {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "st", 8: "st", 9: "st", 10: "st", "A": "st"},
        ("A", 9): {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "st", 8: "st", 9: "st", 10: "st", "A": "st"},
        ("A", 10): {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "st", 8: "st", 9: "st", 10: "st", "A": "st"},
        (2, 2): {2: "sp", 3: "sp", 4: "sp", 5: "sp", 6: "sp", 7: "sp", 8: "h", 9: "h", 10: "h", "A": "h"},
        (3, 3): {2: "sp", 3: "sp", 4: "sp", 5: "sp", 6: "sp", 7: "sp", 8: "h", 9: "h", 10: "h", "A": "h"},
        (4, 4): {2: "h", 3: "h", 4: "h", 5: "sp", 6: "sp", 7: "h", 8: "h", 9: "h", 10: "h", "A": "h"},
        (5, 5): {2: "Dh", 3: "Dh", 4: "Dh", 5: "Dh", 6: "Dh", 7: "Dh", 8: "Dh", 9: "Dh", 10: "h", "A": "h"},
        (6, 6): {2: "sp", 3: "sp", 4: "sp", 5: "sp", 6: "sp", 7: "sp", 8: "h", 9: "h", 10: "h", "A": "h"},
        (7, 7): {2: "sp", 3: "sp", 4: "sp", 5: "sp", 6: "sp", 7: "sp", 8: "sp", 9: "h", 10: "h", "A": "h"},
        (8, 8): {2: "sp", 3: "sp", 4: "sp", 5: "sp", 6: "sp", 7: "sp", 8: "sp", 9: "sp", 10: "sp", "A": "sp"},
        (9, 9): {2: "sp", 3: "sp", 4: "sp", 5: "sp", 6: "sp", 7: "st", 8: "sp", 9: "sp", 10: "st", "A": "st"},
        (10, 10): {2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "st", 8: "st", 9: "st", 10: "st", "A": "st"},
        ("A", "A"): {2: "sp", 3: "sp", 4: "sp", 5: "sp", 6: "sp", 7: "sp", 8: "sp", 9: "sp", 10: "sp", "A": "sp"}
    }
    def get_chart(self, num_decks):
        if num_decks == 2:
            return two_deck_chart
    
    def chart(self, options: List[str], hand, up_card, num_decks, hand_total) -> str:
        if up_card.is_ace:
            up_card = "A"
        else:
            up_card = up_card.value if up_card.value <= 10 else 10
        output = self.__chart(options, hand, up_card, num_decks, hand_total)
        if output == "Dh":
            if "d" in options:
                return "d"
            elif "h" in options:
                return "h"
            else:
                return "st"
        elif output in options:
            return output
        else:
            return "st"
        
    def __chart(self, options: List[str], hand, up_card, num_decks, hand_total) -> str:
        ch = self.get_chart(num_decks)
        count = Counter()
        if len(hand) == 2:
            ace = False
            double = False
            for c in hand:
                if c.is_ace:
                    count["A"] += 1
                    ace = True
                    if count["A"] == 2:
                        double = True
                else:
                    v = c.value if c.value <= 10 else 10
                    count[v] += 1
                    if count[v] == 2:
                        double = True


            if ace:
                if double:
                    return ch[("A", "A")][up_card]
                else:
                    second = [k for k in count.keys()][0]
                    return ch[("A", second)][up_card]
            else:
                if double:
                    val = hand[0].value if hand[0].value <= 10 else 10
                    return ch[(val, val)][up_card]
        else:
            return ch[hand_total][up_card]

            
            