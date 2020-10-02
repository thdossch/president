from player import Player
from skip import Skip
from card import Card
from move import Move

class BasicPlayer(Player):
    '''
    Player class that implements a very simple playing strategy
    '''

    def play(self, last_move):
        move = None
        possible_moves = []
        # Get possible moves
        # Check if the move is the first of the round 
        if last_move.is_round_start():
            possible_moves = self.cards
        else:
            possible_moves = list(filter(lambda card: last_move.rank <= card.rank and \
                                         len(self.get_cards_of_rank(card.rank)) >= last_move.amount, self.cards))
                
        if possible_moves:
            # Get the cards with the same rank
            cards_to_play = self.get_cards_of_rank(possible_moves[0].rank)
            # Update own cards
            self.cards = list(filter(lambda card: card not in cards_to_play, self.cards))
            # Create the move
            move = Move(cards_to_play)
        else:
            move = Skip()
        
        print(f"{self.name} plays {move}")
        return move

    def get_cards_of_rank(self, rank):
        '''
        Function that returns all cards of a given rank

        Parameters: 
            rank: int
        Returns:
            cards: [Card]
        '''
        return list(filter(lambda card: card.rank == rank, self.cards))
        
