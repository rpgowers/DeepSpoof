import numpy as np
import itertools as it
import player_method as pm

def coord_simple(x1,y1,x2,y2):
    row = 5*x1+y1
    col = 5*x2+y2
    return row,col

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

# This should return the new state
# separate the component of actually fetching the payoff
def game_step(players,history,n,N):
    space = (N*n+1)*(n+1)
    A = np.zeros([space,space])
    Q1 = mat_generate(A,n,1)
    Q2 = mat_generate(A,n,2)
    payoff = np.zeros(N)
    guesses = np.zeros(N)
    coins = np.zeros(N)
    #total_coins = 0
    for i,j in enumerate(players):
        coins[i] = j.choose_hand(history)
        print(coins[i])
    for i,j in enumerate(players):
        guesses[i] = j.make_prediction(guesses[0:i],history)
        print(guesses[i])
        #total_coins += j.coins_hand
    #for i,j in enumerate(players)
    #    row,col = coord(N,total_coins,players)
    #    payoff[i] = Q[row,col]
    row,col = coord_simple(players[0].num_coins_hand,guesses[0],players[1].num_coins_hand,guesses[1])
    
    payoff[0] = Q1[int(row),int(col)]
    row,col = coord_simple(players[1].num_coins_hand,guesses[1],players[0].num_coins_hand,guesses[0])
    payoff[1] = Q2[int(row),int(col)]
    return payoff

# Update the Qs in
# j,k = #nr of players
# i,l = #nr of coins 

# Current frequency
# x_i^j = e^(b*Q_i^j)/Z 
# y_i^j = OBSERVED frequency (i.e. history)
# Update weights for choice
# Q_i^j (t+1) = (1-alpha)Q_i^j + sum_l P(i,l)  y^k

realisations = 1
n = 2 # number of coins
N = 2 # number of players
players = [pm.PlayerRand(N,n),pm.PlayerRand(N,n)]

for i in range(realisations):
    print(game_step(players,0,n,N))
