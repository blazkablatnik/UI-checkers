import unittest

import checkers
from checkers import Board


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


class TurnTests(unittest.TestCase):
    def test_turns(self):
        b = Board()
        self.assertTrue(b.color)
        b.legal_moves()
        self.assertTrue(b.color)
        b.legal_moves()[0]
        self.assertTrue(b.color)
        b.push(b.legal_moves()[0])
        self.assertTrue(not b.color)

    def test_turns2(self):
        b = Board()
        b.set_board(",...o.o,,...o,..x")
        self.assertTrue(b.color)
        b.legal_moves()
        self.assertTrue(b.color)
        b.legal_moves()[0]
        self.assertTrue(b.color)
        b.push(b.legal_moves()[0])
        self.assertTrue(not b.color)


class LegalMovesTests(unittest.TestCase):
    def test_move_white(self):
        b = Board()
        b.set_board(",,,,,,.x")
        self.assertEqual("[[Move<x,f(1, 6),t(0, 5)>], [Move<x,f(1, 6),t(2, 5)>]]", str(b.legal_moves()))

    def test_move_black(self):
        b = Board()
        b.set_board(",,....o")
        b.color = checkers.BLACK
        self.assertEqual("[[Move<o,f(4, 2),t(3, 3)>], [Move<o,f(4, 2),t(5, 3)>]]", str(b.legal_moves()))

    def test_jump_white(self):
        b = Board()
        b.set_board(",,....o,...x")
        self.assertEqual("[[Move<x,f(3, 3),t(5, 1)>]]", str(b.legal_moves()))
        self.assertIsNotNone(b.checker_at(4,2))

    def test_jump_black(self):
        b = Board()
        b.set_board(",,,,......x,.....o")
        b.color = checkers.BLACK
        self.assertEqual("[[Move<o,f(5, 5),t(7, 3)>]]", str(b.legal_moves()))
        self.assertIsNotNone(b.checker_at(6, 4))

    def test_double_jump(self):
        b = Board()
        b.set_board(",...o,,...o,..x")
        self.assertEqual("[[Move<x,f(2, 4),t(4, 2)>, Move<x,f(4, 2),t(2, 0)>]]", str(b.legal_moves()))
        self.assertIsNotNone(b.checker_at(3, 3))
        self.assertIsNotNone(b.checker_at(3, 1))

    def test_two_double_jumps(self):
        b = Board()
        b.set_board(",...o.o,,...o,..x")
        self.assertEqual("[[Move<x,f(2, 4),t(4, 2)>, Move<x,f(4, 2),t(2, 0)>], "
                         "[Move<x,f(2, 4),t(4, 2)>, Move<x,f(4, 2),t(6, 0)>]]", str(b.legal_moves()))
        self.assertIsNotNone(b.checker_at(3, 3))
        self.assertIsNotNone(b.checker_at(3, 1))
        self.assertIsNotNone(b.checker_at(5, 1))

    def test_longest_chain(self):
        b = Board()
        b.set_board(",...,.o.o,.....,.o...o,.......,...o...o,....x....,.o.o,...")
        self.assertEqual("[[Move<x,f(4, 7),t(2, 5)>, Move<x,f(2, 5),t(0, 3)>, "
                         "Move<x,f(0, 3),t(2, 1)>, Move<x,f(2, 1),t(4, 3)>, "
                         "Move<x,f(4, 3),t(6, 5)>, Move<x,f(6, 5),t(8, 7)>]]", str(b.legal_moves()))

    def test_complicated_circle_chain(self):
        b = Board()
        b.set_board(",.o.o.o....,,.o.o......,..x")

        ch1 = "[Move<x,f(2, 4),t(0, 2)>, Move<x,f(0, 2),t(2, 0)>, Move<x,f(2, 0),t(4, 2)>, Move<x,f(4, 2),t(2, 4)>]"
        ch2 = "[Move<x,f(2, 4),t(0, 2)>, Move<x,f(0, 2),t(2, 0)>, Move<x,f(2, 0),t(4, 2)>, Move<x,f(4, 2),t(6, 0)>]"
        ch3 = "[Move<x,f(2, 4),t(4, 2)>, Move<x,f(4, 2),t(2, 0)>, Move<x,f(2, 0),t(0, 2)>, Move<x,f(0, 2),t(2, 4)>]"

        self.assertEqual("[" + ch1 + ", " + ch2 + ", " + ch3 + "]", str(b.legal_moves()))
        self.assertIsNotNone(b.checker_at(1, 3))
        self.assertIsNotNone(b.checker_at(3, 3))
        self.assertIsNotNone(b.checker_at(1, 1))
        self.assertIsNotNone(b.checker_at(3, 1))
        self.assertIsNotNone(b.checker_at(5, 1))


