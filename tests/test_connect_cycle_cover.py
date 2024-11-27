import pytest

from cycle_cover import generate_cycle_cover, get_connected_cycle_cover
from helper_operations.cycle_cover_connections import generate_end_tuple_order
from helper_operations.path_operations import cycleQ, get_first_element, pathQ
from helper_operations.permutation_graphs import multinomial, stutterPermutations


class Test_TailsOrdering:
    # def test_end_tuple_order_two_or_more_odd_not_possible(self):
    #     with pytest.raises(ValueError):
    #         generate_end_tuple_order((3, 3, 2))
    #     with pytest.raises(ValueError):
    #         generate_end_tuple_order((3, 3, 3, 2))
    #     with pytest.raises(ValueError):
    #         generate_end_tuple_order((3, 2, 3, 2))
    #     with pytest.raises(ValueError):
    #         generate_end_tuple_order((2, 5, 2, 5))

    def test_end_tuple_order_one_element(self):
        sig = (2,)
        result = generate_end_tuple_order(sig)
        assert result == []
        sig = (0,)
        assert generate_end_tuple_order(sig) == []
        sig = (1,)
        result = generate_end_tuple_order(sig)
        assert result == []

    def test_end_tuple_order_two_elements(self):
        sig = (2, 2)
        result = generate_end_tuple_order(sig)
        assert result == []
        sig = (4, 3)
        result = generate_end_tuple_order(sig)
        assert result == []
        sig = (6, 2)
        result = generate_end_tuple_order(sig)
        assert result == []
        sig = (3, 6)
        result = generate_end_tuple_order(sig)
        assert result == []
        sig = (4, 6)
        result = generate_end_tuple_order(sig)
        assert result == []
        sig = (7, 4)
        result = generate_end_tuple_order(sig)
        assert result == []

    def test_end_tuple_order_2_2_2(self):
        sig = (2, 2, 2)
        result = generate_end_tuple_order(sig)
        assert result == [
            (1, 0, 0),
            (1, 0, 1),
            (2, 1, 1),
            (2, 1, 2),
            (0, 2, 2),
        ]

    def test_end_tuple_order_with_0s_2_2_2(self):
        sig = (0, 0, 0, 2, 2, 2, 0)
        result = generate_end_tuple_order(sig)
        assert result == [
            (4, 3, 3),
            (4, 3, 4),
            (5, 4, 4),
            (5, 4, 5),
            (3, 5, 5),
        ]

    def test_end_tuple_order_6_4_4(self):
        sig = (6, 4, 4)
        result = generate_end_tuple_order(sig)
        assert result == [
            (1, 0, 0),
            (1, 0, 1),
            (2, 1, 1),
            (2, 1, 2),
            (0, 2, 2),
        ]

    def test_end_tuple_order_4_2_8(self):
        sig = (4, 2, 8)
        result = generate_end_tuple_order(sig)
        assert result == [
            (0, 2, 2),
            (0, 2, 0),
            (1, 0, 0),
            (1, 0, 1),
            (2, 1, 1),
        ]

    def test_end_tuple_order_2_4_6(self):
        sig = (2, 4, 6)
        result = generate_end_tuple_order(sig)
        assert result == [
            (1, 2, 2),
            (1, 2, 1),
            (0, 1, 1),
            (0, 1, 0),
            (2, 0, 0),
        ]

    def test_end_tuple_order_2_3_6(self):
        sig = (2, 3, 6)
        result = generate_end_tuple_order(sig)
        assert result == [(1, 2), (0, 1)]

    def test_end_tuple_order_5_2_6(self):
        sig = (5, 2, 6)
        result = generate_end_tuple_order(sig)
        assert result == [(0, 2), (1, 0)]

    def test_end_tuple_order_4_2_3(self):
        sig = (4, 2, 3)
        result = generate_end_tuple_order(sig)
        assert result == [(2, 0), (1, 2)]

    def test_end_tuple_order_evens_2_2_2_2(self):
        sig = (2, 2, 2, 2)
        result = generate_end_tuple_order(sig)
        assert result == [
            (1, 0, 0),
            (1, 0, 1),
            (2, 1, 1),
            (2, 1, 2),
            (0, 2, 2),
            (3, 0, 2),
            (3, 2, 3),
            (1, 3, 3),
            (0, 1, 3),
        ]

    def test_end_tuple_order_odd_2_2_2_3(self):
        sig = (2, 2, 2, 3)
        result = generate_end_tuple_order(sig)
        assert result == [(0, 3), (1, 0), (2, 1)]

    def test_end_tuple_order_odd_2_2_2_2_3(self):
        sig = (2, 2, 2, 2, 3)
        result = generate_end_tuple_order(sig)
        assert result == [(0, 4), (1, 0), (2, 1), (3, 2)]

    def test_end_tuple_order_evens_2_2_2_2_2(self):
        sig = (2, 2, 2, 2, 2)
        result = generate_end_tuple_order(sig)
        assert result == [
            (1, 0, 0),
            (1, 0, 1),
            (2, 1, 1),
            (2, 1, 2),
            (0, 2, 2),
            (3, 0, 2),
            (3, 2, 3),
            (0, 3, 3),
            (1, 0, 3),
            (4, 1, 3),
            (4, 3, 4),
            (2, 4, 4),
            (1, 2, 4),
            (0, 1, 4),
        ]

    def test_end_tuple_order_evens_2_4_6_2_4_2(self):
        sig = (2, 4, 6, 2, 4, 2)
        result = generate_end_tuple_order(sig)
        assert result == [
            (1, 2, 2),
            (1, 2, 1),
            (4, 1, 1),
            (4, 1, 4),
            (2, 4, 4),
            (0, 2, 4),
            (0, 4, 0),
            (2, 0, 0),
            (1, 2, 0),
            (3, 1, 0),
            (3, 0, 3),
            (2, 3, 3),
            (1, 2, 3),
            (4, 1, 3),
            (5, 4, 3),
            (5, 3, 5),
            (0, 5, 5),
            (4, 0, 5),
            (1, 4, 5),
            (2, 1, 5),
        ]
        sorted_sig = (6, 4, 4, 2, 2, 2)
        sorted_result = generate_end_tuple_order(sorted_sig)
        assert sorted_result == [
            (1, 0, 0),
            (1, 0, 1),
            (2, 1, 1),
            (2, 1, 2),
            (0, 2, 2),
            (3, 0, 2),
            (3, 2, 3),
            (0, 3, 3),
            (1, 0, 3),
            (4, 1, 3),
            (4, 3, 4),
            (0, 4, 4),
            (1, 0, 4),
            (2, 1, 4),
            (5, 2, 4),
            (5, 4, 5),
            (3, 5, 5),
            (2, 3, 5),
            (1, 2, 5),
            (0, 1, 5),
        ]

    def test_end_tuple_order_odd_3_2_2_2_2_2_2_2(self):
        sig = (3, 2, 2, 2, 2, 2, 2, 2)
        result = generate_end_tuple_order(sig)
        assert result == [
            (1, 0),
            (2, 1),
            (3, 2),
            (4, 3),
            (5, 4),
            (6, 5),
            (7, 6),
        ]

    def test_end_tuple_order_evens_ten_twos(self):
        sig = tuple([2] * 10)
        result = generate_end_tuple_order(sig)
        assert result == [
            (1, 0, 0),
            (1, 0, 1),
            (2, 1, 1),
            (2, 1, 2),
            (0, 2, 2),
            (3, 0, 2),
            (3, 2, 3),
            (0, 3, 3),
            (1, 0, 3),
            (4, 1, 3),
            (4, 3, 4),
            (0, 4, 4),
            (1, 0, 4),
            (2, 1, 4),
            (5, 2, 4),
            (5, 4, 5),
            (0, 5, 5),
            (1, 0, 5),
            (2, 1, 5),
            (3, 2, 5),
            (6, 3, 5),
            (6, 5, 6),
            (0, 6, 6),
            (1, 0, 6),
            (2, 1, 6),
            (3, 2, 6),
            (4, 3, 6),
            (7, 4, 6),
            (7, 6, 7),
            (0, 7, 7),
            (1, 0, 7),
            (2, 1, 7),
            (3, 2, 7),
            (4, 3, 7),
            (5, 4, 7),
            (8, 5, 7),
            (8, 7, 8),
            (0, 8, 8),
            (1, 0, 8),
            (2, 1, 8),
            (3, 2, 8),
            (4, 3, 8),
            (5, 4, 8),
            (6, 5, 8),
            (9, 6, 8),
            (9, 8, 9),
            (7, 9, 9),
            (6, 7, 9),
            (5, 6, 9),
            (4, 5, 9),
            (3, 4, 9),
            (2, 3, 9),
            (1, 2, 9),
            (0, 1, 9),
        ]

    def test_end_tuple_order_odd_ten_evens(self):
        sig = [3]
        sig.extend([2] * 10)
        tuple_sig = tuple(sig)
        result = generate_end_tuple_order(tuple_sig)
        assert result == [
            (1, 0),
            (2, 1),
            (3, 2),
            (4, 3),
            (5, 4),
            (6, 5),
            (7, 6),
            (8, 7),
            (9, 8),
            (10, 9),
        ]

    def test_end_tuple_order_odd_3_3_2(self):
        sig = (3, 3, 2)
        result = generate_end_tuple_order(sig)
        assert result == [
            (0, 2),
        ]

    def test_end_tuple_order_odd_3_3_2_2(self):
        sig = (3, 3, 2, 2)
        result = generate_end_tuple_order(sig)
        assert result == [
            (0, 2),
            (0, 3),
        ]

    def test_end_tuple_order_odd_3_3_2_2_4_6_2(self):
        sig = (3, 3, 2, 2, 4, 6, 2)
        result = generate_end_tuple_order(sig)
        assert result == [
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
        ]

    def test_end_tuple_order_odd_3_3_2_2(self):
        sig = (2, 3, 2, 1)
        result = generate_end_tuple_order(sig)
        assert result == [
            (1, 0),
            (1, 2),
        ]


