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
    :items:
    _board - The list of all possible moves on the board for reference.
    _red_pieces_information - Stores all of the red pieces information in a dictionary.
    _black_pieces_information - Stores all of the black pieces information in a dictionary.
    _red_pieces_legal_moves - List of all possible moves from red team.
    -black_pieces_legal_moves - List of all possible moves from black team.
    _player_turn - Stores the current color of the active player.
    _game_state - Stores the current game state, UNFINISHED, RED_WON, BLACK_WON, or STALEMATE.
    _active_pieces - Stores the active piece objects for reference.

    :methods:
    pull_piece_information - Stores active piece information in to _red_pieces_information or _black_pieces_information
    get_piece_data - Prints the information stored in _red_pieces_information or _black_pieces_information
    update_move_pool - Cycles through the list of pieces and logs all legal moves to their move pool.
    get_player_turn - Used to get the color of the current player who can move.
    set_player_turn - Sets the player turn to the opposite color.
    get_game_state - Get the current state of the game.
    set_game_state - Changes the state of the game.
    make_move - Moves a piece from a selected start location to a legal end location.
    verify_move_in_board_range - References if the selected move is a location within _board
    general_in_danger - check for any locations that the general can put itself in check
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

        # Player dictionaries/sets for important piece data.
        self._red_pieces_information = {}
        self._black_pieces_information = {}

        # START OF GAME. Red goes first.
        # self._player_turn = 'black'
        # Options are RED_WON, BLACK_WON, STALE_MATE, or UNFINISHED
        self._game_state = 'UNFINISHED'

        # Loads initial game pieces and adds them to the player dictionaries.
        self._active_pieces = NewGame()
        self.update_move_pool(self._active_pieces)

    def pull_piece_information(self, piece_list):
        """
    Update the player dictionaries with active pieces and displays name, player, location, and potential legal moves.
    :param piece_list: Hidden list of Object pieces.
    """
        # Update red dictionary
        self._red_pieces_information = {}
        self._black_pieces_information = {}
        red_count = 1
        black_count = 1
        for i in piece_list:
            if i.get_player() == 'red':
                self._red_pieces_information[red_count] = ["Name: " + str(i.get_piece_name()),
                                                           "player: " + str(i.get_player()),
                                                           "location: " + str(i.get_piece_location()),
                                                           "Moves: " + str(i.get_legal_moves())]
                red_count += 1
            else:
                self._black_pieces_information[black_count] = ["Name: " + str(i.get_piece_name()),
                                                               "player: " + str(i.get_player()),
                                                               "location: " + str(i.get_piece_location()),
                                                               "Moves: " + str(i.get_legal_moves())]
                black_count += 1

    def get_active_pieces(self):
        return self._active_pieces

    def get_piece_data(self):
        """
    Prints red_pieces_information and black_pieces_information to screen.
    """
        print(self.give_general_check_status(self.get_active_pieces()))
        print()
        pprint.pprint(self._red_pieces_information)
        print()
        pprint.pprint(self._black_pieces_information)

    def update_move_pool(self, pieces):
        """
    Takes in a piece object and updates its potential move pool.
    :param pieces: The piece to check for legal moves.
    """
        for i in pieces:
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

        self.update_general_pools(pieces)

        self.general_cant_move_here(pieces)
        self.is_general_in_check(pieces)

        self.pull_piece_information(self._active_pieces)
        return

    def update_general_pools(self, pieces):
        for i in pieces:
            if i.get_piece_name() == 'GENERAL':
                piece = i
                i.general_legal_moves(piece, self._board, self._active_pieces)

    # def set_player_turn(self):
    #     """
    #     Change the current players turn.
    #     """
    #     if self._player_turn == 'red':
    #         self._player_turn = 'black'
    #     else:
    #         self._player_turn = 'red'

    # def get_player_turn(self):
    #     """
    #     :return: Current players turn
    #     """
    #     return self._player_turn

    def set_game_state(self, state):
        """
        Sets the game state to the selected state UNFINISHED, RED_WON, BLACK_WON, STALEMATE
        :param state: State to input
        """
        if state == 'UNFINISHED' or state == 'RED_WON' or state == 'BLACK_WON' or state == 'STALEMATE':
            self._game_state = state
        else:
            return False

    def get_game_state(self):
        """
        :return: The current state.
        """
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
        piece_2 = None # piece is None unless there is a piece in end location

        # Check what game state is.
        if self.get_game_state() != 'UNFINISHED':
            return self._game_state

        if start == end:  # Prevents movement to the same space
            return False

        # Verify start and end are within the board
        if self.verify_move_in_board_range(start) and self.verify_move_in_board_range(end):

            # Find the piece located in start
            for i in self._active_pieces:
                if i.get_piece_location() == start:
                    piece = i
                    break

            # Check to see that a piece is actually selected.

            # or piece.get_player() != self.get_player_turn()
            if piece is None or end not in piece.get_legal_moves():
                return False

            # Check if there is piece at the end location.
            for j in self._active_pieces:
                if j != piece:
                    if j.get_piece_location() == end:
                        piece_2 = j
                        break

            # If there is a piece in end and it is an enemy piece take the piece location and move,
            # otherwise return False.
            if piece_2 is not None:
                if piece_2.get_player() != piece.get_player():
                    self._active_pieces.remove(piece_2)
                    piece.set_current_location(end)
                    self.update_move_pool(self._active_pieces)
                    # self.set_player_turn()
                    return True
                else:
                    return False

            # If there is no piece in the current location and it is a legal move, move the piece.
            else:
                piece.set_current_location(end)
                self.update_move_pool(self._active_pieces)
                # self.set_player_turn()
                return True
        else:
            return False

    def verify_move_in_board_range(self, location):
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

    def give_general_check_status(self, piece_list):
        for i in piece_list:
            if i.get_piece_name() == 'GENERAL':
               print(str(i.get_player()) + str(i.get_in_check()))

    def general_cant_move_here(self, piece_list):
        for i in piece_list:
            if i.get_player() == 'red' and i.get_piece_name() == 'GENERAL':
                red_general = i
            elif i.get_player() == 'black' and i.get_piece_name() == 'GENERAL':
                black_general = i

        for j in piece_list:
            if j.get_player() == 'black':
                for k in j.get_legal_moves():
                    if k in red_general.get_legal_moves():
                        red_general.delete_move(k)

        for m in piece_list:
            if m.get_player() == 'red':
                for n in m.get_legal_moves():
                    if n in black_general.get_legal_moves():
                        black_general.delete_move(n)

    def is_general_in_check(self, piece_list):
        for i in piece_list:
            if i.get_player() == 'red' and i.get_piece_name() == 'GENERAL':
                red_general = i
            elif i.get_player() == 'black' and i.get_piece_name() == 'GENERAL':
                black_general = i

        red_general.set_in_check(False)
        black_general.set_in_check(False)

        black_moves = set()
        red_moves = set()
        for j in piece_list:
            if j.get_piece_name() != 'GENERAL':
                if j.get_player() == 'black':
                    for k in j.get_legal_moves():
                        black_moves.add(k)
                elif j.get_player() == 'red':
                    for k in j.get_legal_moves():
                        red_moves.add(k)

        if red_general.get_piece_location() in black_moves:
            red_general.set_in_check(True)
        else:
            red_general.set_in_check(False)
        if black_general.get_piece_location() in red_moves:
            black_general.set_in_check(True)
        else:
            black_general.set_in_check(False)

