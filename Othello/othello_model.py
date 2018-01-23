'''
This module is to hold the detail data that
the othello_view module does not need to know
by interacting with Othello object.
'''
import othello

CELL_WID = 100 #The default multiple of the width of each cell
CELL_HEI = 100 #The default multiple of the height of each cell
DISC_DIAM = 1.5 #The fraction of diameter of each disc

class Disc():
    '''
    This class changes a character representing a color, black or white
    into full letters
    '''
    def __init__(self, c):
        self._color = 'Black'
        if c == 'W':
            self._color = 'White'

    def color(self):
        return self._color


def get_disc_color(c :str) -> str:
    '''
    This takes a string object, which is representing the color as a letter;
    Black -> B, White -> W,
    and returns color data through Disc class
    '''
    return Disc(c).color()


class CellState():
    '''
    '''
    def __init__ (self):
        '''
        Initializes the board of the game
        '''
        self.disc_dict = {'Black':[],
                          'White':[]}
        self.oth = None

    def get_all_discs(self) -> dict:
        '''
        This returns disc_dictionary
        '''
        return self.disc_dict

    def put_discs(self, row:int, col:int):
        '''
        This puts the a disc on the board of othello object
        at the row and the column indicate

        '''
        self.oth.place_disc(row, col)

    def add_dics(self, row:int, col:int, color:str):
        '''
        This function is triggered only during initializing game board.
        This places a disc of the color at the row and the column indicate
        '''
        b_list, w_list = self.disc_dict.values()

        if not (row,col) in b_list and not (row,col) in w_list:
            self.disc_dict[color].append((row,col))

    def update_cell_state(self):
        '''
        This updates the board of the user interface after
        receiving each color's disc from othello object
        '''
        b_list, w_list = self.oth.get_curr_discs()
        self.disc_dict['Black'] = b_list
        self.disc_dict['White'] = w_list

    def init_othello(self,row,col,first_p,wincond,b_list,w_list):
        '''
        This initializes an othello object.
        '''
        board = othello.make_board(row,col,b_list,w_list)
        self.oth = othello.Othello(row,col,first_p,wincond,board)
        self.oth.is_there_winner()
        self.oth.corner_case()

    def next_turn(self)->Disc:
        '''
        This traces which player is at the current turn
        '''
        return get_disc_color(self.oth.get_curr_turn())

    def winner(self)->str:
        '''
        This finds which player is the winner of the game
        '''
        return self.oth.find_winner()