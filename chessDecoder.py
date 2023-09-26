# This program is a Python program that can accept a file and encode the file into chess games using the PGN file format
# This program was created for educational purposes for a Computer Forensics project at California State University, Sacramento.
# Date Last Modified: 04 May 2018
# update by neko.py 2023/09/20

import math
import re
import pprint
import chess

#global variables
#eventually will be replaced by input, but for testing purposes
order= ('p','n','b','r','q','k')


def decodeAll(txt):
    board = chess.Board()
    legalsSAN=[]
    bin = ""
    for move in txt:
        if '-' in move:
            continue
        #print(board)
        legals = list(board.legal_moves)
        for legMove in legals:
            legalsSAN.append(board._algebraic(legMove))

        sortedLegals=sort(legalsSAN)

        idx = sortedLegals.index(move)
        bits = math.ceil(math.log(len(legals), 2))
        repre = ("{:0" + f"{bits}" + "b}").format(idx)
        bin += repre
        board.push_san(move)
    return listOfHex(bin)
  
    #pre conditions= none: 
    #important note: why? drops remainder when dividing by 8
    #post= returns list of hexidecimal, maybe convert into ASCII directly?
    #converts inputted long string of 0s and 1s into list of 8 char long strings, and then into hexidecimal
def listOfHex(input):
    decode = []
    for i in range(0,int(len(input)/8)+1):
        token=input[i*8:i*8+8]
        decimal=int(token,2)
        token=hex(decimal)[2:]
        decode.append(token)
    
    return decode

    

#earlier alphabet letters then earlier numbers are assumed to have priority. Castling has least priority, king>queen castling
#priority of pieces is inputed as char p=pawn, n=knight, b=bishop, r=rook, q=queen, k=king
#pre: legals is a list of strings that are two to four char long. Starting letter denotes name of piece and if absent then
#it is a pawn move. With the exception of castling which is O-O or O-O-O

def sort(legals):
#arrays for each type
    pawn=[]
    knight=[]
    bishop=[]
    rook=[]
    queen=[]
    king=[]

    returning=[]
    for move in legals:
        if (move[0]=='K'or move[0]=='O'):
            king.append(move)
        elif (move[0]=='B'):
            bishop.append(move)
        elif (move[0]=='N'):
            knight.append(move)
        elif (move[0]=='Q'):
            queen.append(move)
        elif (move[0]=='R'):
            rook.append(move)
        else:
            pawn.append(move)

#sorting all of the moves in order
    bishop=sortmoves(bishop)
    rook=sortmoves(rook)
    knight=sortmoves(knight)
    queen=sortmoves(queen)
    king=sortmoves(king)
    pawn=sortmoves(pawn)
#putting pieces in priority order
    for piece in order:
        if (piece=='k'):
            for move in king:
                returning.append(move)
        elif (piece=='b'):
            for move in bishop:
                returning.append(move)
        elif (piece=='n'):
            for move in knight:
                returning.append(move)
        elif (piece=='q'):
            for move in queen:
                returning.append(move)
        elif (piece=='r'):
            for move in rook:
                returning.append(move)
        else:
            for move in pawn:
                returning.append(move)

    return returning


#avoiding x by doing negative indexing
#uses .sort to easily put earlier alphabet letters and numbers in front
def sortmoves(list):
    if len(list)!=0:
        list.sort(key=lambda x:x[-2:-1])

    return list



if __name__ == '__main__':
    with open('moves.pgn', 'r') as f:
        unsplit = ' '.join([x.strip() for x in re.split('(\d+\.)', '\n'.join(f.readlines())) if x and '.' not in x]).split()
        pprint.pprint(decodeAll(unsplit))
