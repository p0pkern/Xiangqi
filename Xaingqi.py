# Author: Chris Peterman
# Version: 0.0
# Name: Xiangqi Game
# Language: Python 3
# Description: This is a program for the game Xaingqi (known as Chinese Chess). A tactical board game simulating a
# battle between two armies, Red and Black.

# Modules
import pprint


class Xiangqi:
    """
  Main game engine of the game Xiangqi, or Chinese Chess.
  """

    def __init__(self):

        # BOARD FUNCTIONS

        # Reference for in bound moves
        # Red Side
        self._board = [["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "i1"],
                       ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "i2"],
                       ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "i3"],
                       ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "i4"],
                       ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "i5"],
                       #################      RIVER      #####################
                       ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", "i6"],
                       ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "i7"],
                       ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "i8"],
                       ["a9", "b9", "c9", "d9", "e9", "f9", "g9", "h9", "i9"],
                       ["a10", "b10", "c10", "d10", "e10", "f10", "g10", "h10", "i10"]]
        # Black Side

        # Player dictionaries for important piece data.
        self._board_dict_red = {}
        self._board_dict_black = {}

        # START OF GAME. Red goes first.
        self._player_turn = 'red'
        # Options are RED_WON, BLACK_WON, STALE_MATE, or UNFINISHED
        self._game_state = 'UNFINISHED'

        # Loads initial game pieces and adds them to the player dictionaries.
        self._active_pieces = NewGame()
        self.update_move_pool(self._active_pieces)

    def update_dict(self, piece_list):
        """
    Update the player dictionaries with active pieces and displays name, player, location, and potential legal moves.
    :param piece_list: Hidden list of Object pieces.
    """
        # Update red dictionary
        self._board_dict_red = {}
        count = 1
        for i in piece_list:
            if i.get_player() == 'red':
                self._board_dict_red[count] = ["Name: " + str(i.get_piece_name()), "player: " + str(i.get_player()),
                                               "location: " + str(i.get_piece_location()),
                                               "Moves: " + str(i.get_legal_moves())]
                count += 1

        # Update black dictionary
        self._board_dict_black = {}
        count_2 = 1
        for i in piece_list:
            if i.get_player() == 'black':
                self._board_dict_black[count_2] = ["Name: " + str(i.get_piece_name()), "player: " + str(i.get_player()),
                                                   "location: " + str(i.get_piece_location()),
                                                   "Moves: " + str(i.get_legal_moves())]
                count_2 += 1

    def update_move_pool(self, piece):
        """
    Takes in a piece object and updates its potential move pool.
    :param piece: The piece to check for legal moves.
    """
        for i in piece:
            piece = i
            if i.get_piece_name() == 'ADVISOR':
                i.advisor_legal_moves(piece, self._board, self._active_pieces)
            elif i.get_piece_name() == 'ELEPHANT':
                i.elephant_legal_moves(piece, self._board, self._active_pieces)
            elif i.get_piece_name() == 'HORSE':
                i.horse_legal_moves(piece, self._board, self._active_pieces)
            elif i.get_piece_name() == 'CHARIOT':
                i.chariot_legal_moves(piece, self._board, self._active_pieces)
            elif i.get_piece_name() == 'CANNON':
                i.cannon_legal_moves(piece, self._board, self._active_pieces)
            elif i.get_piece_name() == 'SOLDIER':
                i.soldier_legal_moves(piece, self._board, self._active_pieces)
            elif i.get_piece_name() == 'GENERAL':
                i.general_legal_moves(piece, self._board, self._active_pieces)

        self.update_dict(self._active_pieces)
        return True

    def get_piece_data(self):
        """
    Using pretty print to print the dictionary data to the screen.
    """
        pprint.pprint(self._board_dict_red)
        print()
        pprint.pprint(self._board_dict_black)

    def set_player_turn(self):
        """
        Change the current players turn.
        """
        if self._player_turn == 'red':
            self._player_turn = 'black'
        else:
            self._player_turn = 'red'

    def get_player_turn(self):
        return self._player_turn

    def set_game_state(self, state):
        self._game_state = state

    def get_game_state(self):
        return self._game_state

    def make_move(self, start, end):
        """
        Move a piece selected from a start location, written in alphanumeric a1 - i10, to an end location.
        Make move will check if the move is legal and make the move if all conditions are met.
        :param start: The selected piece, if a blank piece is chosen will return False.
        :param end: The place where a selected piece wants to move, will move there and capture a piece if it is a
        legal move.
        :return: True if successful of False if unsuccessful.
        """
        # Starting variables.
        piece = None  # piece is None until a start with a piece in it is selected.
        block = False  # block is False unless there is any piece in an end.
        attack = False  # attack is False unless a blocked piece is the opposing side.

        if start == end:  # Prevents movement to the same space
            return False

        # Check what game state is.
        if self.get_game_state() != 'UNFINISHED':
            print("Game is not unfinished")
            return False

        # Verify start and end are within the board
        if self.legal_location_check(start) and self.legal_location_check(end):

            # Find the piece located in start
            for i in self._active_pieces:
                if i.get_piece_location() == start:
                    piece = i
                    break

            # Check to see that a piece is actually selected.
            if piece is None:
                return False

            if piece.get_player() != self.get_player_turn():
                print("This piece cannot move this turn")
                return False

            # Verify legal move is in move pool.
            if end not in piece.get_legal_moves():
                print("Illegal move")
                return False

            # Check if there is piece at the end location.
            for j in self._active_pieces:
                if j != piece:
                    if j.get_piece_location() == end:
                        piece_2 = j
                        attack = True
                        block = True
                        break

            # If there is a piece in end and it is an enemy piece take the piece location and move,
            # otherwise return False.
            if block is True:
                if attack is True:
                    self._active_pieces.remove(piece_2)
                    piece.move_piece(end)
                    self.update_move_pool(self._active_pieces)
                    self.set_player_turn()
                    print(self.get_player_turn())
                    return True
                else:
                    return False

            # If there is no piece in the current location and it is a legal move, move the piece.
            else:
                piece.move_piece(end)
                self.update_move_pool(self._active_pieces)
                self.set_player_turn()
                print(self.get_player_turn())
                return True
        else:
            return False

    def legal_location_check(self, location):
        """
        Check to see if the alphanumeric location is within the board.
        :param location: The board location to check.
        :return: True or False depending on if the location is on the board.
        """
        in_bounds = False
        for i in self._board:
            if location in i:
                in_bounds = True
                break
        return in_bounds

    # TODO - DEBUGGING AREA