class Test_CycleCoverTailsOrdering:
    """
    Test whether the ordering of the tails of the cycle cover is the same as the tails ordering
    """

    def test_cycle_cover_2_2_2(self):
        sig = (2, 2, 2)
        cycle_cover = generate_cycle_cover(sig)
        end_tuple_order = generate_end_tuple_order(sig)
        cycle_cover_tails = [get_first_element(cycle)[-2:] for cycle in cycle_cover]
        for i, tail in enumerate(cycle_cover_tails[:-1]):
            assert set(tail) == set(end_tuple_order[i][-2:])
        assert len(cycle_cover_tails) - 1 == len(end_tuple_order)

    def test_cycle_cover_four_2s(self):
        sig = (2, 2, 2, 2)
        cycle_cover = generate_cycle_cover(sig)
        end_tuple_order = generate_end_tuple_order(sig)
        cycle_cover_tails = [get_first_element(cycle)[-2:] for cycle in cycle_cover]
        for i, tail in enumerate(cycle_cover_tails[:-1]):
            assert set(tail) == set(end_tuple_order[i][-2:])
        assert len(cycle_cover_tails) - 1 == len(end_tuple_order)

    # def test_cycle_cover_five_2s(self):
    # TODO fix this case in the functions
    #     sig = (2, 2, 2, 2, 2)
    #     cycle_cover = generate_cycle_cover(sig)
    #     end_tuple_order = generate_end_tuple_order(sig)
    #     cycle_cover_tails = [get_first_element(cycle)[-2:] for cycle in cycle_cover]
    #     for i, tail in enumerate(cycle_cover_tails[:-1]):
    #         assert set(tail) == set(end_tuple_order[i][-2:])
    #     assert len(cycle_cover_tails) - 1 == len(end_tuple_order)

    def test_cycle_cover_unsorted_all_even_small(self):
        sig = (0, 2, 0, 4, 2, 0, 2)
        cycle_cover = generate_cycle_cover(sig)
        end_tuple_order = generate_end_tuple_order(sig)
        cycle_cover_tails = [get_first_element(cycle)[-2:] for cycle in cycle_cover]
        for i, tail in enumerate(cycle_cover_tails[:-1]):
            assert set(tail) == set(end_tuple_order[i][-2:])
        assert len(cycle_cover_tails) - 1 == len(end_tuple_order)

    def test_cycle_cover_unsorted_all_even_large(self):
        sig = (2, 4, 6, 0, 2)
        cycle_cover = generate_cycle_cover(sig)
        end_tuple_order = generate_end_tuple_order(sig)
        cycle_cover_tails = [get_first_element(cycle)[-2:] for cycle in cycle_cover]
        for i, tail in enumerate(cycle_cover_tails[:-1]):
            assert set(tail) == set(end_tuple_order[i][-2:])
        assert len(cycle_cover_tails) - 1 == len(end_tuple_order)

    # @pytest.mark.slow
    # def test_cycle_cover_six_2s(self):
    #     sig = (2, 2, 2, 2, 2, 2)
    #     cycle_cover = generate_cycle_cover(sig)
    #     end_tuple_order = generate_end_tuple_order(sig)
    #     cycle_cover_tails = [get_first_element(cycle)[-2:] for cycle in cycle_cover]
    #     for i, tail in enumerate(cycle_cover_tails[:-1]):
    #         assert set(tail) == set(end_tuple_order[i][-2:])
    #     assert len(cycle_cover_tails) - 1 == len(end_tuple_order)

    def test_cycle_cover_3_2_2(self):
        sig = (3, 2, 2)
        cycle_cover = generate_cycle_cover(sig)
        end_tuple_order = generate_end_tuple_order(sig)
        cycle_cover_tails = [get_first_element(cycle)[-1:] for cycle in cycle_cover]
        for i, tail in enumerate(cycle_cover_tails[:-1]):
            assert set(tail) == set(end_tuple_order[i][-1:])
        assert len(cycle_cover_tails) - 1 == len(end_tuple_order)

    def test_cycle_cover_unsorted_2_2_3_2(self):
        sig = (2, 2, 3, 2)
        cycle_cover = generate_cycle_cover(sig)
        end_tuple_order = generate_end_tuple_order(sig)
        cycle_cover_tails = [get_first_element(cycle)[-1:] for cycle in cycle_cover]
        for i, tail in enumerate(cycle_cover_tails[:-1]):
            assert set(tail) == set(end_tuple_order[i][-1:])
        assert len(cycle_cover_tails) - 1 == len(end_tuple_order)

    def test_cycle_cover_unsorted_2_4_2_3(self):
        sig = (2, 4, 2, 3)
        cycle_cover = generate_cycle_cover(sig)
        end_tuple_order = generate_end_tuple_order(sig)
        cycle_cover_tails = [get_first_element(cycle)[-1:] for cycle in cycle_cover]
        for i, tail in enumerate(cycle_cover_tails[:-1]):
            assert set(tail) == set(end_tuple_order[i][-1:])
        assert len(cycle_cover_tails) - 1 == len(end_tuple_order)


