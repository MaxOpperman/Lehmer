import pytest

from cycle_cover import get_connected_cycle_cover


class Test_GuaranteedEdges_Even_1_1_1:
    def test_guaranteed_edges_Even_1_1_1(self):
        for even_val in [2, 4, 6, 10, 14]:
            cyc = get_connected_cycle_cover((even_val, 1, 1, 1))
            # test_guaranteed 1230^k0 1320^k0
            node_1 = (1, 2, 3) + (0,) * (even_val)
            node_2 = (1, 3, 2) + (0,) * (even_val)
            assert (
                abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
            )

            # test_guaranteed 2130^k0 2310^k0
            node_3 = (2, 1, 3) + (0,) * (even_val)
            node_4 = (2, 3, 1) + (0,) * (even_val)
            assert (
                abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
            )

            # test_guaranteed xy0^{k_0}z ~ yx0^{k_0}z
            node_5 = (1, 2) + (0,) * (even_val) + (3,)
            node_6 = (2, 1) + (0,) * (even_val) + (3,)
            assert (
                abs(cyc.index(node_5) - cyc.index(node_6)) == 1
                or abs(cyc.index(node_5) - cyc.index(node_6)) == len(cyc) - 1
            )
            node_7 = (1, 3) + (0,) * (even_val) + (2,)
            node_8 = (3, 1) + (0,) * (even_val) + (2,)
            assert (
                abs(cyc.index(node_7) - cyc.index(node_8)) == 1
                or abs(cyc.index(node_7) - cyc.index(node_8)) == len(cyc) - 1
            )
            node_9 = (2, 3) + (0,) * (even_val) + (1,)
            node_10 = (3, 2) + (0,) * (even_val) + (1,)
            assert (
                abs(cyc.index(node_9) - cyc.index(node_10)) == 1
                or abs(cyc.index(node_9) - cyc.index(node_10)) == len(cyc) - 1
            )

            # test_guaranteed x0^{k_0}yz ~ 0x0^{k_0-1}yz
            node_11 = (1,) + (0,) * (even_val) + (2, 3)
            node_12 = (0, 1) + (0,) * (even_val - 1) + (2, 3)
            node_13 = (1,) + (0,) * (even_val) + (3, 2)
            node_14 = (0, 1) + (0,) * (even_val - 1) + (3, 2)
            node_15 = (2,) + (0,) * (even_val) + (3, 1)
            node_16 = (0, 2) + (0,) * (even_val - 1) + (3, 1)
            node_17 = (2,) + (0,) * (even_val) + (1, 3)
            node_18 = (0, 2) + (0,) * (even_val - 1) + (1, 3)
            node_19 = (3,) + (0,) * (even_val) + (2, 1)
            node_20 = (0, 3) + (0,) * (even_val - 1) + (2, 1)
            node_21 = (3,) + (0,) * (even_val) + (1, 2)
            node_22 = (0, 3) + (0,) * (even_val - 1) + (1, 2)
            for n1, n2 in [
                (node_11, node_12),
                (node_13, node_14),
                (node_15, node_16),
                (node_17, node_18),
                (node_19, node_20),
                (node_21, node_22),
            ]:
                assert (
                    abs(cyc.index(n1) - cyc.index(n2)) == 1
                    or abs(cyc.index(n1) - cyc.index(n2)) == len(cyc) - 1
                )


