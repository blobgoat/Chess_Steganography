# This program is a Python program that can accept a file and encode the file into chess games using the PGN file format
# This program was created for educational purposes for a Computer Forensics project at California State University, Sacramento.
# Date Last Modified: 04 May 2018
# update by neko.py 2023/09/20

import math
import re

import chess

def decodeAll(txt):
    board = chess.Board()
    bin = ""
    for move in txt:
        if '-' in move:
            continue
        #print(board)
        legals = list(board.legal_moves)
        idx = legals.index(board.parse_san(move))
        bits = math.ceil(math.log(len(legals), 2))
        repre = ("{:0" + f"{bits}" + "b}").format(idx)
        bin += repre
        board.push_san(move)
    return hex(int(bin, 2))[2:]
    

if __name__ == '__main__':
    with open('moves.pgn', 'r') as f:
        unsplit = ' '.join([x.strip() for x in re.split('(\d+\.)', '\n'.join(f.readlines())) if x and '.' not in x]).split()
        print(decodeAll(unsplit))
