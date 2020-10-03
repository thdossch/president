from game import Game
from basicPlayer  import BasicPlayer

class President:
    def __init__(self, players, ranks=None):
        '''
        Class that represents a session of President, 

        A session exists out of multiple games, every game players compete to
        become the President.
        The first game every players have equal ranks but after one game they
        can become: 

        President: Receives the 2 best cards of the Scum and returns his lowest cards.
        Vice-President: Receives the best card of the High-Scum and returns his lowest cards
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
        game = Game(self.players, {})
        ranks = game.start()
        self.ranks = ranks

        if len(self.players) < 4:
            result = f"""
            Game is finished: 
                President: {ranks['president'].name}
                Scum: {ranks['scum'].name}
                """
            print(result)
        else:
            result = f"""
            Game is finished: 
                President: {ranks['president'].name}
                Vice-President: {ranks['vice'].name}
                High-Scum: {ranks['high_scum'].name}
                Scum: {ranks['scum'].name}
                """
            print(result)
        
if __name__ == '__main__':
    players = [BasicPlayer("Player1"), BasicPlayer("Player2")]
    players.append(BasicPlayer("Player3"))
    players.append(BasicPlayer("Player4"))
    players.append(BasicPlayer("Player5"))
   
    session = President(players)
    session.play()