# GAME PIECES
class Pieces:
    """
  Major methods of game pieces.

  :items:
  _current_location - Stored alphanumerical reference to the pieces current location on the board.
  _legal_moves - List of all possible moves a piece can make.
  _player - Player color that owns a particular piece.
  _name - Name of the piece.

  :methods:
  get_player - Returns color of player who owns the piece.
  set_player - Sets the ownership color of the piece.
  get_piece_name - Returns the name of the piece.
  get_piece_location - Returns the current location of a piece.
  set_current_location - Adds the selected location to the pieces current location.
  get_legal_moves - Returns the pool of legal moves of a piece.
  clear_piece_move_pool - Empties the move pool of a particular piece.
  add_move_to_pool - Adds a legal move to the pieces move pool.
  delete_move - Removes a selected move from a pieces legal move pool.
  get_indexes_of_location - Get the numerical indexes of a location from the board.
  verify_if_potential_piece - Checks to see if a selected location is the location of a piece.
  potential_movement - Checks to see if a selected location is possible for the current piece.
  general_and_advisor_movement_pool_check - Ensures that the advisors and general can only select legal movements
                                            from the correct pool.
  """

    def __init__(self):
        self._current_location = None
        self._legal_moves = []
        self._player = None
        self._name = None

    def set_player(self, player):
        """Set piece to color of player"""
        self._player = player

    def get_player(self):
        """Gets player color of who owns a piece."""
        return self._player

    def get_piece_name(self):
        """Get the name of the piece."""
        return self._name

    def set_current_location(self, location):
        """Changes a pieces current location to the selected location."""
        self._current_location = location

    def get_piece_location(self):
        """Get alpha numeric location of piece."""
        return self._current_location

    def get_legal_moves(self):
        """Get the current pool of legal moves that a piece can move to."""
        return self._legal_moves

    def clear_piece_move_pool(self):
        """Resets current move pool to zero."""
        self._legal_moves = []

    def add_move_to_pool(self, move):
        """Add a selected alpha numeric location to the pieces move pool."""
        self._legal_moves.append(move)

    def delete_move(self, move):
        """Deletes the selected move from the move pool."""
        self._legal_moves.remove(move)

    def get_indexes_of_location(self, piece, board):
        """
        Returns the index values of the piece on the board.
        :param piece: The alphanumerical piece location.
        :param board: The reference board.
        :return: The index number of the column and the index number of the row.
        """
        for i in board:
            for t in i:
                if piece.get_piece_location() == t:
                    index_column = i.index(t)
                    index_row = board.index(i)
        return index_column, index_row

    def verify_if_potential_piece(self, location, piece_list):
        """
        Checks if there is a piece from the list in the current location
        location - the alphanumeric area of the board
        piece_list - list of current active pieces
        """
        potential_piece = None
        for i in piece_list:
            if i.get_piece_location() == location:
                potential_piece = i
                break
        return potential_piece

    def potential_movement(self, index_row, index_column, row, column, board):
        """
        Checks to see if the desired movement is possible.
        :param index_row: The index of the row of the current piece.
        :param index_column: The index of the column of the current piece.
        :param row: The + or - offset of the row that a piece wants to move.
        :param column: The + or - offset of the column that a piece wants to move.
        :param board: The board for reference of a legal move.
        :return: Either none or the alphanumeric location of the move on the board.
        """
        if (index_row + row) in range(0, 10) and (index_column + column) in range(0, 10):
            move = board[index_row + row][index_column + column]
            return move
        else:
            return None

    def general_and_advisor_movement_pool_check(self, piece):
        """
        Movement pool used for GENERAL and ADVISOR as they must stay in the 'castle'
        :param piece: Piece to check for player ownership
        :return: move_pool of the selected piece
        """
        if piece.get_player() == 'red':
            move_pool = ['d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3']
        else:
            move_pool = ['d8', 'd9', 'd10', 'e8', 'e9', 'e10', 'f8', 'f9', 'f10']
        return move_pool


