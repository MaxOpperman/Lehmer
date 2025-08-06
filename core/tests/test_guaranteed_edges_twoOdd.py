import pytest

from core.cycle_cover import get_connected_cycle_cover


class Test_GuaranteedEdges_Two_Odd_Length_3:
    def test_guaranteed_edges_Odd_3_2(self):
        # this has the subgraph even, 1, 1 & odd, 2, 1
        for odd_val_0 in [3, 5, 7, 9]:
            odd_val_1 = 3
            even_val_2 = 2
            cyc = get_connected_cycle_cover((odd_val_0, odd_val_1, even_val_2))

            # Guaranteed edge 1
            # guaranteed swap at odds
            node_1 = (
                (1,) * (odd_val_1 - 1) + (2,) * (even_val_2) + (0,) * (odd_val_0) + (1,)
            )
            node_2 = (
                (1,) * (odd_val_1 - 1)
                + (2,) * (even_val_2)
                + (0,) * (odd_val_0 - 1)
                + (1, 0)
            )
            assert (
                abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
            )
            node_3 = (
                (0,) * (odd_val_0 - 1) + (2,) * (even_val_2) + (1,) * (odd_val_1) + (0,)
            )
            node_4 = (
                (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (0, 1)
            )
            assert (
                abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
            )

            # Guaranteed edge 2
            # guaranteed swap at odds all odds
            node_5 = (2,) * (even_val_2) + (0,) * (odd_val_0) + (1,) * (odd_val_1)
            node_6 = (
                (2,) * (even_val_2)
                + (0,) * (odd_val_0 - 1)
                + (1, 0)
                + (1,) * (odd_val_1 - 1)
            )
            assert (
                abs(cyc.index(node_5) - cyc.index(node_6)) == 1
                or abs(cyc.index(node_5) - cyc.index(node_6)) == len(cyc) - 1
            )
            node_7 = (2,) * (even_val_2) + (1,) * (odd_val_1) + (0,) * (odd_val_0)
            node_8 = (
                (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (0, 1)
                + (0,) * (odd_val_0 - 1)
            )
            assert (
                abs(cyc.index(node_7) - cyc.index(node_8)) == 1
                or abs(cyc.index(node_7) - cyc.index(node_8)) == len(cyc) - 1
            )

            # Guaranteed edge 3
            # guaranteed swap two trailing odds
            # 2^{k_2} 1^{k_1} 0^{k_0} xy & \sim 2^{k_2} 1^{k_1-1} 01 0^{k_0-1} xy
            node_9 = (
                (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (0, 1)
            )
            node_10 = (
                (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2 - 1)
                + (1, 2)
                + (1,) * (odd_val_1 - 2)
                + (0, 1)
            )
            assert (
                abs(cyc.index(node_9) - cyc.index(node_10)) == 1
                or abs(cyc.index(node_9) - cyc.index(node_10)) == len(cyc) - 1
            )
            node_11 = (
                (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (1, 0)
            )
            node_12 = (
                (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2 - 1)
                + (1, 2)
                + (1,) * (odd_val_1 - 2)
                + (1, 0)
            )
            assert (
                abs(cyc.index(node_11) - cyc.index(node_12)) == 1
                or abs(cyc.index(node_11) - cyc.index(node_12)) == len(cyc) - 1
            )
            node_13 = (
                (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (0,) * (odd_val_0 - 1)
                + (0, 1)
            )
            node_14 = (
                (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 2)
                + (0, 1)
                + (0,) * (odd_val_0 - 2)
                + (0, 1)
            )
            assert (
                abs(cyc.index(node_13) - cyc.index(node_14)) == 1
                or abs(cyc.index(node_13) - cyc.index(node_14)) == len(cyc) - 1
            )
            node_15 = (
                (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (0,) * (odd_val_0 - 1)
                + (1, 0)
            )
            node_16 = (
                (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 2)
                + (0, 1)
                + (0,) * (odd_val_0 - 2)
                + (1, 0)
            )
            assert (
                abs(cyc.index(node_15) - cyc.index(node_16)) == 1
                or abs(cyc.index(node_15) - cyc.index(node_16)) == len(cyc) - 1
            )

            # Guaranteed edge 4
            # odd first, then evens, then second odd
            node_17 = (
                (1,) * (odd_val_1) + (0,) * (odd_val_0 - 1) + (2,) * (even_val_2) + (0,)
            )
            node_18 = (
                (1,) * (odd_val_1 - 1)
                + (0, 1)
                + (0,) * (odd_val_0 - 2)
                + (2,) * (even_val_2)
                + (0,)
            )
            assert (
                abs(cyc.index(node_17) - cyc.index(node_18)) == 1
                or abs(cyc.index(node_17) - cyc.index(node_18)) == len(cyc) - 1
            )
            node_19 = (
                (1,) * (odd_val_1) + (2,) * (even_val_2) + (0,) * (odd_val_0 - 1) + (0,)
            )
            node_20 = (
                (1,) * (odd_val_1 - 1)
                + (2, 1)
                + (2,) * (even_val_2 - 1)
                + (0,) * (odd_val_0 - 1)
                + (0,)
            )
            assert (
                abs(cyc.index(node_19) - cyc.index(node_20)) == 1
                or abs(cyc.index(node_19) - cyc.index(node_20)) == len(cyc) - 1
            )
            node_21 = (
                (0,) * (odd_val_0) + (1,) * (odd_val_1 - 1) + (2,) * (even_val_2) + (1,)
            )
            node_22 = (
                (0,) * (odd_val_0 - 1)
                + (1, 0)
                + (1,) * (odd_val_1 - 2)
                + (2,) * (even_val_2)
                + (1,)
            )
            assert (
                abs(cyc.index(node_21) - cyc.index(node_22)) == 1
                or abs(cyc.index(node_21) - cyc.index(node_22)) == len(cyc) - 1
            )
            node_23 = (
                (0,) * (odd_val_0) + (2,) * (even_val_2) + (1,) * (odd_val_1 - 1) + (1,)
            )
            node_24 = (
                (0,) * (odd_val_0 - 1)
                + (2, 0)
                + (2,) * (even_val_2 - 1)
                + (1,) * (odd_val_1 - 1)
                + (1,)
            )
            assert (
                abs(cyc.index(node_23) - cyc.index(node_24)) == 1
                or abs(cyc.index(node_23) - cyc.index(node_24)) == len(cyc) - 1
            )

            # Guaranteed edge 5
            # odd (some even) then other odd, then even
            node_25 = (0,) * (odd_val_0) + (1,) * (odd_val_1) + (2,) * (even_val_2)
            node_26 = (
                (0,) * (odd_val_0 - 1)
                + (1, 0)
                + (1,) * (odd_val_1 - 1)
                + (2,) * (even_val_2)
            )
            assert (
                abs(cyc.index(node_25) - cyc.index(node_26)) == 1
                or abs(cyc.index(node_25) - cyc.index(node_26)) == len(cyc) - 1
            )
            node_27 = (1,) * (odd_val_1) + (0,) * (odd_val_0) + (2,) * (even_val_2)
            node_28 = (
                (1,) * (odd_val_1 - 1)
                + (0, 1)
                + (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2)
            )
            assert (
                abs(cyc.index(node_27) - cyc.index(node_28)) == 1
                or abs(cyc.index(node_27) - cyc.index(node_28)) == len(cyc) - 1
            )

    def test_guaranteed_edges_Odd_5_2(self):
        # this has the subgraph even, 1, 1 & odd, 2, 1
        for odd_val_0 in [5, 7]:
            odd_val_1 = 5
            even_val_2 = 2
            cyc = get_connected_cycle_cover((odd_val_0, odd_val_1, even_val_2))

            # Guaranteed edge 1
            # guaranteed swap at odds
            node_1 = (
                (1,) * (odd_val_1 - 1) + (2,) * (even_val_2) + (0,) * (odd_val_0) + (1,)
            )
            node_2 = (
                (1,) * (odd_val_1 - 1)
                + (2,) * (even_val_2)
                + (0,) * (odd_val_0 - 1)
                + (1, 0)
            )
            assert (
                abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
            )
            node_3 = (
                (0,) * (odd_val_0 - 1) + (2,) * (even_val_2) + (1,) * (odd_val_1) + (0,)
            )
            node_4 = (
                (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (0, 1)
            )
            assert (
                abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
            )

            # Guaranteed edge 2
            # guaranteed swap at odds all odds
            node_5 = (2,) * (even_val_2) + (0,) * (odd_val_0) + (1,) * (odd_val_1)
            node_6 = (
                (2,) * (even_val_2)
                + (0,) * (odd_val_0 - 1)
                + (1, 0)
                + (1,) * (odd_val_1 - 1)
            )
            assert (
                abs(cyc.index(node_5) - cyc.index(node_6)) == 1
                or abs(cyc.index(node_5) - cyc.index(node_6)) == len(cyc) - 1
            )
            node_7 = (2,) * (even_val_2) + (1,) * (odd_val_1) + (0,) * (odd_val_0)
            node_8 = (
                (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (0, 1)
                + (0,) * (odd_val_0 - 1)
            )
            assert (
                abs(cyc.index(node_7) - cyc.index(node_8)) == 1
                or abs(cyc.index(node_7) - cyc.index(node_8)) == len(cyc) - 1
            )

            # Guaranteed edge 3
            # guaranteed swap two trailing odds
            # 2^{k_2} 1^{k_1} 0^{k_0} xy & \sim 2^{k_2} 1^{k_1-1} 01 0^{k_0-1} xy
            node_9 = (
                (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (0, 1)
            )
            node_10 = (
                (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2 - 1)
                + (1, 2)
                + (1,) * (odd_val_1 - 2)
                + (0, 1)
            )
            assert (
                abs(cyc.index(node_9) - cyc.index(node_10)) == 1
                or abs(cyc.index(node_9) - cyc.index(node_10)) == len(cyc) - 1
            )
            node_11 = (
                (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (1, 0)
            )
            node_12 = (
                (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2 - 1)
                + (1, 2)
                + (1,) * (odd_val_1 - 2)
                + (1, 0)
            )
            assert (
                abs(cyc.index(node_11) - cyc.index(node_12)) == 1
                or abs(cyc.index(node_11) - cyc.index(node_12)) == len(cyc) - 1
            )
            node_13 = (
                (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (0,) * (odd_val_0 - 1)
                + (0, 1)
            )
            node_14 = (
                (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 2)
                + (0, 1)
                + (0,) * (odd_val_0 - 2)
                + (0, 1)
            )
            assert (
                abs(cyc.index(node_13) - cyc.index(node_14)) == 1
                or abs(cyc.index(node_13) - cyc.index(node_14)) == len(cyc) - 1
            )
            node_15 = (
                (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 1)
                + (0,) * (odd_val_0 - 1)
                + (1, 0)
            )
            node_16 = (
                (2,) * (even_val_2)
                + (1,) * (odd_val_1 - 2)
                + (0, 1)
                + (0,) * (odd_val_0 - 2)
                + (1, 0)
            )
            assert (
                abs(cyc.index(node_15) - cyc.index(node_16)) == 1
                or abs(cyc.index(node_15) - cyc.index(node_16)) == len(cyc) - 1
            )

            # Guaranteed edge 4
            # odd first, then evens, then second odd
            node_17 = (
                (1,) * (odd_val_1) + (0,) * (odd_val_0 - 1) + (2,) * (even_val_2) + (0,)
            )
            node_18 = (
                (1,) * (odd_val_1 - 1)
                + (0, 1)
                + (0,) * (odd_val_0 - 2)
                + (2,) * (even_val_2)
                + (0,)
            )
            assert (
                abs(cyc.index(node_17) - cyc.index(node_18)) == 1
                or abs(cyc.index(node_17) - cyc.index(node_18)) == len(cyc) - 1
            )
            node_19 = (
                (1,) * (odd_val_1) + (2,) * (even_val_2) + (0,) * (odd_val_0 - 1) + (0,)
            )
            node_20 = (
                (1,) * (odd_val_1 - 1)
                + (2, 1)
                + (2,) * (even_val_2 - 1)
                + (0,) * (odd_val_0 - 1)
                + (0,)
            )
            assert (
                abs(cyc.index(node_19) - cyc.index(node_20)) == 1
                or abs(cyc.index(node_19) - cyc.index(node_20)) == len(cyc) - 1
            )
            node_21 = (
                (0,) * (odd_val_0) + (1,) * (odd_val_1 - 1) + (2,) * (even_val_2) + (1,)
            )
            node_22 = (
                (0,) * (odd_val_0 - 1)
                + (1, 0)
                + (1,) * (odd_val_1 - 2)
                + (2,) * (even_val_2)
                + (1,)
            )
            assert (
                abs(cyc.index(node_21) - cyc.index(node_22)) == 1
                or abs(cyc.index(node_21) - cyc.index(node_22)) == len(cyc) - 1
            )
            node_23 = (
                (0,) * (odd_val_0) + (2,) * (even_val_2) + (1,) * (odd_val_1 - 1) + (1,)
            )
            node_24 = (
                (0,) * (odd_val_0 - 1)
                + (2, 0)
                + (2,) * (even_val_2 - 1)
                + (1,) * (odd_val_1 - 1)
                + (1,)
            )
            assert (
                abs(cyc.index(node_23) - cyc.index(node_24)) == 1
                or abs(cyc.index(node_23) - cyc.index(node_24)) == len(cyc) - 1
            )

            # Guaranteed edge 5
            # odd (some even) then other odd, then even
            node_25 = (0,) * (odd_val_0) + (1,) * (odd_val_1) + (2,) * (even_val_2)
            node_26 = (
                (0,) * (odd_val_0 - 1)
                + (1, 0)
                + (1,) * (odd_val_1 - 1)
                + (2,) * (even_val_2)
            )
            assert (
                abs(cyc.index(node_25) - cyc.index(node_26)) == 1
                or abs(cyc.index(node_25) - cyc.index(node_26)) == len(cyc) - 1
            )
            node_27 = (1,) * (odd_val_1) + (0,) * (odd_val_0) + (2,) * (even_val_2)
            node_28 = (
                (1,) * (odd_val_1 - 1)
                + (0, 1)
                + (0,) * (odd_val_0 - 1)
                + (2,) * (even_val_2)
            )
            assert (
                abs(cyc.index(node_27) - cyc.index(node_28)) == 1
                or abs(cyc.index(node_27) - cyc.index(node_28)) == len(cyc) - 1
            )

    def test_guaranteed_edges_Odd_5_4(self):
        # this has the subgraph even, 1, 1 & odd, 2, 1
        for odd_val_0 in [3, 5]:
            for odd_val_1 in [3, 5]:
                even_val_2 = 4
                cyc = get_connected_cycle_cover((odd_val_0, odd_val_1, even_val_2))

                # Guaranteed edge 1
                # guaranteed swap at odds
                node_1 = (
                    (1,) * (odd_val_1 - 1)
                    + (2,) * (even_val_2)
                    + (0,) * (odd_val_0)
                    + (1,)
                )
                node_2 = (
                    (1,) * (odd_val_1 - 1)
                    + (2,) * (even_val_2)
                    + (0,) * (odd_val_0 - 1)
                    + (1, 0)
                )
                assert (
                    abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                    or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
                )
                node_3 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                    + (1,) * (odd_val_1)
                    + (0,)
                )
                node_4 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (0, 1)
                )
                assert (
                    abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                    or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
                )

                # Guaranteed edge 2
                # guaranteed swap at odds all odds
                node_5 = (2,) * (even_val_2) + (0,) * (odd_val_0) + (1,) * (odd_val_1)
                node_6 = (
                    (2,) * (even_val_2)
                    + (0,) * (odd_val_0 - 1)
                    + (1, 0)
                    + (1,) * (odd_val_1 - 1)
                )
                assert (
                    abs(cyc.index(node_5) - cyc.index(node_6)) == 1
                    or abs(cyc.index(node_5) - cyc.index(node_6)) == len(cyc) - 1
                )
                node_7 = (2,) * (even_val_2) + (1,) * (odd_val_1) + (0,) * (odd_val_0)
                node_8 = (
                    (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (0, 1)
                    + (0,) * (odd_val_0 - 1)
                )
                assert (
                    abs(cyc.index(node_7) - cyc.index(node_8)) == 1
                    or abs(cyc.index(node_7) - cyc.index(node_8)) == len(cyc) - 1
                )

                # Guaranteed edge 3
                # guaranteed swap two trailing odds
                # 2^{k_2} 1^{k_1} 0^{k_0} xy & \sim 2^{k_2} 1^{k_1-1} 01 0^{k_0-1} xy
                node_9 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (0, 1)
                )
                node_10 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2 - 1)
                    + (1, 2)
                    + (1,) * (odd_val_1 - 2)
                    + (0, 1)
                )
                assert (
                    abs(cyc.index(node_9) - cyc.index(node_10)) == 1
                    or abs(cyc.index(node_9) - cyc.index(node_10)) == len(cyc) - 1
                )
                node_11 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (1, 0)
                )
                node_12 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2 - 1)
                    + (1, 2)
                    + (1,) * (odd_val_1 - 2)
                    + (1, 0)
                )
                assert (
                    abs(cyc.index(node_11) - cyc.index(node_12)) == 1
                    or abs(cyc.index(node_11) - cyc.index(node_12)) == len(cyc) - 1
                )
                node_13 = (
                    (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (0,) * (odd_val_0 - 1)
                    + (0, 1)
                )
                node_14 = (
                    (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 2)
                    + (0, 1)
                    + (0,) * (odd_val_0 - 2)
                    + (0, 1)
                )
                assert (
                    abs(cyc.index(node_13) - cyc.index(node_14)) == 1
                    or abs(cyc.index(node_13) - cyc.index(node_14)) == len(cyc) - 1
                )
                node_15 = (
                    (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (0,) * (odd_val_0 - 1)
                    + (1, 0)
                )
                node_16 = (
                    (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 2)
                    + (0, 1)
                    + (0,) * (odd_val_0 - 2)
                    + (1, 0)
                )
                assert (
                    abs(cyc.index(node_15) - cyc.index(node_16)) == 1
                    or abs(cyc.index(node_15) - cyc.index(node_16)) == len(cyc) - 1
                )

                # Guaranteed edge 4
                # odd first, then evens, then second odd
                node_17 = (
                    (1,) * (odd_val_1)
                    + (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                    + (0,)
                )
                node_18 = (
                    (1,) * (odd_val_1 - 1)
                    + (0, 1)
                    + (0,) * (odd_val_0 - 2)
                    + (2,) * (even_val_2)
                    + (0,)
                )
                assert (
                    abs(cyc.index(node_17) - cyc.index(node_18)) == 1
                    or abs(cyc.index(node_17) - cyc.index(node_18)) == len(cyc) - 1
                )
                node_19 = (
                    (1,) * (odd_val_1)
                    + (2,) * (even_val_2)
                    + (0,) * (odd_val_0 - 1)
                    + (0,)
                )
                node_20 = (
                    (1,) * (odd_val_1 - 1)
                    + (2, 1)
                    + (2,) * (even_val_2 - 1)
                    + (0,) * (odd_val_0 - 1)
                    + (0,)
                )
                assert (
                    abs(cyc.index(node_19) - cyc.index(node_20)) == 1
                    or abs(cyc.index(node_19) - cyc.index(node_20)) == len(cyc) - 1
                )
                node_21 = (
                    (0,) * (odd_val_0)
                    + (1,) * (odd_val_1 - 1)
                    + (2,) * (even_val_2)
                    + (1,)
                )
                node_22 = (
                    (0,) * (odd_val_0 - 1)
                    + (1, 0)
                    + (1,) * (odd_val_1 - 2)
                    + (2,) * (even_val_2)
                    + (1,)
                )
                assert (
                    abs(cyc.index(node_21) - cyc.index(node_22)) == 1
                    or abs(cyc.index(node_21) - cyc.index(node_22)) == len(cyc) - 1
                )
                node_23 = (
                    (0,) * (odd_val_0)
                    + (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (1,)
                )
                node_24 = (
                    (0,) * (odd_val_0 - 1)
                    + (2, 0)
                    + (2,) * (even_val_2 - 1)
                    + (1,) * (odd_val_1 - 1)
                    + (1,)
                )
                assert (
                    abs(cyc.index(node_23) - cyc.index(node_24)) == 1
                    or abs(cyc.index(node_23) - cyc.index(node_24)) == len(cyc) - 1
                )

                # Guaranteed edge 5
                # odd (some even) then other odd, then even
                node_25 = (0,) * (odd_val_0) + (1,) * (odd_val_1) + (2,) * (even_val_2)
                node_26 = (
                    (0,) * (odd_val_0 - 1)
                    + (1, 0)
                    + (1,) * (odd_val_1 - 1)
                    + (2,) * (even_val_2)
                )
                assert (
                    abs(cyc.index(node_25) - cyc.index(node_26)) == 1
                    or abs(cyc.index(node_25) - cyc.index(node_26)) == len(cyc) - 1
                )
                node_27 = (1,) * (odd_val_1) + (0,) * (odd_val_0) + (2,) * (even_val_2)
                node_28 = (
                    (1,) * (odd_val_1 - 1)
                    + (0, 1)
                    + (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                )
                assert (
                    abs(cyc.index(node_27) - cyc.index(node_28)) == 1
                    or abs(cyc.index(node_27) - cyc.index(node_28)) == len(cyc) - 1
                )

    def test_guaranteed_edges_7_3_4(self):
        # this has the subgraph even, 1, 1 & odd, 2, 1
        odd_val_0 = 7
        odd_val_1 = 3
        even_val_2 = 4
        cyc = get_connected_cycle_cover((odd_val_0, odd_val_1, even_val_2))

        # Guaranteed edge 1
        # guaranteed swap at odds
        node_1 = (
            (1,) * (odd_val_1 - 1) + (2,) * (even_val_2) + (0,) * (odd_val_0) + (1,)
        )
        node_2 = (
            (1,) * (odd_val_1 - 1)
            + (2,) * (even_val_2)
            + (0,) * (odd_val_0 - 1)
            + (1, 0)
        )
        assert (
            abs(cyc.index(node_1) - cyc.index(node_2)) == 1
            or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
        )
        node_3 = (
            (0,) * (odd_val_0 - 1) + (2,) * (even_val_2) + (1,) * (odd_val_1) + (0,)
        )
        node_4 = (
            (0,) * (odd_val_0 - 1)
            + (2,) * (even_val_2)
            + (1,) * (odd_val_1 - 1)
            + (0, 1)
        )
        assert (
            abs(cyc.index(node_3) - cyc.index(node_4)) == 1
            or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
        )

        # Guaranteed edge 2
        # guaranteed swap at odds all odds
        node_5 = (2,) * (even_val_2) + (0,) * (odd_val_0) + (1,) * (odd_val_1)
        node_6 = (
            (2,) * (even_val_2)
            + (0,) * (odd_val_0 - 1)
            + (1, 0)
            + (1,) * (odd_val_1 - 1)
        )
        assert (
            abs(cyc.index(node_5) - cyc.index(node_6)) == 1
            or abs(cyc.index(node_5) - cyc.index(node_6)) == len(cyc) - 1
        )
        node_7 = (2,) * (even_val_2) + (1,) * (odd_val_1) + (0,) * (odd_val_0)
        node_8 = (
            (2,) * (even_val_2)
            + (1,) * (odd_val_1 - 1)
            + (0, 1)
            + (0,) * (odd_val_0 - 1)
        )
        assert (
            abs(cyc.index(node_7) - cyc.index(node_8)) == 1
            or abs(cyc.index(node_7) - cyc.index(node_8)) == len(cyc) - 1
        )

        # Guaranteed edge 3
        # guaranteed swap two trailing odds
        # 2^{k_2} 1^{k_1} 0^{k_0} xy & \sim 2^{k_2} 1^{k_1-1} 01 0^{k_0-1} xy
        node_9 = (
            (0,) * (odd_val_0 - 1)
            + (2,) * (even_val_2)
            + (1,) * (odd_val_1 - 1)
            + (0, 1)
        )
        node_10 = (
            (0,) * (odd_val_0 - 1)
            + (2,) * (even_val_2 - 1)
            + (1, 2)
            + (1,) * (odd_val_1 - 2)
            + (0, 1)
        )
        assert (
            abs(cyc.index(node_9) - cyc.index(node_10)) == 1
            or abs(cyc.index(node_9) - cyc.index(node_10)) == len(cyc) - 1
        )
        node_11 = (
            (0,) * (odd_val_0 - 1)
            + (2,) * (even_val_2)
            + (1,) * (odd_val_1 - 1)
            + (1, 0)
        )
        node_12 = (
            (0,) * (odd_val_0 - 1)
            + (2,) * (even_val_2 - 1)
            + (1, 2)
            + (1,) * (odd_val_1 - 2)
            + (1, 0)
        )
        assert (
            abs(cyc.index(node_11) - cyc.index(node_12)) == 1
            or abs(cyc.index(node_11) - cyc.index(node_12)) == len(cyc) - 1
        )
        node_13 = (
            (2,) * (even_val_2)
            + (1,) * (odd_val_1 - 1)
            + (0,) * (odd_val_0 - 1)
            + (0, 1)
        )
        node_14 = (
            (2,) * (even_val_2)
            + (1,) * (odd_val_1 - 2)
            + (0, 1)
            + (0,) * (odd_val_0 - 2)
            + (0, 1)
        )
        assert (
            abs(cyc.index(node_13) - cyc.index(node_14)) == 1
            or abs(cyc.index(node_13) - cyc.index(node_14)) == len(cyc) - 1
        )
        node_15 = (
            (2,) * (even_val_2)
            + (1,) * (odd_val_1 - 1)
            + (0,) * (odd_val_0 - 1)
            + (1, 0)
        )
        node_16 = (
            (2,) * (even_val_2)
            + (1,) * (odd_val_1 - 2)
            + (0, 1)
            + (0,) * (odd_val_0 - 2)
            + (1, 0)
        )
        assert (
            abs(cyc.index(node_15) - cyc.index(node_16)) == 1
            or abs(cyc.index(node_15) - cyc.index(node_16)) == len(cyc) - 1
        )

        # Guaranteed edge 4
        # odd first, then evens, then second odd
        node_17 = (
            (1,) * (odd_val_1) + (0,) * (odd_val_0 - 1) + (2,) * (even_val_2) + (0,)
        )
        node_18 = (
            (1,) * (odd_val_1 - 1)
            + (0, 1)
            + (0,) * (odd_val_0 - 2)
            + (2,) * (even_val_2)
            + (0,)
        )
        assert (
            abs(cyc.index(node_17) - cyc.index(node_18)) == 1
            or abs(cyc.index(node_17) - cyc.index(node_18)) == len(cyc) - 1
        )
        node_19 = (
            (1,) * (odd_val_1) + (2,) * (even_val_2) + (0,) * (odd_val_0 - 1) + (0,)
        )
        node_20 = (
            (1,) * (odd_val_1 - 1)
            + (2, 1)
            + (2,) * (even_val_2 - 1)
            + (0,) * (odd_val_0 - 1)
            + (0,)
        )
        assert (
            abs(cyc.index(node_19) - cyc.index(node_20)) == 1
            or abs(cyc.index(node_19) - cyc.index(node_20)) == len(cyc) - 1
        )
        node_21 = (
            (0,) * (odd_val_0) + (1,) * (odd_val_1 - 1) + (2,) * (even_val_2) + (1,)
        )
        node_22 = (
            (0,) * (odd_val_0 - 1)
            + (1, 0)
            + (1,) * (odd_val_1 - 2)
            + (2,) * (even_val_2)
            + (1,)
        )
        assert (
            abs(cyc.index(node_21) - cyc.index(node_22)) == 1
            or abs(cyc.index(node_21) - cyc.index(node_22)) == len(cyc) - 1
        )
        node_23 = (
            (0,) * (odd_val_0) + (2,) * (even_val_2) + (1,) * (odd_val_1 - 1) + (1,)
        )
        node_24 = (
            (0,) * (odd_val_0 - 1)
            + (2, 0)
            + (2,) * (even_val_2 - 1)
            + (1,) * (odd_val_1 - 1)
            + (1,)
        )
        assert (
            abs(cyc.index(node_23) - cyc.index(node_24)) == 1
            or abs(cyc.index(node_23) - cyc.index(node_24)) == len(cyc) - 1
        )

        # Guaranteed edge 5
        # odd (some even) then other odd, then even
        node_25 = (0,) * (odd_val_0) + (1,) * (odd_val_1) + (2,) * (even_val_2)
        node_26 = (
            (0,) * (odd_val_0 - 1)
            + (1, 0)
            + (1,) * (odd_val_1 - 1)
            + (2,) * (even_val_2)
        )
        assert (
            abs(cyc.index(node_25) - cyc.index(node_26)) == 1
            or abs(cyc.index(node_25) - cyc.index(node_26)) == len(cyc) - 1
        )
        node_27 = (1,) * (odd_val_1) + (0,) * (odd_val_0) + (2,) * (even_val_2)
        node_28 = (
            (1,) * (odd_val_1 - 1)
            + (0, 1)
            + (0,) * (odd_val_0 - 1)
            + (2,) * (even_val_2)
        )
        assert (
            abs(cyc.index(node_27) - cyc.index(node_28)) == 1
            or abs(cyc.index(node_27) - cyc.index(node_28)) == len(cyc) - 1
        )

    def test_guaranteed_edges_Odd_Odd_6(self):
        # this has the subgraph even, 1, 1 & odd, 2, 1
        for odd_val_0 in [3, 5]:
            for odd_val_1 in range(3, odd_val_0 + 1, 2):
                even_val_2 = 6
                cyc = get_connected_cycle_cover((odd_val_0, odd_val_1, even_val_2))

                # Guaranteed edge 1
                # guaranteed swap at odds
                node_1 = (
                    (1,) * (odd_val_1 - 1)
                    + (2,) * (even_val_2)
                    + (0,) * (odd_val_0)
                    + (1,)
                )
                node_2 = (
                    (1,) * (odd_val_1 - 1)
                    + (2,) * (even_val_2)
                    + (0,) * (odd_val_0 - 1)
                    + (1, 0)
                )
                assert (
                    abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                    or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
                )
                node_3 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                    + (1,) * (odd_val_1)
                    + (0,)
                )
                node_4 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (0, 1)
                )
                assert (
                    abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                    or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
                )

                # Guaranteed edge 2
                # guaranteed swap at odds all odds
                node_5 = (2,) * (even_val_2) + (0,) * (odd_val_0) + (1,) * (odd_val_1)
                node_6 = (
                    (2,) * (even_val_2)
                    + (0,) * (odd_val_0 - 1)
                    + (1, 0)
                    + (1,) * (odd_val_1 - 1)
                )
                assert (
                    abs(cyc.index(node_5) - cyc.index(node_6)) == 1
                    or abs(cyc.index(node_5) - cyc.index(node_6)) == len(cyc) - 1
                )
                node_7 = (2,) * (even_val_2) + (1,) * (odd_val_1) + (0,) * (odd_val_0)
                node_8 = (
                    (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (0, 1)
                    + (0,) * (odd_val_0 - 1)
                )
                assert (
                    abs(cyc.index(node_7) - cyc.index(node_8)) == 1
                    or abs(cyc.index(node_7) - cyc.index(node_8)) == len(cyc) - 1
                )

                # Guaranteed edge 3
                # guaranteed swap two trailing odds
                # 2^{k_2} 1^{k_1} 0^{k_0} xy & \sim 2^{k_2} 1^{k_1-1} 01 0^{k_0-1} xy
                node_9 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (0, 1)
                )
                node_10 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2 - 1)
                    + (1, 2)
                    + (1,) * (odd_val_1 - 2)
                    + (0, 1)
                )
                assert (
                    abs(cyc.index(node_9) - cyc.index(node_10)) == 1
                    or abs(cyc.index(node_9) - cyc.index(node_10)) == len(cyc) - 1
                )
                node_11 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (1, 0)
                )
                node_12 = (
                    (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2 - 1)
                    + (1, 2)
                    + (1,) * (odd_val_1 - 2)
                    + (1, 0)
                )
                assert (
                    abs(cyc.index(node_11) - cyc.index(node_12)) == 1
                    or abs(cyc.index(node_11) - cyc.index(node_12)) == len(cyc) - 1
                )
                node_13 = (
                    (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (0,) * (odd_val_0 - 1)
                    + (0, 1)
                )
                node_14 = (
                    (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 2)
                    + (0, 1)
                    + (0,) * (odd_val_0 - 2)
                    + (0, 1)
                )
                assert (
                    abs(cyc.index(node_13) - cyc.index(node_14)) == 1
                    or abs(cyc.index(node_13) - cyc.index(node_14)) == len(cyc) - 1
                )
                node_15 = (
                    (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (0,) * (odd_val_0 - 1)
                    + (1, 0)
                )
                node_16 = (
                    (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 2)
                    + (0, 1)
                    + (0,) * (odd_val_0 - 2)
                    + (1, 0)
                )
                assert (
                    abs(cyc.index(node_15) - cyc.index(node_16)) == 1
                    or abs(cyc.index(node_15) - cyc.index(node_16)) == len(cyc) - 1
                )

                # Guaranteed edge 4
                # odd first, then evens, then second odd
                node_17 = (
                    (1,) * (odd_val_1)
                    + (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                    + (0,)
                )
                node_18 = (
                    (1,) * (odd_val_1 - 1)
                    + (0, 1)
                    + (0,) * (odd_val_0 - 2)
                    + (2,) * (even_val_2)
                    + (0,)
                )
                assert (
                    abs(cyc.index(node_17) - cyc.index(node_18)) == 1
                    or abs(cyc.index(node_17) - cyc.index(node_18)) == len(cyc) - 1
                )
                node_19 = (
                    (1,) * (odd_val_1)
                    + (2,) * (even_val_2)
                    + (0,) * (odd_val_0 - 1)
                    + (0,)
                )
                node_20 = (
                    (1,) * (odd_val_1 - 1)
                    + (2, 1)
                    + (2,) * (even_val_2 - 1)
                    + (0,) * (odd_val_0 - 1)
                    + (0,)
                )
                assert (
                    abs(cyc.index(node_19) - cyc.index(node_20)) == 1
                    or abs(cyc.index(node_19) - cyc.index(node_20)) == len(cyc) - 1
                )
                node_21 = (
                    (0,) * (odd_val_0)
                    + (1,) * (odd_val_1 - 1)
                    + (2,) * (even_val_2)
                    + (1,)
                )
                node_22 = (
                    (0,) * (odd_val_0 - 1)
                    + (1, 0)
                    + (1,) * (odd_val_1 - 2)
                    + (2,) * (even_val_2)
                    + (1,)
                )
                assert (
                    abs(cyc.index(node_21) - cyc.index(node_22)) == 1
                    or abs(cyc.index(node_21) - cyc.index(node_22)) == len(cyc) - 1
                )
                node_23 = (
                    (0,) * (odd_val_0)
                    + (2,) * (even_val_2)
                    + (1,) * (odd_val_1 - 1)
                    + (1,)
                )
                node_24 = (
                    (0,) * (odd_val_0 - 1)
                    + (2, 0)
                    + (2,) * (even_val_2 - 1)
                    + (1,) * (odd_val_1 - 1)
                    + (1,)
                )
                assert (
                    abs(cyc.index(node_23) - cyc.index(node_24)) == 1
                    or abs(cyc.index(node_23) - cyc.index(node_24)) == len(cyc) - 1
                )

                # Guaranteed edge 5
                # odd (some even) then other odd, then even
                node_25 = (0,) * (odd_val_0) + (1,) * (odd_val_1) + (2,) * (even_val_2)
                node_26 = (
                    (0,) * (odd_val_0 - 1)
                    + (1, 0)
                    + (1,) * (odd_val_1 - 1)
                    + (2,) * (even_val_2)
                )
                assert (
                    abs(cyc.index(node_25) - cyc.index(node_26)) == 1
                    or abs(cyc.index(node_25) - cyc.index(node_26)) == len(cyc) - 1
                )
                node_27 = (1,) * (odd_val_1) + (0,) * (odd_val_0) + (2,) * (even_val_2)
                node_28 = (
                    (1,) * (odd_val_1 - 1)
                    + (0, 1)
                    + (0,) * (odd_val_0 - 1)
                    + (2,) * (even_val_2)
                )
                assert (
                    abs(cyc.index(node_27) - cyc.index(node_28)) == 1
                    or abs(cyc.index(node_27) - cyc.index(node_28)) == len(cyc) - 1
                )


# class Test_GuaranteedEdges_Two_Odd_Length_4:
#     def test_guaranteed_edges_Even_Even_1_1(self):
#         # this has the subgraph even, 1, 1 & odd, 2, 1
#         for even_val_0 in [4, 6]:
#             for even_val_1 in range(4, even_val_0 + 1, 2):
#                 odd_val_2 = 1
#                 odd_val_3 = 1
#                 cyc = get_connected_cycle_cover((even_val_0, even_val_1, odd_val_2, odd_val_3))

#                 # Guaranteed edge 1
#                 # guaranteed swap at odds
#                 node_1 = ()
#                 node_2 = (1,) * (odd_val_1 - 1) + (2,) * (even_val_2) + (0,) * (odd_val_0 - 1) + (1, 0)
#                 assert (
#                     abs(cyc.index(node_1) - cyc.index(node_2)) == 1
#                     or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
#                 )
