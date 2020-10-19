from player import Player
from move import Move
from card import Card
from moveGenerator import MoveGenerator
from qtable import QTable
from random import randint
from skip import Skip

class AIPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.table = QTable() 
        self.learning_rate = 0.05
        self.discound_factor = 0.6
        self.epsilon = 0.2
        self.S = None
        self.A = None
        self.amount_cards_played = 0
        

    def get_best_action(self, state, possible_moves=[]):
        keys = self.table[state].keys()
        actions = None
        if not possible_moves:
            actions = self.table[state].keys() 
        else:
            actions = list(filter(lambda action: action in keys, [self.move_to_action(move) for move in possible_moves]))
        m = max(actions, key=lambda action: self.table[state][action])  
        return m

    def move_to_state(self, move):
        if move is Skip():
            return Skip()
        if move.is_round_start():
            return (0,)
        return (move.rank, move.amount)

    def move_to_action(self, move):
        if move is Skip():
            return Skip()
        return (move.rank, move.amount)
    
    def choose_action(self, state, possible_moves):
        if len(possible_moves) == 1:
            return possible_moves[0]

        val = randint(0, 100)
        if val/100 > self.epsilon:
            return self.get_best_action(state, possible_moves)
        else:
            val = randint(0, len(possible_moves)-2)
            best = self.get_best_action(state, possible_moves)
            return list(filter(lambda action: action != best, [self.move_to_action(move) for move in possible_moves]))[val]

    def update(self, new_state, possible_moves):
        r = -0.05 
        r += (self.amount_cards_played * 0.1)
        best_next_action = self.get_best_action(new_state, possible_moves)
        temporal_difference_target = r + self.discound_factor*self.table[new_state][best_next_action]
        temporal_difference = temporal_difference_target - self.table[self.S][self.A]
        self.table[self.S][self.A] += self.learning_rate*temporal_difference

    def action_to_move(self, action, possible_moves):
        return list(filter(lambda move: self.move_to_action(move) == action, possible_moves))[0]
    def play(self, last_move):
        possible_moves = MoveGenerator().generate_possible_moves(self.cards, last_move)
        possible_moves.append(Skip())
                                           
        S_new = self.move_to_state(last_move)
        self.update(S_new, possible_moves)

        self.S = S_new

        self.A = self.choose_action(self.S, possible_moves)

        next_move = self.action_to_move(self.A, possible_moves)
        if not next_move is Skip():
            cards_to_play = next_move.cards 
            self.amount_cards_played = len(cards_to_play)
            self.cards = list(filter(lambda card: card not in cards_to_play, self.cards))

        return self.action_to_move(self.A, possible_moves)


    def print_data(self):
        for state in self.table.table:
            best = self.get_best_action(state)


#ai = AIPlayer("ai")
#ai.give_card(Card(4, 'heart'))
#ai.give_card(Card(5, 'heart'))
#ai.give_card(Card(6, 'heart'))
#ai.play(Move(Card(3, 'heart')))
