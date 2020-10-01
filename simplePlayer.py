from player import Player
from skip import Skip

class SimplePlayer(Player):
    '''
    Player class that implements a very simple playing strategy
    '''

    def play(self, last_move):
        card = self.cards.pop(0) if self.cards else Skip()
        print(f"{self.name} plays {card}")
        return card