# GAME PIECES
class Pieces():
    """
  Game piece object creation. Contains all important functions for piece data such as current location, legal moves,
  player who owns piece.
  """

    def __init__(self):
        self._current_location = None
        self._legal_moves = []
        self._player = None
        self._name = None

    def set_player(self, player):
        """
    Set piece to color of player
    """
        self._player = player

    def get_player(self):
        """
    Gets player color of who owns a piece.
    """
        return self._player

    def get_piece_name(self):
        """
    Get the name of the piece.
    """
        return self._name

    def get_piece_location(self):
        """
    Get alpha numeric location of piece.
    """
        return self._current_location

    def get_legal_moves(self):
        """
    Get the current pool of legal moves that a piece can move to.
    """
        return self._legal_moves

    def clear_pool(self):
        """
    Resets current move pool to zero.
    """
        self._legal_moves = []

    def add_move_to_pool(self, move):
        """
    Add a selected alpha numeric location to the pieces move pool.
    """
        self._legal_moves.append(move)

    def move_piece(self, location):
        """
    Changes a pieces current location to the selected location.
    """
        self._current_location = location

    def delete_move(self, move):
        """
    Deletes the selected move from the move pool.
    """
        self._legal_moves.remove(move)

    # Piece movement operations
    def get_index_of_location(self, piece, board):
        """
        Returns the index values of the piece on the board.
        :param piece: The alphanumerical piece location.
        :param board: The reference board.
        :return: The index number of the column and the index number of the row.
        """
        index_column = None
        index_row = None
        for i in board:
            for t in i:
                if piece.get_piece_location() == t:
                    index_column = i.index(t)
                    index_row = board.index(i)
        return index_column, index_row

    def friendly_player(self, piece, piece_list):
        selection = None
        for i in piece_list:
            if i.get_piece_location() == piece:
                selection = i
                break
        return selection

    def orthogonal_movement(self, index_row, index_column, row, column, board):
        move = board[index_row + row][index_column + column]
        return move

    def movement_pool_check(self, piece):
        """
        Movement pool used for GENERAL and ADVISOR
        :param piece: Piece to check for player ownership
        :return:
        """
        if piece.get_player() == 'red':
            move_pool = ['d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3']
        else:
            move_pool = ['d8', 'd9', 'd10', 'e8', 'e9', 'e10', 'f8', 'f9', 'f10']
        return move_pool


