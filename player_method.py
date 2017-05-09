import random
import numpy as np
from heapq import nsmallest

class Player(object):

    def __init__(self,num_players,num_coins):
        self.num_players = num_players
        self.num_coins = num_coins
        self.num_coins_hand = None
        self.game_prediction = None
        # frequency of myself and the observed events of my opponent
        self.L = (num_coins+1)*(num_players*num_coins+1)	# Possible pair of moves  

        self.freq = np.ones(self.L)/self.L								# Frequency of play 
        self.historic = np.zeros(self.L)									# Frequency of other player (observed)
        self.Q = np.zeros(self.L)													# Starting weights
        self.T = 0 																				# this is the internal clock

        self.alpha = 0.5				# Memory: 0 full recall
        self.beta = 1						# Intesity: larger means more weight on small advantages

    def choose_hand(self,history):
        pass

    def make_prediction(self,previous_guesses,history):
        pass
    
    def update_history(history):
        pass
    
class PlayerLearner(Player):
    def choose_index(self):
        # Picks random move according to learned frequency
        index = np.random.choice(np.arange(self.L),p=self.freq)
        #	Translate move index into nr. coins and guess  
        self.num_coins_hand = index//(self.num_players*self.num_coins+1)
        self.game_prediction = index%(self.num_players*self.num_coins+1)

    def update_history(self,lastplay,P):
        self.T += 1 # update clock by one game step
        self.historic[lastplay] += 1
        
        Z = 0
        for i in range(self.L):
            temp = 0
            for j in range(self.L):
                temp += P[i,j]*self.historic[j]/self.T
            
            self.Q[i] = (1-self.alpha)*self.Q[i]+temp
            Z += np.exp(self.beta*self.Q[i]) 
            
        self.frequency = np.exp(self.beta*self.Q)/Z
            
class PlayerRand(Player):

    def choose_hand(self,history):
        self.num_coins_hand = random.randint(0,self.num_coins)
        #return self.num_coins_hand

    def make_prediction(self,previous_guesses,history):
        while True:
            game_prediction = random.randint(self.num_coins_hand,self.num_coins*self.num_players)
            if not game_prediction in previous_guesses:
                self.game_prediction = game_prediction
                return game_prediction

class PlayerMean(Player):

    def choose_hand(self,history):
        self.num_coins_hand = random.randint(0,self.num_coins)
        #return self.num_coins_hand

    def make_prediction(self,previous_guesses,history):
        game_prediction = round(self.num_coins*(self.num_players-1)/2) + self.num_coins_hand
        possible_predictions = range(self.num_coins_hand,self.num_coins*self.num_players)
        ordered_predicitions = nsmallest(len(possible_predictions), possible_predictions, key=lambda x: abs(x-game_prediction))
        for predicition in ordered_predicitions:
            if not predicition in previous_guesses:
                self.game_prediction = predicition
                return predicition
            
class PlayerExEx(Player):

    def choose_hand(self,history):
        self.num_coins_hand = random.randint(0,self.num_coins)

    def make_predicition(self,previous_guesses,history):
        information = [x - round(self.num_coins*(self.num_players-1)/2) for x in previous_guesses]
        expected_remaining = round(self.num_coins*(self.num_players - 1 - len(information)))
        game_prediction = expected_remaining + sum(information) + self.num_coins_hand
        possible_predictions = range(self.num_coins_hand,self.num_coins*self.num_players)
        ordered_predicitions = nsmallest(len(possible_predictions), possible_predictions, key=lambda x: abs(x-game_prediction))
        for predicition in ordered_predicitions:
            if not predicition in previous_guesses:
                self.game_prediction = predicition
                return predicition

#player_dict = {"rand":PlayerRand(),"mean":PlayerMean(),"exex":PlayerExEx}
