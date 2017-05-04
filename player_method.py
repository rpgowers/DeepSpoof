import random
from heapq import nsmallest

class Player(object):

    def __init__(self,num_players,num_coins):
        self.num_players = num_players
        self.num_coins = num_coins
        self.num_coins_hand = None
        self.game_prediction = None

    def choose_hand(self,history):
        pass

    def make_prediction(self,previous_guesses,history):
        pass

class PlayerRand(Player):

    def choose_hand(self,history):
        self.num_coins_hand = random.randint(0,self.num_coins)
        return self.num_coins_hand

    def make_prediction(self,previous_guesses,history):
        while True:
            game_prediction = random.randint(self.num_coins_hand,self.num_coins*self.num_players)
            if not game_prediction in previous_guesses:
                self.game_prediction = game_prediction
                return game_prediction

class PlayerMean(Player):

    def choose_hand(self,history):
        self.num_coins_hand = random.randint(0,self.num_coins)
        return self.num_coins_hand

    def make_prediction(self,previous_guesses,history):
        game_prediction = round(self.num_coins*(self.num_players-1)/2) + self.num_coins_hand
        possible_predictions = range(self.num_coins_hand,self.num_coins*self.num_players)
        ordered_predicitions = nsmallest(len(possible_predictions), possible_predictions, key=lambda x: abs(x-game_prediction))
        for predicition in ordered_predicitions:
            if not predicition in previous_guesses:
                self.game_prediction = predicition
                return predicition

