import pytest

from cycle_cover import generate_cycle_cover, get_connected_cycle_cover
from helper_operations.cycle_cover_connections import generate_end_tuple_order
from helper_operations.path_operations import cycleQ, get_first_element, pathQ
from helper_operations.permutation_graphs import multinomial, stutterPermutations


class Test_GuaranteedEdges_Even_2_1_subcycles:
    def test_guaranteed_edges_Odd_2_1(self):
        for odd_val in [3, 5, 9, 13]:
            cc = get_connected_cycle_cover((odd_val, 2, 1))
            # guaranteed_top_row
            for i in range(0, odd_val, 2):
                index_1 = cc.index((0,) * (i) + (1,) + (0,) * (odd_val - i) + (1, 2))
                index_2 = cc.index(
                    (0,) * (i + 1) + (1,) + (0,) * (odd_val - 1 - i) + (1, 2)
                )
                assert (
                    abs(index_1 - index_2) == 1 or abs(index_1 - index_2) == len(cc) - 1
                )

            # test_guaranteed_stutter_cross_edge
            node_3 = (0,) * (odd_val - 1) + (1, 1, 2, 0)
            node_4 = (0,) * (odd_val - 1) + (1, 2, 1, 0)
            index_3 = cc.index(node_3)
            index_4 = cc.index(node_4)
            assert abs(index_3 - index_4) == 1 or abs(index_3 - index_4) == len(cc) - 1

            # test_guaranteed_flip_first
            node_5 = (1, 2) + (0,) * (odd_val) + (1,)
            node_6 = (2, 1) + (0,) * (odd_val) + (1,)
            index_5 = cc.index(node_5)
            index_6 = cc.index(node_6)
            assert abs(index_5 - index_6) == 1 or abs(index_5 - index_6) == len(cc) - 1

            # test_guaranteed_e_to_below
            node_8 = (1, 0, 2) + (0,) * (odd_val - 1) + (1,)
            index_8 = cc.index(node_8)
            # reuses node_5
            assert abs(index_5 - index_8) == 1 or abs(index_5 - index_8) == len(cc) - 1

            # test_guaranteed_two_in_middle
            node_9 = (0,) * (odd_val) + (2, 1, 1)
            node_10 = (0,) * (odd_val - 1) + (2, 0, 1, 1)
            index_9 = cc.index(node_9)
            index_10 = cc.index(node_10)
            assert (
                abs(index_9 - index_10) == 1 or abs(index_9 - index_10) == len(cc) - 1
            )

            # test_guaranteed_two_at_start
            node_11 = (2, 1, 1) + (0,) * (odd_val)
            node_12 = (1, 2, 1) + (0,) * (odd_val)
            index_11 = cc.index(node_11)
            index_12 = cc.index(node_12)
            assert (
                abs(index_11 - index_12) == 1 or abs(index_11 - index_12) == len(cc) - 1
            )

            # test_guaranteed_from_even_1_1
            node_13 = (2, 0) + (0,) * (odd_val - 2) + (1, 1, 0)
            node_14 = (0, 2) + (0,) * (odd_val - 2) + (1, 1, 0)
            index_13 = cc.index(node_13)
            index_14 = cc.index(node_14)
            assert (
                abs(index_13 - index_14) == 1 or abs(index_13 - index_14) == len(cc) - 1
            )

            # test_guaranteed_top_right
            node_15 = (0,) * (odd_val) + (2, 1, 1)
            node_16 = (0,) * (odd_val) + (1, 2, 1)
            index_15 = cc.index(node_15)
            index_16 = cc.index(node_16)
            assert (
                abs(index_15 - index_16) == 1 or abs(index_15 - index_16) == len(cc) - 1
            )

            # test_guaranteed_top_right_two_down
            node_17 = (0,) * (odd_val) + (1, 1, 2)
            index_17 = cc.index(node_17)
            # reuses node_16
            assert (
                abs(index_17 - index_16) == 1 or abs(index_17 - index_16) == len(cc) - 1
            )

    def test_guaranteed_edges_Even_1_1(self):
        for even_val in [2, 4, 8, 12]:
            cc = get_connected_cycle_cover((even_val, 1, 1))

            # test_guaranteed_1zeros2
            node_0 = (0, 1) + (0,) * (even_val - 1) + (2,)
            node_1 = (1,) + (0,) * (even_val) + (2,)
            node_2 = (1,) + (0,) * (even_val - 1) + (2, 0)
            index_0 = cc.index(node_0)
            index_1 = cc.index(node_1)
            index_2 = cc.index(node_2)
            assert abs(index_0 - index_1) == 1 or abs(index_0 - index_1) == len(cc) - 1
            assert abs(index_2 - index_1) == 1 or abs(index_2 - index_1) == len(cc) - 1

            # test_guaranteed_2zeros1
            node_3 = (0, 2) + (0,) * (even_val - 1) + (1,)
            node_4 = (2,) + (0,) * (even_val) + (1,)
            node_5 = (2,) + (0,) * (even_val - 1) + (1, 0)
            index_3 = cc.index(node_3)
            index_4 = cc.index(node_4)
            index_5 = cc.index(node_5)
            assert abs(index_3 - index_4) == 1 or abs(index_3 - index_4) == len(cc) - 1
            assert abs(index_5 - index_4) == 1 or abs(index_5 - index_4) == len(cc) - 1


