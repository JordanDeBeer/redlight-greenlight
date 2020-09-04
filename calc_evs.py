#!/usr/bin/env python3
from typing import Dict, NamedTuple, Iterable, Iterator
from dataclasses import dataclass
from math import inf
from itertools import product

number_red_cards = 12
number_green_cards = 25
number_dbl_green_cards = 14

@dataclass(frozen=True)
class BoardState:
    score: tuple

    spent_red: int 
    spent_green: int
    spent_double_green: int
    
    opponent_score: tuple



ev_map: Dict[BoardState, int] = {}

positions = [i for i in range(0,16)] # 17 is a win
stacks = [i for i in range(0,16)]

possible_scores = [i for i in product(positions, stacks) if i[0]+i[1]<17]

# Spent cards
red_cards = [i for i in reversed(range(0,13))]
green_cards = [i for i in reversed(range(0,26))]
dbl_green_cards = [i for i in reversed(range(0,15))]

for t in product(possible_scores, red_cards, green_cards, dbl_green_cards, possible_scores):
    bs = BoardState(t[0],t[1],t[2],t[3],t[4])
    # Deck with no cards is re-shuffled
    if bs.spent_red == 12 and bs.spent_green == 25 and bs.spent_double_green==14:
        continue
        #ev_map[bs] = ev_map[BoardState(bs.score,0,0,0,bs.opponent_score)]
    # Constants for wins where there are 0 red cards left and drawing would result in a win
    if bs.spent_red==12 and 1*bs.spent_green +2*bs.spent_double_green >= 17:
        ev_map[bs] = inf
    # Constants for when there is only red cards left at the start of your turn.
    if bs.score[1] == 0 and bs.spent_green==25 and bs.spent_double_green==14:
        ev_map[bs] = 0

def FindEV():
    # What is our for loop here? We need to start at end nodes in ev_map
    if bs not in ev_map:
        print("bs not in map: ", bs)
        cards_left = 51-bs.spent_red+bs.spent_green+bs.spent_double_green
        red_probability = number_red_cards-bs.spent_red / cards_left
        green_probability = number_green_cards-bs.spent_green / cards_left
        dbl_green_probability = number_dbl_green_cards-bs.spent_double_green / cards_left

        r_bs = BoardState(bs.score,bs.spent_red+1,bs.spent_green,bs.spent_double_green,bs.opponent_score)
        g_bs = BoardState(bs.score[1]+1,bs.spent_red,bs.spent_green+1,bs.spent_double_green,bs.opponent_score)
        dg_bs = BoardState(bs.score[1]+2,bs.spent_red,bs.spent_green,bs.spent_double_green+1,bs.opponent_score)
        
        raw_ev = -bs.score[1]*red_probability + ev_map[g_bs]*green_probability + ev_map[dg_bs]*dbl_green_probability

        # Calc value of removing card from oppt
        actual_ev = raw_ev - (sum(ev_map[r_bs], ev_map[g_bs],ev_map[dg_bs])/3)
        
        ev_map[bs]= actual_ev
    else:
        print("bs in map ", bs)

#FindEV()
print(ev_map)