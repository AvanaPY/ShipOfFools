"""
    Ship of Fools module "diecup.py" by Emil Karlström, DVAMI19

    2020 - 04 - 16
"""

from random import randint

class Die:
    def __init__(self, min_val=1, max_val=6):
        self._value = 0
        self._min_val = min_val
        self._max_val = max_val

        self._banked = False

    def __str__(self):
        return f'({"--" if self.banked else "  "}: {str(self.value)})'

    @property
    def value(self):
        return self._value

    @property
    def banked(self):
        return self._banked
    @banked.setter
    def banked(self, value):
        if isinstance(value, bool):
            self._banked = value
        else:
            raise ValueError('banked cannot be set to a non-bool value.')

    def roll(self):
        """
        Rolls the die.
        """
        self._value = randint(self._min_val, self._max_val)
        return self._value

class DieCup:
    def __init__(self, size=5):
        self._size = size
        self._dice = [Die() for _ in range(size)]

    def __str__(self):
        return f'--------------\nDieCup of size {self._size}:\n\n' + ',\n'.join([str(die) for die in self._dice])
    
    def __iter__(self):
        for die in self._dice:
            yield die

    def print_rolls(self, roll_counter):
        """
        Prints out the rolls in the terminal in a nicely fashion.
        """
        print('—'*(12 + 3 * self._size) + f' Roll number {roll_counter}')
        print('Banked |  ' + ' '.join([str(die.banked)[0].ljust(3) for die in self._dice]))
        print('Value  |  ' + ' '.join([str(die.value).ljust(3) for die in self._dice]))
        print('       |  ' + ' '.join(['|'.ljust(3) for _ in range(self._size)]))
        print('Index  |  ' + ' '.join([str(i).ljust(3) for i in range(self._size)]))
        print('—'*(12 + 3 * self._size))

    def sum(self):
        """
            Return the sum of all dice.
        """
        return sum([die.value for die in self._dice])

    def roll(self):
        """
        Rolls all the dice that are not banked.
        """
        for die in self._dice:
            if not die.banked:
                die.roll()

    def sort_by_banked(self):
        """
        Sorts the dice so the banked ones are to the far left.
        """
        self._dice.sort(key=lambda a : a.banked, reverse=True)

    def bank(self, index):
        """
        Banks the die at index.
        """
        self._dice[index].banked = True

    def bank_all(self):
        """
        Banks all the dice.
        """
        for die in self._dice:
            die.banked = True

    def is_banked(self, index):
        """
        Returns if the die at index is banked or not.
        """
        return self._dice[index].banked

    def release(self, index):
        """
        Releases the die at index.
        """
        self._dice[index].banked = False

    def release_all(self):
        """
        Releases all the dice.
        """
        for die in self._dice:
            die.banked = False

    def value(self, index):
        """
        Returns the value of the die at index.
        """
        return self._dice[index].value

    def all_dice_banked(self):
        """
        Returns if all dice are banked or not.
        """
        for die in self._dice:
            if not die.banked:
                return False
        return True