from player import Player
from move import Move
from card import Card
from move_generator import MoveGenerator
from qtable import QTable
from random import randint
from skip import Skip

class TemporalDifferenceAgent(Player):
    '''
    Player class that implements a temporal difference learning agent
    '''

    def __init__(self, name, learning_rate, discount_factor, epsilon):
        super().__init__(name)
        self.table = QTable() 
        self.learning_rate = learning_rate #0.05
        self.discount_factor = discount_factor #0.6
        self.epsilon = epsilon #0.2
        self.S = None
        self.A = None
        self.amount_cards_played = 0 
        self.amount_cards_played_round = 0 
        
    def play(self, last_move):
        '''
        Overwriting parent method
        '''
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
            self.amount_cards_played_round += len(cards_to_play)
            self.cards = list(filter(lambda card: card not in cards_to_play, self.cards))
        else:
            self.amount_cards_played = -1
            self.amount_cards_played_round = 0
            

        return self.action_to_move(self.A, possible_moves)

    def update(self, new_state, possible_moves):
        r = -0.1
        if self.amount_cards_played == -1:
            r = -2
        else:
            r += (self.amount_cards_played * 0.5)
        r += 0.2 * self.amount_cards_played_round

        temporal_difference_target = r + self.discount_factor*self.get_best_q_value(new_state)
        temporal_difference = temporal_difference_target - self.table[self.S][self.A]
        self.table[self.S][self.A] += self.learning_rate*temporal_difference
    
    def get_best_q_value(self, state):
        '''
        Function that returns the best q-value for a state

        Parameters:
            state: (rank, amount)
        Returns:
            q-value: int
        '''
        return max([self.table[state][action] for action in self.table[state].keys()])

    def get_best_action(self, state, possible_moves):
        '''
        Function that returns the best action according to the QTable given a state and possible moves

        Parameters:
            state: (rank, amount)
            possible_moves: [Move]
        Returns:
            q-value: int
        '''
        return max([self.move_to_action(move) for move in possible_moves], key=lambda action: self.table[state][action])  

    def choose_action(self, state, possible_moves):
        '''
        Function that chooses a action/move to make, looking at epsilon for exploration

        Parameters:
            state: (rank, amount)
            possible_moves: [Move]
        Returns:
            action: (rank, amount)
        '''
        if len(possible_moves) == 1:
            return possible_moves[0]

        val = randint(0, 100)
        if val/100 > self.epsilon:
            return self.get_best_action(state, possible_moves)
        else:
            val = randint(0, len(possible_moves)-2)
            best = self.get_best_action(state, possible_moves)
            return list(filter(lambda action: action != best, [self.move_to_action(move) for move in possible_moves]))[val]

    def notify_round_end(self):
        '''
        Overwriting parent method
        '''
        self.S = None
        self.A = None
        self.amount_cards_played = 0 
        self.amount_cards_played_round = 0 

    def print_data(self):
        '''
        Method that prints the data of agent
        '''
        self.table.show() 

    def move_to_state(self, move):
        '''
        Method that transforms a Move to a tuple used for indexing the QTable

        Parameters:
            move: Move
        Returns:
            move: (rank, amount)
        '''
        if move is Skip():
            return Skip()
        if move.is_round_start():
            return (0,)
        return (move.rank, move.amount)

    def move_to_action(self, move):
        '''
        Method that transforms a Move to a tuple used for indexing the QTable

        Parameters:
            move: Move
        Returns:
            action: (rank, amount)
        '''
        if move is Skip():
            return Skip()
        return (move.rank, move.amount)

    def action_to_move(self, action, possible_moves):
        '''
        Method that seeks the move corresponding to a action

        Parameters:
            action: (rank, amount)
            possible_moves: [Move]
        Returns:
            move: Move
        '''
        return list(filter(lambda move: self.move_to_action(move) == action, possible_moves))[0]

    def notify_game_end(self, rank):
        self.epsilon = max(0.05, self.epsilon * 0.999962)
