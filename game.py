from card import Card
from table import Table
from skip import Skip
from move import Move
from util import vprint
from termcolor import colored
from move_generator import MoveGenerator

class Game:
    def __init__(self, players, ranks, verbose = True):
        '''
        Class that represents a game of President

        A Game exists out of multiple rounds, a round is until only one player did not skip
        Exemple game with 5 players: 
            Game: 
                round -> p1 wins, he can start next round
                round -> p3 wins, he can start next round
                ...
                round -> p1 wins, and has no cards left
                      -> p1 is president

                The game continues
                round -> p3 wins, he can start next round
                ...
                round -> p2 wins, and has no cards left
                      -> p2 is vice-president
                
                The game continues
                round -> p2 wins, he can start next round
                ...
                round -> p3 wins, and has no cards left
                      -> p3 is a Person
                
                The game continues
                round -> p5 wins, he can start next round
                ...
                round -> p4 wins, and has no cards left
                      -> p4 is high-scum
                      -> p5 is scum

            Now a new game can be played with the obtained ranks

        Parameters:
            players: [Player]
        '''
        self.players = players 
        self.table = Table()
        self.ranks = ranks

        # Should game be printed or not
        self.verbose = verbose

        
    def start(self):
        '''
        Function that starts a game
        '''
        # Check if the game has at least 2 players
        if len(self.players) < 2:
            raise ValueError(f"A game can't be played with {len(self.players)} players.")
    
        # Deal the cards
        self.deal()
        # Switch cards between ranks
        self.switch()
        # Play the game
        finish_order = self.play()
        # Process the results
        ranks = self.finish(finish_order)
        # Return the ranks
        return ranks

    def deal(self):
        ''' 
        Function that represents dealing the cards
        '''
        # Take the deck of the table, shuffel it, deal the cards
        deck = self.table.take_deck()
        deck.shuffle()
        for (i, card) in enumerate(deck.take_cards()):
            self.players[i%(len(self.players))].give_card(card)
    
    def switch(self):
        '''
        Function that represents switching the cards between ranks in the beginning of the game
        '''
        if self.ranks:
            self.ranks['president'].switch_with_scum(self.ranks['scum']) 
            if 'vice_president' in self.ranks:
                self.ranks['vice_president'].switch_with_high_scum(self.ranks['high_scum']) 
    def play(self):
        '''
        Function that represents a game

        Returns:
            finish_order: [Player]
        '''
        # Get the starting player for the first round
        starting_player = self.get_starting_player()
        
        # List to keep track of finished players
        finished_players = []

        for player in self.players:
            player.notify_game_start()
       
        vprint("==============================", self.verbose)
        vprint("Start new game", self.verbose) 
        vprint("==============================\n", self.verbose)
        vprint(f"{starting_player.name} is the starting player", self.verbose) 

        # Play rounds until one player lost the game
        while len(finished_players) < len(self.players) - 1:

            # Determine which players are still playing and get player gameloop
            competing_players = list(filter(lambda player: player not in finished_players, self.players))
            player_loop = self.player_loop_generator(competing_players, starting_player)

            # Play a round 

            vprint(f"Next round with: {list(map(lambda player: player.name, competing_players))}", self.verbose)
            round_winner = self.round(competing_players, player_loop)
            vprint(f"Round Finished, winning player: {round_winner.name}", self.verbose)
            vprint("++++++++++++++++++++++++++++++++++++", self.verbose)

            # Check if round_winner is out of cards, if so add to finished_players
            if round_winner.is_finished():
                finished_players.append(round_winner)
                vprint(f"{round_winner.name} is finished", self.verbose)
                # The next player in rotation is now the starting player
                starting_player = next(player_loop)
            else: # round_winner is now the starting_player for the next round
                starting_player = round_winner

            for player in self.players:
                player.notify_round_end()
            # Clear the table so a new round can begin
            self.table.clear()
            
        # Get the scum 
        scum = list(filter(lambda player: player not in finished_players, self.players))[0]
        # Let the scum return his card, by putting them on the table and clearing it
        self.table.put(Move(scum.return_cards()))
        self.table.clear()
        # Add him/her to the finishing_players for the finishing order
        finished_players.append(scum)

        for i, player in enumerate(finished_players):
            # pass player ranking to the player at end of game
            player.notify_game_end(i)
        # Finish the game
        return finished_players

    def round(self, round_players, player_loop):
        '''
        Function that represents one round in a game, 
        this continues until all but one players skipped their turn.

        Parameters:
            round_players: [Player]
            player_loop: Generator -> Player

        Returns: 
            winner: Player
        '''
        skip = Skip()
        round_skips = []

        # Keep looping over players until one has won this round
        while current_player := next(player_loop):
            # If the current player has skipped this round he can't play anymore
            if current_player in round_skips:
                continue

            # If all other players skipped, this player is the winner of this round
            if len(round_skips) == len(round_players) - 1: #TODO check if player can play extra cards even when others skipped
                return current_player
            
            # The round is not finished so this player may make a move

            # Let the player make a move
            if current_player.name == "Anton":
                possible_moves = MoveGenerator().generate_possible_moves(current_player.cards, self.table.last_move())
                possible_moves.append(Skip())
                vprint(colored(str(possible_moves), "red"), self.verbose)

            move = current_player.play(self.table.last_move())
            if current_player.name == "Anton":
                vprint(colored(f"{current_player.name} plays {move}", "yellow"), self.verbose)
            else:
                vprint(f"{current_player.name} plays {move}", self.verbose)

            # Check if the player skips his turn
            if move is skip:
                # Put the player in the list of players that skipped this round
                round_skips.append(current_player)
            else:
                # Put the move on the table
                self.table.put(move)

            # Check if player is out of cards and, thus the winner of this round
            if current_player.is_finished():
                return current_player

    def finish(self, finish_order):
        '''
        Function that represents the end of a game, here President, ..., Scum are set

        Parameters:
            finish_order: [Player]
        '''

        # If the game has 2 or 3 players only President and Scum is used
        ranks = {}
        if len(self.players) < 4:
            ranks['president'] = finish_order[0]
            ranks['scum'] = finish_order[-1]
        else:
            ranks['president'] = finish_order[0]
            ranks['vice_president'] = finish_order[1]
            ranks['high_scum'] = finish_order[-2]
            ranks['scum'] = finish_order[-1]
        
        # Check if the deck is complete, this is to make sure no mistakes are made
        self.table.check_deck()
        
        return ranks


    def get_starting_player(self):
        '''
        Function that returns the player that starts the game, this is the player has the card (3 ♣)  

        Returns:
            Player
        '''
        starting_card = Card(3, "club")
        player = list(filter(lambda player: player.has(starting_card), self.players))
        return player[0]
         
    def player_loop_generator(self, players, starting_player):
        '''
        Function that returns a generator with an infinite playerloop

        Parameters:
            players: [Player]
            starting_player: Player

        Returns:
            player_loop: Generator -> Player
        '''
        current_player_index = players.index(starting_player)
        while True:
            yield players[current_player_index]
            current_player_index = (current_player_index + 1) % len(players)