class General(Pieces):
    """
  The General is the King of the pieces. This is the piece that the enemy team must try and capture. This class will
  contain the data the General needs to update it's move pool.
  Generals can only move in the confines of the castle, in any direction orthoganally.
  """

    def __init__(self):
        super().__init__()
        self._name = 'GENERAL'
        self._in_check = False

    def set_in_check(self, status):
        self._in_check = status

    def get_in_check(self):
        return self._in_check

    def general_legal_moves(self, piece, board, piece_list):
        """
    Will check the board for all of the General's legal moves and add them to the reference pool
    :param piece: Piece to update move pool for.
    :param board: Reference of the board.
    :param piece_list: The list of current active pieces for reference.
    """
        piece.clear_piece_move_pool()  # Clear move pool.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_indexes_of_location(piece, board)
        # Picks correct move pool for the given General piece
        movement_pool = self.general_and_advisor_movement_pool_check(piece)

        # General can move only orthogonally. This will add each legal orthogonal move to the legal move pool.
        try:
            # Upward one row of the board, same column.
            position = self.potential_movement(index_row, index_column, -1, 0, board)
            if position in movement_pool and self.verify_if_potential_piece(position, piece_list) is None:
                piece.add_move_to_pool(position)
            elif position in movement_pool and self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(position)
        except:
            pass
        try:
            # Down one row of the board, same column.
            position = self.potential_movement(index_row, index_column, +1, 0, board)
            if position in movement_pool and self.verify_if_potential_piece(position, piece_list) is None:
                piece.add_move_to_pool(position)
            elif position in movement_pool and self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(position)
        except:
            pass
        try:
            # Left one column on the board, same row.
            position = self.potential_movement(index_row, index_column, 0, -1, board)
            if position in movement_pool and self.verify_if_potential_piece(position, piece_list) is None:
                piece.add_move_to_pool(position)
            elif position in movement_pool and self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(position)
        except:
            pass
        try:
            # Right one column of the board, same row.
            position = self.potential_movement(index_row, index_column, 0, +1, board)
            if position in movement_pool and self.verify_if_potential_piece(position, piece_list) is None:
                piece.add_move_to_pool(position)
            elif position in movement_pool and self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(position)
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

        piece.clear_piece_move_pool()  # Clear move pool.

        # Each General can not leave a specific square. This is all the potential moves that a General could make in the
        # confines of the square.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_indexes_of_location(piece, board)

        # Advisor can move only diagonally in one direction.
        movement_pool = self.general_and_advisor_movement_pool_check(piece)

        # This will add each legal diagonal move to the legal move pool.
        try:
            # Up left
            position = self.potential_movement(index_row, index_column, -1, -1, board)
            if position in movement_pool and self.verify_if_potential_piece(position, piece_list) is None:
                piece.add_move_to_pool(position)
            elif position in movement_pool and self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(position)
        except:
            pass
        try:
            # Up right
            position = self.potential_movement(index_row, index_column, -1, +1, board)
            if position in movement_pool and self.verify_if_potential_piece(position, piece_list) is None:
                piece.add_move_to_pool(position)
            elif position in movement_pool and self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(position)
        except:
            pass
        try:
            # Down left
            position = self.potential_movement(index_row, index_column, +1, -1, board)
            if position in movement_pool and self.verify_if_potential_piece(position, piece_list) is None:
                piece.add_move_to_pool(position)
            elif position in movement_pool and self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(position)
        except:
            pass
        try:
            # Down right
            position = self.potential_movement(index_row, index_column, +1, +1, board)
            if position in movement_pool and self.verify_if_potential_piece(position, piece_list) is None:
                piece.add_move_to_pool(position)
            elif position in movement_pool and self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                piece.add_move_to_pool(position)
        except:
            pass