class PushMovesTests(unittest.TestCase):
    def test_push_simple(self):
        b = Board()
        b.set_board(",,,,,,.x........,,,")
        b.push(b.legal_moves()[0])
        self.assertEqual(",,,,,x.........,,,,", b.get_board())

        b = Board()
        b.set_board(",,....o.....,,,,,,,")
        b.color = checkers.BLACK
        b.push(b.legal_moves()[0])
        self.assertEqual(",,,...o......,,,,,,", b.get_board())
        pass

    def test_push_jump(self):
        b = Board()
        b.set_board(",,....o,...x")
        b.push(b.legal_moves()[0])
        self.assertIsNone(b.checker_at(4, 2))
        self.assertEqual(",.....x....,,,,,,,,", b.get_board())

        b = Board()
        b.set_board(",,,,......x...,.....o....,,,,")
        b.color = checkers.BLACK
        b.push(b.legal_moves()[0])
        self.assertIsNone(b.checker_at(6, 4))
        self.assertEqual(",,,.......o..,,,,,,", b.get_board())
        pass

    def test_push_jump_chain(self):
        b = Board()
        b.set_board(",...,.o.o,.....,.o...o,.......,...o...o,....x....,.o.o,...")
        b.push(b.legal_moves()[0])
        self.assertEqual(",,,,,,,........x.,.o.o......,", b.get_board())
        pass

    def test_push_crowning(self):
        b = Board()
        b.set_board(",.x")
        b.push(b.legal_moves()[1])
        self.assertEqual("..X.......,,,,,,,,,", b.get_board())
        self.assertTrue(b.checker_at(2, 0).crowned)

        b = Board()
        b.set_board(",,,,,,,,....o,")
        b.color = False
        b.push(b.legal_moves()[0])
        self.assertEqual(",,,,,,,,,...O......", b.get_board())
        self.assertTrue(b.checker_at(3, 9).crowned)
        pass

    def test_push_chain_crowning(self):
        # crowning can only happen if chain ended at the proper place (crowning can't happen in the middle of the chain)
        # TODO
        self.assertTrue(False)
        pass

    def test_push_chain_no_crowning(self):
        # TODO
        self.assertTrue(False)
        pass

class SomeTests(unittest.TestCase):
    def test1(self):
        b = Board()
        b.set_board(",.x,,.x,,,,,........o,")
        moves = str(b.legal_moves())
        # note: promotion happens after move is pushed, not when listing legal moves
        self.assertEqual(moves, "[[Move<x,f(1, 1),t(0, 0)>], [Move<x,f(1, 1),t(2, 0)>], "
                                "[Move<x,f(1, 3),t(0, 2)>], [Move<x,f(1, 3),t(2, 2)>]]")

    def test2(self):
        b = Board()
        b.set_board(",.o........,,.o........,,,,,........x.,")
        b.color = False
        moves = str(b.legal_moves())
        self.assertEqual(moves, "[[Move<o,f(1, 1),t(0, 2)>], [Move<o,f(1, 1),t(2, 2)>], "
                                "[Move<o,f(1, 3),t(0, 4)>], [Move<o,f(1, 3),t(2, 4)>]]")

    def test3(self):
        b = Board()
        b.set_board(",.o........,,.o........,,,,,,")
        moves = str(b.legal_moves())
        self.assertEqual(moves, "[]")

    def test4(self):
        b = Board()
        b.set_board(",.o.o......,,..x.......,,,,,,")
        moves = str(b.legal_moves())
        self.assertEqual(moves, "[[Move<x,f(2, 3),t(1, 2)>], [Move<x,f(2, 3),t(3, 2)>]]")

    def test5(self):
        b = Board()
        b.set_board(",.o.o......,..x.......,,,,,,,")
        moves = str(b.legal_moves())
        # note: promotion happens after move is pushed, not when listing legal moves
        self.assertEqual(moves, "[[Move<x,f(2, 2),t(0, 0)>], [Move<x,f(2, 2),t(4, 0)>]]")

    def test6(self):
        b = Board()
        b.set_board(",.o...o....,..o.o.....,...x......,,,,,,")
        moves = str(b.legal_moves())
        self.assertEqual(moves, "[]")

    def test7(self):
        b = Board()
        b.set_board(",...o.o....,,...o.o....,....x.....,,,,,")
        moves = str(b.legal_moves())
        self.assertEqual(moves, "[[Move<x,f(4, 4),t(2, 2)>, Move<x,f(2, 2),t(4, 0)>, "
                                "Move<x,f(4, 0),t(6, 2)>, Move<x,f(6, 2),t(4, 4)>], "
                                "[Move<x,f(4, 4),t(6, 2)>, Move<x,f(6, 2),t(4, 0)>, "
                                "Move<x,f(4, 0),t(2, 2)>, Move<x,f(2, 2),t(4, 4)>]]")

    def test8(self):
        b = Board()
        b.set_board(",...o.o....,,...o......,....x.....,...o......,,,,")
        moves = str(b.legal_moves())
        self.assertEqual(moves, "[[Move<x,f(4, 4),t(2, 2)>, Move<x,f(2, 2),t(4, 0)>, Move<x,f(4, 0),t(6, 2)>]]")