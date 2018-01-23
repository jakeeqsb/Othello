'''
othello.py
This module contains Exceptions, variables, and a class, Othello for the game othello.
This provides only the logic of othello based on FULL rule and the state of the game.
In other words, this does not provide any interfaces or methods about
taking input and giving output.
The Exceptions are for the cases when the users make invalid or
inappropriate moves or decisions in playing the game such that that
user's move intervene the game process.
The exception cases are:
1. when users' move is :
    1) approaching invalid position to place a disc
    2) causing another's valid position lost
    3) causing the game is over
2. when user fails to initialize the game by violating the rule of this game

The variables are to represent the minimum and maximum values for row and column
the symbols, (characters), that are allowed to be used to indicate empty space,
black color, and white color dics

The class deals with the state of the game and the logic of the
game. This only cares how to process the input movement from user
according to the game rule and updating the state of game according to
the user's movement
'''

MODE = 'FULL'
MIN = 4 # The minimum number of row or col could be
MAX = 16 # The maximum number of row or col could be
NONE = '.'
BLACK = 'B'
WHITE = 'W'
SYMBOLS = [NONE, BLACK, WHITE]

'''
This list elements indicate eight directions
of a coordinate for the game board
(0,-1) : West,
(-1,-1) : NorthWest
(-1, 0) : North
(-1, 1) : NorthEast
(0, 1) : East
(1,1) : SouthEast
(1,0) : South
(1,-1): SouthWest
'''
EIGHT_DIRECTIONS =[(0,-1),
                   (-1,-1),
                   (-1, 0),
                   (-1, 1),
                   (0, 1),
                   (1,1),
                   (1,0),
                   (1,-1)]
###############################
# Exceptions
###############################
class InvalidMoveError(Exception):
    '''
    This exception happens when the play in current turn
    tries to access invalid position in the board during the
    game
    '''
    pass

class NoAnothersMove(Exception):
    '''
    This exception raise when the opposite player does not
    have valid positions to place the disc by the current
    player's place of disc
    '''
    pass

class GameOverException(Exception):
    '''
    This exception raise when the game is over,
    a player in the game wins at the game or the two
    players are in the draw case

    '''
    pass

class InvalidRowColInput(Exception):
    """
    This exception raise when the users input invalid row and col values
    that are greater than 16 or less than 4 when initializing
    """
    pass

class RowColInputNotEven(Exception):
    '''
    This exception raise when the user input row and col that are not even number
    when initializing
    '''
    pass

class InvalidWinningCondition(Exception):
    '''
    This exception raise when the user input invalid winning condition for
    this game, which is either '>' or '<'
    '''
    pass

class NotAcceptableSymbol(Exception):
    '''
    This exception raise when user input invalid symbols used to make the board
    of the game; if the user's board does not consist of '.','B', or 'W' this
    exception would happen
    '''
    pass

class BoardInitError(Exception):
    '''
    This exception raise when the number of column that user
    input to make the booard contents does not correspond with
    the column limit input when user input at the begin of
    this game
    '''
    pass

class InvalidPlayerChoose(Exception):
    '''
    This exception raise when user tries to choose invalid first
    player, which is neither 'B' nor 'W'
    '''
    pass

############################################################################
# CLASS
############################################################################
def make_board(row,col,b_list,w_list):
    board = []
    occuplied_places = []
    occuplied_places.append(b_list)
    occuplied_places.append(w_list)


    for r in range(row):
        column = []
        for c in range(col):
            column.append('.')

        board.append(column)

    color = 'B'
    for L in occuplied_places:
        for r,c in L:
            board[r][c] = color
        color = 'W'

    return board


