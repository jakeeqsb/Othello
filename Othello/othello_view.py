'''
This module implements InitalizeOthello and OthelloApplication,
the GUI based on tkinter module.
The first class provides GUI that user can
input data for row, column, first player, and winning condition
to initialize the othello game.
The second class provides the environment that the players can
set the game board and play it. Also, this class shows the result of the
game on the board.

'''
import tkinter
import othello_model
import math
import othello
'''
InitializeOthello()
This class is to make the graphical user interface that
the allows the user put the data initializing the game Othello.
The user can input row value, column value, the player who will
have the choice to place disc first, and the winning condition, which
is if the user have most disc would be the winner or not.
This checks if the data input from user is valid or not to initialize the game.
When the user gets success in initializing data, it makes an OhtelloApplication object
to show the user the board of the game.

'''
class InitializeOthello():
    def __init__ (self):
        '''
        Constructor
        This initializes a label showing the game title,
        a label and an entry to show row and to let the user input
        the row value,
        a label and an entry to show column and to let the user input
        the column value,
        a label and an entry to show first player, allowing the user input
        the first player value,
        a label and an entry to show winning condition and to let the user
        input winning condition,
        and a button to pass above all data to OhtelloApplication class
        to make the class object to proceed the game process.
        '''
        # root
        self._root = tkinter.Tk()

        # Label to show the game title - "OTHELLO GAME"
        self._oth_label = tkinter.Label(self._root, text = "OTHELLO GAME")
        self._oth_label.grid(row = 0)

        # Label and Entry for row value
        self._row_lb = tkinter.Label(self._root, text = 'Row:')
        self._row_lb.grid(row = 1)
        self._row_entry = tkinter.Entry(self._root)
        self._row_entry.grid(row=1, column=1)

        # Label and Entry for column value
        self._col_lb = tkinter.Label(self._root, text = 'Column:')
        self._col_lb.grid(row = 2)
        self._col_entry = tkinter.Entry(self._root)
        self._col_entry.grid(row = 2, column = 1)

        # Label and Entry for first player value
        self._f_player = tkinter.Label(self._root, text = 'First Player: (B/W)')
        self._f_player.grid(row = 3)
        self._f_player_ent = tkinter.Entry(self._root)
        self._f_player_ent.grid(row = 3, column = 1)

        # Label and Entry for winning condition value
        self._win_cond_lb = tkinter.Label(self._root, text = "Winning Condition (</>)")
        self._win_cond_lb.grid(row = 4)
        self._win_cond_ent = tkinter.Entry(self._root)
        self._win_cond_ent.grid(row =4, column = 1)

        # Button for the next step
        self._next = tkinter.Button(self._root,text='Next')
        self._next.bind('<Button-1>', self._call_board_init)
        self._next.grid(row = 5)

    def run(self):
        '''
        This runs the root window
        '''
        self._root.mainloop()

    def _call_board_init(self,event:tkinter.Event):
        '''
        This class checks the error with the data, row, col, first player,
        and winning condition by calling _input_valid_check.
        If the data is all valid, this makes an OthelloApplication object
        to go to the next step.
        If one of the data input is invalid it shows what and how the data is wrong
        within a message window
        '''
        try:
            row = int(self._row_entry.get().strip())
            col = int(self._col_entry.get().strip())
            first_p = self._f_player_ent.get().strip()
            win_cond = self._win_cond_ent.get().strip()

            self._input_valid_check(row,col,first_p,win_cond)
            ot = OthelloApplication(row, col,first_p, win_cond, self._root)
            self._root.destroy()

        except ValueError:
            msg = "The value of row or col for initialization should be integer"
            self._error_msg(msg)
        except othello.RowColInputNotEven:
            msg = "The valuf of row and col should be even numbers"
            self._error_msg(msg)
        except othello.InvalidRowColInput:
            msg = "The value of row and col should be range from " + str(othello.MIN) + " to " + str(othello.MAX)
            self._error_msg(msg)
        except othello.InvalidPlayerChoose:
            msg = "The player selection must be either B or W"
            self._error_msg(msg)
        except othello.InvalidWinningCondition:
            msg = "Invalid input for winning condition"
            self._error_msg(msg)

    def _input_valid_check(self, row, col, first_p, win_cond):
        '''
        This function checks validity of inputs that are row value,
        columnm value, first player of the game, and the winning condition
        used to intialize the game
        '''
        if row % 2 != 0 or col % 2 != 0:
            raise othello.RowColInputNotEven

        if row > othello.MAX or col > othello.MAX or \
                        row < othello.MIN or col < othello.MIN:
            raise othello.InvalidRowColInput

        if first_p != 'B' and first_p != 'W':
            raise othello.InvalidPlayerChoose

        if win_cond != '<' and win_cond != '>':
            raise othello.InvalidWinningCondition

    def _error_msg(self, msg):
        '''
        This pops up an error message to user with msg
        '''
        window = tkinter.Tk()
        lb = tkinter.Label(window, text = "ERROR\n"+msg)
        lb.pack(padx = 20)


