#!/usr/bin/env python3
from math import inf
from itertools import product

ev_map = {}

positions = [i for i in range(0,16)] # 17 is a win
stacks = [i for i in range(0,16)]

possible_scores = [i for i in product(positions, stacks) if i[0]+i[1]<17]

# Spent cards
redCards = [i for i in range(0,12)]
greenCards = [i for i in range(0,25)]
dblGreenCards = [i for i in range(0,14)]

possible_turn_states = product(possible_scores, redCards, greenCards, dblGreenCards)

infinite_states = [i for i in possible_turn_states if redCards==12 and 1*i[2] +2*i[3] >= 17]
zero_states = [i for i in possible_turn_states if i[0][1]==0 and i[2]==25 and i[3]==14]

# Constants for wins where there are 0 red cards left and drawing would result in a win
for i in infinite_states:
    ev_map[f"{i[0][0]}-{i[0][1]}-12-{i[2]}-{i[3]}"] = inf

# Constants for when there is only red cards left at the start of your turn.
for position in zero_states:
    ev_map[f"{i[0][0]}-0-0-25-14"] = 0