# INDIVIDUAL PIECES
class General(Pieces):
    """
  The General is the King of the pieces. This is the piece that the enemy team must try and capture. This class will
  contain the data the General needs to update it's move pool.
  Generals can only move in the confines of the castle, in any direction orthoganally.
  """

    def __init__(self):
        super().__init__()
        self._name = 'GENERAL'

    def general_legal_moves(self, piece, board, piece_list):
        """
    Will check the board for all of the General's legal moves and add them to the reference pool
    :param piece: Piece to update move pool for.
    :param board: Reference of the board.
    :param piece_list: The list of current active pieces for reference.
    """
        piece.clear_pool()  # Clear move pool.

        # Each General can not leave a specific square. This is all the potential moves that a General could make in the
        # confines of the square.
        move_pool_1 = ['d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3']
        move_pool_2 = ['d8', 'd9', 'd10', 'e8', 'e9', 'e10', 'f8', 'f9', 'f10']

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_index_of_location(piece, board)
        # Picks correct move pool for the given General piece
        movement_pool = self.movement_pool_check(piece)

        # General can move only orthogonally. This will add each legal orthogonal move to the legal move pool.
        try:
            # Upward one row of the board, same column.
            pos = self.orthogonal_movement(index_row, index_column, -1, 0, board)
            if pos in movement_pool and self.friendly_player(pos, piece_list) is None:
                piece.add_move_to_pool(pos)
            elif pos in movement_pool and self.friendly_player(pos, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(pos)
        except:
            pass
        try:
            # Down one row of the board, same column.
            pos = self.orthogonal_movement(index_row, index_column, +1, 0, board)
            if pos in movement_pool and self.friendly_player(pos, piece_list) is None:
                piece.add_move_to_pool(pos)
            elif pos in movement_pool and self.friendly_player(pos, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(pos)
        except:
            pass
        try:
            # Left one column on the board, same row.
            pos = self.orthogonal_movement(index_row, index_column, 0, -1, board)
            if pos in movement_pool and self.friendly_player(pos, piece_list) is None:
                piece.add_move_to_pool(pos)
            elif pos in movement_pool and self.friendly_player(pos, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(pos)
        except:
            pass
        try:
            # Right one column of the board, same row.
            pos = self.orthogonal_movement(index_row, index_column, 0, +1, board)
            if pos in movement_pool and self.friendly_player(pos, piece_list) is None:
                piece.add_move_to_pool(pos)
            elif pos in movement_pool and self.friendly_player(pos, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(pos)
        except:
            pass

class Advisor(Pieces):
    """
  Advisors guard the General in the castle. They can move one space any direction diagonally.
  """

    def __init__(self):
        super().__init__()
        self._name = 'ADVISOR'

    def advisor_legal_moves(self, piece, board, piece_list):

        color = piece.get_player()  # Set to current player.
        piece.clear_pool()  # Clear move pool.

        # Each General can not leave a specific square. This is all the potential moves that a General could make in the
        # confines of the square.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_index_of_location(piece, board)

        # Advisor can move only diagonally in one direction.
        # This will add each legal diagonal move to the legal move pool.
        try:
            # Upward one row of the board, same column.
            if color == 'red':
                if board[index_row - 1][index_column - 1] in move_pool_1:
                    piece.add_move_to_pool(board[index_row - 1][index_column - 1])
            elif color == 'black':
                if board[index_row - 1][index_column - 1] in move_pool_2:
                    piece.add_move_to_pool(board[index_row - 1][index_column - 1])
        except:
            pass
        try:
            # Down one row of the board, same column.
            if color == 'red':
                if board[index_row - 1][index_column + 1] in move_pool_1:
                    piece.add_move_to_pool(board[index_row - 1][index_column + 1])
            elif color == 'black':
                if board[index_row - 1][index_column + 1] in move_pool_2:
                    piece.add_move_to_pool(board[index_row - 1][index_column + 1])
        except:
            pass
        try:
            # Left one column on the board, same row.
            if color == 'red':
                if board[index_row + 1][index_column - 1] in move_pool_1:
                    piece.add_move_to_pool(board[index_row + 1][index_column - 1])
            elif color == 'black':
                if board[index_row + 1][index_column - 1] in move_pool_2:
                    piece.add_move_to_pool(board[index_row + 1][index_column - 1])
        except:
            pass
        try:
            # Right one column of the board, same row.
            if color == 'red':
                if board[index_row + 1][index_column + 1] in move_pool_1:
                    piece.add_move_to_pool(board[index_row + 1][index_column + 1])
            elif color == 'black':
                if board[index_row + 1][index_column + 1] in move_pool_2:
                    piece.add_move_to_pool(board[index_row + 1][index_column + 1])
        except:
            pass

        for j in piece_list:
            if j.get_player() == color and j.get_piece_location() in piece.get_legal_moves():
                piece.delete_move(j.get_piece_location())
            if piece.get_piece_location() in j.get_legal_moves() and j.get_player() != piece.get_player():
                remove = j.get_piece_location()
                piece.delete_move(remove)


class Elephant(Pieces):

    def __init__(self):
        super().__init__()
        self._name = 'ELEPHANT'

    def elephant_legal_moves(self, piece, board, piece_list):

        piece.clear_pool()  # Clear move pool.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_index_of_location(piece, board)
        # Picks correct movement pool for advisor
        movement_pool = self.movement_pool_check(piece)

        # Up left
        try:
            pos = self.orthogonal_movement(index_row, index_column, -1, -1, board)
            if pos in movement_pool and self.friendly_player(pos, piece_list) is False:
                piece.add_move_to_pool(pos)
            temp = False
            # Set potential move to up left square.
            a = board[index_row - 1][index_column - 1]
            for i in piece_list:
                if i.get_piece_location() == a and i != piece:
                    temp = True
                    break
            # If there is no piece in the way set potential location to up left square from a
            if temp is not True:
                b = board[index_row - 2][index_column - 2]
                if (index_row - 2) >= 0 and (index_column - 2) >= 0:
                    piece.add_move_to_pool(b)
        except:
            pass

        # Up - right
        try:
            temp_2 = False
            # Set potential move to up right square.
            c = board[index_row - 1][index_column + 1]
            for i in piece_list:
                if i.get_piece_location() == c and i != piece:
                    temp_2 = True
                    break
            # If there is no piece in the way set potential location to up right square from c
            if temp_2 is not True:
                d = board[index_row - 2][index_column + 2]
                if (index_row - 2) >= 0 and (index_column + 2) in range(0, 10):
                    piece.add_move_to_pool(d)
        except:
            pass

        # Down - left
        try:
            temp_3 = False
            # Set potential move to down left square.
            e = board[index_row + 1][index_column - 1]
            for i in piece_list:
                if i.get_piece_location() == e and i != piece:
                    temp_3 = True
                    break
            # If there is no piece in the way set potential location to down left square from e
            if temp_3 is not True:
                f = board[index_row + 2][index_column - 2]
                if (index_row + 2) in range(0, 10) and (index_column - 2) in range(0, 10):
                    piece.add_move_to_pool(f)
        except:
            pass

        # Down - right
        try:
            temp_4 = False
            # Set potential move to down right square.
            g = board[index_row + 1][index_column + 1]
            for i in piece_list:
                if i.get_piece_location() == g and i != piece:
                    temp_4 = True
                    break
            # If there is no piece in the way set potential location to down right square from g
            if temp_4 is not True:
                h = board[index_row + 2][index_column + 2]
                if (index_row + 2) in range(0, 10) and (index_column + 2) in range(0, 10):
                    piece.add_move_to_pool(h)
        except:
            pass

        for n in piece.get_legal_moves():
            for o in piece_list:
                if o.get_player() == piece.get_player() and o.get_piece_location() == n:
                    piece.delete_move(n)


class Horse(Pieces):

    def __init__(self):
        super().__init__()
        self._name = 'HORSE'

    def horse_legal_moves(self, piece, board, piece_list):

        piece.clear_pool()  # Clear move pool.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_index_of_location(piece, board)

        # Check on the Horse legal moves

        # Left - up (left 2 up 1)
        try:
            temp = False
            left_flag = False
            # Set a to the left square, then check to see if any pieces are currently in that square.
            a = board[index_row][index_column - 1]
            for i in piece_list:
                if i.get_piece_location() == a and i != piece:
                    temp = True
                    left_flag = True
                    break
            # If there is no piece in the left square, check to see if the index of the move wraps around the board.
            if temp is not True:
                b = board[index_row - 1][index_column - 2]
                if (index_row - 1) >= 0 and (index_column - 2) >= 0:
                    piece.add_move_to_pool(b)
        except:
            pass
        # left - down (left 2 down 1)
        try:
            if left_flag is not True:
                c = board[index_row + 1][index_column - 2]
                if (index_row + 1) in range(0, 10) and (index_column - 2) in range(0, 10):
                    piece.add_move_to_pool(c)
        except:
            pass

        # Up - left (up 2 left 1)
        try:
            temp_2 = False
            up_flag = False
            # Set a to the left square, then check to see if any pieces are currently in that square.
            d = board[index_row - 1][index_column]
            for i in piece_list:
                if i.get_piece_location() == d and i != piece:
                    temp_2 = True
                    up_flag = True
                    break
            # If there is no piece in the left square, check to see if the index of the move wraps around the board.
            if temp_2 is not True:
                e = board[index_row - 2][index_column - 1]
                if (index_row - 2) >= 0 and (index_column - 1) >= 0:
                    piece.add_move_to_pool(e)
        except:
            pass
        # up - right (up 2 right 1)
        try:
            if up_flag is not True:
                f = board[index_row - 2][index_column + 1]
                if (index_row - 2) in range(0, 10) and (index_column + 1) in range(0, 10):
                    piece.add_move_to_pool(f)
        except:
            pass

        # right - up (right 2 up 1)
        try:
            temp_3 = False
            right_flag = False
            # Set a to the left square, then check to see if any pieces are currently in that square.
            g = board[index_row][index_column + 1]
            for i in piece_list:
                if i.get_piece_location() == g and i != piece:
                    temp_3 = True
                    right_flag = True
                    break
            # If there is no piece in the left square, check to see if the index of the move wraps around the board.
            if temp_3 is not True:
                h = board[index_row - 1][index_column + 2]
                if (index_row - 2) >= 0 and (index_column - 1) >= 0:
                    piece.add_move_to_pool(h)
        except:
            pass
        # right - down (left 2 down 1)
        try:
            if right_flag is not True:
                j = board[index_row + 1][index_column + 2]
                if (index_row + 1) in range(0, 10) and (index_column + 2) in range(0, 10):
                    piece.add_move_to_pool(j)
        except:
            pass

        # down - left (down 2 left 1)
        try:
            temp_4 = False
            down_flag = False
            # Set a to the left square, then check to see if any pieces are currently in that square.
            k = board[index_row + 1][index_column]
            for i in piece_list:
                if i.get_piece_location() == k and i != piece:
                    temp_4 = True
                    down_flag = True
                    break
            # If there is no piece in the left square, check to see if the index of the move wraps around the board.
            if temp_4 is not True:
                l = board[index_row + 2][index_column - 1]
                if (index_row + 2) >= 0 and (index_column - 1) >= 0:
                    piece.add_move_to_pool(l)
        except:
            pass
        # down - right (left 2 down 1)
        try:
            if down_flag is not True:
                m = board[index_row + 2][index_column + 1]
                if (index_row + 2) in range(0, 10) and (index_column + 1) in range(0, 10):
                    piece.add_move_to_pool(m)
        except:
            pass

        for n in piece.get_legal_moves():
            for o in piece_list:
                if o.get_player() == piece.get_player() and o.get_piece_location() == n:
                    piece.delete_move(n)


class Chariot(Pieces):

    def __init__(self):
        super().__init__()
        self._name = 'CHARIOT'

    def chariot_legal_moves(self, piece, board, piece_list):

        piece.clear_pool()  # Clear move pool.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_index_of_location(piece, board)

        red_move_pool = []
        black_move_pool = []

        for x in piece_list:
            if x.get_player() == 'red':
                red_move_pool.append(x.get_piece_location())
            else:
                black_move_pool.append(x.get_piece_location())

        # Down column
        try:
            i = 1
            index_break = False
            while index_row + i < 10 and index_break is False:
                a = board[index_row + i][index_column]
                if a in red_move_pool and piece.get_player() == 'red':
                    index_break = True
                elif a in black_move_pool and piece.get_player() == 'black':
                    index_break = True
                else:
                    piece.add_move_to_pool(a)
                    i += 1
        except:
            pass

        # Up column
        try:
            i = 1
            index_break = False
            while index_row - i >= 0 and index_break is False:
                a = board[index_row - i][index_column]
                if a in red_move_pool and piece.get_player() == 'red':
                    index_break = True
                elif a in black_move_pool and piece.get_player() == 'black':
                    index_break = True
                else:
                    piece.add_move_to_pool(a)
                    i += 1
        except:
            pass

        # Left row
        try:
            i = 1
            index_break = False
            while index_column - i >= 0 and index_break is False:
                a = board[index_row][index_column - i]
                if a in red_move_pool and piece.get_player() == 'red':
                    index_break = True
                elif a in black_move_pool and piece.get_player() == 'black':
                    index_break = True
                else:
                    piece.add_move_to_pool(a)
                    i += 1
        except:
            pass

        # Right
        try:
            i = 1
            index_break = False
            while index_column + i < 10 and index_break is False:
                a = board[index_row][index_column + i]
                if a in red_move_pool and piece.get_player() == 'red':
                    index_break = True
                elif a in black_move_pool and piece.get_player() == 'black':
                    index_break = True
                else:
                    piece.add_move_to_pool(a)
                    i += 1
        except:
            pass


class Cannon(Pieces):

    def __init__(self):
        super().__init__()
        self._name = 'CANNON'

    def cannon_legal_moves(self, piece, board, piece_list):
        piece.clear_pool()  # Clear move pool.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_index_of_location(piece, board)

        red_move_pool = []
        black_move_pool = []

        for x in piece_list:
            if x != piece:
                if x.get_player() == 'red':
                    red_move_pool.append(x.get_piece_location())
                else:
                    black_move_pool.append(x.get_piece_location())

        # Down column
        try:
            i = 1
            index_break = False
            jump_move = None
            while index_row + i < 10 and index_break is False:
                a = board[index_row + i][index_column]
                if a in red_move_pool or a in black_move_pool:
                    for b in piece_list:
                        if b.get_piece_location() == a:
                            jump_move = b
                    index_break = True
                else:
                    piece.add_move_to_pool(a)
                    i += 1

            try:
                if jump_move is not None:
                    jump_index_column, jump_index_row = self.get_index_of_location(jump_move, board)

                    c = 1
                    jump_index_break = False
                    while jump_index_row + c < 10 and jump_index_break is False:
                        d = board[jump_index_row + c][jump_index_column]
                        if d in red_move_pool and piece.get_player() == 'red':
                            jump_index_break = True
                        elif d in black_move_pool and piece.get_player() == 'black':
                            jump_index_break = True
                        else:
                            for e in piece_list:
                                if d == e.get_piece_location():
                                    if e.get_player() != piece.get_player():
                                        piece.add_move_to_pool(d)
                                        jump_index_break = True
                            c += 1
            except:
                pass

        except:
            pass

        # Up column
        try:
            i = 1
            index_break = False
            jump_move = None
            while index_row - i >= 0 and index_break is False:
                a = board[index_row - i][index_column]
                if a in red_move_pool or a in black_move_pool:
                    for b in piece_list:
                        if b.get_piece_location() == a:
                            jump_move = b
                    index_break = True
                else:
                    piece.add_move_to_pool(a)
                    i += 1

            try:
                if jump_move is not None:
                    jump_index_column, jump_index_row = self.get_index_of_location(jump_move, board)

                    c = 1
                    jump_index_break = False
                    while jump_index_row - c < 10 and jump_index_break is False:
                        d = board[jump_index_row - c][jump_index_column]
                        if d in red_move_pool and piece.get_player() == 'red':
                            jump_index_break = True
                        elif d in black_move_pool and piece.get_player() == 'black':
                            jump_index_break = True
                        else:
                            for e in piece_list:
                                if d == e.get_piece_location():
                                    if e.get_player() != piece.get_player():
                                        piece.add_move_to_pool(d)
                                        jump_index_break = True
                            c += 1
            except:
                pass

        except:
            pass

        # # Left row
        try:
            i = 1
            index_break = False
            jump_move = None
            while index_column - i >= 0 and index_break is False:
                a = board[index_row][index_column - i]
                if a in red_move_pool or a in black_move_pool:
                    for b in piece_list:
                        if b.get_piece_location() == a:
                            jump_move = b
                    index_break = True
                else:
                    piece.add_move_to_pool(a)
                    i += 1

            try:
                if jump_move is not None:
                    jump_index_column, jump_index_row = self.get_index_of_location(jump_move, board)

                    c = 1
                    jump_index_break = False
                    while jump_index_column - c >= 0 and jump_index_break is False:
                        d = board[jump_index_row][jump_index_column - c]
                        if d in red_move_pool and piece.get_player() == 'red':
                            jump_index_break = True
                        elif d in black_move_pool and piece.get_player() == 'black':
                            jump_index_break = True
                        else:
                            for e in piece_list:
                                if d == e.get_piece_location():
                                    if e.get_player() != piece.get_player():
                                        piece.add_move_to_pool(d)
                                        jump_index_break = True
                            c += 1
            except:
                pass

        except:
            pass

        # Right Row
        try:
            i = 1
            index_break = False
            jump_move = None
            while index_column + i < 10 and index_break is False:
                a = board[index_row][index_column + i]
                if a in red_move_pool or a in black_move_pool:
                    for b in piece_list:
                        if b.get_piece_location() == a:
                            jump_move = b
                    index_break = True
                else:
                    piece.add_move_to_pool(a)
                    i += 1

            try:
                if jump_move is not None:
                    jump_index_column, jump_index_row = self.get_index_of_location(jump_move, board)

                    c = 1
                    jump_index_break = False
                    while jump_index_column + c < 10 and jump_index_break is False:
                        d = board[jump_index_row][jump_index_column + c]
                        if d in red_move_pool and piece.get_player() == 'red':
                            jump_index_break = True
                        elif d in black_move_pool and piece.get_player() == 'black':
                            jump_index_break = True
                        else:
                            for e in piece_list:
                                if d == e.get_piece_location():
                                    if e.get_player() != piece.get_player():
                                        piece.add_move_to_pool(d)
                                        jump_index_break = True
                            c += 1
            except:
                pass

        except:
            pass


class Soldier(Pieces):

    def __init__(self):
        super().__init__()
        self._name = 'SOLDIER'

    def soldier_legal_moves(self, piece, board, piece_list):
        piece.clear_pool()  # Clear move pool.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_index_of_location(piece, board)

        river_flag = piece.get_piece_location()
        river_flag = str(river_flag)[1:]

        if piece.get_player() == 'red':
            if int(river_flag) >= 6:
                try:
                    a = board[index_row + 1][index_column]
                    b = board[index_row][index_column - 1]
                    c = board[index_row][index_column + 1]
                    piece.add_move_to_pool(a)
                    piece.add_move_to_pool(b)
                    piece.add_move_to_pool(c)
                    for i in piece_list:
                        if i.get_piece_location() in piece.get_legal_moves():
                            if i.get_piece_location() == a and i.get_player() == piece.get_player():
                                piece.delete_move(a)
                            if i.get_piece_location() == b and i.get_player() == piece.get_player():
                                piece.delete_move(b)
                            if i.get_piece_location() == c and i.get_player() == piece.get_player():
                                piece.delete_move(c)
                except:
                    pass
            else:
                try:
                    a = board[index_row + 1][index_column]
                    piece.add_move_to_pool(a)
                    for j in piece_list:
                        if j.get_piece_location() == a and j.get_player() == piece.get_player():
                            piece.delete_move(a)
                except:
                    pass

        else:
            if int(river_flag) <= 5:
                try:
                    a = board[index_row - 1][index_column]
                    b = board[index_row][index_column - 1]
                    c = board[index_row][index_column + 1]
                    piece.add_move_to_pool(a)
                    piece.add_move_to_pool(b)
                    piece.add_move_to_pool(c)
                    for i in piece_list:
                        if i.get_piece_location() in piece.get_legal_moves():
                            if i.get_piece_location() == a and i.get_player() == piece.get_player():
                                piece.delete_move(a)
                            if i.get_piece_location() == b and i.get_player() == piece.get_player():
                                piece.delete_move(b)
                            if i.get_piece_location() == c and i.get_player() == piece.get_player():
                                piece.delete_move(c)
                except:
                    pass
            else:
                try:
                    a = board[index_row - 1][index_column]
                    piece.add_move_to_pool(a)
                    for j in piece_list:
                        if j.get_piece_location() == a and j.get_player() == piece.get_player():
                            piece.delete_move(a)
                except:
                    pass


def NewGame():
    """
  This will load all the initial pieces to the correct locations for a new game.
  Returns a list of all pre-loaded pieces.
  """
    new_game = []

    # RED SIDE
    red_general = General()
    red_general.set_player('red')
    red_general.move_piece('e1')
    new_game.append(red_general)

    # red_advisor_left = Advisor()
    # red_advisor_left.set_player('red')
    # red_advisor_left.move_piece('d1')
    # new_game.append(red_advisor_left)
    #
    # red_advisor_right = Advisor()
    # red_advisor_right.set_player('red')
    # red_advisor_right.move_piece('f1')
    # new_game.append(red_advisor_right)

    # red_elephant_left = Elephant()
    # red_elephant_left.set_player('red')
    # red_elephant_left.move_piece('c1')
    # new_game.append(red_elephant_left)
    #
    # red_elephant_right = Elephant()
    # red_elephant_right.set_player('red')
    # red_elephant_right.move_piece('g1')
    # new_game.append(red_elephant_right)
    #
    # red_horse_left = Horse()
    # red_horse_left.set_player('red')
    # red_horse_left.move_piece('b1')
    # new_game.append(red_horse_left)
    #
    # red_horse_right = Horse()
    # red_horse_right.set_player('red')
    # red_horse_right.move_piece('h1')
    # new_game.append(red_horse_right)
    #
    # red_chariot_right = Chariot()
    # red_chariot_right.set_player('red')
    # red_chariot_right.move_piece('i1')
    # new_game.append(red_chariot_right)
    #
    # red_chariot_left = Chariot()
    # red_chariot_left.set_player('red')
    # red_chariot_left.move_piece('a1')
    # new_game.append(red_chariot_left)
    #
    # red_cannon_right = Cannon()
    # red_cannon_right.set_player('red')
    # red_cannon_right.move_piece('b3')
    # new_game.append(red_cannon_right)
    #
    # red_cannon_left = Cannon()
    # red_cannon_left.set_player('red')
    # red_cannon_left.move_piece('h3')
    # new_game.append(red_cannon_left)
    #
    # red_soldier_one = Soldier()
    # red_soldier_one.set_player('red')
    # red_soldier_one.move_piece('a4')
    # new_game.append(red_soldier_one)
    #
    # red_soldier_two = Soldier()
    # red_soldier_two.set_player('red')
    # red_soldier_two.move_piece('c4')
    # new_game.append(red_soldier_two)
    #
    # red_soldier_three = Soldier()
    # red_soldier_three.set_player('red')
    # red_soldier_three.move_piece('e4')
    # new_game.append(red_soldier_three)
    #
    # red_soldier_four = Soldier()
    # red_soldier_four.set_player('red')
    # red_soldier_four.move_piece('g4')
    # new_game.append(red_soldier_four)
    #
    # red_soldier_five = Soldier()
    # red_soldier_five.set_player('red')
    # red_soldier_five.move_piece('i4')
    # new_game.append(red_soldier_five)

    # BLACK SIDE
    black_general = General()
    black_general.set_player('black')
    black_general.move_piece('e10')
    new_game.append(black_general)
    #
    # black_advisor_left = Advisor()
    # black_advisor_left.set_player('black')
    # black_advisor_left.move_piece('d10')
    # new_game.append(black_advisor_left)
    #
    # black_advisor_right = Advisor()
    # black_advisor_right.set_player('black')
    # black_advisor_right.move_piece('f10')
    # new_game.append(black_advisor_right)
    #
    black_elephant_left = Elephant()
    black_elephant_left.set_player('red')
    black_elephant_left.move_piece('e9')
    new_game.append(black_elephant_left)
    #
    # black_elephant_right = Elephant()
    # black_elephant_right.set_player('black')
    # black_elephant_right.move_piece('g10')
    # new_game.append(black_elephant_right)
    #
    # black_horse_left = Horse()
    # black_horse_left.set_player('black')
    # black_horse_left.move_piece('b10')
    # new_game.append(black_horse_left)
    #
    # black_horse_right = Horse()
    # black_horse_right.set_player('black')
    # black_horse_right.move_piece('h10')
    # new_game.append(black_horse_right)
    #
    # black_chariot_right = Chariot()
    # black_chariot_right.set_player('black')
    # black_chariot_right.move_piece('a10')
    # new_game.append(black_chariot_right)

    # black_chariot_right = Chariot()
    # black_chariot_right.set_player('black')
    # black_chariot_right.move_piece('e10')
    # new_game.append(black_chariot_right)

    # black_cannon_right = Cannon()
    # black_cannon_right.set_player('black')
    # black_cannon_right.move_piece('b8')
    # new_game.append(black_cannon_right)
    #
    # black_cannon_left = Cannon()
    # black_cannon_left.set_player('black')
    # black_cannon_left.move_piece('h8')
    # new_game.append(black_cannon_left)
    #
    # black_soldier_one = Soldier()
    # black_soldier_one.set_player('black')
    # black_soldier_one.move_piece('a7')
    # new_game.append(black_soldier_one)
    #
    # black_soldier_two = Soldier()
    # black_soldier_two.set_player('black')
    # black_soldier_two.move_piece('c7')
    # new_game.append(black_soldier_two)
    #
    # black_soldier_three = Soldier()
    # black_soldier_three.set_player('black')
    # black_soldier_three.move_piece('e7')
    # new_game.append(black_soldier_three)
    #
    # black_soldier_four = Soldier()
    # black_soldier_four.set_player('black')
    # black_soldier_four.move_piece('g7')
    # new_game.append(black_soldier_four)
    #
    # black_soldier_five = Soldier()
    # black_soldier_five.set_player('black')
    # black_soldier_five.move_piece('i7')
    # new_game.append(black_soldier_five)

    return new_game


# TESTING PURPOSES
xi = Xiangqi()
xi.get_piece_data()
# xi.make_move('a7', 'a6')
# print()
# xi.get_piece_data()
# xi.make_move('e8', 'c6')
# print()
# xi.get_piece_data()
# xi.make_move('c6', 'e4')
# print()
# xi.get_piece_data()
# xi.make_move('e4', 'c2')
# print()
# xi.get_piece_data()
