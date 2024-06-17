import math

import pytest

from cycle_cover import HpathCycleCover
from helper_operations.path_operations import cycleQ, pathQ
from helper_operations.permutation_graphs import multinomial, stutterPermutations


def recursive_cycle_check(cycle, total_length=0):
    assert isinstance(cycle, list)
    if isinstance(cycle[0][0], int):
        assert cycleQ(cycle)
        assert len(cycle) == len(set(cycle))
        total_length += len(cycle)
    else:
        for sub_cycle in cycle:
            total_length = recursive_cycle_check(sub_cycle, total_length)
    return total_length


class Test_HpathCycleCover_Even_1_1:
    def test_HpathCycleCover_2_1_1(self):
        signature = [2, 1, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_4_1_1(self):
        signature = [4, 1, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_6_1_1(self):
        signature = [6, 1, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_8_1_1(self):
        signature = [8, 1, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_10_1_1(self):
        signature = [10, 1, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_12_1_1(self):
        signature = [12, 1, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)


class Test_HpathCycleCover_Odd_1_1:
    def test_HpathCycleCover_3_1_1(self):
        signature = [3, 1, 1]
        cycle = HpathCycleCover(signature)
        assert len(cycle) == 1
        assert pathQ(cycle[0])
        assert len(cycle[0]) == len(set(cycle[0]))
        assert len(cycle[0]) == multinomial(signature)

    def test_HpathCycleCover_5_1_1(self):
        signature = [5, 1, 1]
        cycle = HpathCycleCover(signature)
        assert len(cycle) == 1
        assert pathQ(cycle[0])
        assert len(cycle[0]) == len(set(cycle[0]))
        assert len(cycle[0]) == multinomial(signature)

    def test_HpathCycleCover_7_1_1(self):
        signature = [7, 1, 1]
        cycle = HpathCycleCover(signature)
        assert len(cycle) == 1
        assert pathQ(cycle[0])
        assert len(cycle[0]) == len(set(cycle[0]))
        assert len(cycle[0]) == multinomial(signature)

    def test_HpathCycleCover_9_1_1(self):
        signature = [9, 1, 1]
        cycle = HpathCycleCover(signature)
        assert len(cycle) == 1
        assert pathQ(cycle[0])
        assert len(cycle[0]) == len(set(cycle[0]))
        assert len(cycle[0]) == multinomial(signature)

    def test_HpathCycleCover_11_1_1(self):
        signature = [11, 1, 1]
        cycle = HpathCycleCover(signature)
        assert len(cycle) == 1
        assert pathQ(cycle[0])
        assert len(cycle[0]) == len(set(cycle[0]))
        assert len(cycle[0]) == multinomial(signature)


class TestHpathCycleCover_Odd_2_1:
    def test_HpathCycleCover_3_2_1(self):
        signature = [3, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_5_2_1(self):
        signature = [5, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_7_2_1(self):
        signature = [7, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_9_2_1(self):
        signature = [9, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_11_2_1(self):
        signature = [11, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_13_2_1(self):
        signature = [13, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)


class Test_HpathCycleCover_Even_2_1:
    def test_HpathCycleCover_2_2_1(self):
        signature = [2, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_4_2_1(self):
        signature = [4, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_6_2_1(self):
        signature = [6, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_8_2_1(self):
        signature = [8, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_10_2_1(self):
        signature = [10, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_12_2_1(self):
        signature = [12, 2, 1]
        path = HpathCycleCover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature) - len(
            stutterPermutations(signature)
        )


class Test_HpathCycleCover_All_But_One_Even:
    def test_HpathCycleCover_2_2_3(self):
        signature = [2, 2, 3]
        cycles = HpathCycleCover(signature)
        assert len(cycles) == len(signature)
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_6_3_4(self):
        signature = [6, 3, 4]
        cycles = HpathCycleCover(signature)
        assert len(cycles) == len(signature)
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_2_2_2_2_3(self):
        signature = [2, 2, 2, 2, 3]
        cycles = HpathCycleCover(signature)
        assert len(cycles) == len(signature)
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_4_3_2_2(self):
        signature = [4, 3, 2, 2]
        cycles = HpathCycleCover(signature)
        assert len(cycles) == len(signature)
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )


class Test_HpathCycleCover_All_Even:
    def test_HpathCycleCover_2_2_2(self):
        signature = [2, 2, 2]
        cycles = HpathCycleCover(signature)
        assert len(cycles) == len(signature) * (len(signature) + 1) // 2
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_4_2_2(self):
        signature = [4, 2, 2]
        cycles = HpathCycleCover(signature)
        assert len(cycles) == len(signature) * (len(signature) + 1) // 2
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_2_2_2_2_2(self):
        signature = [2, 2, 2, 2, 2]
        cycles = HpathCycleCover(signature)
        assert len(cycles) == len(signature) * (len(signature) + 1) // 2
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_2_2_4_2(self):
        signature = [2, 2, 4, 2]
        cycles = HpathCycleCover(signature)
        assert len(cycles) == len(signature) * (len(signature) + 1) // 2
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_4_6_6(self):
        signature = [4, 6, 6]
        cycles = HpathCycleCover(signature)
        assert len(cycles) == len(signature) * (len(signature) + 1) // 2
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )
