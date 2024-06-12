import collections
import math
import pytest
from helper_operations.path_operations import cycleQ, pathQ
from helper_operations.permutation_graphs import HpathQ, extend, multinomial
from cycle_cover import HpathEven_1_1, HpathOdd_2_1


class Test_HpathOdd_2_1:
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


class Test_HpathEven_1_1:
    def test_Hpath2_1_1(self):
        test_path = HpathEven_1_1(2)
        assert pathQ(test_path)
        assert len(test_path) == len(set(test_path))
        assert len(test_path) == 12
        cyc = extend(HpathOdd_2_1(1)[::-1], (0,)) + extend(test_path, (1,))
        assert cycleQ(cyc)
        assert len(cyc) == 24

    def test_Hpath4_1_1(self):
        test_path = HpathEven_1_1(4)
        assert pathQ(test_path)
        assert len(test_path) == len(set(test_path))
        assert len(test_path) == 30
        cyc = extend(HpathOdd_2_1(3)[::-1], (0,)) + extend(test_path, (1,))
        assert cycleQ(cyc)

    def test_Hpath6_2_1(self):
        test_path = HpathEven_1_1(6)
        assert pathQ(test_path)
        assert len(test_path) == len(set(test_path))
        assert len(test_path) == 56
        cyc = extend(HpathOdd_2_1(5)[::-1], (0,)) + extend(test_path, (1,))
        assert cycleQ(cyc)

    def test_Hpath8_2_1(self):
        test_path = HpathEven_1_1(8)
        assert pathQ(test_path)
        assert len(test_path) == len(set(test_path))
        assert len(test_path) == 90
        cyc = extend(HpathOdd_2_1(7)[::-1], (0,)) + extend(test_path, (1,))
        assert cycleQ(cyc)

    def test_Hpath10_2_1(self):
        test_path = HpathEven_1_1(10)
        assert pathQ(test_path)
        assert len(test_path) == len(set(test_path))
        assert len(test_path) == 11*12
        cyc = extend(HpathOdd_2_1(9)[::-1], (0,)) + extend(test_path, (1,))
        assert cycleQ(cyc)