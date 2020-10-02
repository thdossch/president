from card import Card

class Move: 
    def __init__(self, cards):
        '''
        Class that represents a move in the game

        Parameters:
            cards: Card | [Card]
        '''
        # Check if the move is the start of a round ( cards == [] )
        if not cards:
            self.roundstart = True
        else:
            self.roundstart = False
            # Check if the move is just one card
            if isinstance(cards, Card):
                self.rank = cards.rank
                self.amount = 1
            else: # The move contains multiple cards
                self.rank = cards[0].rank
                self.amount = len(cards)
        self.cards = cards

    def is_round_start(self):
        '''
        Function that checks if the move is the start of a round

        Returns:
            is_start: boolean
        '''
        return self.roundstart

    def __in__(self, other):
        return other in self.cards

    def __repr__(self):
        return f"Move: {self.cards}" if self.cards else "Move: Round Start"
