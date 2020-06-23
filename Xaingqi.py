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
    self._board = [["a1","b1","c1","d1","e1","f1","g1","h1","i1"],
                   ["a2","b2","c2","d2","e2","f2","g2","h2","i2"],
                   ["a3","b3","c3","d3","e3","f3","g3","h3","i3"],
                   ["a4","b4","c4","d4","e4","f4","g4","h4","i4"],
                   ["a5","b5","c5","d5","e5","f5","g5","h5","i5"],
                   #################  RIVER  #####################
                   ["a6","b6","c6","d6","e6","f6","g6","h6","i6"],
                   ["a7","b7","c7","d7","e7","f7","g7","h7","i7"],
                   ["a8","b8","c8","d8","e8","f8","g8","h8","i8"],
                   ["a9","b9","c9","d9","e9","f9","g9","h9","i9"],
                ["a10","b10","c10","d10","e10","f10","g10","h10","i10"]]
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
      if i.get_piece_name() == 'GENERAL':
        i.general_legal_moves(piece, self._board, self._active_pieces)
      elif i.get_piece_name() == 'ADVISOR':
        i.advisor_legal_moves(piece, self._board, self._active_pieces)
      elif i.get_piece_name() == 'ELEPHANT':
        i.elephant_legal_moves(piece, self._board, self._active_pieces)
      elif i.get_piece_name() == 'HORSE':
        i.horse_legal_moves(piece, self._board, self._active_pieces)

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

  def make_move(self, start, end):
    """
    Move a piece selected from a start location, written in alphanumberic a1 - i10, to an end location. Make move will
    check if the move is legal and make the move if all conditions are met.
    :param start: The selected piece, if a blank piece is chosen will return False.
    :param end: The place where a selected piece wants to move, will move there and capture a piece if it is a legal move.
    :return: True if successful of False if unsuccessful.
    """
    # Starting variables.
    piece = None  # piece is None until a start with a piece in it is selected.
    block = False  # block is False unless there is any piece in an end.
    attack = False  # attack is False unless a blocked piece is the opposing side.

    if start == end:  # Prevents movement to the same space
     return False

    # Check what game state is.
    # TODO - Add stuff to check what the current game state is.

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

      # If there is a piece in end and it is an enemy piece take the piece location and move, otherwise return False.
      if block is True:
        if attack is True:
          self._active_pieces.remove(piece_2)
          piece.move_piece(end)
          self.update_move_pool(self._active_pieces)
          return True
        else:
          return False

      # If there is no piece in the current location and it is a legal move, move the piece.
      else:
        piece.move_piece(end)
        self.update_move_pool(self._active_pieces)
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

  def get_index_of_location(self, piece, board):
    index_column = None
    index_row = None
    for i in board:
      for t in i:
       if piece.get_piece_location() == t:
         index_column = i.index(t)
         index_row = board.index(i)
    return index_column, index_row

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
    color = piece.get_player()  # Set to current player.
    piece.clear_pool()  # Clear move pool.

    # Each General can not leave a specific square. This is all the potential moves that a General could make in the
    # confines of the square.
    if color == 'red':
      move_pool_1 = ['d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3']
    elif color == 'black':
      move_pool_2 = ['d8', 'd9', 'd10', 'e8', 'e9', 'e10', 'f8', 'f9', 'f10']

    # Set the index for row and column to the pieces current location for reference.
    index_column, index_row = self.get_index_of_location(piece, board)

    # General can move only orthogonally. This will add each legal orthogonal move to the legal move pool.
    try:
      # Upward one row of the board, same column.
      if color == 'red':
        if board[index_row - 1][index_column] in move_pool_1:
          piece.add_move_to_pool(board[index_row - 1][index_column])
      elif color == 'black':
        if board[index_row - 1][index_column] in move_pool_2:
          piece.add_move_to_pool(board[index_row - 1][index_column])
    except:
      pass
    try:
      # Down one row of the board, same column.
      if color == 'red':
        if board[index_row + 1][index_column] in move_pool_1:
          piece.add_move_to_pool(board[index_row + 1][index_column])
      elif color == 'black':
        if board[index_row + 1][index_column] in move_pool_2:
          piece.add_move_to_pool(board[index_row + 1][index_column])
    except:
      pass
    try:
      # Left one column on the board, same row.
      if color == 'red':
        if board[index_row][index_column - 1] in move_pool_1:
          piece.add_move_to_pool(board[index_row][index_column - 1])
      elif color == 'black':
        if board[index_row][index_column - 1] in move_pool_2:
          piece.add_move_to_pool(board[index_row][index_column - 1])
    except:
      pass
    try:
      # Right one column of the board, same row.
      if color == 'red':
        if board[index_row][index_column + 1] in move_pool_1:
          piece.add_move_to_pool(board[index_row][index_column + 1])
      elif color == 'black':
        if board[index_row][index_column + 1] in move_pool_2:
          piece.add_move_to_pool(board[index_row][index_column + 1])
    except:
      pass

    for j in piece_list:
      if j.get_player() == color and j.get_piece_location() in piece.get_legal_moves():
        remove = j.get_piece_location()
        piece.delete_move(remove)
    return True

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
    if color == 'red':
      move_pool_1 = ['d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3']
    elif color == 'black':
      move_pool_2 = ['d8', 'd9', 'd10', 'e8', 'e9', 'e10', 'f8', 'f9', 'f10']

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
        remove = j.get_piece_location()
        piece.delete_move(remove)
    return True