class Test_GuaranteedEdges_Even_2_1_1:
    def test_guaranteed_edges_Even_2_1_1(self):
        for even_val in [2, 4, 6, 10, 14]:
            cyc = get_connected_cycle_cover((even_val, 2, 1, 1))
            # test_guaranteed 20^{k_0}113 ~ 020^{k_0-1}113
            node_1 = (2,) + (0,) * (even_val) + (1, 1, 3)
            node_2 = (0, 2) + (0,) * (even_val - 1) + (1, 1, 3)
            assert (
                abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
            )

            # test_guaranteed 30^{k_0}112 ~ 030^{k_0-1}112
            node_3 = (3,) + (0,) * (even_val) + (1, 1, 2)
            node_4 = (0, 3) + (0,) * (even_val - 1) + (1, 1, 2)
            assert (
                abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
            )

            # test_guaranteed 20^{k_0}131 ~ 020^{k_0-1}131
            node_5 = (2,) + (0,) * (even_val) + (1, 3, 1)
            node_6 = (0, 2) + (0,) * (even_val - 1) + (1, 3, 1)
            assert (
                abs(cyc.index(node_5) - cyc.index(node_6)) == 1
                or abs(cyc.index(node_5) - cyc.index(node_6)) == len(cyc) - 1
            )

            # test_guaranteed 30^{k_0}121 ~ 030^{k_0-1}121
            node_7 = (3,) + (0,) * (even_val) + (1, 2, 1)
            node_8 = (0, 3) + (0,) * (even_val - 1) + (1, 2, 1)
            assert (
                abs(cyc.index(node_7) - cyc.index(node_8)) == 1
                or abs(cyc.index(node_7) - cyc.index(node_8)) == len(cyc) - 1
            )

            # test_guaranteed 20^{k_0}311 ~ 020^{k_0-1}311
            node_9 = (2,) + (0,) * (even_val) + (3, 1, 1)
            node_10 = (0, 2) + (0,) * (even_val - 1) + (3, 1, 1)
            assert (
                abs(cyc.index(node_9) - cyc.index(node_10)) == 1
                or abs(cyc.index(node_9) - cyc.index(node_10)) == len(cyc) - 1
            )

            # test_guaranteed 30^{k_0}211 ~ 030^{k_0-1}211
            node_11 = (3,) + (0,) * (even_val) + (2, 1, 1)
            node_12 = (0, 3) + (0,) * (even_val - 1) + (2, 1, 1)
            assert (
                abs(cyc.index(node_11) - cyc.index(node_12)) == 1
                or abs(cyc.index(node_11) - cyc.index(node_12)) == len(cyc) - 1
            )

            # test_guaranteed 3110^{k_0-1}20 ~ 1310^{k_0-1}20
            node_13 = (3, 1, 1) + (0,) * (even_val - 1) + (2, 0)
            node_14 = (1, 3, 1) + (0,) * (even_val - 1) + (2, 0)
            assert (
                abs(cyc.index(node_13) - cyc.index(node_14)) == 1
                or abs(cyc.index(node_13) - cyc.index(node_14)) == len(cyc) - 1
            )

            # test_guaranteed 2110^{k_0-1}30 ~ 1210^{k_0-1}30
            node_15 = (2, 1, 1) + (0,) * (even_val - 1) + (3, 0)
            node_16 = (1, 2, 1) + (0,) * (even_val - 1) + (3, 0)
            assert (
                abs(cyc.index(node_16) - cyc.index(node_15)) == 1
                or abs(cyc.index(node_16) - cyc.index(node_15)) == len(cyc) - 1
            )

            # test_guaranteed 0^{k_0}1123\sim 0^{k_0}1213
            node_17 = (0,) * (even_val) + (1, 1, 2, 3)
            node_18 = (0,) * (even_val) + (1, 2, 1, 3)
            assert (
                abs(cyc.index(node_17) - cyc.index(node_18)) == 1
                or abs(cyc.index(node_17) - cyc.index(node_18)) == len(cyc) - 1
            )

            # test_guaranteed 0^{k_0}1132\sim 0^{k_0}1312
            node_19 = (0,) * (even_val) + (1, 1, 3, 2)
            node_20 = (0,) * (even_val) + (1, 3, 1, 2)
            assert (
                abs(cyc.index(node_19) - cyc.index(node_20)) == 1
                or abs(cyc.index(node_19) - cyc.index(node_20)) == len(cyc) - 1
            )

            # test_guaranteed 110^{k_0}32 \sim 1010^{k_0-1}32
            node_21 = (1, 1) + (0,) * (even_val) + (3, 2)
            node_22 = (1, 0, 1) + (0,) * (even_val - 1) + (3, 2)
            assert (
                abs(cyc.index(node_21) - cyc.index(node_22)) == 1
                or abs(cyc.index(node_21) - cyc.index(node_22)) == len(cyc) - 1
            )

            # test_guaranteed 110^{k_0}23 \sim 1010^{k_0-1}23
            node_23 = (1, 1) + (0,) * (even_val) + (2, 3)
            node_24 = (1, 0, 1) + (0,) * (even_val - 1) + (2, 3)
            assert (
                abs(cyc.index(node_23) - cyc.index(node_24)) == 1
                or abs(cyc.index(node_23) - cyc.index(node_24)) == len(cyc) - 1
            )
