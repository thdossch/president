from game import Game
from basicPlayer  import BasicPlayer
from randomPlayer  import RandomPlayer
from ai  import AIPlayer
from util import vprint

class President:
    def __init__(self, players, ranks=None):
        '''
        Class that represents a session of President, 

        A session exists out of multiple games, every game players compete to
        become the President.
        The first game all players have equal ranks but after one game they
        can become: 

        President: Receives the 2 best cards of the Scum and returns his lowest cards.
        Vice-President: Receives the best card of the High-Scum and returns his lowest card.
        Person: No extra rules here
        High-Scum: Receives the worst card of the Vice-President and returns his best cards
        Scum: Receives the 2 worst card of the President and returns his 2 best cards
        '''
        self.players = players 
        self.ranks = ranks

    def play(self):
        '''
        Function that starts the session, keeps looping until interrupted
        '''
        while True:
            game = Game(self.players, self.ranks)
            self.ranks = game.start()

            if len(self.players) < 4:
                result = f"""
                Game is finished: 
                    President: {self.ranks['president'].name}
                    Scum: {self.ranks['scum'].name}
                    """
                print(result)
            else:
                result = f"""
                Game is finished: 
                    President: {self.ranks['president'].name}
                    Vice-President: {self.ranks['vice_president'].name}
                    High-Scum: {self.ranks['high_scum'].name}
                    Scum: {self.ranks['scum'].name}
                    """
                print(result)

            if not (ans := input('Play again? (y/n): ')) or ans == 'n':
                break 


    def simulate(self, games, verbose = True):
        '''
        Function that starts the session, then plays given amount of games and prints history of players' roles.
        It returns this history so that these statistics can possibly be used somewhere else.
        '''

        history = dict()
        for player in self.players:
            history[player] = {'p': 0, 'vp': 0, 'hs': 0, 's': 0 }

        win_percentage = []
        last_hun = []
        for i in range(games):
            if i % 1000 == 0 and i != 0:
                print(f"After {i} iterations:")
                wins = dict()
                for player in self.players:
                    wins[player.name] = 0
                for win_for_player in last_hun:
                    wins[win_for_player] = wins[win_for_player] + 1
                print()
                print("For the last 1000 games:")
                for player in wins:
                    print(f"\t{player} won {wins[player]} times")
                win_percentage.append(round(wins['Player1']/1000, 2))

            game = Game(self.players, self.ranks, verbose)
            self.ranks = game.start()

            if len(self.players) < 4:
                history[self.ranks['president']]['p'] += 1
                history[self.ranks['scum']]['s'] += 1

                result = f"""
                Game is finished: 
                    President: {self.ranks['president'].name}
                    Scum: {self.ranks['scum'].name}
                    """
                vprint(result, verbose)

            else:
                history[self.ranks['president']]['p'] += 1
                history[self.ranks['vice_president']]['vp'] += 1
                history[self.ranks['high_scum']]['hs'] += 1
                history[self.ranks['scum']]['s'] += 1

                result = f"""
                Game is finished: 
                    President: {self.ranks['president'].name}
                    Vice-President: {self.ranks['vice_president'].name}
                    High-Scum: {self.ranks['high_scum'].name}
                    Scum: {self.ranks['scum'].name}
                    """
                vprint(result, verbose)

            if len(last_hun) < 1000:
                last_hun.append(self.ranks['president'].name)
            else:
                last_hun.pop(0)
                last_hun.append(self.ranks['president'].name)

        print("\n++++++++++++++++++++++++++++++++++++")
        print("Simulation finished")
        print("++++++++++++++++++++++++++++++++++++")
        wins = dict()
        for player in self.players:
            wins[player.name] = 0
        for win_for_player in last_hun:
            wins[win_for_player] = wins[win_for_player] + 1
        print()
        print("For the last 1000 games:")
        for player in wins:
            print(f"{player} won {wins[player]} times")
        win_percentage.append(round(wins['Player1']/1000, 2))
        
        for perc in win_percentage:
            print(f"{perc}% -> ", end='')
        print()

        for player in self.players:
            if len(self.players) < 4:
                result = f"""
                Player {player.name}
                    President: {history[player]['p']} times
                    Scum: {history[player]['s']} times
                """
                print(result)
            else:
                    result = f"""
                    Player {player.name}
                        President: {history[player]['p']} times
                        Vice-President: {history[player]['vp']} times
                        High-Scum: {history[player]['hs']} times
                        Scum: {history[player]['s']} times
                        """
                    print(result)

        return history

        
if __name__ == '__main__':
    players = [AIPlayer("Player1"), RandomPlayer("Player2")]
    #players.append(BasicPlayer("Player3"))
    #players.append(BasicPlayer("Player4"))
    #players.append(BasicPlayer("Player5"))
   
    session = President(players)
    #session.play()
    session.simulate(10000, False)
    ai = players[0]
    ai.print_data()
