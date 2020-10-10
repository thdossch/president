from move import Move

class MoveGenerator:
    def __init__(self):
        '''
        Class that can generate moves based on cards and the last placed card of the game.
        '''
        self.joker = 2
        self.special_cards = {7: (lambda card: card.rank < 7)}

    def generate_possible_moves(self, cards, last_move):
        if last_move.is_round_start():
            return [Move(cards) for cards in self.get_all_card_combinations(cards)]

        # check if last card has a special rule
        if last_move.rank in self.special_cards.keys():
            valid_cards = list(filter(self.special_cards[last_move.rank], cards))

        # use the default rules if not
        else:
            valid_cards = list(filter(lambda card: last_move.rank <= card.rank, cards))

        # TODO: think it would be better to already filter out cards before passing them to get_all_card_combos?
        # valid_cards = list(filter(lambda card: [c.rank for c in valid_cards].count(card.rank) >= last_move.amount, valid_cards))

        possible_moves = self.get_all_card_combinations(valid_cards)
        return [Move(cards) for cards in list(filter(lambda move: len(move) >= last_move.amount, possible_moves))]

    def get_all_card_combinations(self, cards):
        cards_dict = {} 
        for card in cards:
            if not card.rank in cards_dict:
                cards_dict[card.rank] = [card]
            else:
                cards_dict[card.rank].append(card) 
        
        # Check if the cardsdict contains joker key, if not add it
        if not self.joker in cards_dict:
            cards_dict[self.joker] = []

        possible_moves = []

        # Generate all moves
        for rank in cards_dict.keys():
            if rank != self.joker:
                possible_moves += self.get_all_combinations(cards_dict[rank], cards_dict[self.joker])

        # Add the moves that only contains jokers
        joker_only_moves = self.get_all_combinations(cards_dict[self.joker])
        possible_moves += joker_only_moves

        return possible_moves

    def get_all_combinations(self, cards, jokers=[]):
        return [ (cards + jokers)[0:i+1] for i in range(len(cards + jokers)) ]
