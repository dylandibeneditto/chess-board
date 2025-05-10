import csv
import os
import re

def normalize_moves(moves):
    return re.sub(r"\d+\.\s*", "", moves)

def load_openings():
    openings = []
    base_path = "./engine/openings"
    for filename in ["a.tsv", "b.tsv", "c.tsv", "d.tsv", "e.tsv"]:
        file_path = os.path.join(base_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if len(row) >= 3:
                    eco, name, moves = row
                    normalized_moves = normalize_moves(moves)
                    openings.append((eco, name, normalized_moves))
    return openings

def find_opening(moves, openings):
    best_match = ("?", "Unknown Opening")
    best_length = 0

    for eco, name, opening_moves in openings:
        if "".join(moves[:len("".join(opening_moves.split(" ")))]) == "".join(opening_moves.split(" ")):
            if len(opening_moves) > best_length:
                best_match = (eco, name)
                best_length = len(opening_moves)
                
    return best_match

OPENINGS = load_openings()

def get_opening(moves):
    return find_opening(moves, OPENINGS)