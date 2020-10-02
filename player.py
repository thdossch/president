from skip import Skip

class Player:
    def __init__(self, name):
        '''
        Class that represents a player

        Parameters:
            name: string
        '''
        self.name = name
        self.cards = []

    def give_card(self, card):
        '''
        Function that represents receiving a card in the game

        When receiving a card the deck gets sorted
    
        Parameters: 
            card: Card
        '''
        self.cards.append(card)
        self.cards.sort()
    
    def has(self, card):
        '''
        Function that represents asking if a player has a card

        Parameters:
            card: Card

        Returns:
            has: boolean
        '''
        return card in self.cards
    
    def play(self, last_move):
        '''
        Function that represents a player making a move in the game

        Parameters:
            last_move: Card | [Card]

        Returns: 
            move: Skip | Card | [Card]
        '''
        raise NotImplementedError
    
    def is_finished(self):
        '''
        Function that checks if a player is finished

        Returns:
            finished: boolean
        '''
        return not self.cards

    def return_cards(self):
        '''
        Function that represents a player giving his cards back

        Returns
            cards: [Card]
        '''
        cards = self.cards
        self.cards = []
        return cards

    def __repr__(self):
        return f"{self.name}: {self.cards}"

     
