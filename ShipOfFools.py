"""
    Ship of Fools by Emil Karlström, DVAMI19

    2020 - 04 - 16
"""

from game import ShipOfFoolsGame
from playroom import Room


if __name__ == "__main__":
    room = Room()
    room.game = ShipOfFoolsGame()

    room.add_player('Dennis')
    room.add_player('Emil')

    play_round = 1
    while not room.game_finished():
        print(f'ROUND {play_round}')
        room.play_round()
        room.print_leaderboard()

        play_round += 1

    room.print_winner()