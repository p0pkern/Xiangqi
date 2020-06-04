# Author: Chris Peterman
# Version: 0.0
# Name: Xiangqi Game

#Modules
import pprint

class Xiangqi():

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

    # Storage for red and black players for data access
    self._board_dict_red = {}
    self._board_dict_black = {}

    # START OF GAME
    self._player_turn = 'red'
    # Options are RED_WON, BLACK_WON, STALE_MATE
    self._game_state = 'UNFINISHED' 

    # Initialize Game Pieces
    self._active_pieces = NewGame()
    self.update_dict_red(self._active_pieces)
    self.update_dict_black(self._active_pieces)
  
  # Update dictionary data for red
  def update_dict_red(self, pieces):
    self._board_dict_red = {}
    count = 1
    for i in self._active_pieces:
      if i.get_player() == 'red':
       self._board_dict_red[count] = ["Name: " + str(i.get_piece_name()), "player: " + str(i.get_player()), "location: " + str(i.get_piece_location()), "Moves: " + str(i.get_legal_moves())]
       count += 1

  # Update dictionary data for black
  def update_dict_black(self, pieces):
    self._board_dict_black = {}
    count_2 = 1
    for i in self._active_pieces:
      if i.get_player() == 'black':
       self._board_dict_black[count_2] = ["Name: " + str(i.get_piece_name()), "player: " + str(i.get_player()), "location: " + str(i.get_piece_location()), "Moves: " + str(i.get_legal_moves())]
       count_2 += 1

  # Print piece information from dictionary 
  def get_piece_data(self):
    pprint.pprint(self._board_dict_red)
    print()
    pprint.pprint(self._board_dict_black)

  # Print board layout
  def get_board(self):
    for i in self._board:
      print(i)

  # PLAYER TURN FUNCTIONS
  def set_player_turn(self):
    if self._player_turn == 'red':
      self._player_turn = 'black'
    else:
      self._player_turn = 'red'
    return True
  
  # Move a piece
  def make_move(self, start, end):
    piece = None
    block = False
    attack = False
    if start == end:
      return False
    if self.legal_location_check(start) and self.legal_location_check(end):
      for i in self._active_pieces:
        if i.get_piece_location() == start:
          piece = i
      if piece is None:
        return False
      for t in self._active_pieces:
        for j in self._active_pieces:
          if j != piece:
            if j.get_piece_location() == end:
              piece_2 = j
              attack = True
              block = True
              break
        if block is True:
          if attack is True:
            self._active_pieces.remove(piece_2)
            piece.move_piece(end)
            self.update_dict_red(self._active_pieces)
            self.update_dict_black(self._active_pieces)
            # legal_move_check()
            return True
          else:
            return False
        else:
          piece.move_piece(end)
          self.update_dict_red(self._active_pieces)
          self.update_dict_black(self._active_pieces)
      else:
        return False
    else:
      return False

  # PLAYER MOVEMENTS
  def legal_location_check(self, location):
    in_bounds = False
    for i in self._board:
      if location in i:
        in_bounds = True
        break
    return in_bounds

  # DEBUGGING
  def get_active_pieces(self):
    return self._active_pieces

# GAME PIECES

# Common functions for each piece
class Pieces():
  """
  Common functions for all game pieces
  """
  def __init__(self):
    self._current_location = None
    self._legal_moves = []
    self._player = None
    self._name = None
  
  # PLAYER POSSESSION FUNCTIONS

  # Return current player value
  def get_player(self):
    return self._player

  # Set current player value
  def set_player(self, player):
    self._player = player

  # Get name of piece
  def get_piece_name(self):
    return self._name

  # Get piece location
  def get_piece_location(self):
    return self._current_location

  # Get legal moves pool
  def get_legal_moves(self):
    return self._legal_moves
 
  # Adds legal moves to a move pool list.
  def set_legal_moves(self, location):
    if location not in self._legal_moves:
      if Xiangqi.legal_location_check(location):
        self._legal_moves.append(location)
    else:
      return False

  # Moves the piece, clears out legal moves, and checks for any
  # legal moves. If so it adds them to the legal move pool
  def move_piece(self, location):
    self._current_location = location
    self._legal_moves = []
    #TODO Put in function to check all legal moves

# INDIVIDUAL PIECES
class General(Pieces):

  def __init__(self):
    super().__init__()
    self._name = 'GENERAL'

  def add_legal_moves(self):
    pass

def legal_move_check(self):
   #TODO checks to see if any moves are legal for the General within parameters
   pass
  # if name == 'GENERAL':
  #   General.add_legal_moves()
  # else:
  #   return False
  # pass


def NewGame():

  new_game = []
  
  # RED SIDE
  red_general = General()
  red_general.set_player('red')
  red_general.move_piece('e1')
  new_game.append(red_general)

  # BLACK SIDE
  black_general = General()
  black_general.set_player('black')
  black_general.move_piece('d1')
  new_game.append(black_general)

  return new_game

    
xi = Xiangqi()
xi.get_piece_data()
print(xi.make_move('e1','c1'))
print()
xi.get_piece_data()
print(xi.make_move('d1', 'c1'))
xi.get_piece_data()