class Elephant(Pieces):

    def __init__(self):
        super().__init__()
        self._name = 'ELEPHANT'

    def elephant_legal_moves(self, piece, board, piece_list):

        piece.clear_piece_move_pool()  # Clear move pool.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_indexes_of_location(piece, board)

        # Up left
        try:
            position = self.potential_movement(index_row, index_column, -1, -1, board)
            if self.verify_if_potential_piece(position, piece_list) is None and position is not None:
                position = self.potential_movement(index_row, index_column, -2, -2, board)
                if self.verify_if_potential_piece(position, piece_list) is None or self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position)
        except:
            pass
        # Up - right
        try:
            position = self.potential_movement(index_row, index_column, -1, +1, board)
            if self.verify_if_potential_piece(position, piece_list) is None and position is not None:
                position = self.potential_movement(index_row, index_column, -2, +2, board)
                if self.verify_if_potential_piece(position, piece_list) is None or self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position)
        except:
            pass

        # Down - left
        try:
            position = self.potential_movement(index_row, index_column, +1, -1, board)
            if self.verify_if_potential_piece(position, piece_list) is None and position is not None:
                position = self.potential_movement(index_row, index_column, +2, -2, board)
                if self.verify_if_potential_piece(position, piece_list) is None or self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position)
        except:
            pass

        # Down - right
        try:
            position = self.potential_movement(index_row, index_column, +1, +1, board)
            if self.verify_if_potential_piece(position, piece_list) is None and position is not None:
                position = self.potential_movement(index_row, index_column, +2, +2, board)
                if self.verify_if_potential_piece(position, piece_list) is None or self.verify_if_potential_piece(position, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position)
        except:
            pass


