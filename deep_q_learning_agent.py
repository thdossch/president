import torch
import random
from itertools import count
from collections import deque
from player import Player
from move import Move
from card import Card
from move_generator import MoveGenerator
from qtable import QTable
from random import randint
from skip import Skip



N_ACTIONS = 13*4 + 1 

output_to_action_mapping = [ (0,0) ] + [ (rank, amount) for rank in range(3,16) for amount in (1,5) ]

class PresidentNetwork(torch.nn.Module):
    def __init__(self, hidden_nodes):
        super(PresidentNetwork, self).__init__()
        self.linear1 = torch.nn.Linear(15, hidden_nodes)
        self.linear2 = torch.nn.Linear(hidden_nodes, N_ACTIONS)
    
    def forward(self, x):
        x = torch.nn.functional.relu(self.linear1(x))
        return self.linear2(x)


class DeepQLearningAgent(Player):
    '''
    Player class that implements a deep Q learning agent
    '''
    def __init__(self, name, train = False):
        super().__init__(name)
        self.train = train
        self.name = name
        self.BATCH_SIZE = 16
        self.MEM_SIZE = 50000
        self.GAMMA = 0.99
        self.EPS_END = 0.05
        self.eps = 1.0
        self.EPS_DECAY = 0.99
        self.N_ACTIONS = N_ACTIONS 
        self.network = PresidentNetwork(132)
        self.optimizer = torch.optim.Adam(self.network.parameters(), lr=1e-3)
        self.memory = deque(maxlen=self.MEM_SIZE)

    def play(self, last_move):
        '''
        Overwriting parent method
        '''
        possible_moves = MoveGenerator().generate_possible_moves(self.cards, last_move)
        possible_moves.append(Skip())
                                           
        state = self.get_state(last_move)

        #if not self.train:
        action = self.actual_play(state)
        
        next_move = self.action_to_move(action, possible_moves)
        if not next_move is Skip():
            cards_to_play = next_move.cards 
            self.cards = list(filter(lambda card: card not in cards_to_play, self.cards))

        return next_move 


    def actual_play(self, state):
        return output_to_action_mapping(self.select_action(state, 0))

    def select_action(self, state, eps):
        sample = random.random()
        if sample > eps:
            with torch.no_grad():
                return self.network(state).argmax().item()
        else:
            return random.randrange(self.N_ACTIONS)     

    def get_state(self, move):
        '''
        Method 

        Parameters:
            move: Move
        Returns:
            move: [ amount_3 amount_4 ... value_last amount_last ]
        '''
        if move is Skip():
            return self.cards_to_list + [ 0, 0 ]
        if move.is_round_start():
            return self.cards_to_list + [ 3, 0 ]
        return self.cards_to_list + [move.rank, move.amount]

    def cards_to_list(self):
        card_count = 13
        cards = [ 0 for _ in range(card_count) ]

        for card in self.cards:
            if card.rank == 2:
                cards[card_count-1] += 1
            else:
                cards[cards.rank-3] += 1
        
        return cards

    def move_to_action(self, move):
        '''
        Method that transforms a Move to a tuple used for indexing the QTable

        Parameters:
            move: Move
        Returns:
            action: (rank, amount)
        '''
        if move is Skip():
            return (0, 0) 
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

