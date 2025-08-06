import pytest

from core.cycle_cover import get_connected_cycle_cover


class Test_GuaranteedEdges_One_Odd_Length_3:
    def test_guaranteed_edges_Odd_Even_Even(self):
        # this has odd as the largets number in the signature
        for odd_val_0 in [3, 5, 7, 9]:
            for even_val_1 in range(2, odd_val_0 + 1, 2):
                for even_val_2 in range(2, even_val_1 + 1, 2):
                    if (odd_val_0 == 9 and even_val_1 >= 4) or (
                        odd_val_0 == 7 and even_val_2 >= 4
                    ):
                        break
                    cyc = get_connected_cycle_cover((odd_val_0, even_val_1, even_val_2))

                    # Guaranteed edge 1
                    # guaranteed swap at odds
                    node_1 = (
                        (1,) * (even_val_1) + (0,) * (odd_val_0) + (2,) * (even_val_2)
                    )
                    node_2 = (
                        (1,) * (even_val_1)
                        + (0,) * (odd_val_0 - 1)
                        + (2, 0)
                        + (2,) * (even_val_2 - 1)
                    )
                    assert (
                        abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                        or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
                    )
                    # and the other one with evens swapped
                    node_3 = (
                        (2,) * (even_val_2) + (0,) * (odd_val_0) + (1,) * (even_val_1)
                    )
                    node_4 = (
                        (2,) * (even_val_2)
                        + (0,) * (odd_val_0 - 1)
                        + (1, 0)
                        + (1,) * (even_val_1 - 1)
                    )
                    assert (
                        abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                        or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
                    )

    def test_guaranteed_edges_Even_Odd_Even(self):
        # this has odd as the second largest number in the signature
        for even_val_0 in [4, 6, 8]:
            for odd_val_1 in range(3, even_val_0 + 1, 2):
                for even_val_2 in range(2, odd_val_1 + 1, 2):
                    if even_val_0 == 8 and odd_val_1 >= 7:
                        break
                    cyc = get_connected_cycle_cover((even_val_0, odd_val_1, even_val_2))

                    # Guaranteed edge 1
                    # guaranteed swap at odds
                    node_1 = (
                        (0,) * (even_val_0) + (1,) * (odd_val_1) + (2,) * (even_val_2)
                    )
                    node_2 = (
                        (0,) * (even_val_0)
                        + (1,) * (odd_val_1 - 1)
                        + (2, 1)
                        + (2,) * (even_val_2 - 1)
                    )
                    assert (
                        abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                        or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
                    )
                    # and the other one with evens swapped
                    node_3 = (
                        (2,) * (even_val_2) + (1,) * (odd_val_1) + (0,) * (even_val_0)
                    )
                    node_4 = (
                        (2,) * (even_val_2)
                        + (1,) * (odd_val_1 - 1)
                        + (0, 1)
                        + (0,) * (even_val_0 - 1)
                    )
                    assert (
                        abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                        or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
                    )

    def test_guaranteed_edges_Even_Even_Odd(self):
        # this has odd as the second largest number in the signature
        for even_val_0 in [4, 6, 8]:
            even_val_1 = 4
            odd_val_2 = 3
            cyc = get_connected_cycle_cover((even_val_0, even_val_1, odd_val_2))

            # Guaranteed edge 1
            # guaranteed swap at odds
            node_1 = (0,) * (even_val_0) + (2,) * (odd_val_2) + (1,) * (even_val_1)
            node_2 = (
                (0,) * (even_val_0)
                + (2,) * (odd_val_2 - 1)
                + (1, 2)
                + (1,) * (even_val_1 - 1)
            )
            assert (
                abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
            )
            # and the other one with evens swapped
            node_3 = (1,) * (even_val_1) + (2,) * (odd_val_2) + (0,) * (even_val_0)
            node_4 = (
                (1,) * (even_val_1)
                + (2,) * (odd_val_2 - 1)
                + (0, 2)
                + (0,) * (even_val_0 - 1)
            )
            assert (
                abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
            )

    def test_guaranteed_edges_Odd_2_2_2(self):
        # this has odd as the second largest number in the signature
        for odd_val_0 in [3, 5, 7]:
            even_val_1 = 2
            even_val_2 = 2
            even_val_3 = 2
            # Guaranteed edge 1
            # guaranteed swap at odds
            cyc = get_connected_cycle_cover(
                (odd_val_0, even_val_1, even_val_2, even_val_3)
            )

            node_1 = (
                (1,) * (even_val_1)
                + (2,) * (even_val_2)
                + (0,) * (odd_val_0)
                + (3,) * (even_val_3)
            )
            node_2 = (
                (1,) * (even_val_1)
                + (2,) * (even_val_2)
                + (0,) * (odd_val_0 - 1)
                + (3, 0)
                + (3,) * (even_val_3 - 1)
            )
            assert (
                abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
            )
            # and the other one with evens swapped
            node_3 = (
                (2,) * (even_val_2)
                + (1,) * (even_val_1)
                + (0,) * (odd_val_0)
                + (3,) * (even_val_3)
            )
            node_4 = (
                (2,) * (even_val_2)
                + (1,) * (even_val_1)
                + (0,) * (odd_val_0 - 1)
                + (3, 0)
                + (3,) * (even_val_3 - 1)
            )
            assert (
                abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
            )
            node_5 = (
                (3,) * (even_val_3)
                + (2,) * (even_val_2)
                + (0,) * (odd_val_0)
                + (1,) * (even_val_1)
            )
            node_6 = (
                (3,) * (even_val_3)
                + (2,) * (even_val_2)
                + (0,) * (odd_val_0 - 1)
                + (1, 0)
                + (1,) * (even_val_1 - 1)
            )
            assert (
                abs(cyc.index(node_5) - cyc.index(node_6)) == 1
                or abs(cyc.index(node_5) - cyc.index(node_6)) == len(cyc) - 1
            )
            node_7 = (
                (2,) * (even_val_2)
                + (3,) * (even_val_3)
                + (0,) * (odd_val_0)
                + (1,) * (even_val_1)
            )
            node_8 = (
                (2,) * (even_val_2)
                + (3,) * (even_val_3)
                + (0,) * (odd_val_0 - 1)
                + (1, 0)
                + (1,) * (even_val_1 - 1)
            )
            assert (
                abs(cyc.index(node_7) - cyc.index(node_8)) == 1
                or abs(cyc.index(node_7) - cyc.index(node_8)) == len(cyc) - 1
            )
            node_9 = (
                (3,) * (even_val_3)
                + (1,) * (even_val_1)
                + (0,) * (odd_val_0)
                + (2,) * (even_val_2)
            )
            node_10 = (
                (3,) * (even_val_3)
                + (1,) * (even_val_1)
                + (0,) * (odd_val_0 - 1)
                + (2, 0)
                + (2,) * (even_val_2 - 1)
            )
            assert (
                abs(cyc.index(node_9) - cyc.index(node_10)) == 1
                or abs(cyc.index(node_9) - cyc.index(node_10)) == len(cyc) - 1
            )
            node_11 = (
                (1,) * (even_val_1)
                + (3,) * (even_val_3)
                + (0,) * (odd_val_0)
                + (2,) * (even_val_2)
            )
            node_12 = (
                (1,) * (even_val_1)
                + (3,) * (even_val_3)
                + (0,) * (odd_val_0 - 1)
                + (2, 0)
                + (2,) * (even_val_2 - 1)
            )
            assert (
                abs(cyc.index(node_11) - cyc.index(node_12)) == 1
                or abs(cyc.index(node_11) - cyc.index(node_12)) == len(cyc) - 1
            )
