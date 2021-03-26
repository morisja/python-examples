#!/usr/bin/python3
import enum
import sys
from collections import namedtuple
import unittest
import random
import string


class GameStatus(enum.Enum):
    playon = 0
    draw = 1
    complete = 2


GameState = namedtuple("GameState", ["GameStatus", "winner"])
GameMove = namedtuple("GameMove", ["x", "y", "mark"])


class TTTException(Exception):
    pass


class IncorrectPlayerException(TTTException):
    def __init__(self):
        self.message = "Not players turn"


class InvalidMoveException(TTTException):
    def __init__(self, reason):
        self.message = f"Move not valid {reason}"

class TicTacToe:

    def __init__(self, board_state=None, next_player="x", game_id="".join(random.choice(string.ascii_lowercase) for i in range(10))):
        self._game_id = game_id

        if not board_state:
            self.board = []
            for n in range(0, 3):
                self.board.append([None, None, None])
        else:
            self.board = board_state

        self.history = []
        self.next_player = next_player
        self.game_status = GameStatus.playon
        self.winner = None

    @property
    def game_id(self):
        return self._game_id

    def get_square(self, x: int, y: int) -> str:
        return self.board[x][y] if self.board[x][y] else " "

    def get_next_player(self) -> str:
        return self.next_player

    def get_game_state(self) -> GameState:
        return GameState(self.game_status, self.winner)

    def draw_map(self) -> str:
        a = []
        a.append("+---+---+---+")
        for x in range(0, 3):
            a.append("+{},1+{},2+{},3+".format(x, x, x))
            a.append("+---+---+---+")
        return "\n".join(a)

    def __str__(self) -> str:
        a = []
        a.append("+---+---+---+")
        for x in range(0, 3):
            a.append("+ {} + {} + {} +".format(self.get_square(x, 0),
                     self.get_square(x, 1), self.get_square(x, 2)))
            a.append("+---+---+---+")
        return "\n".join(a)

    def square_is_empty(self, x: int, y: int):
        return not self.board[x][y]

    def play_move(self, x: int, y: int, mark: str) -> GameState:
        if mark != self.next_player:
            raise IncorrectPlayerException()
        if not self.square_is_empty(x, y):
            raise InvalidMoveException("Square occupied")
        self.board[x][y] = mark
        self.history.append(GameMove(x,y,mark))
        if mark == "x":
            self.next_player = "o"
        else:
            self.next_player = "x"
        return self.eval_game(mark)

    @staticmethod
    def _transpose_board(board):
        return [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]

    def eval_game(self, mark) -> GameState:
        if self.is_row_filled(self.board) or self.is_row_filled(self._transpose_board(self.board)) or self.is_diag_filled(self.board):
            self.winner = mark
            self.game_status = GameStatus.complete
        if self.is_board_full():
            self.game_status = GameStatus.draw
        return self.get_game_state()

    def is_board_full(self):
        count = 0
        for x in range(0, 3):
            for y in range(0, 3):
                if self.board[x][y]:
                    count += 1
        if count == (3*3):
            return True

    def list_empty(self):
        empty=[]
        for x in range(0, 3):
            for y in range(0, 3):
                if not self.board[x][y]:
                    empty.append( (x,y))
        return empty

    def is_row_filled(self, board):
        for x in range(0, 3):
            marks = set()
            [marks.add(m) for m in board[x]]
            if len(marks) == 1 and None not in marks:
                return True

    def is_diag_filled(self, board):
        diag1 = [board[0][0], board[1][1], board[2][2]]
        diag2 = [board[0][2], board[1][1], board[2][0]]
        marks = set()
        [marks.add(m) for m in diag1]
        if all(diag1) and len(marks) == 1:
            return True
        marks = set()
        [marks.add(m) for m in diag2]
        if all(diag2) and len(marks) == 1:
            return True

    def get_history(self):
        return self.history

class TestSum(unittest.TestCase):

    def test_row(self):
        data = [["x", "x", "x"],
                [None, None, None],
                [None, None, None]]
        t = TicTacToe()
        self.assertTrue(t.is_row_filled(data))

    def test_col(self):
        data = [["x", None, None],
                ["x", None, None],
                ["x", None, None]]
        t = TicTacToe()
        self.assertTrue(t.is_row_filled(t._transpose_board(data)))

    def test_diag(self):
        data = [[None, None, "x"],
                [None, "x", None],
                ["x", None, None]]
        t = TicTacToe()
        self.assertTrue(t.is_diag_filled(data))

    def test_game(self):
        t = TicTacToe()
        t.play_move(0, 0, "x")
        t.play_move(0, 1, "o")

        t.play_move(1, 1, "x")
        t.play_move(0, 2, "o")
        res = t.play_move(2, 2, "x")
        self.assertEqual(res.winner, "x")




def play_a_game():
    t = TicTacToe()
    print(t.game_id)
    t.play_move(0, 0, "x")
    t.play_move(0, 1, "o")

    t.play_move(1, 1, "x")
    t.play_move(0, 2, "o")
    print(t.get_history())
    print(t.list_empty())

play_a_game()

unittest.main()

# t.play_move(2,2,"x")
#import pdb
# pdb.set_trace()
