from connect_cycle_cover import get_connected_cycle_cover
from helper_operations.path_operations import (
    adjacent,
    non_stutter_cycleQ,
    pathQ,
    stutterPermutationQ,
)
from helper_operations.permutation_graphs import multinomial, stutterPermutations
from lehmer_paths import incorporate_stutters


class TestLehmerPathVsCycleCondition:
    """
    Test the condition for a path to be a cycle. There is only a path and no cycle for:\n
    - Linear neighbor-swap graphs (even-1 or odd-1)
    - Odd-odd signatures
    - Odd-even / even-odd signatures
    - Even-1-1 signatures
    """

    def test_linear_path(self):
        assert non_stutter_cycleQ([1, 1]) == False
        assert non_stutter_cycleQ([2, 1]) == False
        assert non_stutter_cycleQ([1, 3]) == False
        assert non_stutter_cycleQ([4, 1]) == False
        assert non_stutter_cycleQ([1, 5]) == False
        assert non_stutter_cycleQ([6, 1]) == False
        assert non_stutter_cycleQ([1, 7]) == False
        assert non_stutter_cycleQ([8, 1]) == False
        assert non_stutter_cycleQ([1, 9]) == False
        assert non_stutter_cycleQ([10, 1]) == False

    def test_odd_odd(self):
        assert non_stutter_cycleQ([3, 3]) == False
        assert non_stutter_cycleQ([5, 5]) == False
        assert non_stutter_cycleQ([7, 3]) == False
        assert non_stutter_cycleQ([11, 9]) == False
        assert non_stutter_cycleQ([11, 5]) == False
        assert non_stutter_cycleQ([7, 13]) == False
        assert non_stutter_cycleQ([15, 21]) == False

    def test_odd_even(self):
        assert non_stutter_cycleQ([3, 2]) == False
        assert non_stutter_cycleQ([5, 4]) == False
        assert non_stutter_cycleQ([7, 6]) == False
        assert non_stutter_cycleQ([11, 10]) == False
        assert non_stutter_cycleQ([11, 6]) == False
        assert non_stutter_cycleQ([7, 12]) == False
        assert non_stutter_cycleQ([15, 20]) == False

    def test_even_odd(self):
        assert non_stutter_cycleQ([2, 3]) == False
        assert non_stutter_cycleQ([4, 5]) == False
        assert non_stutter_cycleQ([6, 7]) == False
        assert non_stutter_cycleQ([10, 11]) == False
        assert non_stutter_cycleQ([12, 15]) == False
        assert non_stutter_cycleQ([6, 13]) == False
        assert non_stutter_cycleQ([14, 23]) == False

    def test_even_1_1(self):
        assert non_stutter_cycleQ([2, 1, 1]) == False
        assert non_stutter_cycleQ([4, 1, 1]) == False
        assert non_stutter_cycleQ([1, 1, 6]) == False
        assert non_stutter_cycleQ([1, 10, 1]) == False
        assert non_stutter_cycleQ([1, 12, 1]) == False
        assert non_stutter_cycleQ([1, 1, 14]) == False
        assert non_stutter_cycleQ([1, 1, 16]) == False
        assert non_stutter_cycleQ([22, 1, 1]) == False
        assert non_stutter_cycleQ([1, 1, 30]) == False

    def test_cycle_at_least_2_odd(self):
        assert non_stutter_cycleQ([3, 3, 1]) == True
        assert non_stutter_cycleQ([3, 3, 3]) == True
        assert non_stutter_cycleQ([3, 3, 5]) == True
        assert non_stutter_cycleQ([13, 3, 4]) == True
        assert non_stutter_cycleQ([7, 9, 2, 4, 5]) == True
        assert non_stutter_cycleQ([3, 3, 3, 3, 3, 4, 4, 4]) == True

    def test_cycle_at_least_2_even(self):
        assert non_stutter_cycleQ([2, 2, 1]) == True
        assert non_stutter_cycleQ([2, 2, 2]) == True
        assert non_stutter_cycleQ([2, 2, 4]) == True
        assert non_stutter_cycleQ([12, 2, 3]) == True
        assert non_stutter_cycleQ([6, 8, 2, 3, 4]) == True
        assert non_stutter_cycleQ([2, 2, 2, 2, 2, 2, 2, 3]) == True


