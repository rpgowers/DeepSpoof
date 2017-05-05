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

def game_step(players,history,N,P):
    payoff = np.zeros(N)
    guesses = np.zeros(N)
    coins = np.zeros(N)
    
    #for i,j in enumerate(players):
    #    coins[i] = j.choose_hand(history)
        #print(coins[i])
    #for i,j in enumerate(players):
    #    guesses[i] = j.make_prediction(guesses[0:i],history)
        #print(guesses[i])
        
    players[0].choose_index()
    players[1].choose_hand(history)
    guesses[0] = players[0].game_prediction
    guesses[1] = players[1].make_prediction(guesses,history)
    
    row1,col1 = coord_simple(players[0].num_coins_hand,guesses[0],players[1].num_coins_hand,guesses[1])
    payoff[0] = P[0][int(row1),int(col1)]
    row2,col2 = coord_simple(players[1].num_coins_hand,guesses[1],players[0].num_coins_hand,guesses[0])
    payoff[1] = P[1][int(row2),int(col2)]
    lastplay = int(col1)
    
    players[0].update_history(lastplay,P[0])
    #for i,j in enumerate(players):
    #    j.update_history(lastplay,P[i])
        
    return payoff,lastplay

# Update the Qs in
# j,k = #nr of players
# i,l = #nr of coins 

# Current frequency
# x_(i,v)^j = e^(Beta*Q_i^j)/Z 
# y_i^j = OBSERVED frequency (i.e. history)
# Update weights for choice
# Alpha = memory, 0 is full memory and equal weights to past obs.
#								 >0 more recent more weight
#								  0 no memory
# Beta = 	intensity, 0 is uniformly at random pick
#										 >0 small historical advantage increases frequency
# Q_i^j (t+1) = (1-Alpha)Q_i^j + sum_l P(i,l)  y^k

def full_game(players,n,N,realisations):
    space = (N*n+1)*(n+1)
    A = np.zeros([space,space])
    P1 = mat_generate(A,n,1)
    P2 = mat_generate(A,n,2)
    for i in range(realisations):
        print(game_step(players,0,N,[P1,P2]))
    

realisations = 10
n = 2 # number of coins
N = 2 # number of players

players = [pm.PlayerLearner(N,n),pm.PlayerRand(N,n)]
full_game(players,n,N,realisations)
