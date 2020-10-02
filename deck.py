from card import Card
from random import shuffle

class Deck:
    def __init__(self):
        '''
        Class that represents a deck of cards
        '''
        self.cards = [ Card(rank, suit) for rank in range(1, 14) for suit in ['club', 'diamond', 'heart', 'spade'] ]
    
    def take_cards(self):
        while self.cards and (card := self.cards.pop()):
            yield card
    
    def return_cards(self, cards):
        # Cards is only one card
        if isinstance(cards, Card):
            self.cards.append(cards)
        # Multiple cards are returned
        else:
            for card in cards: 
                self.cards.append(card)

    def shuffle(self):
        '''
        Function that shuffles the cards in this deck
        '''
        shuffle(self.cards)
    
    @property
    def complete(self):
        '''
        Property that represents if the deck is completer
        
        Returns: 
            complete: boolean
        '''
        return len(self.cards) == 52

    def __repr__(self):
        return '\n'.join([str(card) for card in self.cards])