class TestLehmerPaths:
    def test_incorporate_stutters_no_stutters(self):
        assert incorporate_stutters([1, 1]) == get_connected_cycle_cover([1, 1])
        assert incorporate_stutters([3, 3]) == get_connected_cycle_cover([3, 3])
        assert incorporate_stutters([3, 2, 1]) == get_connected_cycle_cover([3, 2, 1])
        assert incorporate_stutters([3, 3, 2]) == get_connected_cycle_cover([3, 3, 2])
        assert incorporate_stutters([7, 1]) == get_connected_cycle_cover([7, 1])
        assert incorporate_stutters([5, 5]) == get_connected_cycle_cover([5, 5])

    def test_incorporate_stutters_one_element(self):
        assert incorporate_stutters([1]) == get_connected_cycle_cover([1])
        assert incorporate_stutters([3]) == get_connected_cycle_cover([3])

    def test_incorporate_stutters_2_1(self):
        sig = [1, 2]
        result = incorporate_stutters(sig)
        expected_result = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
        assert result == expected_result
        assert incorporate_stutters([2, 1]) == [(0, 0, 1), (0, 1, 0), (1, 0, 0)]

    def test_incorporate_stutters_1_4(self):
        sig = [1, 4]
        result = incorporate_stutters(sig)
        expected_result = [
            (1, 1, 1, 1, 0),
            (1, 1, 1, 0, 1),
            (1, 1, 0, 1, 1),
            (1, 0, 1, 1, 1),
            (0, 1, 1, 1, 1),
        ]
        assert result == expected_result
        assert len(result) == multinomial(sig) + len(stutterPermutations(sig)) - (
            1
            if stutterPermutationQ(result[0]) or stutterPermutationQ(result[-1])
            else 0
        )

    def test_incorporate_stutters_2_2(self):
        sig = [2, 2]
        result = incorporate_stutters(sig)
        expected_result = [
            (1, 0, 0, 1),
            (0, 1, 0, 1),
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 0),
        ]
        assert result == expected_result
        assert pathQ(result)
        assert len(result) == multinomial(sig) + len(stutterPermutations(sig)) - (
            1
            if stutterPermutationQ(result[0]) or stutterPermutationQ(result[-1])
            else 0
        )

    def test_incorporate_stutters_2_3(self):
        sig = [2, 3]
        result = incorporate_stutters(sig)
        expected_result = [
            (1, 1, 1, 0, 0),
            (1, 1, 0, 1, 0),
            (1, 1, 0, 0, 1),
            (1, 1, 0, 1, 0),
            (1, 0, 1, 1, 0),
            (1, 0, 1, 0, 1),
            (1, 0, 0, 1, 1),
            (0, 1, 0, 1, 1),
            (0, 0, 1, 1, 1),
            (0, 1, 0, 1, 1),
            (0, 1, 1, 0, 1),
            (0, 1, 1, 1, 0),
        ]
        assert result == expected_result
        assert pathQ(result)
        assert len(result) == multinomial(sig) + len(stutterPermutations(sig)) - (
            1
            if stutterPermutationQ(result[0]) or stutterPermutationQ(result[-1])
            else 0
        )

    def test_incorporate_stutters_3_4(self):
        sig = [3, 4]
        result = incorporate_stutters(sig)
        assert pathQ(result)
        assert len(result) == multinomial(sig) + len(stutterPermutations(sig)) - (
            1
            if stutterPermutationQ(result[0]) or stutterPermutationQ(result[-1])
            else 0
        )

    def test_incorporate_stutters_2_1_2(self):
        sig = [2, 1, 2]
        result = incorporate_stutters(sig)
        assert pathQ(result)
        assert len(result) == multinomial(sig) + len(stutterPermutations(sig)) - (
            1
            if stutterPermutationQ(result[0]) or stutterPermutationQ(result[-1])
            else 0
        )

    def test_incorporate_stutters_2_2_2(self):
        sig = [2, 2, 2]
        result = incorporate_stutters(sig)
        assert pathQ(result)
        assert len(result) == multinomial(sig) + len(stutterPermutations(sig)) - (
            1
            if stutterPermutationQ(result[0]) or stutterPermutationQ(result[-1])
            else 0
        )

    def test_incorporate_stutters_2_2_3(self):
        sig = [2, 2, 3]
        result = incorporate_stutters(sig)
        assert pathQ(result)
        assert len(result) == multinomial(sig) + len(stutterPermutations(sig)) - (
            1
            if stutterPermutationQ(result[0]) or stutterPermutationQ(result[-1])
            else 0
        )

    def test_incorporate_stutters_2_2_4(self):
        sig = [2, 2, 4]
        result = incorporate_stutters(sig)
        assert pathQ(result)
        assert len(result) == multinomial(sig) + len(stutterPermutations(sig)) - (
            1
            if stutterPermutationQ(result[0]) or stutterPermutationQ(result[-1])
            else 0
        )

    def test_incorporate_stutters_5_4(self):
        sig = [5, 4]
        result = incorporate_stutters(sig)
        assert pathQ(result)
        assert len(result) == multinomial(sig) + len(stutterPermutations(sig)) - (
            1
            if stutterPermutationQ(result[0]) or stutterPermutationQ(result[-1])
            else 0
        )

    def test_incorporate_stutters_4_6(self):
        sig = [4, 6]
        result = incorporate_stutters(sig)
        assert pathQ(result)
        assert len(result) == multinomial(sig) + len(stutterPermutations(sig)) - (
            1
            if stutterPermutationQ(result[0]) or stutterPermutationQ(result[-1])
            else 0
        )
