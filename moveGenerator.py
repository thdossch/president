
class MoveGenerator:
    def __init__(self):
        '''
        Class that can generate moves based on a player and the last placed card of the game.

        '''
        self.special_cards = {7: (lambda card: card.rank < 7)}

        # 2 should be the joker card
        self.joker = 2

    def possible_cards(self, player, last_move):
        #TODO: last_move beter als last_card (want returnt card niet move)
        if last_move.rank in self.special_cards.keys():
            #sws cleaner
            moves = list(filter(self.special_cards[last_move.rank], player.cards))
            return list(filter(lambda card: len(player.get_cards_of_rank(card.rank)) >= last_move.amount, moves))

        # default rule
        return list(filter(lambda card: last_move.rank <= card.rank and \
                           len(player.get_cards_of_rank(card.rank)) >= last_move.amount, player.cards))

        