class Horse(Pieces):

    def __init__(self):
        super().__init__()
        self._name = 'HORSE'

    def horse_legal_moves(self, piece, board, piece_list):

        piece.clear_piece_move_pool()  # Clear move pool.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_indexes_of_location(piece, board)

        # Check on the Horse legal moves

        # Left - up (left 2 up 1)
        try:
            position = self.potential_movement(index_row, index_column, 0, -1, board)
            if self.verify_if_potential_piece(position, piece_list) is None and position is not None:
                #left up
                position_2 = self.potential_movement(index_row, index_column, -1, -2, board)
                #left down
                position_3 = self.potential_movement(index_row, index_column, +1, -2, board)
                if self.verify_if_potential_piece(position_2, piece_list) is None or self.verify_if_potential_piece(position_2, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position_2)
                if self.verify_if_potential_piece(position_3, piece_list) is None or self.verify_if_potential_piece(position_3, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position_3)
        except:
            pass

        # Up - left (up 2 left 1)
        try:
            position = self.potential_movement(index_row, index_column, -1, 0, board)
            if self.verify_if_potential_piece(position, piece_list) is None and position is not None:
                # up left
                position_2 = self.potential_movement(index_row, index_column, -2, -1, board)
                # up right
                position_3 = self.potential_movement(index_row, index_column, -2, +1, board)
                if self.verify_if_potential_piece(position_2, piece_list) is None or self.verify_if_potential_piece(position_2, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position_2)
                if self.verify_if_potential_piece(position_3, piece_list) is None or self.verify_if_potential_piece(position_3, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position_3)
        except:
            pass
        # right - up (right 2 up 1)
        try:
            position = self.potential_movement(index_row, index_column, 0, +1, board)
            if self.verify_if_potential_piece(position, piece_list) is None and position is not None:
                # right up
                position_2 = self.potential_movement(index_row, index_column, -1, +2, board)
                # right down
                position_3 = self.potential_movement(index_row, index_column, +1, +2, board)
                if self.verify_if_potential_piece(position_2, piece_list) is None or self.verify_if_potential_piece(position_2, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position_2)
                if self.verify_if_potential_piece(position_3, piece_list) is None or self.verify_if_potential_piece(position_3, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position_3)
        except:
            pass
        # down - left (down 2 left 1)
        try:
            position = self.potential_movement(index_row, index_column, +1, 0, board)
            if self.verify_if_potential_piece(position, piece_list) is None and position is not None:
                # down left
                position_2 = self.potential_movement(index_row, index_column, +2, -1, board)
                # down right
                position_3 = self.potential_movement(index_row, index_column, +2, +1, board)
                if self.verify_if_potential_piece(position_2, piece_list) is None or self.verify_if_potential_piece(position_2, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position_2)
                if self.verify_if_potential_piece(position_3, piece_list) is None or self.verify_if_potential_piece(position_3, piece_list).get_player() != piece.get_player():
                    piece.add_move_to_pool(position_3)
        except:
            pass


