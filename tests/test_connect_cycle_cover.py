import pytest

from connect_cycle_cover import generate_end_tuple_order, get_connected_cycle_cover
from cycle_cover import generate_cycle_cover
from helper_operations.path_operations import cycleQ, pathQ
from helper_operations.permutation_graphs import multinomial, stutterPermutations


class Test_TailsOrdering:
    def test_end_tuple_order_two_or_more_odd_not_possible(self):
        sig_two_or_more_odd = [3, 3, 2]
        with pytest.raises(ValueError):
            generate_end_tuple_order(
                sig_two_or_more_odd, generate_cycle_cover(sig_two_or_more_odd)
            )
        with pytest.raises(ValueError):
            generate_end_tuple_order(
                sig_two_or_more_odd, generate_cycle_cover(sig_two_or_more_odd)
            )
        with pytest.raises(ValueError):
            generate_end_tuple_order(
                sig_two_or_more_odd, generate_cycle_cover(sig_two_or_more_odd)
            )
        with pytest.raises(ValueError):
            generate_end_tuple_order(
                sig_two_or_more_odd, generate_cycle_cover(sig_two_or_more_odd)
            )        

    def test_end_tuple_order_one_element(self):
        sig = [2]
        result = generate_end_tuple_order(sig, generate_cycle_cover(sig))
        assert result == [(0, 0)]
        sig = [0]
        assert generate_end_tuple_order(sig, generate_cycle_cover(sig)) == [()]
        sig = [1]
        result = generate_end_tuple_order(sig, generate_cycle_cover(sig))
        assert result == [(0,)]

    def test_end_tuple_order_two_elements(self):
        sig = [2, 2]
        result = generate_end_tuple_order(sig, generate_cycle_cover(sig))
        assert result == [(0, 1)]
        sig = [4, 3]
        result = generate_end_tuple_order(sig, generate_cycle_cover(sig))
        assert result == [(0,)]
        sig = [6, 2]
        result = generate_end_tuple_order(sig, generate_cycle_cover(sig))
        assert result == [(0, 1)]
        sig = [3, 6]
        result = generate_end_tuple_order(sig, generate_cycle_cover(sig))
        assert result == [(1,)]
        sig = [4, 6]
        result = generate_end_tuple_order(sig, generate_cycle_cover(sig))
        assert result == [(1, 0)]
        sig = [7, 4]
        result = generate_end_tuple_order(sig, generate_cycle_cover(sig))
        assert result == [(1,)]


