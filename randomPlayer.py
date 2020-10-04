from player import Player
from skip import Skip
from card import Card
from move import Move
from moveGenerator import MoveGenerator
from random import randint

class RandomPlayer(Player):
    '''
    Player class that implements a random playing strategy
    '''
    def play(self, last_move):
        move = None
        # Get possible moves
        possible_moves = MoveGenerator().generate_possible_moves(self.cards, last_move)

        if possible_moves:
            # Get the cards with the same rank
            cards_to_play = possible_moves[randint(0, len(possible_moves)-1)]
            # Update own cards
            print(cards_to_play)
            self.cards = list(filter(lambda card: card not in cards_to_play, self.cards))
            # Create the move
            move = Move(cards_to_play)
        else:
            move = Skip()
        
        print(f"{self.name} plays {move}")
        return move

        
