
class Validator:
    def __init__(self):
        '''
        Class that represents a player

        Parameters:
            name: string
        '''
        self.special_cards = {7: (lambda card: 7 > card.rank)}

    def default_possible_moves(self, player, last_move):
        #TODO: last_move beter als last_card (want returnt card niet move)
        if last_move.rank in self.special_cards.keys():
            moves = list(filter(self.special_cards[last_move.rank], player.cards))
            return list(filter(lambda card: len(player.get_cards_of_rank(card.rank)) >= last_move.amount, moves))

        return list(filter(lambda card: last_move.rank <= card.rank and \
                           len(player.get_cards_of_rank(card.rank)) >= last_move.amount, player.cards))

        