class Test_GuaranteedEdges_Odd_Odd_1:
    def test_guaranteed_edges_Odd_Odd_1(self):
        for odd_val_1 in [3, 5, 7, 9]:
            for odd_val_2 in range(3, odd_val_1 + 1, 2):
                if odd_val_2 == 7 or (odd_val_1 == 9 and odd_val_2 > 3):
                    # the (7, 7, 1) - (9, 5, 1) - (9, 7, 1) - (9, 9, 1) are too large
                    # for my laptop memory due to Verhoeff's algorithm
                    break
                print(f"computing odd-odd {odd_val_1, odd_val_2}")
                cc = get_connected_cycle_cover((odd_val_1, odd_val_2, 1))

                # test_guaranteed_zeros2ones
                node_0 = (0,) * (odd_val_1 - 1) + (2, 0) + (1,) * (odd_val_2)
                node_1 = (0,) * (odd_val_1) + (2,) + (1,) * (odd_val_2)
                node_2 = (0,) * (odd_val_1) + (1, 2) + (1,) * (odd_val_2 - 1)
                index_0 = cc.index(node_0)
                index_1 = cc.index(node_1)
                index_2 = cc.index(node_2)
                assert (
                    abs(index_0 - index_1) == 1 or abs(index_0 - index_1) == len(cc) - 1
                )
                assert (
                    abs(index_2 - index_1) == 1 or abs(index_2 - index_1) == len(cc) - 1
                )

                # test_guaranteed_ones2zeros
                node_3 = (1,) * (odd_val_2 - 1) + (2, 1) + (0,) * (odd_val_1)
                node_4 = (1,) * (odd_val_2) + (2,) + (0,) * (odd_val_1)
                node_5 = (1,) * (odd_val_2) + (0, 2) + (0,) * (odd_val_1 - 1)
                index_3 = cc.index(node_3)
                index_4 = cc.index(node_4)
                index_5 = cc.index(node_5)
                assert (
                    abs(index_3 - index_4) == 1 or abs(index_3 - index_4) == len(cc) - 1
                )
                assert (
                    abs(index_5 - index_4) == 1 or abs(index_5 - index_4) == len(cc) - 1
                )

                # test_guaranteed_12start and 02 start
                node_6 = (1, 2) + (0,) * (odd_val_1) + (1,) * (odd_val_2 - 1)
                node_7 = (1, 0, 2) + (0,) * (odd_val_1 - 1) + (1,) * (odd_val_2 - 1)
                index_6 = cc.index(node_6)
                index_7 = cc.index(node_7)
                assert (
                    abs(index_6 - index_7) == 1 or abs(index_6 - index_7) == len(cc) - 1
                )
                node_8 = (0, 2) + (1,) * (odd_val_2) + (0,) * (odd_val_1 - 1)
                node_9 = (0, 1, 2) + (1,) * (odd_val_2 - 1) + (0,) * (odd_val_1 - 1)
                index_8 = cc.index(node_8)
                index_9 = cc.index(node_9)
                assert (
                    abs(index_8 - index_9) == 1 or abs(index_8 - index_9) == len(cc) - 1
                )

                # test_guaranteed_2start
                node_10 = (2,) + (0,) * (odd_val_1) + (1,) * (odd_val_2)
                node_11 = (0, 2) + (0,) * (odd_val_1 - 1) + (1,) * (odd_val_2)
                index_10 = cc.index(node_10)
                index_11 = cc.index(node_11)
                assert (
                    abs(index_10 - index_11) == 1
                    or abs(index_10 - index_11) == len(cc) - 1
                )
                node_12 = (2,) + (1,) * (odd_val_2) + (0,) * (odd_val_1)
                node_13 = (1, 2) + (1,) * (odd_val_2 - 1) + (0,) * (odd_val_1)
                index_12 = cc.index(node_12)
                index_13 = cc.index(node_13)
                assert (
                    abs(index_12 - index_13) == 1
                    or abs(index_12 - index_13) == len(cc) - 1
                )


