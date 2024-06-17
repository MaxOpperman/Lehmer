import pytest

from cycle_cover import (
    HpathEven_1_1,
    HpathOdd_2_1,
    incorporatedOdd_2_1,
    parallelSubCycleOdd_2_1,
)
from helper_operations.path_operations import cycleQ, pathQ
from helper_operations.permutation_graphs import HpathQ, extend, multinomial


class Test_HpathOdd_2_1:
    def test_Hpath1_2_1(self):
        assert HpathQ(HpathOdd_2_1(1), [1, 2, 1])

    def test_Hpath3_2_1(self):
        k_odd = 3
        path = HpathOdd_2_1(k_odd)
        assert pathQ(path, [k_odd, 2, 1])
        assert len(path) == len(set(path))
        first_node = (1, 2) + (0,) * k_odd + (1,)
        last_node = (0, 2, 1) + (0,) * (k_odd - 1) + (1,)
        assert path[0] == first_node
        assert path[-1] == last_node
        assert len(path) == 24

    def test_Hpath5_2_1(self):
        k_odd = 5
        path = HpathOdd_2_1(k_odd)
        assert pathQ(path, [k_odd, 2, 1])
        assert len(path) == len(set(path))
        first_node = (1, 2) + (0,) * k_odd + (1,)
        last_node = (0, 2, 1) + (0,) * (k_odd - 1) + (1,)
        assert path[0] == first_node
        assert path[-1] == last_node

    def test_Hpath7_2_1(self):
        k_odd = 7
        path = HpathOdd_2_1(k_odd)
        assert pathQ(path, [k_odd, 2, 1])
        assert len(path) == len(set(path))
        first_node = (1, 2) + (0,) * k_odd + (1,)
        last_node = (0, 2, 1) + (0,) * (k_odd - 1) + (1,)
        assert path[0] == first_node
        assert path[-1] == last_node
        assert len(path) == 80

    def test_Hpath9_2_1(self):
        k_odd = 9
        path = HpathOdd_2_1(k_odd)
        assert pathQ(path, [k_odd, 2, 1])
        assert len(path) == len(set(path))
        first_node = (1, 2) + (0,) * k_odd + (1,)
        last_node = (0, 2, 1) + (0,) * (k_odd - 1) + (1,)
        assert path[0] == first_node
        assert path[-1] == last_node
        assert len(path) == 120

    def test_Hpath11_2_1(self):
        k_odd = 11
        path = HpathOdd_2_1(k_odd)
        assert pathQ(path, [k_odd, 2, 1])
        assert len(path) == len(set(path))
        first_node = (1, 2) + (0,) * k_odd + (1,)
        last_node = (0, 2, 1) + (0,) * (k_odd - 1) + (1,)
        assert path[0] == first_node
        assert path[-1] == last_node
        assert len(path) == 14 * 12

    def test_Hpath13_2_1(self):
        k_odd = 13
        path = HpathOdd_2_1(k_odd)
        assert pathQ(path, [k_odd, 2, 1])
        assert len(path) == len(set(path))
        first_node = (1, 2) + (0,) * k_odd + (1,)
        last_node = (0, 2, 1) + (0,) * (k_odd - 1) + (1,)
        assert path[0] == first_node
        assert path[-1] == last_node
        assert len(path) == 16 * 14


class Test_ParallelSubCycleOdd_2_1:
    def test_parallelSubCycle3_2_1(self):
        even_k = 2
        path = parallelSubCycleOdd_2_1(even_k)
        assert cycleQ(path)
        assert len(path) == len(set(path))
        assert len(path) == 2 * multinomial([even_k, 2])
        first_node = (0, 1) + (0,) * (even_k - 1) + (1, 0, 2)
        last_node = (1,) + (0,) * (even_k) + (1, 0, 2)
        assert path[0] == first_node
        assert path[-1] == last_node

    def test_parallelSubCycle5_2_1(self):
        even_k = 4
        path = parallelSubCycleOdd_2_1(even_k)
        assert cycleQ(path)
        assert len(path) == len(set(path))
        assert len(path) == 2 * multinomial([even_k, 2])
        first_node = (0, 1) + (0,) * (even_k - 1) + (1, 0, 2)
        last_node = (1,) + (0,) * (even_k) + (1, 0, 2)
        assert path[0] == first_node
        assert path[-1] == last_node

    def test_parallelSubCycle7_2_1(self):
        even_k = 6
        path = parallelSubCycleOdd_2_1(even_k)
        assert cycleQ(path)
        assert len(path) == len(set(path))
        assert len(path) == 2 * multinomial([even_k, 2])
        first_node = (0, 1) + (0,) * (even_k - 1) + (1, 0, 2)
        last_node = (1,) + (0,) * (even_k) + (1, 0, 2)
        assert path[0] == first_node
        assert path[-1] == last_node

    def test_parallelSubCycle9_2_1(self):
        even_k = 8
        path = parallelSubCycleOdd_2_1(even_k)
        assert cycleQ(path)
        assert len(path) == len(set(path))
        assert len(path) == 2 * multinomial([even_k, 2])
        first_node = (0, 1) + (0,) * (even_k - 1) + (1, 0, 2)
        last_node = (1,) + (0,) * (even_k) + (1, 0, 2)
        assert path[0] == first_node
        assert path[-1] == last_node


class Test_IncorporatedOdd_2_1:
    def test_Hpath1_2_1(self):
        assert HpathQ(incorporatedOdd_2_1(1), [1, 2, 1])

    def test_incorporated3_2_1(self):
        odd_k = 3
        path = incorporatedOdd_2_1(odd_k)
        assert pathQ(path)
        assert len(path) == len(set(path))
        assert len(path) == len(HpathOdd_2_1(odd_k)) + 2 * multinomial([odd_k - 1, 2])

    def test_incorporated5_2_1(self):
        odd_k = 5
        path = incorporatedOdd_2_1(odd_k)
        assert pathQ(path)
        assert len(path) == len(set(path))
        assert len(path) == len(HpathOdd_2_1(odd_k)) + 2 * multinomial([odd_k - 1, 2])

    def test_incorporated7_2_1(self):
        odd_k = 7
        path = incorporatedOdd_2_1(odd_k)
        assert pathQ(path)
        assert len(path) == len(set(path))
        assert len(path) == len(HpathOdd_2_1(odd_k)) + 2 * multinomial([odd_k - 1, 2])

    def test_incorporated9_2_1(self):
        odd_k = 9
        path = incorporatedOdd_2_1(odd_k)
        assert pathQ(path)
        assert len(path) == len(set(path))
        assert len(path) == len(HpathOdd_2_1(odd_k)) + 2 * multinomial([odd_k - 1, 2])

    def test_incorporated11_2_1(self):
        odd_k = 11
        path = incorporatedOdd_2_1(odd_k)
        assert pathQ(path)
        assert len(path) == len(set(path))
        assert len(path) == len(HpathOdd_2_1(odd_k)) + 2 * multinomial([odd_k - 1, 2])


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
        assert len(test_path) == 11 * 12
        cyc = extend(HpathOdd_2_1(9)[::-1], (0,)) + extend(test_path, (1,))
        assert cycleQ(cyc)
