from player import Player
from skip import Skip
from card import Card

class BasicPlayer(Player):
    '''
    Player class that implements a very simple playing strategy
    '''

    def play(self, last_move):
        move = None
        possible_moves = []
        # Get possible moves
        # Check if the move is the first of the round 
        if not last_move:
            possible_moves = self.cards
        elif isinstance(last_move, Card): # Check if the move contains one card
            possible_moves = list(filter(lambda card: last_move.rank <= card.rank, self.cards))
        else: # The move contains multiple cards
            possible_moves = list(filter(lambda card: last_move[0].rank <= card.rank and \
                                         len(self.get_cards_of_rank(card.rank)) >= len(last_move), self.cards))
                



        if possible_moves:
            # Get the cards with the same rank
            move = self.get_cards_of_rank(possible_moves[0].rank)
            # Update own cards
            self.cards = list(filter(lambda card: card not in move, self.cards))
        else:
            move = Skip()
        
        print(f"{self.name} plays {move}")
        return move

    def get_cards_of_rank(self, rank):
        return list(filter(lambda card: card.rank == rank, self.cards))
        
