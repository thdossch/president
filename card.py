class Card:
    def __init__(self, rank, suit):
        '''
        Class that represents one playingcard

        Parameters:
            rank: int    (in [1..13])
            suit: string (in ['club', 'diamond', 'heart', 'spade'])
        '''
        if rank < 1 or rank > 13:
            raise ValueError(f"'{rank} is not a valid card rank")
        # We like to construct an 'A' with rank 1 but actually it is the highest rank
        if rank == 1:
            self.rank = 14
        else:
            self.rank = rank

        if suit not in ['club', 'diamond', 'heart', 'spade']:
            raise ValueError(f"'{suit} is not a valid card suit")
        self.suit = suit

    def __repr__(self):
        suit_signs = {'club': '♣', 'diamond': '♦', 'heart': '♥', 'spade': '♠'}
        rank_signs = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        rank_sign = self.rank if self.rank not in rank_signs else rank_signs[self.rank]
        return f"({rank_sign} {suit_signs[self.suit]})" 

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        if self.rank < other.rank:
            return True
        return self.suit < other.suit if self.rank == other.rank else False
