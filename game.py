# Steps
# DONE 1. set up the board, using a list of lists. Create a temp board
# DONE 2. create functions that will merge left, right, up, and down. Will create
#  functions to reverse and transpose the list of lists to do this
# DONE 3. set the start of the game, creating an empty game board filled with 2 values
#  of the number 2
# DONE 4. set up rounds of the game, where the user will have the option to merge in
#  any one of the four directions, and after they move, then new board will display
# DONE 5. set up adding a new value time they make a successful move
# DONE 6. set up functions testing if the user has lost or won
import copy
import random

import os as _os

boardSize = 4


# display function

def display(board):
    # clear screen each turn then print the whole board once
    _os.system('cls' if _os.name == 'nt' else 'clear')
    print("+------+------+------+------+\n"
          f"|{cell(board[0][0])}|{cell(board[0][1])}|{cell(board[0][2])}|{cell(board[0][3])}|\n"
          "+------+------+------+------+\n"
          f"|{cell(board[1][0])}|{cell(board[1][1])}|{cell(board[1][2])}|{cell(board[1][3])}|\n"
          "+------+------+------+------+\n"
          f"|{cell(board[2][0])}|{cell(board[2][1])}|{cell(board[2][2])}|{cell(board[2][3])}|\n"
          "+------+------+------+------+\n"
          f"|{cell(board[3][0])}|{cell(board[3][1])}|{cell(board[3][2])}|{cell(board[3][3])}|\n"
          "+------+------+------+------+")

def cell(v):
    s = "" if v == 0 else str(v)
    return f" {s:^4} "  # centered in 6 chars
    # set up the number of spaces needed to the length of the largest value
    # numSpaces = len(str(largest))

    # for row in board:
    #     currentRow = "|"
    #     for element in row:
    #         # if element is 0, add a space to make it blank
    #         if element == 0:
    #             currentRow += (" " * numSpaces) + "|"
    #         else:

    #             currentRow += (" " * (numSpaces - len(str(element)))) + str(element) + "|"

    #     print(currentRow)
    # print()  # this is to add an extra line after the board has been created


# 2. Functions to merge left, right, up, down
def mergeOneRowLeft(row):
    # move every element in the row as far left as possible
    # the in range(start, stop, step) so we start at the very end of the row, stop at the
    # first index, and going back each time
    for j in range(boardSize-1):
        for i in range(boardSize-1, 0, -1):  # starts at the end of the list, and traverses down, stop at 0 bc we will check [i-1] which should touch 0
            # test if there is an empty space, move over if
            if row[i-1] == 0:
                row[i-1] = row[i]
                row[i] = 0
    # now check for merging
    for i in range(boardSize-1):  # NOTE: we use boardSize - 1 when we are looking for values like [i+1] to prevent it from going out of bounds
        # check if the current value is equal to the one on its right
        if row[i] == row[i + 1]:
            row[i] *= 2
            row[i+1] = 0
    # now merge again to move everything left
    for i in range(boardSize-1, 0, -1):
        if row[i-1] == 0:
            # move the number to the empty spot
            row[i-1] = row[i]
            row[i] = 0
    return row


# this function will merge the whole board to the left
def merge_left(currentBoard):
    for i in range(boardSize):
        currentBoard[i] = mergeOneRowLeft(currentBoard[i])

    return currentBoard


# now instead of writing all the functions again for each move (right, down, up) what we will do for RIGHT is
# reverse the order of the list (this will flip the numbers around), merge it left!, and then reverse it again
# this will be the same as if merging right (think abt it)
def reverse(row):
    newRow = []
    for i in range(boardSize-1, -1, -1):
        newRow.append(row[i])
    return newRow


# this function will merge whole board right
def merge_right(currentBoard):
    for i in range(boardSize):
        currentBoard[i] = reverse(currentBoard[i])
        currentBoard[i] = mergeOneRowLeft(currentBoard[i])
        currentBoard[i] = reverse(currentBoard[i])
    return currentBoard


# this is function transposes the whole board - item first row sec col will go second row first col, like flipping it
# sideways
def transpose(currentBoard):
    for i in range(boardSize):
        for j in range(i, boardSize):
            if not j == i:
                temp = currentBoard[i][j]
                currentBoard[i][j] = currentBoard[j][i]
                currentBoard[j][i] = temp
    return currentBoard


