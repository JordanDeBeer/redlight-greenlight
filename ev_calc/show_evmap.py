#!/usr/bin/env python3

from dataclasses import dataclass
import pickle

@dataclass(frozen=True)
class BoardState:
    score: tuple

    spent_red: int
    spent_green: int
    spent_double_green: int

    opponent_score: tuple

ev_map = {}

with open("./ev_map.pkl", "rb") as f:
    ev_map = pickle.load(f)

for k,v in ev_map.items():
    print(f"{k}:{v}")
