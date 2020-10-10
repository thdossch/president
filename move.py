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
                # Check if the move is not only a joker
                if cards.rank == 2:
                    self.rank = 15
                else:
                    self.rank = cards.rank
                self.amount = 1
                self.jokers = 0
            else: # The move contains multiple cards
                normal_cards, jokers = self.extract_jokers(cards)
                # Check if the move is not only jokers
                if normal_cards == []:
                    self.rank = 15
                else:
                    self.rank = normal_cards[0].rank
                self.amount = len(normal_cards) + len(jokers)
                self.jokers = len(jokers)
        self.cards = cards

    def is_round_start(self):
        '''
        Function that checks if the move is the start of a round

        Returns:
            is_start: boolean
        '''
        return self.roundstart

    def extract_jokers(self, cards):
        normal_cards = list(filter(lambda card: card.rank != 2, cards))
        jokers = list(filter(lambda card: card.rank == 2, cards))
        return normal_cards, jokers

    def __in__(self, other):
        return other in self.cards

    def __repr__(self):
        return f"Move: {self.cards}" if self.cards else "Move: Round Start"
