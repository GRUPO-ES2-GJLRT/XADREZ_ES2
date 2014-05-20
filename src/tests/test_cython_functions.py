# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from cython.functions import (
    p0x88_to_tuple,
    tuple_to_0x88,
    chess_notation_to_0x88,
    p0x88_to_chess_notation,
    chess_notation_to_tuple
)


class TestPositionConverters(unittest.TestCase):

    def test_0x88_0_to_tuple_0_7(self):
        self.assertEqual(p0x88_to_tuple(0), (0, 7))

    def test_0x88_112_to_tuple_0_0(self):
        self.assertEqual(p0x88_to_tuple(112), (0, 0))

    def test_tuple_0_0_to_0x88_112(self):
        self.assertEqual(tuple_to_0x88((0, 0)), 112)

    def test_tuple_0_7_to_0x88_0(self):
        self.assertEqual(tuple_to_0x88((0, 7)), 0)

    def test_cn_A8_to_0x88_0(self):
        self.assertEqual(chess_notation_to_0x88("a8"), 0)

    def test_cn_A1_to_0x88_112(self):
        self.assertEqual(chess_notation_to_0x88("a1"), 112)

    def test_0x88_0_to_cn_A8(self):
        self.assertEqual(p0x88_to_chess_notation(0), "a8")

    def test_0x88_112_to_cn_A1(self):
        self.assertEqual(p0x88_to_chess_notation(112), "a1")

    def test_cn_A8_to_tuple_0_7(self):
        self.assertEqual(chess_notation_to_tuple("a8"), (0, 7))

    def test_cn_A1_to_tuple_0_0(self):
        self.assertEqual(chess_notation_to_tuple("a1"), (0, 0))


class TestCythonFunctions(TestPositionConverters):
    pass