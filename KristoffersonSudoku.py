"""
I certify that the file I am submitting is all my own work.
None of it is copied from any source or any person.
Signed: Rachel Kristofferson.
Date: 7/27/2024
"""

"""
Author: Rachel Kristofferson
Date: 7/27/2024
Class: CSC115
Project: Final - Sudoku
File Name: KristoffersonSudoku.py
Description: A sudoku puzzle.


Resources:

https://www.youtube.com/watch?v=KWgYha0clzw
https://www.youtube.com/watch?v=6iF8Xb7Z3wQ
https://docs.python.org/3/library/random.html
https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
https://www.youtube.com/watch?v=z49F119uv6g
https://www.geeksforgeeks.org/backtracking-algorithm-in-python/
https://www.youtube.com/watch?v=7TAmGm3aoqA
https://www.youtube.com/watch?v=eqUwSA0xI-s



"""
import random

class Sudoku:

    def __init__(self):
        self.board = self.initialize_board() # The function returns a board
        self.generate_board()

    # Initialize the Sudoku board
    def initialize_board(self):
        """Create a 9x9 board initialized with zeros. First for loop creates a 
        row of 9 0s. The second for loop repeats that line of 0s 9 times."""
        self.board = []
        for _ in range(9):
            row = [0] * 9
            self.board.append(row)
        return self.board    
    

    def generate_board(self):
        """Generate a valid Sudoku board then remove the designated numbers based
        on difficulty chosen."""
        self.fill_board()
        self.remove_numbers()

    def fill_board(self):
        """Fill the board with numbers 1-9. This function is achieved by using the 
        backtracking algorithm, which will find one number that works and continue 
        to fill the board going off that solution, otherwise it will go back up to
        the starting value and try again."""

        def solve():
            for row in range(9):
                for col in range(9):
                    if self.board[row][col] == 0: # Find an empty cell.
                        num_list = list(range(1, 10)) # Create a list 1-9
                        random.shuffle(num_list) # Shuffle the list
                        for num in num_list:
                            if self.is_valid(num, row, col):
                                self.board[row][col] = num # Place the number
                                if solve(): # Recursively keep filling the board.
                                    return True
                                self.board[row][col] = 0 # If a solution isn't found, reset back to 0 - Backtrack.
                        return False
            return True 
        solve()

    def is_valid(self, num, row, col):

        """Check if a number can be placed in the given row and column.
        Loops through each row/column to see if num is in the row/column."""
        # Check row
        for i in range(9):
            if self.board[row][i] == num:
                return False
            
        # Check column
        for i in range(9):
            if self.board[i][col] == num:
                return False
            

        # Check 3x3 box
        """ Ex: If 4 was passed into is_valid as a parameter for row the calculation
        would be 3 * (4 // 3) = 3. Since dividing ints will take the floor of the
        quotient, will allow me to figure out what 3x3 box the row is in. Then I
        loop through the 3x3 box same as the check column/row loops.
        """
        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)

        for i in range(3):
            for j in range(3):
                if self.board[box_row + i][box_col + j] == num:
                    return False
        
        return True # Valid number

    def remove_numbers(self):
        difficulty = input("Select difficulty (easy, medium, hard): ").lower()
        if difficulty not in ["easy", "medium", "hard"]:
            print("Invalid difficulty! Defaulting to 'easy'.")
            difficulty = "easy"
        
        """Remove numbers from the board to create the puzzle based on difficulty.
        Easy will have 45 numbers, medium 35, and hard 25 numbers. It will default
        to easy if the input for difficulty isn't recognized."""
        num_to_remove = {"easy": 36, "medium": 46, "hard": 56}.get(difficulty, 36)  
        

        for _ in range(num_to_remove):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while self.board[row][col] == 0:
                row = random.randint(0, 8) 
                col = random.randint(0, 8)
            self.board[row][col] = 0



    def display_board(self):
        """Display the Sudoku board with dividers as well as row/column identifiers."""
        size = 9
        box_size = 3

        # Print column headers 1-9
        print("\n   ", end="")
        for col in range(size):
            if col % box_size == 0:
                print("| ", end="")  # Print vertical divider between 3x3 grids
            print(f"{col + 1}", end=" ")
        print()  # New line after the column headers

        for row in range(size):
            if row % box_size == 0:
                print("-" * (size * 2 + box_size * 2 + 2))  # Print horizontal divider between 3x3 grids
            
            print(f"{row + 1}  ", end="") # Adds the 1-9 row numbers.

            for col in range(size):
                if col % box_size == 0:
                    print("|", end=" ")  # Print vertical divider between 3x3 grids
                
                if 0 <= row < len(self.board) and 0 <= col < len(self.board[row]):
                    num = self.board[row][col]  # Get the value if indices are valid
                else:
                    num = None 
            
                if num != 0:
                    print(num, end=" ")  # Print the number
                else:
                    print('.', end=" ")  # Internally the board is made up of zeroes. Externally it will be a period.
        
            
            print()  # New line at the end of each row

    def is_solved(self):
        """Check if the Sudoku is solved."""
        for row in self.board:
            if 0 in row:
                return False
        return True
    
    def is_solvable(self):
        """Check if the board is solvable without modifying the board by using
        a copy. Reusing the code from fill_board to check if the board will be
        solvable if a seemingly correct value is placed.
        """
        board_copy = [row[:] for row in self.board]
        
        def solve():
            for row in range(9):
                for col in range(9):
                    if board_copy[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid(num, row, col):
                                board_copy[row][col] = num
                                if solve():
                                    return True
                                board_copy[row][col] = 0
                        return False
            return True
        
        return solve()

    def play_sudoku(self):
 
        print("\tWelcome to Sudoku!\n")
        self.display_board()

        while not self.is_solved():
            try:
                """ Read and validate row/col/num input. Invalid input will be 
                handled immediatly and you'll begin again at entering in row. """
                
                row_input = input("Enter the row (1-9): ")
                row = int(row_input) - 1
                if not (0 <= row < 9): # Not including 9 because index is 0-8
                    print("Row must be between 1 and 9.")
                    continue

                col_input = input("Enter the column (1-9): ")
                col = int(col_input) - 1
                if not (0 <= col < 9):
                    print("Column must be between 1 and 9.")
                    continue

                num_input = input("Enter the number (1-9): ")
                num = int(num_input)
                if not (1 <= num <= 9):
                    print("Number must be between 1 and 9.")
                    continue
                    

                if self.is_valid (num, row, col):
                    self.board[row][col] = num   
                    if not self.is_solvable():
                        print("This move makes the puzzle unsolvable. You've Lost.")
                        return # Game ends
                    self.display_board() # Displays the new valid value on board.
                else:
                    print("Invalid move! Try again.")
            except ValueError:
                print("Invalid input! Please enter numbers only.")
            except IndexError:
                print("Row and column must be between 1 and 9.")
        
        print("Congratulations! You've solved the Sudoku puzzle!")


if __name__ == "__main__":
    play = Sudoku()
    play.play_sudoku()