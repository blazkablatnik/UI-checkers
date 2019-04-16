import unittest
from checkers import Board, Utility

# TODO: what do these tests test? instead of test1, test2, ... more descriptive test names are needed


class NotationTests(unittest.TestCase):
    def test_simple(self):
        bstr = ".x.x.x.x.x,x.x.x.x.x.,,,,,,,.o.o.o.o.o,o.o.o.o.o."
        b = Board()
        b.set_board(bstr)
        self.assertEqual(bstr, b.get_board())

    def test_empty(self):
        bstr = ",,,,,,,,,"
        b = Board()
        b.set_board(bstr)
        self.assertEqual(bstr, b.get_board())

    def test_clear(self):
        bstr = ".x.x,,,,,,,,,o.o."
        b = Board()
        b.set_board(bstr)
        b.clear_board()
        self.assertEqual(",,,,,,,,,", b.get_board())

    def test_default(self):
        bstr = ".o.o.o.o.o,o.o.o.o.o.,.o.o.o.o.o,o.o.o.o.o.,,,.x.x.x.x.x,x.x.x.x.x.,.x.x.x.x.x,x.x.x.x.x."
        b = Board()
        self.assertEqual(bstr, b.get_board())

    def test_middle(self):
        # This is correct becuase implementation doesn't actually check if all checkers are on black fields only
        # (as it's per rules of checkers).
        bstr = ",,,,...xoxo...,...oxox...,,,,"
        b = Board()
        b.set_board(bstr)
        self.assertEqual(bstr, b.get_board())

    def test_trimmed1(self):
        # Notation input can be trimmed from right, however output is not.
        bstr = ".x.x,"
        b = Board()
        b.set_board(bstr)
        self.assertEqual(".x.x......,,,,,,,,,", b.get_board())

    def test_trimmed2(self):
        bstr = ",,,,...x.x.o,o.o.x"
        b = Board()
        b.set_board(bstr)
        self.assertEqual(",,,,...x.x.o..,o.o.x.....,,,,", b.get_board())


class SomeTests(unittest.TestCase):
    def test1(self):
        b = Board()
        b.set_board(",.x,,.x,,,,,........o,")
        moves = Utility().moves_to_string(b.legal_moves())
        self.assertEqual(moves, "Move[X,f(1, 1),t(0, 0)],Move[X,f(1, 1),t(0, 2)],Move[x,f(3, 1),t(2, 0)],Move[x,f(3, 1),t(2, 2)]")

    def test2(self):
        b = Board()
        b.set_board(",.o........,,.o........,,,,,........x.,")
        b.color = False
        moves = Utility().moves_to_string(b.legal_moves())
        self.assertEqual(moves, "Move[o,f(1, 1),t(2, 0)],Move[o,f(1, 1),t(2, 2)],Move[o,f(3, 1),t(4, 0)],Move[o,f(3, 1),t(4, 2)]")

    def test3(self):
        b = Board()
        b.set_board(",.o........,,.o........,,,,,,")
        moves = Utility().moves_to_string(b.legal_moves())
        self.assertEqual(moves, "")

    def test4(self):
        b = Board()
        b.set_board(",.o.o......,,..x.......,,,,,,")
        moves = Utility().moves_to_string(b.legal_moves())
        self.assertEqual(moves, "Move[x,f(3, 2),t(2, 1)],Move[x,f(3, 2),t(2, 3)]")

    def test5(self):
        b = Board()
        b.set_board(",.o.o......,..x.......,,,,,,,")
        moves = Utility().moves_to_string(b.legal_moves())
        self.assertEqual(moves, "Move[X,f(2, 2),t(0, 0)],Move[X,f(2, 2),t(0, 4)]")

    def test6(self):
        b = Board()
        b.set_board(",.o...o....,..o.o.....,...x......,,,,,,")
        moves = Utility().moves_to_string(b.legal_moves())
        self.assertEqual(moves, "")

    def test7(self):
        b = Board()
        b.set_board(",...o.o....,,...o.o....,....x.....,,,,,")
        moves = Utility().moves_to_string(b.legal_moves())
        self.assertEqual(moves, "Move[x,f(4, 4),t(2, 2)]Move[x,f(2, 2),t(0, 4)]Move[x,f(0, 4),t(2, 6)]Move[x,f(2, 6),t(4, 4)],Move[x,f(4, 4),t(2, 6)]Move[x,f(2, 6),t(0, 4)]Move[x,f(0, 4),t(2, 2)]Move[x,f(2, 2),t(4, 4)]")

    def test8(self):
        b = Board()
        b.set_board(",...o.o....,,...o......,....x.....,...o......,,,,")
        moves = Utility().moves_to_string(b.legal_moves())
        self.assertEqual(moves, "Move[x,f(4, 4),t(2, 2)]Move[x,f(2, 2),t(0, 4)]Move[x,f(0, 4),t(2, 6)]")