# this function will merge the whole board up
def merge_up(currentBoard):
    # transpose the whole board, merge it all left, and then transpose it back
    currentBoard = transpose(currentBoard)
    currentBoard = merge_left(currentBoard)
    currentBoard = transpose(currentBoard)
    return currentBoard


# this function will merge it down
def merge_down(currentBoard):
    # transpose it (flip it to the side and merge right to simulate merging down), merge right, then transpose it back
    currentBoard = transpose(currentBoard)
    currentBoard = merge_right(currentBoard)
    currentBoard = transpose(currentBoard)
    return currentBoard


# this function picks a new value for the board
def pickNewValue():
    if random.randint(1, 8) == 1:  # every 8 moves, we will add in a 4 to the game
        return 4
    return 2


# this function will add a value to the board in one of the empty spaces on the board
def addNewValue(board):
    rowNum = random.randint(0, boardSize-1)
    colNum = random.randint(0, boardSize-1)

    # keep picking a spot until we find an empty place
    while not board[rowNum][colNum] == 0:  # basically (while false)
        rowNum = random.randint(0, boardSize - 1)
        colNum = random.randint(0, boardSize - 1)

    board[rowNum][colNum] = pickNewValue()


# this function is to test if the person has won
def won(currentBoard):
    for row in currentBoard:
        if 2048 in row:
            return True
    return False


# this function is to test if the user has lost :/ meaning they cant move the board anymore
def noMoves(currentBoard):
    # create two temporary boards
    tempBoard1 = copy.deepcopy(currentBoard)
    tempBoard2 = copy.deepcopy(currentBoard)

    # now we will merge tempBoard1 in every direction and checking each time if it is equal to tempBoard2
    # if they are still the same, then that means there is no more moves they are able to make and user LOSt
    tempBoard1 = merge_down(tempBoard1)
    if tempBoard1 == tempBoard2:  # meaning merging down did nothing, try merging up
        tempBoard1 = merge_up(tempBoard1)
        if tempBoard1 == tempBoard2:  # merge up did not work, merge right
            tempBoard1 = merge_right(tempBoard1)
            if tempBoard1 == tempBoard2:  # merge right did not work, go left
                tempBoard1 = merge_left(tempBoard1)
                if tempBoard1 == tempBoard2:  # the user can not move anymore at all, they lose
                    return True
    return False


def main():

    # create a blank board
    board = []
    for i in range(boardSize):
        row = []
        for j in range(boardSize):
            row.append(0)
        board.append(row)

    # now we need to fill in 2 spots with the random values
    numNeeded = 2
    while numNeeded > 0:
        rowNum = random.randint(0, boardSize-1)
        colNum = random.randint(0, boardSize-1)

        if board[rowNum][colNum] == 0:
            board[rowNum][colNum] = pickNewValue()
            numNeeded -= 1

    # printing the welcome to the game
    print("Welcome to 2048. Your goal is to combine values to get the number 2048, by merging numbers of equal value."
          "\nYou need to type: 'A' for merge down, 'D' for merge right, 'W' for merge up, 'S' for merge down.\nHere is "
          "the starting board")
    display(board)

    gameOver = False
    while not gameOver:
        move = input("Enter which way you want to merge: WASD or (Q) to quit...: ")

        # will create a deep copy of the board in case of anything
        tempBoard = copy.deepcopy(board)
        valid_input = True

        if move.lower() == "d":  # merge right
            board = merge_right(board)
        elif move.lower() == "w":  # move up
            board = merge_up(board)
        elif move.lower() == "s":  # move down
            board = merge_down(board)
        elif move.lower() == "a":  # merge left
            board = merge_left(board)
        elif move.lower() == "q":  # quit the program... BYE
            break
        else:
            valid_input = False  # the user put some other shit besides what was asked

        # if the input was not valid, they need to input another value again, pass everything below so the loop
        # starts again
        if not valid_input:
            print("Input not valid, please enter WASD to move the board or (Q) to quit...")
        else:
            # if the way they moved was unsuccessful, make the user choose another way to move
            if board == tempBoard:
                print("Try a different direction. The one you previously chose did not move the board")
            else:
                # going to check if the user won before a new value is added to the board (after their move WASD)
                if won(board):
                    display(board)
                    print("You won!!! SLAY")
                    gameOver = True
                else:
                    # add a new value to board
                    addNewValue(board)

                    display(board)

                    # find out if the user has lost or nah
                    if noMoves(board):
                        print("There are no more moves you can make...You LOST!")
                        gameOver = True


if __name__ == "__main__":
    main()
