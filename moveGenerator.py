import itertools

class MoveGenerator:
    def __init__(self):
        '''
        Class that can generate moves based on cards and the last placed card of the game.
        '''
        # 2 should be the joker card
        self.joker = 2
        self.special_cards = {7: (lambda card: card.rank < 7)}

    def get_all_combinations(self, cards, jokers):
        return [ (cards + jokers)[0:i+1] for i in range(len(cards + jokers)) ]

    def get_all_card_combos(self, cards):
        #TODO: cleaner? / fix joker another way?
        ranks = set([c.rank for c in cards]) # set doesn't allow duplicates, so this returns all unique ranks

        # separate jokers and other cards
        jokers = list(filter(lambda card: card.rank == self.joker, cards))
        not_jokers =  list(filter(lambda card: card.rank != self.joker, cards))
        
        possible_moves = []

        for rank in ranks:
            moves = self.get_all_combinations(list(filter(lambda card: card.rank == rank, not_jokers)), jokers)
            possible_moves += moves
        joker_only_moves = self.get_all_combinations(list(filter(lambda card: card.rank == self.joker, not_jokers)), [])
        possible_moves += joker_only_moves

        return possible_moves

    def generate_possible_moves(self, cards, last_move):
        if last_move.is_round_start():
            return self.get_all_card_combos(cards)

        # check if last card has a special rule
        if last_move.rank in self.special_cards.keys():
            valid_cards = list(filter(self.special_cards[last_move.rank], cards))

        # use the default rules if not
        else:
            valid_cards = list(filter(lambda card: last_move.rank <= card.rank, cards))

        # TODO: think it would be better to already filter out cards before passing them to get_all_card_combos?
        # valid_cards = list(filter(lambda card: [c.rank for c in valid_cards].count(card.rank) >= last_move.amount, valid_cards))
        possible_moves = self.get_all_card_combos(valid_cards)
        return list(filter(lambda move: len(move) >= last_move.amount, possible_moves))
