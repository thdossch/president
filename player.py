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
            last_move: Move

        Returns: 
            move: Skip | Move
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

    def take_worst_card(self):
        '''
        Function that takes the worst card of a player

        Returns:
            worst_card: Card
        '''
        return self.cards.pop(0)

    def take_best_card(self):
        '''
        Function that takes the best card of a player

        Returns:
            best_card: Card
        '''
        return self.cards.pop(-1)

    def switch_with_high_scum(self, high_scum):
        '''
        Function that represents the vice-president switching hit worst card for the best
        card of the scum

        Parameters:
            high_scum: Player
        '''
        high_scum.give_card(self.take_worst_card()) 
        self.give_card(high_scum.take_best_card())

    def switch_with_scum(self, scum):
        '''
        Function that represents the president switching hit 2 worst cards for the 2 best
        cards of the scum

        Parameters:
            scum: Player
        '''
        scum.give_card(self.take_worst_card()) 
        scum.give_card(self.take_worst_card()) 
        self.give_card(scum.take_best_card())
        self.give_card(scum.take_best_card())

    def __repr__(self):
        return f"{self.name}: {self.cards}"

     
