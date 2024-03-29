import unittest

import checkers
from checkers import Board, Checker, Move, WHITE, BLACK


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


class GetCheckersTest(unittest.TestCase):

    def test_1(self):
        bstr = "x"
        b = Board()
        b.set_board(bstr)
        # https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertCountEqual
        # tests if list have same elements
        self.assertCountEqual([(0, 0, Checker(WHITE))], b.get_checkers())

    def test_2(self):
        bstr = ".....o"
        b = Board()
        b.set_board(bstr)
        self.assertCountEqual([(5, 0, Checker(BLACK))], b.get_checkers())

    def test_3(self):
        bstr = "...o......,....x.....,.....x....,..o...o..."
        b = Board()
        b.set_board(bstr)
        self.assertCountEqual([(3, 0, Checker(BLACK)), (2, 3, Checker(BLACK)), (6, 3, Checker(BLACK)),
                               (4, 1, Checker(WHITE)), (5, 2, Checker(WHITE))], b.get_checkers())


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

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        # self.maxDiff = None

    def test_move_white(self):
        b = Board()
        b.set_board(",,,,,,.x")
        self.assertEqual("[[Move<x,f(1, 6),t(0, 5)>], [Move<x,f(1, 6),t(2, 5)>]]", str(b.legal_moves()))

    def test_move_black(self):
        b = Board()
        b.set_board(",,....o")
        b.color = checkers.BLACK
        self.assertEqual("[[Move<o,f(4, 2),t(3, 3)>], [Move<o,f(4, 2),t(5, 3)>]]", str(b.legal_moves()))

    def test_move_king_white(self):
        b = Board()
        b.set_board(",,.......X")
        self.assertEqual("[[Move<X,f(7, 2),t(6, 1)>], [Move<X,f(7, 2),t(5, 0)>], [Move<X,f(7, 2),t(8, 1)>], "
                         "[Move<X,f(7, 2),t(9, 0)>], [Move<X,f(7, 2),t(6, 3)>], [Move<X,f(7, 2),t(5, 4)>], "
                         "[Move<X,f(7, 2),t(4, 5)>], [Move<X,f(7, 2),t(3, 6)>], [Move<X,f(7, 2),t(2, 7)>], "
                         "[Move<X,f(7, 2),t(1, 8)>], [Move<X,f(7, 2),t(0, 9)>], [Move<X,f(7, 2),t(8, 3)>], "
                         "[Move<X,f(7, 2),t(9, 4)>]]", str(b.legal_moves()))

    def test_move_two_kings_white(self):
        b = Board()
        b.set_board(".......X.X")
        wc = Checker(WHITE, True) # white, crowned checker (X)
        self.assertCountEqual([[Move(wc, (7, 0), (6, 1))], [Move(wc, (7, 0), (5, 2))], [Move(wc, (7, 0), (4, 3))],
                               [Move(wc, (7, 0), (3, 4))], [Move(wc, (7, 0), (2, 5))], [Move(wc, (7, 0), (1, 6))],
                               [Move(wc, (7, 0), (0, 7))], [Move(wc, (7, 0), (8, 1))], [Move(wc, (7, 0), (9, 2))],
                               [Move(wc, (9, 0), (8, 1))], [Move(wc, (9, 0), (7, 2))], [Move(wc, (9, 0), (6, 3))],
                               [Move(wc, (9, 0), (5, 4))], [Move(wc, (9, 0), (4, 5))], [Move(wc, (9, 0), (3, 6))],
                               [Move(wc, (9, 0), (2, 7))], [Move(wc, (9, 0), (1, 8))], [Move(wc, (9, 0), (0, 9))],
                               ], b.legal_moves())

    def test_move_king_black_corner(self):
        b = Board()
        b.set_board(",,,,,,,,,.........O")
        b.color = BLACK
        bc = Checker(BLACK, True)
        self.assertCountEqual([[Move(bc, (9, 9), (8, 8))], [Move(bc, (9, 9), (7, 7))], [Move(bc, (9, 9), (6, 6))],
                               [Move(bc, (9, 9), (5, 5))], [Move(bc, (9, 9), (4, 4))], [Move(bc, (9, 9), (3, 3))],
                               [Move(bc, (9, 9), (2, 2))], [Move(bc, (9, 9), (1, 1))], [Move(bc, (9, 9), (0, 0))],
                               ], b.legal_moves())

    def test_move_king_black_blocked(self):
        b = Board()
        b.set_board(",,.....O....,,...o......,........o.")
        b.color = checkers.BLACK
        self.assertEqual("[[Move<O,f(5, 2),t(4, 1)>], [Move<O,f(5, 2),t(3, 0)>], [Move<O,f(5, 2),t(6, 1)>], "
                         "[Move<O,f(5, 2),t(7, 0)>], [Move<O,f(5, 2),t(4, 3)>], [Move<O,f(5, 2),t(6, 3)>], "
                         "[Move<O,f(5, 2),t(7, 4)>], [Move<o,f(3, 4),t(2, 5)>], [Move<o,f(3, 4),t(4, 5)>], "
                         "[Move<o,f(8, 5),t(7, 6)>], [Move<o,f(8, 5),t(9, 6)>]]", str(b.legal_moves()))

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

    def test_crowned_jump(self):
        b = Board()
        b.set_board(",,,,o.........,.o.....o..,,,....X.....,")
        self.assertEqual("[[Move<X,f(4, 8),t(8, 4)>], [Move<X,f(4, 8),t(9, 3)>]]", str(b.legal_moves()))

    def test_crowned_double_jump(self):
        b = Board()
        b.set_board(",,......o...,,....o.....,,....o.....,,..X.......,")
        self.assertEqual("[[Move<X,f(2, 8),t(5, 5)>, Move<X,f(5, 5),t(3, 3)>], "
                         "[Move<X,f(2, 8),t(5, 5)>, Move<X,f(5, 5),t(2, 2)>], "
                         "[Move<X,f(2, 8),t(5, 5)>, Move<X,f(5, 5),t(1, 1)>], "
                         "[Move<X,f(2, 8),t(5, 5)>, Move<X,f(5, 5),t(0, 0)>], "
                         "[Move<X,f(2, 8),t(7, 3)>, Move<X,f(7, 3),t(5, 1)>], "
                         "[Move<X,f(2, 8),t(7, 3)>, Move<X,f(7, 3),t(4, 0)>]]", str(b.legal_moves()))


