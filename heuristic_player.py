from player import Player
from skip import Skip
from card import Card
from move import Move
from move_generator import MoveGenerator

class HeuristicPlayer(Player):
    '''
    Player class that implements a very simple playing strategy
    '''

    def play(self, last_move):
        '''
        Overwriting parent method
        '''
        move = None
        
        # Get all possible moves
        possible_moves = MoveGenerator().generate_possible_moves(self.cards, last_move)
                
        if possible_moves:
            # Get the best move for this playertype
            move = self.find_best_move(possible_moves)
            # Get the cards that will be played
            cards_to_play = move.cards 
            # Update own cards
            self.cards = list(filter(lambda card: card not in cards_to_play, self.cards))
            # Create the move
            move = Move(cards_to_play)
        else:
            move = Skip()

        return move

    def find_best_move(self, possible_moves):
        '''
        Function that determines the best move to play for the BasicPlayer

        Parameters:
            possible_moves: [Move]
        Returns:
            best_move: Move
        '''
        moves_dict = {} 
        for move in possible_moves:
            if not move.rank in moves_dict:
                moves_dict[move.rank] = [move]
            else:
                moves_dict[move.rank].append(move) 
        
        # Check if the player can make a move without a joker
        for rank in moves_dict.keys():
            if moves_without_joker := self.moves_without_joker(moves_dict[rank]):
                return moves_without_joker[-1]
        
        # Check if the player can make a move with a joker
        for rank in moves_dict.keys():
            if moves_with_joker := self.moves_with_joker(moves_dict[rank]):
                return moves_with_joker[0]
    
    def moves_without_joker(self, moves):
        '''
        Function that filers a list of moves and returns a list without jokers

        Parameters:
            moves: [Card]
        Returns:
            moves_without_joker: [Card]
        '''
        return list(filter(lambda move: move.jokers == 0, moves))

    def moves_with_joker(self, moves):
        '''
        Function that filers a list of moves and returns a list with moves containing a joker

        Parameters:
            moves: [Card]
        Returns:
            moves_with_joker: [Card]
        '''
        return list(filter(lambda move: move.jokers >= 0, moves))
