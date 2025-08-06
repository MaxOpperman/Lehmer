import pytest

from core.cycle_cover import get_connected_cycle_cover


class Test_GuaranteedEdges_All_Even_Length_3:
    def test_guaranteed_edges_Even_2_2(self):
        # this has the subgraph even, 1, 1 & odd, 2, 1
        for even_val in [2, 4, 6, 10, 14]:
            cyc = get_connected_cycle_cover((even_val, 2, 2))
            # there is one guaranteed edge x^{k_x-1} 0^{k_0} 1^{k_1} x & \sim x^{k_x-1} 0x 0^{k_0-1} 1^{k_1} x
            node_1 = (1,) + (0,) * (even_val) + (2, 2, 1)
            node_2 = (0, 1) + (0,) * (even_val - 1) + (2, 2, 1)
            assert (
                abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
            )
            node_3 = (1, 2, 2) + (0,) * (even_val) + (1,)
            node_4 = (2, 1, 2) + (0,) * (even_val) + (1,)
            assert (
                abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
            )
            node_5 = (2,) + (0,) * (even_val) + (1, 1, 2)
            node_6 = (0, 2) + (0,) * (even_val - 1) + (1, 1, 2)
            assert (
                abs(cyc.index(node_5) - cyc.index(node_6)) == 1
                or abs(cyc.index(node_5) - cyc.index(node_6)) == len(cyc) - 1
            )
            node_7 = (2, 1, 1) + (0,) * (even_val) + (2,)
            node_8 = (1, 2, 1) + (0,) * (even_val) + (2,)
            assert (
                abs(cyc.index(node_7) - cyc.index(node_8)) == 1
                or abs(cyc.index(node_7) - cyc.index(node_8)) == len(cyc) - 1
            )
            node_9 = (0,) * (even_val - 1) + (1, 1, 2, 2, 0)
            node_10 = (0,) * (even_val - 2) + (1, 0, 1, 2, 2, 0)
            assert (
                abs(cyc.index(node_9) - cyc.index(node_10)) == 1
                or abs(cyc.index(node_9) - cyc.index(node_10)) == len(cyc) - 1
            )
            node_11 = (0,) * (even_val - 1) + (2, 2, 1, 1, 0)
            node_12 = (0,) * (even_val - 2) + (2, 0, 2, 1, 1, 0)
            assert (
                abs(cyc.index(node_11) - cyc.index(node_12)) == 1
                or abs(cyc.index(node_11) - cyc.index(node_12)) == len(cyc) - 1
            )

    def test_guaranteed_edges_Even_Even_2(self):
        # this has the subgraph even, odd, 1 & odd, even, 1
        for even_val_0 in [4, 6]:
            for even_val_1 in range(4, even_val_0 + 1, 2):
                print(f"computed sig {even_val_0, even_val_1, 2}")
                cyc = get_connected_cycle_cover((even_val_0, even_val_1, 2))
                # there is one guaranteed edge x^{k_x-1} 0^{k_0} 1^{k_1} x & \sim x^{k_x-1} 0x 0^{k_0-1} 1^{k_1} x
                node_1 = (1,) * (even_val_1 - 1) + (0,) * (even_val_0) + (2, 2, 1)
                node_2 = (
                    (1,) * (even_val_1 - 2)
                    + (0, 1)
                    + (0,) * (even_val_0 - 1)
                    + (2, 2, 1)
                )
                assert (
                    abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                    or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
                )
                node_3 = (1,) * (even_val_1 - 1) + (2, 2) + (0,) * (even_val_0) + (1,)
                node_4 = (
                    (1,) * (even_val_1 - 2) + (2, 1, 2) + (0,) * (even_val_0) + (1,)
                )
                assert (
                    abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                    or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
                )
                node_5 = (2,) + (0,) * (even_val_0) + (1,) * (even_val_1) + (2,)
                node_6 = (0, 2) + (0,) * (even_val_0 - 1) + (1,) * (even_val_1) + (2,)
                assert (
                    abs(cyc.index(node_5) - cyc.index(node_6)) == 1
                    or abs(cyc.index(node_5) - cyc.index(node_6)) == len(cyc) - 1
                )
                node_7 = (2,) + (1,) * (even_val_1) + (0,) * (even_val_0) + (2,)
                node_8 = (1, 2) + (1,) * (even_val_1 - 1) + (0,) * (even_val_0) + (2,)
                assert (
                    abs(cyc.index(node_7) - cyc.index(node_8)) == 1
                    or abs(cyc.index(node_7) - cyc.index(node_8)) == len(cyc) - 1
                )
                node_9 = (0,) * (even_val_0 - 1) + (1,) * (even_val_1) + (2, 2, 0)
                node_10 = (
                    (0,) * (even_val_0 - 2)
                    + (1, 0)
                    + (1,) * (even_val_1 - 1)
                    + (2, 2, 0)
                )
                assert (
                    abs(cyc.index(node_9) - cyc.index(node_10)) == 1
                    or abs(cyc.index(node_9) - cyc.index(node_10)) == len(cyc) - 1
                )
                node_11 = (0,) * (even_val_0 - 1) + (2, 2) + (1,) * (even_val_1) + (0,)
                node_12 = (
                    (0,) * (even_val_0 - 2) + (2, 0, 2) + (1,) * (even_val_1) + (0,)
                )
                assert (
                    abs(cyc.index(node_11) - cyc.index(node_12)) == 1
                    or abs(cyc.index(node_11) - cyc.index(node_12)) == len(cyc) - 1
                )

    def test_guaranteed_edges_Even_Even_Even(self):
        # this has the subgraph two odd - rest even
        for even_val_0 in [4, 6]:
            for even_val_1 in range(4, even_val_0 + 1, 2):
                for even_val_2 in range(4, even_val_1 + 1, 2):
                    if (even_val_0, even_val_1, even_val_2) == (6, 6, 6):
                        # this is slightly too slow :(
                        break
                    cyc = get_connected_cycle_cover(
                        (even_val_0, even_val_1, even_val_2)
                    )
                    # there is one guaranteed edge x^{k_x-1} 0^{k_0} 1^{k_1} x & \sim x^{k_x-1} 0x 0^{k_0-1} 1^{k_1} x
                    node_1 = (
                        (1,) * (even_val_1 - 1)
                        + (0,) * (even_val_0)
                        + (2,) * (even_val_2)
                        + (1,)
                    )
                    node_2 = (
                        (1,) * (even_val_1 - 2)
                        + (0, 1)
                        + (0,) * (even_val_0 - 1)
                        + (2,) * (even_val_2)
                        + (1,)
                    )
                    assert (
                        abs(cyc.index(node_1) - cyc.index(node_2)) == 1
                        or abs(cyc.index(node_1) - cyc.index(node_2)) == len(cyc) - 1
                    )
                    node_3 = (
                        (1,) * (even_val_1 - 1)
                        + (2,) * (even_val_2)
                        + (0,) * (even_val_0)
                        + (1,)
                    )
                    node_4 = (
                        (1,) * (even_val_1 - 2)
                        + (
                            2,
                            1,
                        )
                        + (2,) * (even_val_2 - 1)
                        + (0,) * (even_val_0)
                        + (1,)
                    )
                    assert (
                        abs(cyc.index(node_3) - cyc.index(node_4)) == 1
                        or abs(cyc.index(node_3) - cyc.index(node_4)) == len(cyc) - 1
                    )
                    node_5 = (
                        (2,) * (even_val_2 - 1)
                        + (0,) * (even_val_0)
                        + (1,) * (even_val_1)
                        + (2,)
                    )
                    node_6 = (
                        (2,) * (even_val_2 - 2)
                        + (0, 2)
                        + (0,) * (even_val_0 - 1)
                        + (1,) * (even_val_1)
                        + (2,)
                    )
                    assert (
                        abs(cyc.index(node_5) - cyc.index(node_6)) == 1
                        or abs(cyc.index(node_5) - cyc.index(node_6)) == len(cyc) - 1
                    )
                    node_7 = (
                        (2,) * (even_val_2 - 1)
                        + (1,) * (even_val_1)
                        + (0,) * (even_val_0)
                        + (2,)
                    )
                    node_8 = (
                        (2,) * (even_val_2 - 2)
                        + (1, 2)
                        + (1,) * (even_val_1 - 1)
                        + (0,) * (even_val_0)
                        + (2,)
                    )
                    assert (
                        abs(cyc.index(node_7) - cyc.index(node_8)) == 1
                        or abs(cyc.index(node_7) - cyc.index(node_8)) == len(cyc) - 1
                    )
                    node_9 = (
                        (0,) * (even_val_0 - 1)
                        + (1,) * (even_val_1)
                        + (2,) * (even_val_2)
                        + (0,)
                    )
                    node_10 = (
                        (0,) * (even_val_0 - 2)
                        + (1, 0)
                        + (1,) * (even_val_1 - 1)
                        + (2,) * (even_val_2)
                        + (0,)
                    )
                    assert (
                        abs(cyc.index(node_9) - cyc.index(node_10)) == 1
                        or abs(cyc.index(node_9) - cyc.index(node_10)) == len(cyc) - 1
                    )
                    node_11 = (
                        (0,) * (even_val_0 - 1)
                        + (2,) * (even_val_2)
                        + (1,) * (even_val_1)
                        + (0,)
                    )
                    node_12 = (
                        (0,) * (even_val_0 - 2)
                        + (2, 0)
                        + (2,) * (even_val_2 - 1)
                        + (1,) * (even_val_1)
                        + (0,)
                    )
                    assert (
                        abs(cyc.index(node_11) - cyc.index(node_12)) == 1
                        or abs(cyc.index(node_11) - cyc.index(node_12)) == len(cyc) - 1
                    )
