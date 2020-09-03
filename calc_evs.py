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
red_cards = [i for i in range(0,12)]
green_cards = [i for i in range(0,25)]
dbl_green_cards = [i for i in range(0,14)]

# States where drawing is a guaranteed win
infinite_states = [BoardState(i) for i in product(possible_scores, red_cards, green_cards, dbl_green_cards, possible_scores) if i[1]==12 and 1*i[2] +2*i[3] >= 17]

# States where we are forced to draw a red card
zero_states = [BoardState(i) for i in product(possible_scores, red_cards, green_cards, dbl_green_cards, possible_scores) if i[0][1]==0 and i[2]==25 and i[3]==14]

# Constants for wins where there are 0 red cards left and drawing would result in a win
for i in infinite_states:
    ev_map[i] = inf

# Constants for when there is only red cards left at the start of your turn.
for i in zero_states:
    ev_map[i] = 0


def FindEV():
    for t in product(possible_scores, red_cards, green_cards, dbl_green_cards, possible_scores):
        bs = BoardState(t[0],t[1],t[2],t[3],t[4])
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

            print("added bs to map ", bs)
            ev_map[bs]= actual_ev
        else:
            print("bs in map ", bs)

FindEV()