class Elephant(Pieces):

  def __init__(self):
    super().__init__()
    self._name = 'ELEPHANT'

  def elephant_legal_moves(self, piece, board, piece_list):

    color = piece.get_player()  # Set to current player.
    piece.clear_pool()  # Clear move pool.

    # Set the index for row and column to the pieces current location for reference.
    index_column, index_row = self.get_index_of_location(piece, board)

    # Up left
    try:
      temp = False
      # Set a to the left square, then check to see if any pieces are currently in that square, illegal move.
      a = board[index_row - 1][index_column - 1]
      for i in piece_list:
        if i.get_piece_location() == a and i != piece:
          temp = True
          break
      # If there is no piece in the left square, check to see if the index of the move wraps around the board.
      if temp is not True:
        b = board[index_row - 2][index_column - 2]
        if (index_row - 2) >= 0 and (index_column - 2) >= 0:
          piece.add_move_to_pool(b)
    except:
      pass
    try:
      temp_2 = False
      # Set a to the left square, then check to see if any pieces are currently in that square.
      c = board[index_row - 1][index_column + 1]
      for i in piece_list:
        if i.get_piece_location() == c and i != piece:
          temp_2 = True
          break
      # If there is no piece in the left square, check to see if the index of the move wraps around the board.
      if temp_2 is not True:
        d = board[index_row - 2][index_column + 2]
        if (index_row - 2) >= 0 and (index_column + 2) in range(0, 10):
          piece.add_move_to_pool(d)
    except:
      pass
    try:
      temp_3 = False
      # Set a to the left square, then check to see if any pieces are currently in that square.
      e = board[index_row + 1][index_column - 1]
      for i in piece_list:
        if i.get_piece_location() == e and i != piece:
          temp_3 = True
          break
      # If there is no piece in the left square, check to see if the index of the move wraps around the board.
      if temp_3 is not True:
        f = board[index_row + 2][index_column - 2]
        if (index_row + 2) in range(0, 10) and (index_column - 2) in range(0, 10):
          piece.add_move_to_pool(f)
    except:
      pass
    try:
      temp_4 = False
      # Set a to the left square, then check to see if any pieces are currently in that square.
      g = board[index_row + 1][index_column + 1]
      for i in piece_list:
        if i.get_piece_location() == g and i != piece:
          temp_4 = True
          break
      # If there is no piece in the left square, check to see if the index of the move wraps around the board.
      if temp_4 is not True:
        h = board[index_row + 2][index_column + 2]
        if (index_row + 2) in range(0, 10) and (index_column + 2) in range(0, 10):
          piece.add_move_to_pool(h)
    except:
      pass

class Horse(Pieces):

  def __init__(self):
    super().__init__()
    self._name = 'HORSE'

  def horse_legal_moves(self, piece, board, piece_list):
    color = piece.get_player()  # Set to current player.
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
      print("broken 2")
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
      print("broken")
      pass
    # up - right (up 2 right 1)
    try:
      if up_flag is not True:
        f = board[index_row - 2][index_column + 1]
        if (index_row - 2) in range(0, 10) and (index_column + 1) in range(0, 10):
          piece.add_move_to_pool(f)
    except:
      print("broken")
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

def NewGame():
  """
  This will load all the initial pieces to the correct locations for a new game. Returns a list of all pre-loaded pieces.
  """
  new_game = []
  
  # RED SIDE
  # red_general = General()
  # red_general.set_player('red')
  # red_general.move_piece('e1')
  # new_game.append(red_general)
  #
  # red_advisor_left = Advisor()
  # red_advisor_left.set_player('red')
  # red_advisor_left.move_piece('d1')
  # new_game.append(red_advisor_left)
  #
  # red_advisor_right = Advisor()
  # red_advisor_right.set_player('red')
  # red_advisor_right.move_piece('f1')
  # new_game.append(red_advisor_right)

  red_elephant_left = Elephant()
  red_elephant_left.set_player('red')
  red_elephant_left.move_piece('g8')
  new_game.append(red_elephant_left)

  # red_elephant_right = Elephant()
  # red_elephant_right.set_player('red')
  # red_elephant_right.move_piece('g1')
  # new_game.append(red_elephant_right)

  red_horse_left = Horse()
  red_horse_left.set_player('red')
  red_horse_left.move_piece('h9')
  new_game.append(red_horse_left)

  # red_horse_right = Horse()
  # red_horse_right.set_player('red')
  # red_horse_right.move_piece('c3')
  # new_game.append(red_horse_right)


  # BLACK SIDE
  # black_general = General()
  # black_general.set_player('black')
  # black_general.move_piece('e10')
  # new_game.append(black_general)
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
  # red_elephant_left = Elephant()
  # red_elephant_left.set_player('black')
  # red_elephant_left.move_piece('a2')
  # new_game.append(red_elephant_left)
  #
  # red_elephant_right = Elephant()
  # red_elephant_right.set_player('black')
  # red_elephant_right.move_piece('g10')
  # new_game.append(red_elephant_right)
  #
  # red_horse_left = Horse()
  # red_horse_left.set_player('black')
  # red_horse_left.move_piece('b10')
  # new_game.append(red_horse_left)
  #
  # red_horse_right = Horse()
  # red_horse_right.set_player('black')
  # red_horse_right.move_piece('h10')
  # new_game.append(red_horse_right)

  return new_game

# TESTING PURPOSES
xi = Xiangqi()
xi.get_piece_data()
# xi.make_move('c3', 'a2')
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


