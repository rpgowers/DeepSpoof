#!/bin/python

import numpy as np
import itertools as it
import player_method as pm
import matplotlib.pylab as plt

def coord_simple(x1,y1,x2,y2):
    row = 5*x1+y1
    col = 5*x2+y2
    return row,col

# A is the payoff matrix
# n is number of coins
# p is number of players
def mat_generate(A,n,p):
    m = 2*n
    for x1,x2 in it.product(range(n+1),range(n+1)):
        for y1,y2 in it.product(range(m+1),range(m+1)):
            row, col = coord_simple(x1,y1,x2,y2)
            #print(row,col)
            if y1 < x1:
                A[row,col] = -9
            elif y1 > x1+n:
                A[row,col] = -9
            elif (y1 == y2) & (p == 2):
                A[row,col] = -9
            elif y1 == x1+x2:
                A[row,col] = 1
            elif y2 == x1+x2:
                A[row,col] = -1
            else:
                A[row,col] = 0
            
    return A

def input_play(n):
		while True: 
			var = int( input("Pick the number of coins in your hand, between 0 and %i: " % n))
			if var>=0 and var<=n :
				print("You picked: %i" % var)
				return var

def input_guess(n):
		while True: 
			var = int( input("What is the total number of coins between you and the other player? It has to be between 0 and %i : " % (2*n) ))
			if var>=0 and var<=2*n :
				print("You guessed: %i" % var)
				return var

def game_step(players,history,N,P):
    payoff	= np.zeros(N)
    guesses = np.zeros(N)
    coins		= np.zeros(N)
    
    # First player picks his move
    players[1].num_coins_hand = input_play(n)

    players[0].choose_index()
    guesses[0]  = players[0].game_prediction
    print("Player 1 guesses: %i" % guesses[0])
    # history is a dead parameter

    guesses[1] = input_guess(n) 
    
    row1,col1 = coord_simple(players[0].num_coins_hand,guesses[0],players[1].num_coins_hand,guesses[1])
    payoff[0] = P[0][int(row1),int(col1)]

    row2,col2 = coord_simple(players[1].num_coins_hand,guesses[1],players[0].num_coins_hand,guesses[0])
    payoff[1] = P[1][int(row2),int(col2)]

    lastplay = int(col1)
    
    players[0].update_history(lastplay,P[0])
    #for i,j in enumerate(players):
    #    j.update_history(lastplay,P[i])
        
    print("Your oppnent had    : %i coins " % players[0].num_coins_hand)
    print("You scored          : %i " % payoff[0])
    print("The computer scored : %i " % payoff[1] 
    return payoff

def full_game(players,n,N,realisations):
    space = (N*n+1)*(n+1)
    A = np.zeros([space,space])
    P1 = mat_generate(A,n,1)
    P2 = mat_generate(A,n,2)
    payoff = np.zeros([realisations, 2])
    for i in range(realisations):
        payoff[i] = (game_step(players,0,N,[P1,P2]))
        
    return payoff
    

realisations = 20

# No touch, no break...keep alive and next time good bring to you
# https://www.youtube.com/watch?v=To2-xGxTiuU
n = 2 # number of coins
N = 2 # number of players

players = [pm.PlayerLearner(N,n),pm.PlayerRand(N,n)]
payoff = full_game(players,n,N,realisations)

plt.plot(range(realisations), np.cumsum(payoff[:,0]),label='l33t ov3r10rD')
plt.plot(range(realisations), np.cumsum(payoff[:,1]),label='puNy h00man haXx3r')
plt.legend()
plt.show()
savefig('win.png',bbox_inches='tight')
