#!/usr/bin/env python3
import sys
from typing import Dict, NamedTuple, Iterable, Iterator
from dataclasses import dataclass
from math import inf
from itertools import product
import pickle

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


ev_map: Dict[BoardState, float] = {}
with open("./ev_map.pkl", "rb") as f:
    try:
        ev_map = pickle.load(f)
    except EOFError:
        print("no pickled file to load")


positions = [i for i in range(0, 16)]  # 17 is a win
stacks = [i for i in range(0, 16)]

possible_scores = [i for i in product(positions, stacks) if i[0] + i[1] < 17]

# Spent cards
red_cards = [i for i in range(0, 13)]
green_cards = [i for i in range(0, 26)]
dbl_green_cards = [i for i in range(0, 15)]


def build_constants():
    for t in product(
        possible_scores, red_cards, green_cards, dbl_green_cards, possible_scores
    ):
        bs = BoardState(t[0], t[1], t[2], t[3], t[4])
        if bs in ev_map:
            continue
        # Deck with no cards is invalid as it is re-shuffled
        if bs.spent_red == 12 and bs.spent_green == 25 and bs.spent_double_green == 14:
            continue
            ##ev_map[bs] = ev_map[BoardState(bs.score,0,0,0,bs.opponent_score)]
        # Constants for wins where there are 0 red cards left and drawing would result in a win
        if (
            bs.spent_red == 12
            and 1 * (number_green_cards - bs.spent_green)
            + 2 * (number_dbl_green_cards - bs.spent_double_green)
            >= 17
        ):
            ev_map[bs] = inf
        # Constants for when there is only red cards left at the start of your turn.
        if bs.score[1] == 0 and bs.spent_green == 25 and bs.spent_double_green == 14:
            ev_map[bs] = 0
        # Constants for when there is only red cards left not at the start of your turn
        # In a 2 player game, if there are an even number of reds it is -ev of a fresh deck
        # and ev of a fresh deck for odds
        # if bs.score[1] != 0 and bs.spent_green == 25 and bs.spent_double_green == 14:
        # ev_map[bs] = bs.score[1]
    with open("./ev_map.pkl", "wb") as f:
        pickle.dump(ev_map, f)


def find_ev(bs: BoardState):
    if bs not in ev_map:
        cards_left = 51 - bs.spent_red + bs.spent_green + bs.spent_double_green
        # What about if cards_left is 1? The next draw would leave an empty deck
        if cards_left == 0:
            return
        red_probability = number_red_cards - bs.spent_red / cards_left
        green_probability = number_green_cards - bs.spent_green / cards_left
        dbl_green_probability = (
            number_dbl_green_cards - bs.spent_double_green / cards_left
        )

        # Checks the EV of the future board state
        raw_ev = 0.0
        r_ev = 0.0
        g_ev = 0.0
        dg_ev = 0.0

        if bs.spent_red != 12:
            r_ev = -bs.score[1] * red_probability
        if bs.spent_green != 25:
            g_bs = BoardState(
                (bs.score[0], bs.score[1] + 1),
                bs.spent_red,
                bs.spent_green + 1,
                bs.spent_double_green,
                (bs.opponent_score[0], bs.opponent_score[1]),
            )
            if g_bs.score[0] + g_bs.score[1] >= 17:
                g_ev = inf * green_probability
            else:
                g_ev = ev_map[g_bs] * green_probability
        if bs.spent_double_green != 14:
            dg_bs = BoardState(
                (bs.score[0], bs.score[1] + 2),
                bs.spent_red,
                bs.spent_green,
                bs.spent_double_green + 1,
                (bs.opponent_score[0], bs.opponent_score[1]),
            )
            if dg_bs.score[0] + dg_bs.score[1] >= 17:
                dg_ev = inf * dbl_green_probability
            else:
                dg_ev = ev_map[dg_bs] * dbl_green_probability

        # Calc value of removing card from oppt
        ev_diff = raw_ev - (
            r_ev * red_probability
            + g_ev * green_probability
            + dg_ev * dbl_green_probability
        )
        actual_ev = raw_ev - ev_diff

        print("bs added in FindEV", bs)
        ev_map[bs] = actual_ev