class PushPopMovesTests(unittest.TestCase):
    def test_push_simple(self):
        b = Board()
        b.set_board(",,,,,,.x........,,,")
        b.push(b.legal_moves()[0])
        self.assertEqual(",,,,,x.........,,,,", b.get_board())
        b.pop()
        self.assertEqual(",,,,,,.x........,,,", b.get_board())

        b = Board()
        b.set_board(",,....o.....,,,,,,,")
        b.color = checkers.BLACK
        b.push(b.legal_moves()[0])
        self.assertEqual(",,,...o......,,,,,,", b.get_board())
        b.pop()
        self.assertEqual(",,....o.....,,,,,,,", b.get_board())
        pass

    def test_push_jump(self):
        b = Board()
        b.set_board(",,....o,...x")
        b.push(b.legal_moves()[0])
        self.assertIsNone(b.checker_at(4, 2))
        self.assertEqual(",.....x....,,,,,,,,", b.get_board())
        b.pop()
        self.assertIsNotNone(b.checker_at(4, 2))
        self.assertEqual(",,....o.....,...x......,,,,,,", b.get_board())

        b = Board()
        b.set_board(",,,,......x...,.....o....,,,,")
        b.color = checkers.BLACK
        b.push(b.legal_moves()[0])
        self.assertIsNone(b.checker_at(6, 4))
        self.assertEqual(",,,.......o..,,,,,,", b.get_board())
        b.pop()
        self.assertIsNotNone(b.checker_at(6, 4))
        self.assertEqual(",,,,......x...,.....o....,,,,", b.get_board())
        pass

    def test_push_jump_chain(self):
        b = Board()
        b.set_board(",...,.o.o,.....,.o...o,.......,...o...o,....x....,.o.o,...")
        b.push(b.legal_moves()[0])
        self.assertEqual(",,,,,,,........x.,.o.o......,", b.get_board())
        b.pop()
        self.assertEqual(",,.o.o......,,.o...o....,,...o...o..,....x.....,.o.o......,", b.get_board())
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
        b.pop()
        self.assertEqual(",,,,,,,,....o.....,", b.get_board())
        self.assertFalse(b.checker_at(4, 8).crowned)
        pass

    def test_jump_crowning(self):
        b = Board()
        b.set_board("...,...o,....x")
        b.push(b.legal_moves()[0])
        self.assertEqual("..X.......,,,,,,,,,", b.get_board())
        self.assertEqual(Checker(WHITE, True), b.checker_at(2, 0))
        b.pop()
        self.assertEqual(",...o......,....x.....,,,,,,,", b.get_board())
        self.assertEqual(Checker(WHITE, False), b.checker_at(4, 2))

    def test_push_chain_crowning(self):
        # crowning can only happen if chain ended at the proper place (crowning can't happen in the middle of the chain)
        b = Board()
        b.set_board(",......o...,,....o.....,...x......")
        b.push(b.legal_moves()[0])
        self.assertIsNotNone(b.checker_at(7, 0))
        self.assertTrue(b.checker_at(7, 0).crowned)
        b.pop()
        self.assertEqual(",......o...,,....o.....,...x......,,,,,", b.get_board())
        self.assertIsNone(b.checker_at(7, 0))
        self.assertFalse(b.checker_at(3, 4).crowned)
        pass

    def test_push_chain_no_crowning(self):
        b = Board()
        b.set_board(",......o.o.,,....o.....,...x......")
        b.push(b.legal_moves()[0])
        self.assertIsNotNone(b.checker_at(9, 2))
        self.assertFalse(b.checker_at(9, 2).crowned)
        b.pop()
        self.assertEqual(",......o.o.,,....o.....,...x......,,,,,", b.get_board())
        self.assertIsNone(b.checker_at(9, 2))
        self.assertFalse(b.checker_at(3, 4).crowned)
        pass

    def test_push_jump_chain_end_on_jumped(self):
        b = Board()
        b.set_board(",,,,,....x.x...,.x.x......,......x.x.,.x........,..O.......")
        b.color = BLACK
        print(b.legal_moves()[0])
        b.push(b.legal_moves()[0])
        self.assertEqual(",,,,,,...O......,,,", b.get_board())
        b.pop()
        self.assertEqual(",,,,,....x.x...,.x.x......,......x.x.,.x........,..O.......", b.get_board())

    def test_promotion_pop(self):
        b = Board()
        b.set_board(",x")
        b.push(b.legal_moves()[0])
        chk = Checker(WHITE, True)
        self.assertTrue(b.move_stack[-1][-1].is_promotion)
        self.assertEqual(b.checker_at(1, 0), chk)
        b.push([Move(chk, (1, 0), (5, 4))])
        self.assertEqual(b.checker_at(5, 4), chk)
        b.pop()
        self.assertEqual(b.checker_at(1, 0), Checker(WHITE, True))
        b.pop()
        self.assertEqual(b.checker_at(0, 1), Checker(WHITE, False))

    def test_border_twice(self):
        b = Board()
        b.set_board("...X")
        cx = Checker(WHITE, True)
        b.push([Move(cx, (3, 0), (5, 2))])
        self.assertTrue(True, cx.crowned)
        b.push([Move(cx, (5, 2), (7, 0))])
        self.assertTrue(True, cx.crowned)
        b.pop()
        self.assertTrue(True, cx.crowned)
        b.pop()
        self.assertTrue(True, cx.crowned)



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