'''
OthelloApplication
This class, first, is divided in to two different frame.

The first frame, which is the upper is to mainly show the rule of the game,
which player is at current turn, the score of each disc, the button to process the next step.

The bottom frame shows the board of the game that users can place the disc at their own turn.

'''
class OthelloApplication():
    def __init__(self, row_max:int, col_max:int, first_player:str, win_cond :str ,root):

        self._root_window = tkinter.Tk()

        # Data for board size, the first player, the winning condition
        self.row_max = row_max
        self.col_max = col_max
        self.first_player = first_player
        self.curr_player = 'B'
        self.win_cond = win_cond

        # If it's True, it means the game is on initialization mode for the game board
        self.init_mode = True
        self.cell_state = othello_model.CellState()

        self.width = self.row_max * othello_model.CELL_WID
        self.height = self.col_max * othello_model.CELL_HEI

        ####################################################
        #_upper_frame
        ####################################################
        self._upper_frame = tkinter.Frame(self._root_window)
        self._upper_frame.pack(fill = 'x')

        # A label to show the game rule
        self._rule = tkinter.Label(self._upper_frame, text = 'FULL', bg = 'green')
        self._rule.pack()

        # A label to show which player is at the current turn
        self._curr_p_init_lb = tkinter.Label(self._upper_frame, text = "Place black disc first")
        self._curr_p_init_lb.pack(side = 'left')

        # A button to process next step of the game during initialization of the board
        self._next = tkinter.Button(self._upper_frame, text = 'Next')
        self._next.bind('<Button-1>' ,self._change_init_to_white)
        self._next.pack(side = 'right')

        # To show the score of the each board, they are Label objects
        self._black_score = None
        self._white_score = None

        ####################################################
        # Bottom Frame
        ####################################################
        self._bottom_frame = tkinter.Frame(self._root_window)
        self._bottom_frame.pack()
        # the game board
        self._board = tkinter.Canvas(self._bottom_frame, width = self.width, height = self.height, bg = 'green')
        self._board.pack(padx = 20, pady = 20)

        self._create_board(self.width, self.height)

        self._board.bind('<Button-1>', self._on_board_clicked)
        self._board.bind('<Configure>', self._on_canvas_resize)

    def _create_board(self, row, col):
        '''
        This class makes the game board sized by row x col
        '''
        delta_x, delta_y = self._get_delta_x_y()

        row = row - (row%self.row_max)
        col = col - (col%self.col_max)


        if delta_x == 0 and delta_y == 0:
            delta_x = 3
            delta_y = 3

        for x in range(delta_x, row, delta_x):
            self._board.create_line(x, 0, x, col, fill="black")
        for y in range(delta_y, col, delta_y):
            self._board.create_line(0, y, row, y, fill="black")


    def _on_canvas_resize(self,event : tkinter.Event):
        '''
        This function is triggered when user tries to resize the window
        of the game. This resizes the game board according to the chaning size of
        the game board.
        '''
        try:
            self._board.delete(tkinter.ALL)
            wid = self._board.winfo_width()
            hei = self._board.winfo_height()
            self._create_board(wid, hei)
            self._draw_discs()
        except ValueError:
            pass


    def _on_board_clicked(self, event: tkinter.Event):
        '''
        This function is triggered when the users make mouse click on
        _board canvas to place a disc or discs chosen by the player at the
        current turn at each cell on the board.
        Then it updates the game board.
        '''
        delta_x, delta_y = self._get_delta_x_y()

        row = int(event.y/delta_y)
        col = int(event.x/delta_x)

        if self.init_mode :
            color = othello_model.get_disc_color(self.curr_player)
            self.cell_state.add_dics(row,col,color)

        else:
            try:
                self.cell_state.put_discs(row,col)
                self._update_turn()

            except othello.GameOverException:
                self._winner_msg()
            except othello.NoAnothersMove:
                pass
            except othello.InvalidMoveError:
                pass
            finally:
                self.cell_state.update_cell_state()
                self._update_score()

        self._draw_discs()


    def _draw_discs(self):
        '''
        This draws all discs of each color on the game board as cell_state
        object specifies
        '''
        discs = self.cell_state.get_all_discs()

        for color, coord in discs.items():
            for row,col in coord:
                self._draw_disc(row, col, color)

    def _draw_disc(self, row, col, color):
        '''
        This function places a disc colored by the color at the
        coordinate specified by row and col
        '''
        delta_x,delta_y = self._get_delta_x_y()

        row *= delta_y # y coordinate
        col *= delta_x # x coordinate
        x = (delta_x/2)
        y = (delta_y/2)
        self._board.create_oval(col + (x * .5), row + (y * .5), col + (x*othello_model.DISC_DIAM) , row + (y*othello_model.DISC_DIAM)
                                ,fill = color)

    def _change_init_to_white(self, event: tkinter.Event):
        '''
        This function is to change the turn from black to white to let
        the white user place discs as the player wants in initializing board.
        This changes the next button to a button to start the game by finishing
        the initialization of the game board.
        '''
        self.curr_player = 'W'

        self._curr_p_init_lb.destroy()
        self._next.destroy()

        self._curr_p_init_lb = tkinter.Label(self._upper_frame, text="Place white disc")
        self._curr_p_init_lb.pack(side='left')

        self._next = tkinter.Button(self._upper_frame, text='GameStart')
        self._next.bind('<Button-1>', self._game_start)
        self._next.pack(side='right')


    def _game_start(self, event:tkinter.Event):
        '''
        This function is triggered when user click the gamestart button.
        '''
        try:
            self.curr_player = othello_model.get_disc_color(self.first_player)
            self.init_mode = False
            b_list, w_list = self.cell_state.get_all_discs().values()
            self.cell_state.init_othello(self.row_max, self.col_max, self.first_player, self.win_cond, b_list, w_list)
            self._update_turn()
        except othello.GameOverException:
            self._winner_msg()
        except othello.NoAnothersMove:
            self._update_turn()
        finally:
            self._next.destroy()
            self._update_score()


    def _update_turn(self):
        '''
        This function is to update the current turn of the game
        '''
        self.curr_player = self.cell_state.next_turn()
        self._curr_p_init_lb.destroy()
        self._curr_p_init_lb = tkinter.Label(self._upper_frame, text="TRUN: " + self.curr_player)
        self._curr_p_init_lb.pack()


    def _update_score(self):
        '''
        This function is to update and show the score of each disc to the users.
        '''
        b_list, w_list = self.cell_state.get_all_discs().values()

        b_score = len(b_list)
        w_score = len(w_list)

        if self._black_score and self._white_score != None:
            self._black_score.destroy()
            self._white_score.destroy()

        self._black_score = tkinter.Label(self._upper_frame, text = 'Black: ' + str(b_score))
        self._white_score = tkinter.Label(self._upper_frame, text = "White: " + str(w_score))
        self._black_score.pack(side = 'left', padx= 20)
        self._white_score.pack(side = 'right',padx = 20)

    def _winner_msg(self):
        '''
        This is making a window showing which player is the winner of the game
        based on the winning condition.
        '''
        winner = self.cell_state.winner()
        self._curr_p_init_lb.destroy()
        self._curr_p_init_lb = tkinter.Label(self._upper_frame, text="GAMEOVER\nWINNER: " + winner)
        self._curr_p_init_lb.pack(padx= 20)

    def _get_delta_x_y (self):
        '''
        This function returns width and column of each cell as integer
        '''
        delta_x = int(self._board.winfo_width() / self.col_max)
        delta_y = int(self._board.winfo_height() / self.row_max)
        return (delta_x, delta_y)