build_constants()

for bs in ev_map.copy().keys():
    try:
        ## Add score.position increase
        i = 1
        while bs.score[0] + i + bs.score[1] < 17:
            upper_bs = BoardState(
                (bs.score[0] + i, bs.score[1]),
                bs.spent_red,
                bs.spent_green,
                bs.spent_double_green,
                (bs.opponent_score[0], bs.opponent_score[1]),
            )
            find_ev(upper_bs)
            i += 1
        ## Add score.stack increase
        i = 1
        while bs.score[0] + bs.score[1] + i < 17:
            upper_bs = BoardState(
                (bs.score[0], bs.score[1] + i),
                bs.spent_red,
                bs.spent_green,
                bs.spent_double_green,
                (bs.opponent_score[0], bs.opponent_score[1]),
            )
            find_ev(upper_bs)
            i += 1
        ## Add spent_red increase
        i = 1
        while bs.spent_red + i < 12:
            upper_bs = BoardState(
                (bs.score[0], bs.score[1]),
                bs.spent_red + i,
                bs.spent_green,
                bs.spent_double_green,
                (bs.opponent_score[0], bs.opponent_score[1]),
            )
            find_ev(upper_bs)
            i += 1
        ## Add spent_green increase
        while bs.spent_green + i < 25:
            upper_bs = BoardState(
                (bs.score[0], bs.score[1]),
                bs.spent_red,
                bs.spent_green + i,
                bs.spent_double_green,
                (bs.opponent_score[0], bs.opponent_score[1]),
            )
            find_ev(upper_bs)
            i += 1
        while bs.spent_double_green + i < 14:
            upper_bs = BoardState(
                (bs.score[0], bs.score[1]),
                bs.spent_red,
                bs.spent_green,
                bs.spent_double_green + i,
                (bs.opponent_score[0], bs.opponent_score[1]),
            )
            find_ev(upper_bs)
            i += 1
        ## Add oppenent_score.position increase
        i = 1
        while bs.opponent_score[0] + i + bs.opponent_score[1] < 17:
            upper_bs = BoardState(
                (bs.score[0], bs.score[1]),
                bs.spent_red,
                bs.spent_green,
                bs.spent_double_green,
                (bs.opponent_score[0] + i, bs.opponent_score[1]),
            )
            find_ev(upper_bs)
            i += 1
        ## Add oppenent_score.stack increase
        i = 1
        while bs.opponent_score[0] + bs.opponent_score[1] + i < 17:
            upper_bs = BoardState(
                (bs.score[0], bs.score[1]),
                bs.spent_red,
                bs.spent_green,
                bs.spent_double_green,
                (bs.opponent_score[0], bs.opponent_score[1] + i),
            )
            find_ev(upper_bs)
            i += 1
    except KeyError:
        pass


leftover = []
try:
    for t in product(
        possible_scores, red_cards, green_cards, dbl_green_cards, possible_scores
    ):
        bs = BoardState(t[0], t[1], t[2], t[3], t[4])
        try:
            find_ev(bs)
        except KeyError as e:
            find_ev(e.args[0])
except KeyError as e:
    with open("./ev_map.pkl", "wb") as f:
        pickle.dump(ev_map, f)
    print("Unexpected error:", sys.exc_info()[0])
    leftover.append(e.args[0])

for bs in leftover:
    try:
        find_ev(bs)
    except KeyError as e:
        print("adding to leftover: ", e.args[0])
        leftover.append(e.args[0])
        with open("./ev_map.pkl", "wb") as f:
            pickle.dump(ev_map, f)
        continue

with open("./ev_map.pkl", "wb") as f:
    pickle.dump(ev_map, f)
