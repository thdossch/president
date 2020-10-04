
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

    def generate_possible_moves(self, player, last_move):
        valid_cards = list(filter(lambda card: last_move.rank <= card.rank, player.cards))
        ranks = self.get_all_ranks(valid_cards)
        jokers = list(filter(lambda card: card.rank == self.joker), player.cards)

        possible_moves = []
        for rank in ranks:
            moves = self.get_all_combinations(list(filter(lambda card: card.rank == rank, valid_cards)), jokers)
            possible_moves.append(moves)
        return possible_moves

    def get_all_ranks(self, cards):
        ranks = []
        for card in cards:
            if card.rank not in ranks and rank != self.joker:
                ranks.append(rank)
        return ranks

    def get_all_combinations(self, cards, jokers):
        return [ (cards + jokers)[0:i+1] for i in range(len(cards + jokers)) ]