class Test_ConnectCycleCoverEdgeCases:
    def test_connect_cycle_cover_negative(self):
        with pytest.raises(ValueError):
            get_connected_cycle_cover((-1,))
        with pytest.raises(ValueError):
            get_connected_cycle_cover((1, 2, -2, 4))

    def test_connect_cycle_cover_empty(self):
        assert get_connected_cycle_cover(tuple()) == []

    def test_connect_cycle_cover_one_element(self):
        # these are stutter permutations
        assert get_connected_cycle_cover((0,)) == []
        assert get_connected_cycle_cover((1,)) == []
        assert get_connected_cycle_cover((2,)) == []
        assert get_connected_cycle_cover((5,)) == []
        assert get_connected_cycle_cover((0, 2)) == []
        assert get_connected_cycle_cover((0, 0, 0, 0, 2)) == []

    def test_connect_cycle_cover_binary(self):
        assert get_connected_cycle_cover((1, 1)) == [(0, 1), (1, 0)]
        assert get_connected_cycle_cover((4, 1)) == [
            (0, 0, 0, 1, 0),
            (0, 0, 1, 0, 0),
            (0, 1, 0, 0, 0),
            (1, 0, 0, 0, 0),
        ]
        assert get_connected_cycle_cover((1, 3)) == [
            (1, 1, 1, 0),
            (1, 1, 0, 1),
            (1, 0, 1, 1),
            (0, 1, 1, 1),
        ]
        assert get_connected_cycle_cover((2, 2)) == [
            (1, 0, 0, 1),
            (0, 1, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
        ]
        result_5_5 = get_connected_cycle_cover((5, 5))
        assert len(result_5_5) == multinomial((5, 5))
        assert len(result_5_5) == len(set(result_5_5))
        assert pathQ(result_5_5)

        result_3_7 = get_connected_cycle_cover((3, 7))
        assert len(result_3_7) == multinomial((3, 7))
        assert len(result_3_7) == len(set(result_3_7))
        assert pathQ(result_3_7)

    def test_connect_cycle_cover_binary_with_stutters(self):
        sig_6_4 = (6, 4)
        result_6_4 = get_connected_cycle_cover(sig_6_4)
        assert len(result_6_4) == multinomial(sig_6_4) - len(
            stutterPermutations(sig_6_4)
        )
        assert len(result_6_4) == len(set(result_6_4))
        assert cycleQ(result_6_4)

        sig_7_2 = (7, 2)
        result_7_2 = get_connected_cycle_cover(sig_7_2)
        assert len(result_7_2) == multinomial(sig_7_2) - len(
            stutterPermutations(sig_7_2)
        )
        assert len(result_7_2) == len(set(result_7_2))
        assert pathQ(result_7_2)

        sig_4_5 = (4, 5)
        result_4_5 = get_connected_cycle_cover(sig_4_5)
        assert len(result_4_5) == multinomial(sig_4_5) - len(
            stutterPermutations(sig_4_5)
        )
        assert len(result_4_5) == len(set(result_4_5))
        assert pathQ(result_4_5)

    def test_connect_cycle_cover_SJT(self):
        sjt_5 = (1, 1, 1, 1, 1)
        result_sjt_5 = get_connected_cycle_cover(sjt_5)
        assert len(result_sjt_5) == multinomial(sjt_5)
        assert len(result_sjt_5) == len(set(result_sjt_5))
        assert cycleQ(result_sjt_5)

        sjt_6 = (1, 1, 1, 1, 1, 1)
        result_sjt_6 = get_connected_cycle_cover(sjt_6)
        assert len(result_sjt_6) == multinomial(sjt_6)
        assert len(result_sjt_6) == len(set(result_sjt_6))
        assert cycleQ(result_sjt_6)

        sjt_7 = (1, 1, 1, 1, 1, 1, 1)
        result_sjt_7 = get_connected_cycle_cover(sjt_7)
        assert len(result_sjt_7) == multinomial(sjt_7)
        assert len(result_sjt_7) == len(set(result_sjt_7))
        assert cycleQ(result_sjt_7)


class Test_ConnectCycleCoverEven11:
    def test_connect_cycle_cover_2_1_1(self):
        sig_2_1_1 = (2, 1, 1)
        result_2_1_1 = get_connected_cycle_cover(sig_2_1_1)
        assert len(result_2_1_1) == multinomial(sig_2_1_1)
        assert len(result_2_1_1) == len(set(result_2_1_1))
        assert pathQ(result_2_1_1)

    def test_connect_cycle_cover_1_6_1(self):
        sig_1_6_1 = (1, 6, 1)
        result_6_1_1 = get_connected_cycle_cover(sig_1_6_1)
        assert len(result_6_1_1) == multinomial(sig_1_6_1)
        assert len(result_6_1_1) == len(set(result_6_1_1))
        assert pathQ(result_6_1_1)

    def test_connect_cycle_cover_1_1_8(self):
        sig_1_1_8 = (1, 1, 8)
        result_1_1_8 = get_connected_cycle_cover(sig_1_1_8)
        assert len(result_1_1_8) == multinomial(sig_1_1_8)
        assert len(result_1_1_8) == len(set(result_1_1_8))
        assert pathQ(result_1_1_8)


class Test_ConnectCycleCoverEvenOdd1:
    def test_connect_cycle_cover_4_3_1(self):
        signature = (4, 3, 1)
        cycles = get_connected_cycle_cover(signature)
        assert len(cycles) == multinomial(signature)
        assert cycleQ(cycles)

    def test_connect_cycle_cover_3_6_1(self):
        signature = (3, 6, 1)
        cycles = get_connected_cycle_cover(signature)
        assert len(cycles) == multinomial(signature)
        assert cycleQ(cycles)

    def test_connect_cycle_cover_1_5_6(self):
        signature = (1, 5, 6)
        cycles = get_connected_cycle_cover(signature)
        assert len(cycles) == multinomial(signature)
        assert cycleQ(cycles)

    def test_connect_cycle_cover_4_1_7(self):
        signature = (4, 1, 7)
        cycles = get_connected_cycle_cover(signature)
        assert len(cycles) == multinomial(signature)
        assert cycleQ(cycles)

    def test_connect_cycle_cover_1_8_3(self):
        signature = (1, 8, 3)
        cycles = get_connected_cycle_cover(signature)
        assert len(cycles) == multinomial(signature)
        assert cycleQ(cycles)


class Test_ConnectCycleCoverEquivStachowiak:
    def test_connect_cycle_cover_stachowiak(self):
        stachowiak_3_5_2 = (3, 5, 2)
        result_stachowiak_3_5_2 = get_connected_cycle_cover(stachowiak_3_5_2)
        assert len(result_stachowiak_3_5_2) == multinomial(stachowiak_3_5_2)
        assert len(result_stachowiak_3_5_2) == len(set(result_stachowiak_3_5_2))
        assert cycleQ(result_stachowiak_3_5_2)

        stachowiak_4_3_3 = (4, 3, 3)
        result_stachowiak_4_3_3 = get_connected_cycle_cover(stachowiak_4_3_3)
        assert len(result_stachowiak_4_3_3) == multinomial(stachowiak_4_3_3)
        assert len(result_stachowiak_4_3_3) == len(set(result_stachowiak_4_3_3))
        assert cycleQ(result_stachowiak_4_3_3)

        stachowiak_3_3_1_1 = (3, 3, 1, 1)
        result_stachowiak_3_3_1_1 = get_connected_cycle_cover(stachowiak_3_3_1_1)
        assert len(result_stachowiak_3_3_1_1) == multinomial(stachowiak_3_3_1_1)
        assert len(result_stachowiak_3_3_1_1) == len(set(result_stachowiak_3_3_1_1))
        assert cycleQ(result_stachowiak_3_3_1_1)


class Test_ConnectCycleCoverEvenOrOdd21:
    def test_connect_cycle_cover_odd_2_1(self):
        # note that odd-2-1 is a path if odd equals 1
        sig_3_2_1 = (3, 2, 1)
        result_3_2_1 = get_connected_cycle_cover(sig_3_2_1)
        assert len(result_3_2_1) == multinomial(sig_3_2_1)
        assert len(result_3_2_1) == len(set(result_3_2_1))
        assert cycleQ(result_3_2_1)

        sig_5_1_2 = (5, 1, 2)
        result_5_1_2 = get_connected_cycle_cover(sig_5_1_2)
        assert len(result_5_1_2) == multinomial(sig_5_1_2)
        assert len(result_5_1_2) == len(set(result_5_1_2))
        assert cycleQ(result_5_1_2)

    def test_connect_cycle_cover_2_2_1(self):
        sig_2_2_1 = (2, 2, 1)
        result_2_2_1 = get_connected_cycle_cover(sig_2_2_1)
        assert len(result_2_2_1) == multinomial(sig_2_2_1) - len(
            stutterPermutations(sig_2_2_1)
        )
        assert len(result_2_2_1) == len(set(result_2_2_1))
        assert cycleQ(result_2_2_1)

    def test_connect_cycle_cover_4_1_2(self):
        sig_4_1_2 = (4, 1, 2)
        result_4_1_2 = get_connected_cycle_cover(sig_4_1_2)
        assert len(result_4_1_2) == multinomial(sig_4_1_2) - len(
            stutterPermutations(sig_4_1_2)
        )
        assert len(result_4_1_2) == len(set(result_4_1_2))
        assert cycleQ(result_4_1_2)

    def test_connect_cycle_cover_1_6_2(self):
        sig_1_6_2 = (1, 6, 2)
        result_1_6_2 = get_connected_cycle_cover(sig_1_6_2)
        assert len(result_1_6_2) == multinomial(sig_1_6_2) - len(
            stutterPermutations(sig_1_6_2)
        )
        assert len(result_1_6_2) == len(set(result_1_6_2))
        assert cycleQ(result_1_6_2)


class Test_ConnectCycleCoverAllEven:
    def test_connect_cycle_cover_2_2_2(self):
        sig_2_2_2 = (2, 2, 2)
        result_2_2_2 = get_connected_cycle_cover(sig_2_2_2)
        assert len(result_2_2_2) == multinomial(sig_2_2_2) - len(
            stutterPermutations(sig_2_2_2)
        )
        assert len(result_2_2_2) == len(set(result_2_2_2))
        assert cycleQ(result_2_2_2)

    def test_connect_cycle_cover_4_2_2(self):
        sig_4_2_2 = (4, 2, 2)
        result_4_2_2 = get_connected_cycle_cover(sig_4_2_2)
        assert len(result_4_2_2) == multinomial(sig_4_2_2) - len(
            stutterPermutations(sig_4_2_2)
        )
        assert len(result_4_2_2) == len(set(result_4_2_2))
        assert cycleQ(result_4_2_2)


class Test_ConnectCycleCoverAllButOneEven:
    def test_connect_cycle_cover_2_2_3(self):
        sig_2_2_3 = (2, 2, 3)
        result_2_2_3 = get_connected_cycle_cover(sig_2_2_3)
        assert len(result_2_2_3) == multinomial(sig_2_2_3) - len(
            stutterPermutations(sig_2_2_3)
        )
        assert len(result_2_2_3) == len(set(result_2_2_3))
        assert cycleQ(result_2_2_3)

    def test_connect_cycle_cover_4_3_2(self):
        sig_4_3_2 = (4, 3, 2)
        result_4_3_2 = get_connected_cycle_cover(sig_4_3_2)
        assert len(result_4_3_2) == multinomial(sig_4_3_2) - len(
            stutterPermutations(sig_4_3_2)
        )
        assert len(result_4_3_2) == len(set(result_4_3_2))
        assert cycleQ(result_4_3_2)
