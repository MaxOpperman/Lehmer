import pytest

from cycle_cover import CycleCover
from helper_operations.path_operations import pathQ, recursive_cycle_check
from helper_operations.permutation_graphs import multinomial, stutterPermutations
from verhoeff import HpathNS


generate_cycle_cover = CycleCover().generate_cycle_cover


class Test_HpathCycleCover_Edge_Cases:
    def test_HpathCycleCover_Empty(self):
        with pytest.raises(ValueError) as e_info:
            generate_cycle_cover([])

    def test_HpathCycleCover_1_Element(self):
        p = generate_cycle_cover([2])
        assert len(p) == 1
        assert len(p[0]) == 1
        assert len(p[0][0]) == 2

    def test_HpathCycleCover_50(self):
        p = generate_cycle_cover([50])
        assert len(p) == 1
        assert len(p[0]) == 1
        assert len(p[0][0]) == 50

    def test_HpathCycleCover_Verhoeff(self):
        signature = [4, 4]
        p = generate_cycle_cover(signature)
        assert len(p) == 1
        assert p[0] == HpathNS(4, 4)
        assert recursive_cycle_check(p) == multinomial(signature) - len(
            stutterPermutations(signature)
        )


class Test_HpathCycleCover_Even_1_1:
    def test_HpathCycleCover_2_1_1(self):
        signature = [2, 1, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_4_1_1(self):
        signature = [4, 1, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_6_1_1(self):
        signature = [6, 1, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_8_1_1(self):
        signature = [8, 1, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    @pytest.mark.slow
    def test_HpathCycleCover_10_1_1(self):
        signature = [10, 1, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    @pytest.mark.slow
    def test_HpathCycleCover_12_1_1(self):
        signature = [12, 1, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)


class Test_HpathCycleCover_Odd_1_1:
    def test_HpathCycleCover_3_1_1(self):
        signature = [3, 1, 1]
        cycle = generate_cycle_cover(signature)
        assert len(cycle) == 1
        assert pathQ(cycle[0])
        assert len(cycle[0]) == len(set(cycle[0]))
        assert len(cycle[0]) == multinomial(signature)

    def test_HpathCycleCover_5_1_1(self):
        signature = [5, 1, 1]
        cycle = generate_cycle_cover(signature)
        assert len(cycle) == 1
        assert pathQ(cycle[0])
        assert len(cycle[0]) == len(set(cycle[0]))
        assert len(cycle[0]) == multinomial(signature)

    def test_HpathCycleCover_7_1_1(self):
        signature = [7, 1, 1]
        cycle = generate_cycle_cover(signature)
        assert len(cycle) == 1
        assert pathQ(cycle[0])
        assert len(cycle[0]) == len(set(cycle[0]))
        assert len(cycle[0]) == multinomial(signature)

    @pytest.mark.slow
    def test_HpathCycleCover_9_1_1(self):
        signature = [9, 1, 1]
        cycle = generate_cycle_cover(signature)
        assert len(cycle) == 1
        assert pathQ(cycle[0])
        assert len(cycle[0]) == len(set(cycle[0]))
        assert len(cycle[0]) == multinomial(signature)

    @pytest.mark.slow
    def test_HpathCycleCover_11_1_1(self):
        signature = [11, 1, 1]
        cycle = generate_cycle_cover(signature)
        assert len(cycle) == 1
        assert pathQ(cycle[0])
        assert len(cycle[0]) == len(set(cycle[0]))
        assert len(cycle[0]) == multinomial(signature)


class TestHpathCycleCover_Odd_2_1:
    def test_HpathCycleCover_3_2_1(self):
        signature = [3, 2, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_5_2_1(self):
        signature = [5, 2, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    def test_HpathCycleCover_7_2_1(self):
        signature = [7, 2, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    @pytest.mark.slow
    def test_HpathCycleCover_9_2_1(self):
        signature = [9, 2, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)

    @pytest.mark.slow
    def test_HpathCycleCover_13_2_1(self):
        signature = [13, 2, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature)


class Test_HpathCycleCover_Even_2_1:
    def test_HpathCycleCover_2_2_1(self):
        signature = [2, 2, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_4_2_1(self):
        signature = [4, 2, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_6_2_1(self):
        signature = [6, 2, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    @pytest.mark.slow
    def test_HpathCycleCover_8_2_1(self):
        signature = [8, 2, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_12_2_1(self):
        signature = [12, 2, 1]
        path = generate_cycle_cover(signature)
        assert len(path) == 1
        assert pathQ(path[0])
        assert len(path[0]) == len(set(path[0]))
        assert len(path[0]) == multinomial(signature) - len(
            stutterPermutations(signature)
        )


class Test_HpathCycleCover_All_But_One_Even:
    def test_HpathCycleCover_2_2_3(self):
        signature = [2, 2, 3]
        cycles = generate_cycle_cover(signature)
        assert len(cycles) == len(signature)
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_4_2_3(self):
        signature = [4, 2, 3]
        cycles = generate_cycle_cover(signature)
        assert len(cycles) == len(signature)
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    @pytest.mark.slow
    def test_HpathCycleCover_6_3_4(self):
        signature = [6, 3, 4]
        cycles = generate_cycle_cover(signature)
        assert len(cycles) == len(signature)
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    @pytest.mark.slow
    def test_HpathCycleCover_2_2_2_2_3(self):
        signature = [2, 2, 2, 2, 3]
        cycles = generate_cycle_cover(signature)
        assert len(cycles) == len(signature)
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_4_3_2_2(self):
        signature = [4, 3, 2, 2]
        cycles = generate_cycle_cover(signature)
        assert len(cycles) == len(signature)
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )


class Test_HpathCycleCover_All_Even:
    def test_HpathCycleCover_2_2_2(self):
        signature = [2, 2, 2]
        cycles = generate_cycle_cover(signature)
        assert len(cycles) == len(signature) * (len(signature) + 1) // 2
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_4_2_2(self):
        signature = [4, 2, 2]
        cycles = generate_cycle_cover(signature)
        assert len(cycles) == len(signature) * (len(signature) + 1) // 2
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    @pytest.mark.slow
    def test_HpathCycleCover_2_2_2_2_2(self):
        signature = [2, 2, 2, 2, 2]
        cycles = generate_cycle_cover(signature)
        assert len(cycles) == len(signature) * (len(signature) + 1) // 2
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_2_2_4_2(self):
        signature = [2, 2, 4, 2]
        cycles = generate_cycle_cover(signature)
        assert len(cycles) == len(signature) * (len(signature) + 1) // 2
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )

    def test_HpathCycleCover_4_6_4(self):
        signature = [4, 6, 4]
        cycles = generate_cycle_cover(signature)
        assert len(cycles) == len(signature) * (len(signature) + 1) // 2
        total_length = recursive_cycle_check(cycles)
        assert total_length == multinomial(signature) - len(
            stutterPermutations(signature)
        )
