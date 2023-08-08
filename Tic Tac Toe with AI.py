import random
""" define constants here, EMPTY to define empty cells, input list to search through X and O """
EMPTY_CELL = ' '
INPUT_LIST = ('X','O')
input_list2 = (0,1,2)
global user1
global player_win_counter
global comp_win_counter
global draw_counter
player_win_counter = 0
comp_win_counter = 0
draw_counter = 0


def display_board(board):
    """Prints the current state of the board."""
    if board == sample_board:
        print('-------------------')    
    else:
        print('-------------')
    for row in board:
        print('|', end=' ')
        for cell in row:
            print(cell, end=' | ')
        if board == sample_board:
            print('\n------------------')
        else:
            print('\n-------------')


def get_empty_cells_list(board):
    """Returns a list of empty cells on the board."""
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY_CELL:
                empty_cells.append((i, j))
    return empty_cells


def who_is_winner(board, player):
    """Checks if the specified player has won."""
    # Check the rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True

    # Check the columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == player:
            return True

    # Check the diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False

def check_if_full(board):
    """Checks if the board is full."""
    for row in board:
        if EMPTY_CELL in row:
            return False
    return True


def check_board_stat(board):
    """Checks what is the current status of the board
       Parameters, pass out board and the player."""
    if who_is_winner(board, COMP_PLAYER):
        return 1  # AI wins
    elif who_is_winner(board, HUMAN_PLAYER):
        return -1  # Human wins
    else:
        return 0  # Draw


def minimax(board, depth, maximizing_player):
    """Minimax algorithm with alpha-beta pruning
       First check what is the current status of the board."""
    if who_is_winner(board, COMP_PLAYER):
        return 1
    elif who_is_winner(board, HUMAN_PLAYER):
        return -1
    elif check_if_full(board):
        return 0
    """ First case is to maximize player, in this case since we are designing the AI, the AI will be the player
       set max_util to a random negative infinity value, assign our COMP_PLAYER to a random empty cell
       run the minimax algorithm with a specified depth (start at the lowest) and return the value.
       find the maximum between the max_util assigned earlier and the current util value and return the maximum util (best utility) """
    if maximizing_player:
        max_util = float('-inf')
        for i, j in get_empty_cells_list(board):
            board[i][j] = COMP_PLAYER
            util = minimax(board, depth + 1, False)  #set maximizing_player to false because we are designing the code for the AI to win.
            board[i][j] = EMPTY_CELL
            max_util = max(max_util, util)
        return max_util
    else:
        min_util = float('inf')
        for i, j in get_empty_cells_list(board):
            board[i][j] = HUMAN_PLAYER
            util = minimax(board, depth + 1, True)
            board[i][j] = EMPTY_CELL
            min_util = min(min_util, util)
        return min_util


def get_best_move(board, counter):
    """Returns the best move for the AI player using the minimax algorithm."""

    """" run a counter to increase difficulty according to turn
    easy is just random placement of symbol on the board by AI
    medium is a probability of picking a random symbol or running minimax with alpha beta pruning to maximize our AI utility
    hard is using minimax with alphabeta pruning to get the best utility """

    """" aside from running mini max and getting the maximum util value, we compare it with the predefined best util
    if our util is better than the best_util, replace best_util with current util value. Also here we pull our assigned i, j empty cell
    and assign it to best move. Repeat this until we get the best possible util (highest utility) and pull the corresponding i, j move """

    if counter == 1:
        # Random move for easy difficulty
        return random.choice(get_empty_cells_list(board))
    elif counter == 2:
         #Random move or best move for medium difficulty
        if random.randint(0, 100) < 60:
            return random.choice(get_empty_cells_list(board))
        else:
            best_util = float('-inf')
            best_move = None
            for i, j in get_empty_cells_list(board):
                board[i][j] = COMP_PLAYER
                util = minimax(board, 0, False)
                board[i][j] = EMPTY_CELL

                if util > best_util:
                    best_util = util
                    best_move = (i, j)

            return best_move
    else:
        #best moves for hardest difficulty 
        best_util = float('-inf')
        best_move = None
        for i, j in get_empty_cells_list(board):
            board[i][j] = COMP_PLAYER
            util = minimax(board, 0, False)
            board[i][j] = EMPTY_CELL

            if util > best_util:
                best_util = util
                best_move = (i, j)

        return best_move

def get_player_ai_mark():
    """ function to let the user pick a mark and the AI automatically choses the opposite one, we set a flag so that this occurs only once per game
    error handling for case sensitivity as well as if player types in wrong symbol by comparing with input list """

    flag = True
    while flag:
        user1_in = input("%s, please choose which symbol you would like to play with X or O " %user1)
        HUMAN_PLAYER = user1_in.upper()
        if HUMAN_PLAYER not in INPUT_LIST:
          print("Please select either X or O to proceed")
        else:
          if HUMAN_PLAYER == 'X':
            COMP_PLAYER = 'O'
          elif HUMAN_PLAYER == 'O':
            COMP_PLAYER = 'X'
          flag = False

    return HUMAN_PLAYER, COMP_PLAYER





def play_game():
    """ main function to play the game, a loop to repeat the game with error handling in place, counter to increment difficulty """
    play_again = "Y"
    counter = 0
    win_counter_reset = 0
    tie_counter_reset = 0
    global player_win_counter
    global comp_win_counter
    global draw_counter
   #flag = True
    while play_again == "Y":


        counter += 1

        if win_counter_reset >= 2:
          player_in = input("%s, it looks like the AI is beating you quite easily, would you like to tone down the difficulty? Y/N " %user1)
          reset_diff = player_in.upper()
          if reset_diff == "Y":
            counter = 1

            win_counter_reset = 0

        #print(counter)  #debug


        if tie_counter_reset >= 2:
          player_in2 = input("%s, it looks like you are having a tough time with playing against AI, would you like to tone down the difficulty? Y/N " %user1)
          reset_diff = player_in2.upper()
          if reset_diff == "Y":
            counter = 1
            tie_counter_reset = 0

        """Plays the Tic Tac Toe game."""
        
        
        
        board = [[EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
                 [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
                 [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL]]
        display_board(board)

        if counter == 1:
            print("This should be quite easy")
        elif counter == 2:
            print("I'm getting smarter!")
        else:
            print("You can't win anymore")


        global HUMAN_PLAYER
        global COMP_PLAYER
        HUMAN_PLAYER, COMP_PLAYER = get_player_ai_mark()



        """ run while loop to check if board is not full and the player has not won to start game
        human and ai player turns one by one with checking for winner and draw in between"""

        while not check_if_full(board) and not who_is_winner(board, HUMAN_PLAYER):

            # Player's turn
            row = int(input("Select the row (0-2): "))
            if row not in input_list2:
                print("Please select from 0 to 2")
                continue
            
            col = int(input("Select the column (0-2): "))
            if col not in input_list2:
                print("Please select from 0 to 2")
                continue


            if board[row][col] != EMPTY_CELL:
                print("Invalid move. Please choose again:")
                continue

           # mark player's cell and update board
            board[row][col] = HUMAN_PLAYER
            display_board(board)

            if who_is_winner(board, HUMAN_PLAYER):
                print("Congrats %s, you win!" %user1)
                player_win_counter += 1
                break

            if check_if_full(board):
                print("No winner, no loser. It is a draw!")
                tie_counter_reset += 1
                draw_counter += 1
                break

            # Computer's turn
            print("AI's turn...")
            ai_row, ai_col = get_best_move(board, counter)
            board[ai_row][ai_col] = COMP_PLAYER
            display_board(board)

            if who_is_winner(board, COMP_PLAYER):
                print("The computer has bested you!")
                win_counter_reset += 1
                comp_win_counter += 1
                break

            if check_if_full(board):
                print("No winner, no loser. It is a draw!")
                break

        next_round = input("Do you wish to play again? Select Y to confirm replay \n")
        play_again = next_round.upper()
        
    print("Hi " +str(user1) + ", you have won " + str(player_win_counter) + " times, Computer has won " +str(comp_win_counter) + " times and you have tied with computer " + str(draw_counter) + " times!")
    print("Thanks for playing, have a nice day!")

# Start the game
""" get the user name for some added humanization of the game """

user1 = input("Hello, Welcome to Tic Tac Toe against AI! What is your name? ")          
global sample_board
sample_board = [[('0,0'), ('0,1'), ('0,2')],
                [('1,0'), ('1,1'), ('1,2')],
                [('2,0'), ('2,1'), ('2,2')]]
display_board(sample_board)

play_game()
