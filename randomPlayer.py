from player import Player
from skip import Skip
from card import Card
from move import Move
from moveGenerator import MoveGenerator

class BasicPlayer(Player):
    '''
    Player class that implements a very simple playing strategy
    '''

    def play(self, last_move):
        move = None
        possible_cards = []
        # Get possible moves
        # Check if the move is the first of the round 
        if last_move.is_round_start():
            possible_cards = self.cards
        else:
            possible_cards = MoveGenerator().possible_cards(self, last_move)
                
        if possible_cards:
            # Get the cards with the same rank
            cards_to_play = self.get_cards_of_rank(possible_cards[0].rank)
            # Update own cards
            self.cards = list(filter(lambda card: card not in cards_to_play, self.cards))
            # Create the move
            move = Move(cards_to_play)
        else:
            move = Skip()
        
        print(f"{self.name} plays {move}")
        return move

        
