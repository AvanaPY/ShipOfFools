"""
    Ship of Fools module "game.py" by Emil Karlström, DVAMI19

    2020 - 04 - 16
"""
from diecup import DieCup
from playroom import Player
import re

class ShipOfFoolsGame():
    WINNING_SCORE = 21
    def __init__(self):
        self._name = 'Ship of Fools'
        self._cup = DieCup()

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self._name

    @property
    def cup(self):
        return self._cup

    def play_round(self):
        """
            Plays a single round of Ship of Fools for a player and returns a score.
        """
        self._cup.release_all()

        max_throws = 3
        throws = max_throws
        while throws > 0 and not self.all_dice_banked():
            to_bank = self._roll_and_get_input(max_throws - throws + 1)
            self._bank(to_bank)

            throws -= 1

        self.cup.bank_all()

        if all(self._flags()):
            full_ship_score = 6 + 5 + 4  # The "off score" if you have a ship, captain, and mate.
            score = self.cup.sum() - full_ship_score
        else:
            score = 0
        return score

    def _roll_and_get_input(self, roll_counter):
        """
        Rolls all the dice in the game's DieCup, prints the rolls, and then grabs the user's input and parses it into a list of indexes.

        Returns: List of indexes of dice to bank.
        """
        self.cup.sort_by_banked()
        self.cup.roll()
        self.cup.print_rolls(roll_counter)
        success = False
        to_bank = None
        while not success:
            try:
                print(f'Which indices to bank? | ', end='')

                # Use regular expressions to find all the single digits in the input
                to_bank = re.findall(r'\d ?', input())

                # Map the function a -> int(a) over the regular expression max
                # Then turn it into a list
                to_bank = list(map(lambda a: int(a), to_bank))

                # Sort it by value in the cup from highest to lowest
                # This is so we bank 6s before 5s, 5s before 4s and so on.
                # Keep in mind the list is still in index form.

                to_bank = sorted(to_bank, key=(lambda a : self.cup.value(a)), reverse=True)

                success = True
            except IndexError:
                print(f'Index out of range, please try again.')
        
        return to_bank

    def _bank(self, to_bank: list):
        """
            Banks all the die in the index-based to_bank list if possible.
        """
        # We have to attempt twice

        # Assume a list of indexes such that the mapped die value becomes like such [6, 6, 5, 4]
        # If we don't attempt twice, the algorithm will fail on the second 6 because we will already have a ship
        # But obviously this is a valid list of dice to bank because we have a Ship, Captain and Mate.
        # Looping over the list twice solves this issue that there can be two 6s for instance.
        for attempt in range(2):

            # Copy the list so we can remove from the original list, not the most efficient way 
            # of dealing with the problem but will work for now as the lists are very small
            for index in to_bank[:]:
                try:
                    self.try_bank(index)
                    to_bank.remove(index)
                    
                except AssertionError as e: 
                    # If an AssertionError occurs it means it came from game.try_bank
                    # This also means that our attempt to bank the index was a failure
                    # Assuming we are on our second attempt, since the to_bank list is all ordered by in-cup value, all future
                    # attempts to bank will fail hence we can simply return and skipp them entirely.

                    # If we are on our first attempt, there is a chance we have not tried all dice yet
                    # and skipping would be a mistake since we could be missing crucial dice that are placed
                    # later in the list.

                    if attempt == 1:
                        print(f'Could not bank {self.cup.value(index)} due to "{e}"')
                        return
                except IndexError:
                    # If there is an index error, assume it's a mistake by the user and do nothing
                    pass
                except Exception as e:
                    print(f'A very bad error occured, this should never happen.')
                    print(str(e))

    def try_bank(self, index):
        """
        Attempts to bank a die at index.

        Raises
            AssertionError with approporiate error message.
        """

        # Flags :   Index 0 - Ship
        #           Index 1 - Captain
        #           Index 2 - Mate

        flags = self._flags()
        val = self.cup.value(index)
        
        # Check if value is 6 and we do NOT have a ship
        if val == 6 and not flags[0]:
            self.cup.bank(index)
            return

        # If there is no ship, raise an AssertionError
        # Then check if value is 5 and we do NOT have a captain
        assert flags[0], 'There is no ship'
        if val == 5 and not flags[1]:
            self.cup.bank(index)
            return

        # If there is no captain, raise an AssertionError
        # Then check if value is 4 and we do NOT have a mate
        assert flags[1], 'There is no captain'
        if val == 4 and not flags[2]:
            self.cup.bank(index)
            return
            
        # If there is no mate, raise an AssertionError
        assert flags[2], 'There is no mate'

        # If we have a Ship, Captain, and Mate
        # Then we can just bank the index
        self.cup.bank(index)

    def all_dice_banked(self):
        """
            Wrapper for cup.all_dice_banked.
            Returns True if all dice are banked, else False.
        """
        return self.cup.all_dice_banked()
    
    def _flags(self):
        """
            Returns a list of three (3) boolean flags where index
                0 - Represents if there is a ship
                1 - Represents if there is a captain
                2 - Represents if there is a mate
        """
        flags = {6:False, 5:False, 4:False}
        for die in self.cup:
            if die.value in (6, 5, 4) and die.banked:
                flags[die.value] = True
        return [flags[i] for i in flags]