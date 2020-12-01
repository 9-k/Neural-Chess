# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 16:54:05 2020

@author: Ian
"""
import numpy as np
import chess.pgn

def winner(game):
    """
    Returns winner of game. 0 for black, 1 white, -1 tie.
    """
    results = game.headers['Result']
    if (results == '0-1'):
        #print("Black wins.")
        return 0
    elif (results == '1-0'):
        #print("White wins.")
        return 1
    elif (results == "1/2-1/2"):
        #print("Tied.")
        return -1
    else:
        raise Exception("Can't tell who won. Is the header mangled?")
        
        

def bitboard(state): 
    """This function takes a python-chess board of type chess.Board
    and returns a 768 (8 rows x 8 columns x 6 piece types x 2 colors)
    entry long 1-D numpy array that represents the positions, class, and color
    of each piece on the board. The returned string is just concatenations of
    64 entry long vectors. Each vector counts the whole board like [a1, b1, ...
    h1, a2, b2, ..., h2, ... a8, b8, ..., h8].
    The order of pieces is as follows: White pawn, knight,
    bishop, rook, queen, king. Then, black pawn, knight,
    bishop, rook, queen, king."""
    
    bitboard = []
    for k in range(2):
        for i in range(6):
            piece = list(state.pieces(i+1, 1-k))
            piece_bits = [0] * 64
            for pos in piece:
                piece_bits[pos] = 1
            bitboard.extend(piece_bits)
    return bitboard

def listify_good_pgns(pgn):
    """
    takes pgn of many games and breaks into python list, each entry being a game.
    only takes games that are a certain length and not tied haha
    """
    game_list = []
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break  # this is the end of file
        game_length = game.headers['PlyCount']
        if int(game_length) < 25:
            continue #if the game is short and garbage throw it out
        if winner(game) == -1:
            continue #if it's tied throw it out
        game_list.append(game)
    print("finished reading the pgn, boss!")
    return game_list
        
def create_training_data(game_list):
    """
    takes python list of games and turns it into two vectors: a bitboard representation
    of every state and a vector representing if the winner created that state.
    """
    all_states = []
    did_white_win = []
    i = 0
    k = 0
    num_of_games = len(game_list)
    for game in game_list:
        if i == 10000:
            print("Just hit 10k games. Saving to prevent OOM errors.")
            all_states = np.array(all_states, dtype = np.int8)
            did_white_win = np.array(did_white_win)
            np.savez_compressed("data/dww" + str(k), did_white_win)
            np.savez_compressed("data/all_states" + str(k), all_states)
            k = k+1
            i = 0
            all_states = []
            did_white_win = []
            
        victor = winner(game)
        print("working on game " + str(k*10000 + i) + "/" + str(num_of_games))
        i = i+1
        for state in game.mainline(): 
            did_white_win.append([victor])
            all_states.append(bitboard(state.board()))   
            
    all_states = np.array(all_states, dtype = np.int8)
    did_white_win = np.array(did_white_win)
    k = k+1
    np.savez_compressed("data/all_states" + str(k), all_states)
    np.savez_compressed("data/dww" + str(k), did_white_win)


if __name__ == "__main__":
    pgn = open("data/ficsgamesdb_2016_standard2000_nomovetimes_169446.pgn")
    game_list = listify_good_pgns(pgn)    
    create_training_data(game_list)