class Test_GuaranteedEdges_Even_Odd_1:
    def test_guaranteed_edges_Even_Odd_1(self):
        # even is larger than odd
        for even_val_0 in [4, 6, 8]:
            for odd_val_1 in range(3, even_val_0 + 1, 2):
                if even_val_0 == 8 and odd_val_1 > 3:
                    break
                print(f"computing even-odd {(even_val_0, odd_val_1, 1)}")
                cc = get_connected_cycle_cover((even_val_0, odd_val_1, 1))

                # test_guaranteed_zeros2ones
                node_0 = (0,) * (even_val_0 - 1) + (2, 0) + (1,) * (odd_val_1)
                node_1 = (0,) * (even_val_0) + (2,) + (1,) * (odd_val_1)
                node_2 = (0,) * (even_val_0) + (1, 2) + (1,) * (odd_val_1 - 1)
                index_0 = cc.index(node_0)
                index_1 = cc.index(node_1)
                index_2 = cc.index(node_2)
                assert (
                    abs(index_0 - index_1) == 1 or abs(index_0 - index_1) == len(cc) - 1
                )
                assert (
                    abs(index_2 - index_1) == 1 or abs(index_2 - index_1) == len(cc) - 1
                )

                # test_guaranteed_ones2zeros
                node_3 = (1,) * (odd_val_1 - 1) + (2, 1) + (0,) * (even_val_0)
                node_4 = (1,) * (odd_val_1) + (2,) + (0,) * (even_val_0)
                node_5 = (1,) * (odd_val_1) + (0, 2) + (0,) * (even_val_0 - 1)
                index_3 = cc.index(node_3)
                index_4 = cc.index(node_4)
                index_5 = cc.index(node_5)
                assert (
                    abs(index_3 - index_4) == 1 or abs(index_3 - index_4) == len(cc) - 1
                )
                assert (
                    abs(index_5 - index_4) == 1 or abs(index_5 - index_4) == len(cc) - 1
                )

                # test_guaranteed_Even2OddOdd
                node_6 = (0, 2) + (1,) * (odd_val_1) + (0,) * (even_val_0 - 1)
                node_7 = (0, 1, 2) + (1,) * (odd_val_1 - 1) + (0,) * (even_val_0 - 1)
                index_6 = cc.index(node_6)
                index_7 = cc.index(node_7)
                assert (
                    abs(index_6 - index_7) == 1 or abs(index_6 - index_7) == len(cc) - 1
                )

                # test_guaranteed_stutter_cross_edge
                # TODO, veranderen als even < odd
                node_8 = (1,) * (odd_val_1 - 1) + (0,) * (even_val_0) + (2, 1)
                node_9 = (1,) * (odd_val_1 - 1) + (0,) * (even_val_0 - 1) + (2, 0, 1)
                index_8 = cc.index(node_8)
                index_9 = cc.index(node_9)
                assert (
                    abs(index_8 - index_9) == 1 or abs(index_8 - index_9) == len(cc) - 1
                )

                # test_guaranteed_2EvenOdd
                node_10 = (2,) + (0,) * (even_val_0) + (1,) * (odd_val_1)
                node_11 = (0, 2) + (0,) * (even_val_0 - 1) + (1,) * (odd_val_1)
                index_10 = cc.index(node_10)
                index_11 = cc.index(node_11)
                assert (
                    abs(index_10 - index_11) == 1
                    or abs(index_10 - index_11) == len(cc) - 1
                )

                # test_guaranteed_2OddEven
                node_12 = (2,) + (1,) * (odd_val_1) + (0,) * (even_val_0)
                node_13 = (1, 2) + (1,) * (odd_val_1 - 1) + (0,) * (even_val_0)
                index_12 = cc.index(node_12)
                index_13 = cc.index(node_13)
                assert (
                    abs(index_12 - index_13) == 1
                    or abs(index_12 - index_13) == len(cc) - 1
                )

                # test_guaranteed_2OddEven1odd
                node_14 = (2,) + (1,) * (odd_val_1 - 1) + (0,) * (even_val_0) + (1,)
                node_15 = (1, 2) + (1,) * (odd_val_1 - 2) + (0,) * (even_val_0) + (1,)
                index_14 = cc.index(node_14)
                index_15 = cc.index(node_15)
                assert (
                    abs(index_14 - index_15) == 1
                    or abs(index_14 - index_15) == len(cc) - 1
                )

                # test_guaranteed_2EvenOdd1even
                node_16 = (2,) + (0,) * (even_val_0 - 1) + (1,) * (odd_val_1) + (0,)
                node_17 = (0, 2) + (0,) * (even_val_0 - 2) + (1,) * (odd_val_1) + (0,)
                index_16 = cc.index(node_16)
                index_17 = cc.index(node_17)
                assert (
                    abs(index_16 - index_17) == 1
                    or abs(index_16 - index_17) == len(cc) - 1
                )

                # test_guaranteed_OddEven1
                node_18 = (
                    (1,) * (odd_val_1 - 1) + (0, 1) + (0,) * (even_val_0 - 1) + (2,)
                )
                node_19 = (1,) * (odd_val_1) + (0,) * (even_val_0) + (2,)
                node_20 = (1,) * (odd_val_1) + (0,) * (even_val_0 - 1) + (2, 0)
                index_18 = cc.index(node_18)
                index_19 = cc.index(node_19)
                index_20 = cc.index(node_20)
                assert (
                    abs(index_18 - index_19) == 1
                    or abs(index_18 - index_19) == len(cc) - 1
                )
                assert (
                    abs(index_20 - index_19) == 1
                    or abs(index_20 - index_19) == len(cc) - 1
                )
                # test_guaranteed_EvenOdd1
                node_18 = (
                    (0,) * (even_val_0 - 1) + (1, 0) + (1,) * (odd_val_1 - 1) + (2,)
                )
                node_19 = (0,) * (even_val_0) + (1,) * (odd_val_1) + (2,)
                node_20 = (0,) * (even_val_0) + (1,) * (odd_val_1 - 1) + (2, 1)
                index_18 = cc.index(node_18)
                index_19 = cc.index(node_19)
                index_20 = cc.index(node_20)
                assert (
                    abs(index_18 - index_19) == 1
                    or abs(index_18 - index_19) == len(cc) - 1
                )
                assert (
                    abs(index_20 - index_19) == 1
                    or abs(index_20 - index_19) == len(cc) - 1
                )

    def test_guaranteed_edges_Odd_Odd_1(self):
        # odd is larger than even
        for odd_val_0 in [5, 7]:
            even_val_1 = 4
            print(f"computing even-odd {(odd_val_0, even_val_1, 1)}")
            cc = get_connected_cycle_cover((odd_val_0, even_val_1, 1))

            # test_guaranteed_zeros2ones
            node_0 = (0,) * (odd_val_0 - 1) + (2, 0) + (1,) * (even_val_1)
            node_1 = (0,) * (odd_val_0) + (2,) + (1,) * (even_val_1)
            node_2 = (0,) * (odd_val_0) + (1, 2) + (1,) * (even_val_1 - 1)
            index_0 = cc.index(node_0)
            index_1 = cc.index(node_1)
            index_2 = cc.index(node_2)
            assert abs(index_0 - index_1) == 1 or abs(index_0 - index_1) == len(cc) - 1
            assert abs(index_2 - index_1) == 1 or abs(index_2 - index_1) == len(cc) - 1

            # test_guaranteed_ones2zeros
            node_3 = (1,) * (even_val_1 - 1) + (2, 1) + (0,) * (odd_val_0)
            node_4 = (1,) * (even_val_1) + (2,) + (0,) * (odd_val_0)
            node_5 = (1,) * (even_val_1) + (0, 2) + (0,) * (odd_val_0 - 1)
            index_3 = cc.index(node_3)
            index_4 = cc.index(node_4)
            index_5 = cc.index(node_5)
            assert abs(index_3 - index_4) == 1 or abs(index_3 - index_4) == len(cc) - 1
            assert abs(index_5 - index_4) == 1 or abs(index_5 - index_4) == len(cc) - 1

            # test_guaranteed_Even2OddOdd
            node_6 = (1, 2) + (0,) * (odd_val_0) + (1,) * (even_val_1 - 1)
            node_7 = (1, 0, 2) + (0,) * (odd_val_0 - 1) + (1,) * (even_val_1 - 1)
            index_6 = cc.index(node_6)
            index_7 = cc.index(node_7)
            assert abs(index_6 - index_7) == 1 or abs(index_6 - index_7) == len(cc) - 1

            # test_guaranteed_stutter_cross_edge
            # TODO, veranderen als even < odd
            node_8 = (0,) * (odd_val_0 - 1) + (1,) * (even_val_1) + (2, 0)
            node_9 = (0,) * (odd_val_0 - 1) + (1,) * (even_val_1 - 1) + (2, 1, 0)
            index_8 = cc.index(node_8)
            index_9 = cc.index(node_9)
            assert abs(index_8 - index_9) == 1 or abs(index_8 - index_9) == len(cc) - 1

            # test_guaranteed_2EvenOdd
            node_10 = (2,) + (1,) * (even_val_1) + (0,) * (odd_val_0)
            node_11 = (1, 2) + (1,) * (even_val_1 - 1) + (0,) * (odd_val_0)
            index_10 = cc.index(node_10)
            index_11 = cc.index(node_11)
            assert (
                abs(index_10 - index_11) == 1 or abs(index_10 - index_11) == len(cc) - 1
            )

            # test_guaranteed_2OddEven
            node_12 = (2,) + (0,) * (odd_val_0) + (1,) * (even_val_1)
            node_13 = (0, 2) + (0,) * (odd_val_0 - 1) + (1,) * (even_val_1)
            index_12 = cc.index(node_12)
            index_13 = cc.index(node_13)
            assert (
                abs(index_12 - index_13) == 1 or abs(index_12 - index_13) == len(cc) - 1
            )

            # test_guaranteed_2OddEven1odd
            node_14 = (2,) + (0,) * (odd_val_0 - 1) + (1,) * (even_val_1) + (0,)
            node_15 = (0, 2) + (0,) * (odd_val_0 - 2) + (1,) * (even_val_1) + (0,)
            index_14 = cc.index(node_14)
            index_15 = cc.index(node_15)
            assert (
                abs(index_14 - index_15) == 1 or abs(index_14 - index_15) == len(cc) - 1
            )

            # test_guaranteed_2EvenOdd1even
            node_16 = (2,) + (1,) * (even_val_1 - 1) + (0,) * (odd_val_0) + (1,)
            node_17 = (1, 2) + (1,) * (even_val_1 - 2) + (0,) * (odd_val_0) + (1,)
            index_16 = cc.index(node_16)
            index_17 = cc.index(node_17)
            assert (
                abs(index_16 - index_17) == 1 or abs(index_16 - index_17) == len(cc) - 1
            )

            # test_guaranteed_OddEven1
            node_18 = (0,) * (odd_val_0 - 1) + (1, 0) + (1,) * (even_val_1 - 1) + (2,)
            node_19 = (0,) * (odd_val_0) + (1,) * (even_val_1) + (2,)
            node_20 = (0,) * (odd_val_0) + (1,) * (even_val_1 - 1) + (2, 1)
            index_18 = cc.index(node_18)
            index_19 = cc.index(node_19)
            index_20 = cc.index(node_20)
            assert (
                abs(index_18 - index_19) == 1 or abs(index_18 - index_19) == len(cc) - 1
            )
            assert (
                abs(index_20 - index_19) == 1 or abs(index_20 - index_19) == len(cc) - 1
            )
            # test_guaranteed_EvenOdd1
            node_21 = (1,) * (even_val_1 - 1) + (0, 1) + (0,) * (odd_val_0 - 1) + (2,)
            node_22 = (1,) * (even_val_1) + (0,) * (odd_val_0) + (2,)
            node_23 = (1,) * (even_val_1) + (0,) * (odd_val_0 - 1) + (2, 0)
            index_21 = cc.index(node_21)
            index_22 = cc.index(node_22)
            index_23 = cc.index(node_23)
            assert (
                abs(index_21 - index_22) == 1 or abs(index_21 - index_22) == len(cc) - 1
            )
            assert (
                abs(index_23 - index_22) == 1 or abs(index_23 - index_22) == len(cc) - 1
            )