class Test_ConnectCycleCover:
    def test_connect_cycle_cover_negative(self):
        with pytest.raises(ValueError):
            get_connected_cycle_cover([-1])
        with pytest.raises(ValueError):
            get_connected_cycle_cover([1, 2, -2, 4])

    def test_connect_cycle_cover_empty(self):
        assert get_connected_cycle_cover([]) == []

    def test_connect_cycle_cover_one_element(self):
        assert get_connected_cycle_cover([0]) == []
        assert get_connected_cycle_cover([1]) == [(0,)]
        assert get_connected_cycle_cover([2]) == [(0, 0)]
        assert get_connected_cycle_cover([5]) == [(0, 0, 0, 0, 0)]
        assert get_connected_cycle_cover([0, 2]) == [(1, 1)]
        assert get_connected_cycle_cover([0, 0, 0, 0, 2]) == [(4, 4)]

    def test_connect_cycle_cover_binary(self):
        assert get_connected_cycle_cover([1, 1]) == [(0, 1), (1, 0)]
        assert get_connected_cycle_cover([4, 1]) == [
            (0, 0, 0, 1, 0),
            (0, 0, 1, 0, 0),
            (0, 1, 0, 0, 0),
            (1, 0, 0, 0, 0),
        ]
        assert get_connected_cycle_cover([1, 3]) == [
            (1, 1, 1, 0),
            (1, 1, 0, 1),
            (1, 0, 1, 1),
            (0, 1, 1, 1),
        ]
        assert get_connected_cycle_cover([2, 2]) == [
            (1, 0, 0, 1),
            (0, 1, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
        ]
        result_5_5 = get_connected_cycle_cover([5, 5])
        assert len(result_5_5) == multinomial([5, 5])
        assert len(result_5_5) == len(set(result_5_5))
        assert pathQ(result_5_5)

        result_3_7 = get_connected_cycle_cover([3, 7])
        assert len(result_3_7) == multinomial([3, 7])
        assert len(result_3_7) == len(set(result_3_7))
        assert pathQ(result_3_7)

    def test_connect_cycle_cover_binary_with_stutters(self):
        sig_6_4 = [6, 4]
        result_6_4 = get_connected_cycle_cover(sig_6_4)
        assert len(result_6_4) == multinomial(sig_6_4) - len(
            stutterPermutations(sig_6_4)
        )
        assert len(result_6_4) == len(set(result_6_4))
        assert cycleQ(result_6_4)

        sig_7_2 = [7, 2]
        result_7_2 = get_connected_cycle_cover(sig_7_2)
        assert len(result_7_2) == multinomial(sig_7_2) - len(
            stutterPermutations(sig_7_2)
        )
        assert len(result_7_2) == len(set(result_7_2))
        assert pathQ(result_7_2)

        sig_4_5 = [4, 5]
        result_4_5 = get_connected_cycle_cover(sig_4_5)
        assert len(result_4_5) == multinomial(sig_4_5) - len(
            stutterPermutations(sig_4_5)
        )
        assert len(result_4_5) == len(set(result_4_5))
        assert pathQ(result_4_5)

    def test_connect_cycle_cover_SJT(self):
        sjt_5 = [1, 1, 1, 1, 1]
        result_sjt_5 = get_connected_cycle_cover(sjt_5)
        assert len(result_sjt_5) == multinomial(sjt_5)
        assert len(result_sjt_5) == len(set(result_sjt_5))
        assert cycleQ(result_sjt_5)

        sjt_6 = [1, 1, 1, 1, 1, 1]
        result_sjt_6 = get_connected_cycle_cover(sjt_6)
        assert len(result_sjt_6) == multinomial(sjt_6)
        assert len(result_sjt_6) == len(set(result_sjt_6))
        assert cycleQ(result_sjt_6)

    def test_connect_cycle_cover_stachowiak(self):
        stachowiak_3_5_2 = [3, 5, 2]
        result_stachowiak_3_5_2 = get_connected_cycle_cover(stachowiak_3_5_2)
        assert len(result_stachowiak_3_5_2) == multinomial(stachowiak_3_5_2)
        assert len(result_stachowiak_3_5_2) == len(set(result_stachowiak_3_5_2))
        assert cycleQ(result_stachowiak_3_5_2)

        stachowiak_4_3_3 = [4, 3, 3]
        result_stachowiak_4_3_3 = get_connected_cycle_cover(stachowiak_4_3_3)
        assert len(result_stachowiak_4_3_3) == multinomial(stachowiak_4_3_3)
        assert len(result_stachowiak_4_3_3) == len(set(result_stachowiak_4_3_3))
        assert cycleQ(result_stachowiak_4_3_3)

        stachowiak_3_3_1_1 = [3, 3, 1, 1]
        result_stachowiak_3_3_1_1 = get_connected_cycle_cover(stachowiak_3_3_1_1)
        assert len(result_stachowiak_3_3_1_1) == multinomial(stachowiak_3_3_1_1)
        assert len(result_stachowiak_3_3_1_1) == len(set(result_stachowiak_3_3_1_1))
        assert cycleQ(result_stachowiak_3_3_1_1)

    def test_connect_cycle_cover_odd_2_1(self):
        # note that odd-2-1 is a path if odd equals 1
        sig_3_2_1 = [3, 2, 1]
        result_3_2_1 = get_connected_cycle_cover(sig_3_2_1)
        assert len(result_3_2_1) == multinomial(sig_3_2_1)
        assert len(result_3_2_1) == len(set(result_3_2_1))
        assert cycleQ(result_3_2_1)

        sig_5_1_2 = [5, 1, 2]
        result_5_1_2 = get_connected_cycle_cover(sig_5_1_2)
        assert len(result_5_1_2) == multinomial(sig_5_1_2)
        assert len(result_5_1_2) == len(set(result_5_1_2))
        assert cycleQ(result_5_1_2)

    def test_connect_cycle_cover_2_1_1(self):
        sig_2_1_1 = [2, 1, 1]
        result_2_1_1 = get_connected_cycle_cover(sig_2_1_1)
        assert len(result_2_1_1) == multinomial(sig_2_1_1)
        assert len(result_2_1_1) == len(set(result_2_1_1))
        assert pathQ(result_2_1_1)

    def test_connect_cycle_cover_1_6_1(self):
        sig_1_6_1 = [1, 6, 1]
        result_6_1_1 = get_connected_cycle_cover(sig_1_6_1)
        assert len(result_6_1_1) == multinomial(sig_1_6_1)
        assert len(result_6_1_1) == len(set(result_6_1_1))
        assert pathQ(result_6_1_1)

    def test_connect_cycle_cover_1_1_8(self):
        sig_1_1_8 = [1, 1, 8]
        result_1_1_8 = get_connected_cycle_cover(sig_1_1_8)
        assert len(result_1_1_8) == multinomial(sig_1_1_8)
        assert len(result_1_1_8) == len(set(result_1_1_8))
        assert pathQ(result_1_1_8)

    def test_connect_cycle_cover_2_2_1(self):
        sig_2_2_1 = [2, 2, 1]
        result_2_2_1 = get_connected_cycle_cover(sig_2_2_1)
        print(result_2_2_1)
        assert len(result_2_2_1) == multinomial(sig_2_2_1) - len(
            stutterPermutations(sig_2_2_1)
        )
        assert len(result_2_2_1) == len(set(result_2_2_1))
        assert cycleQ(result_2_2_1)

    def test_connect_cycle_cover_4_1_2(self):
        sig_4_1_2 = [4, 1, 2]
        result_4_1_2 = get_connected_cycle_cover(sig_4_1_2)
        assert len(result_4_1_2) == multinomial(sig_4_1_2) - len(
            stutterPermutations(sig_4_1_2)
        )
        assert len(result_4_1_2) == len(set(result_4_1_2))
        assert cycleQ(result_4_1_2)

    def test_connect_cycle_cover_1_6_2(self):
        sig_1_6_2 = [1, 6, 2]
        result_1_6_2 = get_connected_cycle_cover(sig_1_6_2)
        assert len(result_1_6_2) == multinomial(sig_1_6_2) - len(
            stutterPermutations(sig_1_6_2)
        )
        assert len(result_1_6_2) == len(set(result_1_6_2))
        assert cycleQ(result_1_6_2)

    def test_connect_cycle_cover_2_2_2(self):
        sig_2_2_2 = [2, 2, 2]
        result_2_2_2 = get_connected_cycle_cover(sig_2_2_2)
        assert len(result_2_2_2) == multinomial(sig_2_2_2) - len(
            stutterPermutations(sig_2_2_2)
        )
        assert len(result_2_2_2) == len(set(result_2_2_2))
        assert cycleQ(result_2_2_2)

    def test_connect_cycle_cover_2_2_3(self):
        sig_2_2_3 = [2, 2, 3]
        result_2_2_3 = get_connected_cycle_cover(sig_2_2_3)
        assert len(result_2_2_3) == multinomial(sig_2_2_3) - len(
            stutterPermutations(sig_2_2_3)
        )
        assert len(result_2_2_3) == len(set(result_2_2_3))
        assert cycleQ(result_2_2_3)

    def test_connect_cycle_cover_4_2_2(self):
        sig_4_2_2 = [4, 2, 2]
        result_4_2_2 = get_connected_cycle_cover(sig_4_2_2)
        assert len(result_4_2_2) == multinomial(sig_4_2_2) - len(
            stutterPermutations(sig_4_2_2)
        )
        assert len(result_4_2_2) == len(set(result_4_2_2))
        assert cycleQ(result_4_2_2)