class Chariot(Pieces):

    def __init__(self):
        super().__init__()
        self._name = 'CHARIOT'

    def chariot_legal_moves(self, piece, board, piece_list):

        piece.clear_piece_move_pool()  # Clear move pool.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_indexes_of_location(piece, board)

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
        piece.clear_piece_move_pool()  # Clear move pool.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_indexes_of_location(piece, board)

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
                    jump_index_column, jump_index_row = self.get_indexes_of_location(jump_move, board)

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
                    jump_index_column, jump_index_row = self.get_indexes_of_location(jump_move, board)

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
                    jump_index_column, jump_index_row = self.get_indexes_of_location(jump_move, board)

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
                    jump_index_column, jump_index_row = self.get_indexes_of_location(jump_move, board)

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
        piece.clear_piece_move_pool()  # Clear move pool.

        # Set the index for row and column to the pieces current location for reference.
        index_column, index_row = self.get_indexes_of_location(piece, board)

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
    red_general.set_current_location('d1')
    new_game.append(red_general)

    # red_advisor_left = Advisor()
    # red_advisor_left.set_player('red')
    # red_advisor_left.set_current_location('e2')
    # new_game.append(red_advisor_left)

    # red_advisor_right = Advisor()
    # red_advisor_right.set_player('red')
    # red_advisor_right.set_current_location('f1')
    # new_game.append(red_advisor_right)

    # red_elephant_left = Elephant()
    # red_elephant_left.set_player('black')
    # red_elephant_left.set_current_location('e3')
    # new_game.append(red_elephant_left)
    #
    # red_elephant_right = Elephant()
    # red_elephant_right.set_player('red')
    # red_elephant_right.set_current_location('g5')
    # new_game.append(red_elephant_right)
    #
    # red_horse_left = Horse()
    # red_horse_left.set_player('red')
    # red_horse_left.set_current_location('b1')
    # new_game.append(red_horse_left)
    #
    # red_horse_right = Horse()
    # red_horse_right.set_player('red')
    # red_horse_right.set_current_location('h1')
    # new_game.append(red_horse_right)
    #
    # red_chariot_right = Chariot()
    # red_chariot_right.set_player('red')
    # red_chariot_right.set_current_location('i1')
    # new_game.append(red_chariot_right)
    #
    # red_chariot_left = Chariot()
    # red_chariot_left.set_player('red')
    # red_chariot_left.set_current_location('a1')
    # new_game.append(red_chariot_left)
    #
    # red_cannon_right = Cannon()
    # red_cannon_right.set_player('red')
    # red_cannon_right.set_current_location('b3')
    # new_game.append(red_cannon_right)
    #
    # red_cannon_left = Cannon()
    # red_cannon_left.set_player('red')
    # red_cannon_left.set_current_location('h3')
    # new_game.append(red_cannon_left)
    #
    # red_soldier_one = Soldier()
    # red_soldier_one.set_player('red')
    # red_soldier_one.set_current_location('a4')
    # new_game.append(red_soldier_one)
    #
    # red_soldier_two = Soldier()
    # red_soldier_two.set_player('red')
    # red_soldier_two.set_current_location('c4')
    # new_game.append(red_soldier_two)
    #
    # red_soldier_three = Soldier()
    # red_soldier_three.set_player('red')
    # red_soldier_three.set_current_location('e4')
    # new_game.append(red_soldier_three)
    #
    # red_soldier_four = Soldier()
    # red_soldier_four.set_player('red')
    # red_soldier_four.set_current_location('g4')
    # new_game.append(red_soldier_four)
    #
    # red_soldier_five = Soldier()
    # red_soldier_five.set_player('red')
    # red_soldier_five.set_current_location('i4')
    # new_game.append(red_soldier_five)

    # BLACK SIDE
    black_general = General()
    black_general.set_player('black')
    black_general.set_current_location('e10')
    new_game.append(black_general)
    #
    # black_advisor_left = Advisor()
    # black_advisor_left.set_player('black')
    # black_advisor_left.set_current_location('d10')
    # new_game.append(black_advisor_left)
    #
    # black_advisor_right = Advisor()
    # black_advisor_right.set_player('black')
    # black_advisor_right.set_current_location('f10')
    # new_game.append(black_advisor_right)

    # black_elephant_left = Elephant()
    # black_elephant_left.set_player('black')
    # black_elephant_left.set_current_location('e10')
    # new_game.append(black_elephant_left)
    #
    # black_elephant_right = Elephant()
    # black_elephant_right.set_player('black')
    # black_elephant_right.set_current_location('g10')
    # new_game.append(black_elephant_right)
    #
    # black_horse_left = Horse()
    # black_horse_left.set_player('black')
    # black_horse_left.set_current_location('d5')
    # new_game.append(black_horse_left)
    #
    # black_horse_right = Horse()
    # black_horse_right.set_player('black')
    # black_horse_right.set_current_location('h10')
    # new_game.append(black_horse_right)
    #
    black_chariot_right = Chariot()
    black_chariot_right.set_player('black')
    black_chariot_right.set_current_location('e9')
    new_game.append(black_chariot_right)

    black_chariot_right = Chariot()
    black_chariot_right.set_player('black')
    black_chariot_right.set_current_location('f9')
    new_game.append(black_chariot_right)

    # black_cannon_right = Cannon()
    # black_cannon_right.set_player('black')
    # black_cannon_right.set_current_location('b8')
    # new_game.append(black_cannon_right)
    #
    # black_cannon_left = Cannon()
    # black_cannon_left.set_player('black')
    # black_cannon_left.set_current_location('h8')
    # new_game.append(black_cannon_left)
    #
    # black_soldier_one = Soldier()
    # black_soldier_one.set_player('black')
    # black_soldier_one.set_current_location('a7')
    # new_game.append(black_soldier_one)
    #
    # black_soldier_two = Soldier()
    # black_soldier_two.set_player('black')
    # black_soldier_two.set_current_location('c7')
    # new_game.append(black_soldier_two)
    #
    # black_soldier_three = Soldier()
    # black_soldier_three.set_player('black')
    # black_soldier_three.set_current_location('e7')
    # new_game.append(black_soldier_three)
    #
    # black_soldier_four = Soldier()
    # black_soldier_four.set_player('black')
    # black_soldier_four.set_current_location('d2')
    # new_game.append(black_soldier_four)
    #
    # black_soldier_five = Soldier()
    # black_soldier_five.set_player('black')
    # black_soldier_five.set_current_location('i7')
    # new_game.append(black_soldier_five)

    return new_game


# TESTING PURPOSES
xi = Xiangqi()
xi.make_move('e9', 'd9')
print()
xi.make_move('d1', 'e1')
print()
# xi.make_move('c6', 'e4')
# print()
# xi.get_piece_data()
# xi.make_move('e4', 'c2')
# print()
# xi.get_piece_data()
