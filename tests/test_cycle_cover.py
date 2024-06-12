import collections
import math
import pytest
from helper_operations.path_operations import pathQ
from helper_operations.permutation_graphs import HpathQ, multinomial
from cycle_cover import HpathOdd_2_1


class Test_CycleCover:
    def test_Hpath1_2_1(self):
        assert HpathQ(HpathOdd_2_1(1), [1, 2, 1])

    def test_Hpath3_2_1(self):
        path = HpathOdd_2_1(3)
        assert pathQ(path, [3, 2, 1])
        assert len(path) == len(set(path))
        assert len(path) == 24

    def test_Hpath5_2_1(self):
        path = HpathOdd_2_1(5)
        assert pathQ(path)
        assert len(path) == len(set(path))
        assert len(path) == 48

    def test_Hpath7_2_1(self):
        path = HpathOdd_2_1(7)
        assert pathQ(path)
        # print duplicates in the path
        for item, count in collections.Counter(path).items():
            if count > 1:
                print(item, count)
        assert len(path) == len(set(path))
        assert len(path) == 80

    def test_Hpath9_2_1(self):
        path = HpathOdd_2_1(9)
        assert pathQ(path)
        # print duplicates in the path
        for item, count in collections.Counter(path).items():
            if count > 1:
                print(item, count)
        assert len(path) == len(set(path))
        assert len(path) == 120

    def test_Hpath11_2_1(self):
        path = HpathOdd_2_1(11)
        assert pathQ(path)
        # print duplicates in the path
        for item, count in collections.Counter(path).items():
            if count > 1:
                print(item, count)
        assert len(path) == len(set(path))
        assert len(path) == 14 * 12

    def test_Hpath13_2_1(self):
        path = HpathOdd_2_1(13)
        assert pathQ(path)
        # print duplicates in the path
        for item, count in collections.Counter(path).items():
            if count > 1:
                print(item, count)
        assert len(path) == len(set(path))
        assert len(path) == 16 * 14