class Othello:
    ######################################
    # Constructor
    ######################################
    def __init__ (self,
                  row: int, col: int, first_player: str,
                  winning_cond: str,  board: [['str']]):
        self.board = board
        self.turn = first_player
        self.another = self._get_another()
        self.row_max = row
        self.col_max = col
        self.winning_cond = winning_cond
        self.b_disk, self.w_disk = self._get_curr_discs()
        self.b_valid_pos, self.w_valid_pos = self._get_valid_pos()

        if len(self._get_current_valid_pos()) == 0:
            self._turn_change()


    ######################################
    # PUBLIC
    ######################################
    def place_disc(self, row: int, col: int):
        '''
        This function places a disk at the position
        that the row and the col value indicate.
        '''
        valid_pos = self._get_current_valid_pos()

        if not (row, col) in valid_pos:
            raise InvalidMoveError

        self._travel_eight_dir_to_flip(row,col,valid_pos)
        self._update_disc_num()
        self._update_discs_valid_pos()
        self.is_there_winner()
        self.corner_case()
        self._turn_change()

    def find_winner(self):
        '''
        This function tries to find which player is the winner of this game
        according to the winning condition
        '''
        if self.winning_cond == ">":
            if self.get_num_b_disk() > self.get_num_w_disk():
                return "BLACK"
            if self.get_num_b_disk() == self.get_num_w_disk():
                return "NONE"
            return "WHITE"

        else:
            if self.get_num_b_disk() < self.get_num_w_disk():
                return "BLACK"
            elif self.get_num_b_disk() == self.get_num_w_disk():
                return "NONE"
            return "WHITE"

    def get_curr_discs(self):
        return self._get_curr_discs()

    def get_curr_turn(self):
        return self.turn

    def get_num_b_disk(self):
        '''This returns the number of black disc on the current board'''
        return len(self.b_disk)

    def get_num_w_disk(self):
        '''This returns the number of white discs on the current board'''
        return len(self.w_disk)

    def is_there_winner(self):
        '''
        This function tries to find if a winner of this game
        comes up.
        This function does not deal with the expceptional case
        that the two players do not have valid positions to place
        their disc although there are places to put disc on the board
        '''
        curr_total_disc = self._get_curr_total_disc()
        num_of_board = self._num_of_board()

        if curr_total_disc == num_of_board:
            raise GameOverException

    def corner_case(self):
        '''
        This function calls two functions, _first_corner_case() and _second_cornercase()
        to check the two exceptional cases at the same time
        '''
        self._first_corner_case()
        self._second_corner_case()



    ######################################
    # PRIVATE
    ######################################
    def _get_current_valid_pos(self):
        '''
        This function returns the current player's valid position set
        '''
        if self.turn == BLACK:
            return self.b_valid_pos
        return self.w_valid_pos

    def _update_disc_num(self):
        '''This updates the number of each disc of black and white'''
        self.b_disk, self.w_disk = self._get_curr_discs()

    def _get_curr_discs(self) -> (list, list):
        '''
        This function finds the position of each disc of
        black and white color on the current game board and return
        them in two lists.
        '''
        b_disc = []
        w_disc = []

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pos = (i, j)
                if self.board[i][j] == BLACK:
                    b_disc.append(pos)
                elif self.board[i][j] == WHITE:
                    w_disc.append(pos)

        return (b_disc, w_disc)

    def _update_discs_valid_pos(self):
        '''This updates valid position to place disc of black and white'''
        self.b_valid_pos, self.w_valid_pos = self._get_valid_pos()

    def _get_valid_pos(self) -> (set, set):
        '''
        This function returns a set of the valid positions
        that each player can pose their disc on their turn.
        '''
        b_valid_set = self._travel_eight_dir_to_find(BLACK, WHITE)
        w_valid_set = self._travel_eight_dir_to_find(WHITE, BLACK)
        return (b_valid_set, w_valid_set)



    

    def _travel_eight_dir_to_flip(self, row:int, col: int, validpos : set):
        '''
        This function travels the eight directions from the coordinate that
        the row and the col indicate to flip the discs of opponent player
        to the current players
        '''
        for i, j in EIGHT_DIRECTIONS:
            try:
                if self.board[row + i][col + j] == self.another:
                    nr = row + i + i
                    nc = col + j + j
                    while True:
                        try:
                            if nr < 0 or nc < 0:
                                break
                            if self.board[nr][nc] == self.turn:
                                self._update_board(row, col, i, j)
                                break
                            elif self.board[nr][nc] == NONE:
                                break
                            nr += i
                            nc += j

                        except IndexError:
                            break
            except IndexError:
                pass

    def _update_board(self, row:int, col:int, i:int, j:int):
        '''This function changes the another player's disc to
         current player's one from the index that the row and the col
         indicate toward the direction that the i and j point
         '''
        while True:
            self.board[row][col] = self.turn
            row += i
            col += j
            if self.board[row][col] == self.turn:
                break

    def _travel_eight_dir_to_find(self, own: str, another:str):
        """
        own : a player
        another : the other
        This function travels the eight directions to find valid positions
        to place discs for the player the own represents
        """
        valid_set = set()

        L = self.w_disk
        if own == BLACK:
            L = self.b_disk

        for r,c in L:
            for i, j in EIGHT_DIRECTIONS:
                try:
                    if self.board[r+i][c+j] == another:
                        nr = r + i + i
                        nc = c + j + j
                        while True:
                            try:
                                if nr < 0 or nc < 0:
                                    break
                                if self.board[nr][nc] == NONE:
                                    valid_set.add((nr,nc))
                                    break
                                elif self.board[nr][nc] == own:
                                    break
                                nr += i
                                nc += j
                            except IndexError:
                                break
                except IndexError:
                    pass

        return valid_set



    def _turn_change(self):
        '''THis function change the turn of the game from the current player
        to the next player
        '''
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

        self.another = self._get_another()

    def _get_another (self):
        ''' This function returns not the current player but the another one'''
        if self.turn == BLACK:
            return WHITE
        return BLACK

    
    def _first_corner_case(self):
        '''
        1. If the two players have no valid positions to place their own
        discs; if this happens GameOverException raises
        '''
        if len(self.b_valid_pos) == 0 and len(self.w_valid_pos) == 0 \
                and self._get_curr_total_disc() != self._num_of_board():
            raise GameOverException

    def _second_corner_case(self):
        '''
        2. If the other player have no place to valid position to place
        the disc; in this case, NoAnotherMove raises
        '''
        anothers_valid_pos = self.b_valid_pos
        if self.turn == BLACK:
            anothers_valid_pos = self.w_valid_pos

        if len(anothers_valid_pos) == 0:
            raise NoAnothersMove

    def _get_curr_total_disc(self):
        '''This return total number of the current disc on the current board'''
        return self.get_num_b_disk() + self.get_num_w_disk()

    def _num_of_board(self):
        '''This returns the number of disc places on the board'''
        return self.row_max * self.col_max