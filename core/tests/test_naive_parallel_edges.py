import pytest

from core.helper_operations.naive_parallel_edges import (
    filter_adjacent_edges_by_tail,
    find_cross_edges,
    find_end_tuple_order,
    find_parallel_edges_in_cycle_cover,
)


class Test_Find_Tails_Order:
    def test_empty_cycle_cover(self):
        with pytest.raises(
            ValueError, match="Cycle cover should contain at least one cycle"
        ):
            find_end_tuple_order([])
        with pytest.raises(
            ValueError, match="Cycle cover should contain at least one cycle"
        ):
            find_end_tuple_order([], True)

    def test_invalid_cycle_cover_structure(self):
        cc = [[(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]]
        with pytest.raises(ValueError):
            find_end_tuple_order(cc)
        with pytest.raises(ValueError):
            find_end_tuple_order(cc, True)

    def test_no_tails(self):
        cc = [
            [[(0, 1, 1), (1, 0, 1), (1, 1, 0)]],
            [[(1, 2, 3), (2, 1, 3), (2, 3, 1), (3, 2, 1), (3, 1, 2), (1, 3, 2)]],
        ]
        with pytest.raises(ValueError):
            find_end_tuple_order(cc)
        with pytest.raises(ValueError):
            find_end_tuple_order(cc, True)

    def test_no_tails_len3(self):
        cc = [
            [[(0, 1, 1), (1, 0, 1), (1, 1, 0)]],
            [[(1, 2, 0), (2, 1, 0), (2, 0, 1), (0, 2, 1), (0, 1, 2), (1, 0, 2)]],
        ]
        res1 = find_end_tuple_order(cc)
        assert res1 == [(0, 1), (0, 1)]
        with pytest.raises(ValueError):
            find_end_tuple_order(cc, True)

    def test_simple(self):
        cc = [[[(0, 1, 1), (1, 0, 1)]], [[(1, 1, 0)]]]
        res1 = find_end_tuple_order(cc)
        assert res1 == [(0, 1), (1, 0)]
        res2 = find_end_tuple_order(cc, True)
        assert res2 == [(1, 0, 1), (1, 1, 0)]

    def test_sig_1_2_1(self):
        cc = [
            [[(0, 1, 1, 2), (1, 0, 1, 2), (1, 1, 0, 2)]],
            [[(2, 1, 1, 0), (1, 2, 1, 0), (1, 1, 2, 0)]],
            [
                [
                    (2, 1, 0, 1),
                    (1, 2, 0, 1),
                    (1, 0, 2, 1),
                    (0, 1, 2, 1),
                    (0, 2, 1, 1),
                    (2, 0, 1, 1),
                ]
            ],
        ]
        res1 = find_end_tuple_order(cc)
        assert res1 == [(0, 2), (1, 0), (2, 1)]
        res2 = find_end_tuple_order(cc, True)
        assert res2 == [(1, 0, 2), (1, 1, 0), (0, 2, 1)]

    def test_sig_multiple_parallel_tails(self):
        # should select the lexicographical minimum tails
        cc = [
            [
                [
                    (0, 1, 1, 2),
                    (1, 0, 1, 2),
                    (1, 1, 0, 2),
                    (2, 1, 1, 0),
                    (1, 2, 1, 0),
                    (1, 1, 2, 0),
                ]
            ],
            [
                [
                    (2, 1, 0, 1),
                    (1, 2, 0, 1),
                    (1, 0, 2, 1),
                    (0, 1, 2, 1),
                    (0, 2, 1, 1),
                    (2, 0, 1, 1),
                ]
            ],
        ]
        res1 = find_end_tuple_order(cc)
        assert res1 == [(1, 0), (0, 1)]
        res2 = find_end_tuple_order(cc, True)
        assert res2 == [(0, 1, 2), (0, 2, 1)]


class Test_Filter_Adjacent_Edges_By_Tail:
    def test_filter_empty(self):
        cyc = []
        tail = tuple()
        with pytest.raises(IndexError):
            filter_adjacent_edges_by_tail(cyc, tail)

    def test_filter_simple(self):
        cyc = [(1, 2, 0), (2, 1, 0), (2, 0, 1), (0, 2, 1), (0, 1, 2), (1, 0, 2)]
        res1 = filter_adjacent_edges_by_tail(cyc, (1, 0))
        assert res1 == []
        res2 = filter_adjacent_edges_by_tail(cyc, (0,))
        assert res2 == [((1, 2, 0), (2, 1, 0))]
        res2 = filter_adjacent_edges_by_tail(cyc, (1,))
        assert res2 == [((2, 0, 1), (0, 2, 1))]
        res2 = filter_adjacent_edges_by_tail(cyc, (2,))
        assert res2 == [((0, 1, 2), (1, 0, 2))]
        res3 = filter_adjacent_edges_by_tail(cyc, tuple())
        assert res3 == []


class Test_Find_Parallel_Edges_In_Cycle_Cover:
    def test_empty_cycle_cover(self):
        assert find_parallel_edges_in_cycle_cover([], []) == []
        assert find_parallel_edges_in_cycle_cover([], [(1, 2)]) == []

    def test_length_one_cycle(self):
        cc = [
            [
                (0, 1, 1, 2),
                (1, 0, 1, 2),
                (1, 1, 0, 2),
                (2, 1, 1, 0),
                (1, 2, 1, 0),
                (1, 1, 2, 0),
            ]
        ]
        res = find_parallel_edges_in_cycle_cover(
            cc,
            [(2, 3)],
        )
        assert res == {(2, 3): [[]]}
        res = find_parallel_edges_in_cycle_cover(cc, [(2, 1)])
        assert res == {(2, 1): [[]]}
        res = find_parallel_edges_in_cycle_cover(cc, [(1, 2)])
        assert res == {(1, 2): [[((0, 1, 1, 2), (1, 0, 1, 2))]]}

    def test_length_two_cycles(self):
        cc = [
            [
                [
                    (0, 1, 1, 2),
                    (1, 0, 1, 2),
                    (1, 1, 0, 2),
                    (2, 1, 1, 0),
                    (1, 2, 1, 0),
                    (1, 1, 2, 0),
                ]
            ],
            [
                [
                    (2, 1, 0, 1),
                    (1, 2, 0, 1),
                    (1, 0, 2, 1),
                    (0, 1, 2, 1),
                    (0, 2, 1, 1),
                    (2, 0, 1, 1),
                ]
            ],
        ]
        with pytest.raises(ValueError):
            find_parallel_edges_in_cycle_cover(cc, [(2, 3)])
        with pytest.raises(ValueError):
            find_parallel_edges_in_cycle_cover(cc, [(0, 2)])
        res = find_parallel_edges_in_cycle_cover(cc, [(1, 2)])
        assert res == {
            (1, 2): [((0, 1, 1, 2), (1, 0, 1, 2))],
            (2, 1): [((1, 0, 2, 1), (0, 1, 2, 1))],
        }
        res = find_parallel_edges_in_cycle_cover(cc, [(1, 0)])
        assert res == {
            (1, 0): [((2, 1, 1, 0), (1, 2, 1, 0))],
            (0, 1): [((2, 1, 0, 1), (1, 2, 0, 1))],
        }

    def test_weird_cycles(self):
        cc = [
            [[(2, 1, 1, 0), (1, 2, 1, 0), (1, 1, 2, 0)]],
            [
                [
                    (2, 1, 0, 1),
                    (1, 2, 0, 1),
                    (1, 0, 2, 1),
                    (0, 1, 2, 1),
                    (0, 2, 1, 1),
                    (2, 0, 1, 1),
                ]
            ],
            [[(1, 1, 0, 2), (1, 0, 1, 2), (0, 1, 1, 2)]],
        ]
        res = find_parallel_edges_in_cycle_cover(cc, [(1, 0), (2, 1)])
        assert res == {
            (1, 0): [((2, 1, 1, 0), (1, 2, 1, 0))],
            (0, 1): [((2, 1, 0, 1), (1, 2, 0, 1))],
            (2, 1): [((1, 0, 2, 1), (0, 1, 2, 1))],
            (1, 2): [((1, 0, 1, 2), (0, 1, 1, 2))],
        }
        with pytest.raises(ValueError):
            find_parallel_edges_in_cycle_cover(cc, [(1, 0), (0, 1)])


class Test_Find_Cross_Edges:
    def test_empty_cycle_cover(self):
        with pytest.raises(
            ValueError, match="Cycle cover should contain at least one cycle."
        ):
            find_cross_edges([], [])
        with pytest.raises(
            ValueError, match="Cycle cover should contain at least one cycle."
        ):
            find_cross_edges([], [(1, 0)])

    def test_len_one_cycle_cover(self):
        cc = [
            [
                (0, 1, 1, 2),
                (1, 0, 1, 2),
                (1, 1, 0, 2),
                (2, 1, 1, 0),
                (1, 2, 1, 0),
                (1, 1, 2, 0),
            ]
        ]
        with pytest.raises(ValueError):
            find_cross_edges(cc, [(1, 2)])

    def test_simple_cycle(self):
        cc = [
            [[(2, 1, 1, 0), (1, 2, 1, 0), (1, 1, 2, 0)]],
            [
                [
                    (2, 1, 0, 1),
                    (1, 2, 0, 1),
                    (1, 0, 2, 1),
                    (0, 1, 2, 1),
                    (0, 2, 1, 1),
                    (2, 0, 1, 1),
                ]
            ],
            [[(1, 1, 0, 2), (1, 0, 1, 2), (0, 1, 1, 2)]],
        ]
        res = find_cross_edges(cc, [(1, 0), (2, 1)])
        assert res == {
            ((1, 0), (0, 1)): [
                (((2, 1, 1, 0), (1, 2, 1, 0)), ((2, 1, 0, 1), (1, 2, 0, 1)))
            ],
            ((2, 1), (1, 2)): [
                (((1, 0, 2, 1), (0, 1, 2, 1)), ((1, 0, 1, 2), (0, 1, 1, 2)))
            ],
        }

    def test_multiple_cross_edges_2_2_1(self):
        cc221 = [
            [[(0, 1, 0, 1, 2), (0, 1, 1, 0, 2), (1, 0, 1, 0, 2), (1, 0, 0, 1, 2)]],
            [
                [
                    (1, 0, 0, 2, 1),
                    (1, 0, 2, 0, 1),
                    (0, 1, 2, 0, 1),
                    (0, 2, 1, 0, 1),
                    (1, 2, 0, 0, 1),
                    (2, 1, 0, 0, 1),
                    (2, 0, 1, 0, 1),
                    (2, 0, 0, 1, 1),
                    (0, 2, 0, 1, 1),
                    (0, 0, 2, 1, 1),
                    (0, 0, 1, 2, 1),
                    (0, 1, 0, 2, 1),
                ]
            ],
            [
                [
                    (0, 2, 1, 1, 0),
                    (2, 0, 1, 1, 0),
                    (2, 1, 0, 1, 0),
                    (2, 1, 1, 0, 0),
                    (1, 2, 1, 0, 0),
                    (1, 1, 2, 0, 0),
                    (1, 1, 0, 2, 0),
                    (1, 0, 1, 2, 0),
                    (0, 1, 1, 2, 0),
                    (0, 1, 2, 1, 0),
                    (1, 0, 2, 1, 0),
                    (1, 2, 0, 1, 0),
                ]
            ],
        ]
        res = find_cross_edges(cc221, [(1, 2), (0, 1)])
        assert res == {
            ((1, 2), (2, 1)): [
                (((1, 0, 0, 1, 2), (0, 1, 0, 1, 2)), ((1, 0, 0, 2, 1), (0, 1, 0, 2, 1)))
            ],
            ((0, 1), (1, 0)): [
                (
                    ((1, 0, 2, 0, 1), (0, 1, 2, 0, 1)),
                    ((1, 0, 2, 1, 0), (0, 1, 2, 1, 0)),
                ),
                (
                    ((2, 1, 0, 0, 1), (2, 0, 1, 0, 1)),
                    ((2, 1, 0, 1, 0), (2, 0, 1, 1, 0)),
                ),
            ],
        }
