"""
    Ship of Fools module "playroom.py" by Emil Karlström, DVAMI19

    2020 - 04 - 16
"""

import re
class Player:
    def __init__(self, name):
        self._name = name
        self._score = 0

    def __str__(self):
        return f'Player {self.name.ljust(8)} with score {self.score:2}'

    @property
    def name(self):
        return self._name

    @property
    def score(self):
        return self._score
    @score.setter
    def score(self, value):
        self._score = value

    def reset_score(self):
        """
            Resets the score to 0.
        """
        self._score = 0

class Room:
    def __init__(self):
        self._players = []
        self._game = None

    def __str__(self):
        return f'Room of size {self.size}\nOngoing game: {self.game}\n\n' + '\n'.join([str(p) for p in self._players])

    @property
    def size(self):
        """
            Returns the amount of players in the room.
        """
        return len(self._players)

    @property
    def game(self):
        """
            Returns the game itself.
        """
        return self._game
    @game.setter
    def game(self, value):
        """
            Sets the game equal to an instance of ShipOfFoolsGame.
        """
        self._game = value

    def leader_board(self):
        """
            Returns a sorted list of all players in the room.
        """
        board = sorted(self._players, key=(lambda a : a.score), reverse=True)
        return board

    def add_player(self, player_name : str):
        """
            Creates a new player with name player_name and adds it to the room
        """
        player = Player(player_name)
        self._players.append(player)

    def reset_scores(self):
        """
        Resets all score.
        """
        for player in self._players:
            player.reset_score()

    def game_finished(self):
        """
            Returns if the game is finished or not.
        """
        leader_board = self.leader_board()
        return leader_board[0].score >= self.game.WINNING_SCORE

    def play_round(self):
        """
            Loops through all players and plays one round for each of them.
        """

        for player in self._players:
            
            print('-' * 6 + f' PLAYER {player.name} ' + '-' * 6)

            self._game.pre_round()
            self._game.play_round(player)

            print(f'{player.name} finished with a score of {player.score}')

    def print_leaderboard(self):
        """
            Prints the leaderboard in a nicely fashion.
        """
        width = 4 + 10 + 3 + 3  # The width of the leaderboard in the terminal. It's the sum of the "sections" in the print function inside the upcoming for loop.

        print('\nLEADERBOARD\n' + '—' * width)
        
        leader_board = self.leader_board()
        for index, player in enumerate(leader_board):
            print(f'#{index+1:2d} {player.name.ljust(10)} - {player.score:3d}')
            
        print('—' * width, end='\n\n')
    
    def print_winner(self):
        winner = self.leader_board()[0]

        output = f'{winner.name} has won the game with {winner.score} points'
        length = len(output)
        print(f'\n{"—"*length}\n{output}\n{"—"*length}\n')