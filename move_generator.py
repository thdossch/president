from move import Move

class MoveGenerator:
    def __init__(self):
        '''
        Class that can generate moves based on cards and the last placed card of the game.
        '''
        self.joker = 2
        self.special_cards = {7: (lambda card: card.rank < 7)}

    def generate_possible_moves(self, cards, last_move):
        '''
        Function that generates all possible moves that can be played for a set of cards and the last move

        Parameters:
            last_move: Move
        Returns:
            possible_moves: [Move]
        '''
        if last_move.is_round_start():
            return [Move(cards) for cards in self.get_all_card_combinations(cards)]

        # check if last card has a special rule
        if last_move.rank in self.special_cards.keys():
            valid_cards = list(filter(self.special_cards[last_move.rank], cards))

        # use the default rules if not
        else:
            valid_cards = list(filter(lambda card: last_move.rank <= card.rank or card.rank == self.joker, cards))

        possible_moves = self.get_all_card_combinations(valid_cards)
        return [Move(cards) for cards in list(filter(lambda move: len(move) >= last_move.amount, possible_moves))]

    def get_all_card_combinations(self, cards):
        '''
        Function that generates all possible card combinations, that are valid in President, for a given list of cards

        Parameters:
            cards: [Card]
        Returns:
            possible_combinations: [[Card]]
        '''
        cards_dict = {} 
        for card in cards:
            if not card.rank in cards_dict:
                cards_dict[card.rank] = [card]
            else:
                cards_dict[card.rank].append(card) 
        
        # Check if the cardsdict contains joker key, if not add it
        if not self.joker in cards_dict:
            cards_dict[self.joker] = []

        possible_combinations = []

        # Generate all moves
        for rank in cards_dict.keys():
            if rank != self.joker:
                possible_combinations += self.get_all_combinations(cards_dict[rank], cards_dict[self.joker])

        # Add the moves that only contains jokers
        joker_only_moves = self.get_all_combinations(cards_dict[self.joker])
        possible_combinations += joker_only_moves

        return possible_combinations

    def get_all_combinations(self, cards, jokers=[]):
        '''
        Function that generates possible combinations of a list of cards and jokers, used to combine
        cards of one rank and jokers

        Parameters:
            cards: [Card]
            jokers: [Card]
        Returns:
            combinations: [[Card]]
        '''
        return [ (cards + jokers)[0:i+1] for i in range(len(cards + jokers)) ]
