from deck import Deck

class Table:
    def __init__(self):
        '''
        Class that represents the playingfield
        '''
        self.deck = Deck()
        self.moves = []
    
    def put(self, move):
        '''
        Function that represents putting cards on the table

        Parameters: 
            move: Card | [Card]
        '''
        self.moves.append(move)

    def last_move(self):
        '''
        Function that returns the last move

        Returns:
            cards: Card | [Card]
        '''
        return self.moves[-1] if self.moves else []

    def clear(self):
        '''
        Function that represents taking all cards off the table and putting them back in 
        the deck.
        '''
        # Return the cards from the table to the deck
        [ self.deck.return_cards(move) for move in self.moves ]
        # There are no cards on the table anymore
        self.moves = []

    def take_deck(self):
        '''
        Function that represents taking the deck of the table

        Returns: 
            deck: Deck
        '''
        return self.deck

    def check_deck(self):
        '''
        Function that represents someone checking if the deck contains all cards

        Raises:
            ValueError
        '''
        if not self.deck.complete:
            raise ValueError(f"The deck is not complete, it contains {len(self.deck.cards)} cards")
