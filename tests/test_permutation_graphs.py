"""
Smoke test for permutation graphs

Copyright (c) 2018 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the (To Be Supplied) License.
"""

import pytest

from helper_operations.permutation_graphs import (
    HpathQ,
    _halveSignature,
    _permutations,
    _stutterize,
    binomial,
    count_inversions,
    defect,
    extend,
    extend_cycle_cover,
    generate_adj,
    get_num_of_inversions,
    graph,
    multinomial,
    multiset,
    nonStutterPermutations,
    perm,
    rotate,
    selectByTail,
    shorten,
    signature,
    stutterPermutations,
    swapPair,
)


class TestMain:
    def test_binomial_negative(self):
        with pytest.raises(AssertionError):
            binomial(-1, 0)
        with pytest.raises(AssertionError):
            binomial(0, -1)
        with pytest.raises(AssertionError):
            binomial(-1, -1)

    def test_binomial_0_0(self):
        result = binomial(0, 0)
        assert result == 1

    def test_binomial_0_1(self):
        result = binomial(0, 1)
        assert result == 1

    def test_binomial_1_0(self):
        result = binomial(1, 0)
        assert result == 1

    def test_binomial_3_3(self):
        result = binomial(3, 3)
        assert result == 20

    def test_multinomial_empty(self):
        s = []
        result = multinomial(s)
        assert result == 1

    def test_multinomial_2(self):
        s = [2]
        result = multinomial(s)
        assert result == 1

    def test_multinomial_3_3(self):
        s = [3, 3]
        result = multinomial(s)
        assert result == 20

    def test_multinomial_3_2_1(self):
        s = [3, 2, 1]
        result = multinomial(s)
        assert result == 60

    def test_multinomial_negative(self):
        with pytest.raises(AssertionError):
            multinomial([-1])
        with pytest.raises(AssertionError):
            multinomial([1, -1])
        with pytest.raises(AssertionError):
            multinomial([1, 1, -1])
        with pytest.raises(AssertionError):
            multinomial([1, 1, -2, -1])

    def test_signature_empty(self):
        p = tuple()
        result = signature(p)
        assert not result

    def test_signature_1(self):
        p = (0,)
        result = signature(p)
        assert result == [1]

    def test_signature_0_0_1(self):
        p = (2,)
        result = signature(p)
        assert result == [0, 0, 1]

    def test_signature_3_2_1(self):
        p = (2, 0, 1, 0, 1, 0)
        result = signature(p)
        assert result == [3, 2, 1]

    def test_signature_2_0_1(self):
        p = (2, 0, 0)
        result = signature(p)
        assert result == [2, 0, 1]

    def test_signature_2_3_1(self):
        p = (1, 0, 1, 2, 0, 1)
        result = signature(p)
        assert result == [2, 3, 1]

    def check_permutations(self, s: list[int], ps: list[list[int]]):
        """Check that all permutations in ps differ, none are missing, and all have signature s"""
        assert len(ps) == len(set(tuple(p) for p in ps))  # no duplicates
        assert len(ps) == multinomial(s)  # no missing
        assert all(signature(p) == s for p in ps)  # all have signature s

    def test_perm_empty(self):
        """Empty signature"""
        s = []
        result = perm(s)
        assert result == [[]]

    def test_perm_0(self):
        """Singleton signature without objects"""
        s = [0]
        result = perm(s)
        assert result == [[]]

    def test_perm_2(self):
        """Two objects of same color"""
        s = [2]
        result = perm(s)
        self.check_permutations(s, result)

    def test_perm_2_0_1(self):
        """Three objects with two colors"""
        s = [2, 0, 1]
        result = perm(s)
        # we may need to test this non-deterministically: length, all different, all with correct signature
        self.check_permutations(s, result)

    def test_perm_2_1_1(self):
        s = [2, 1, 1]
        result = perm(s)
        self.check_permutations(s, result)

    def test_get_number_of_inversions_empty(self):
        p = []
        result = get_num_of_inversions(p)
        assert result == 0

    def test_get_number_of_inversions_0(self):
        p = [5]
        result = get_num_of_inversions(p)
        assert result == 0

    def test_get_number_of_inversions_12(self):
        p = (1, 2)
        result = get_num_of_inversions(p)
        assert result == 0

    def test_get_number_of_inversions_21(self):
        p = (2, 1)
        result = get_num_of_inversions(p)
        assert result == 1

    def test_get_number_of_inversions_21113(self):
        p = (2, 1, 1, 1, 3)
        result = get_num_of_inversions(p)
        assert result == 3

    def test_get_number_of_inversions_202(self):
        p = (2, 0, 2)
        result = get_num_of_inversions(p)
        assert result == 1

    def test_count_inversions_empty(self):
        s = []
        result = count_inversions(s)
        assert result == dict()

    def test_count_inversions_0(self):
        s = [0]
        result = count_inversions(s)
        assert result == {(): 0}

    def test_count_inversions_2(self):
        s = [2]
        result = count_inversions(s)
        assert result == {
            (
                0,
                0,
            ): 0
        }

    def test_count_inversions_1_1(self):
        s = [0, 1, 1]
        result = count_inversions(s)
        assert result == {(1, 2): 0, (2, 1): 1}

    def test_count_inversions_2_1(self):
        s = [2, 1]
        result = count_inversions(s)
        assert result == {(0, 0, 1): 0, (0, 1, 0): 1, (1, 0, 0): 2}

    def test_count_inversions_2_2(self):
        s = [2, 2]
        result = count_inversions(s)
        assert result == {
            (0, 0, 1, 1): 0,
            (0, 1, 0, 1): 1,
            (1, 0, 0, 1): 2,
            (0, 1, 1, 0): 2,
            (1, 0, 1, 0): 3,
            (1, 1, 0, 0): 4,
        }

    def test_defect_empty(self):
        s = []
        result = defect(s)
        assert result == 0

    def test_defect_0(self):
        s = [0]
        result = defect(s)
        assert result == 0

    def test_defect_1_1(self):
        s = [1, 1]
        result = defect(s)
        assert result == 0

    def test_defect_4_1(self):
        s = [4, 1]
        result = defect(s)
        assert result == 1

    def test_defect_5_1(self):
        s = [5, 1]
        result = defect(s)
        assert result == 0

    def test_defect_2_2(self):
        s = [2, 2]
        result = defect(s)
        assert result == 2

    def test_defect_2_1_1(self):
        s = [2, 1, 1]
        result = defect(s)
        assert result == 0

    def test_defect_3_3_4(self):
        s = [3, 3, 4]
        result = defect(s)
        assert result == 0

    def test_defect_2_2_2(self):
        s = [2, 2, 2]
        result = defect(s)
        assert result == 6

    def test_swapPair_empty(self):
        p = tuple()
        with pytest.raises(ValueError):
            swapPair(p, 0)

    def test_swapPair_0(self):
        p = (0,)
        with pytest.raises(ValueError):
            swapPair(p, 0)

    def test_swapPair_12(self):
        p = (1, 2)
        result = swapPair(p, 0)
        assert result == (2, 1)

    def test_swapPair_21(self):
        p = (2, 1)
        result = swapPair(p, 0)
        assert result == (1, 2)

    def test_swapPair_00012(self):
        p = (0, 0, 0, 1, 2)
        assert swapPair(p, 0) == (0, 0, 0, 1, 2)
        assert swapPair(p, 1) == (0, 0, 0, 1, 2)
        assert swapPair(p, 2) == (0, 0, 1, 0, 2)
        assert swapPair(p, 3) == (0, 0, 0, 2, 1)
        with pytest.raises(ValueError):
            swapPair(p, 4)

    def test_swapPair_00012_negative_i(self):
        p = (0, 0, 0, 1, 2)
        assert swapPair(p, -1) == (2, 0, 0, 1, 0)
        assert swapPair(p, -2) == (0, 0, 0, 2, 1)
        assert swapPair(p, -3) == (0, 0, 1, 0, 2)
        assert swapPair(p, -4) == (0, 0, 0, 1, 2)
        assert swapPair(p, -5) == (0, 0, 0, 1, 2)

    def test_swapPair_00012_with_j(self):
        p = (0, 0, 0, 1, 2)
        assert swapPair(p, 0, 0) == (0, 0, 0, 1, 2)
        assert swapPair(p, 1, 0) == (0, 0, 0, 1, 2)
        assert swapPair(p, 2, 0) == (0, 0, 0, 1, 2)
        assert swapPair(p, 3, 0) == (1, 0, 0, 0, 2)
        assert swapPair(p, 4, 0) == (2, 0, 0, 1, 0)
        with pytest.raises(ValueError):
            swapPair(p, 2, 5)
        assert swapPair(p, 2, 4) == (0, 0, 2, 1, 0)
        assert swapPair(p, -1, 0) == (2, 0, 0, 1, 0)
        assert swapPair(p, -2, 0) == (1, 0, 0, 0, 2)
        assert swapPair(p, 0, -1) == (2, 0, 0, 1, 0)

    def test_generate_adj_empty(self):
        p = []
        result = generate_adj(p)
        assert result == []

    def test_generate_adj_0(self):
        p = [0]
        result = generate_adj(p)
        assert result == []

    def test_generate_adj_12(self):
        p = (1, 2)
        result = generate_adj(p)
        assert result == [(2, 1)]

    def test_generate_adj_21(self):
        p = (2, 1)
        result = generate_adj(p)
        assert result == [(1, 2)]

    def test_generate_adj_10012(self):
        p = (1, 0, 0, 1, 2)
        result = generate_adj(p)
        assert result == [(0, 1, 0, 1, 2), (1, 0, 1, 0, 2), (1, 0, 0, 2, 1)]

    def test_generate_adj_100120(self):
        p = (1, 0, 0, 1, 2, 0)
        result = generate_adj(p)
        assert result == [
            (0, 1, 0, 1, 2, 0),
            (1, 0, 1, 0, 2, 0),
            (1, 0, 0, 2, 1, 0),
            (1, 0, 0, 1, 0, 2),
        ]

    def test_generate_adj_001122(self):
        p = (0, 0, 1, 1, 2, 2)
        result = generate_adj(p)
        assert result == [(0, 1, 0, 1, 2, 2), (0, 0, 1, 2, 1, 2)]

    def test_graph_empty(self):
        s = []
        result = graph(s)
        assert result == dict()

    def test_graph_0(self):
        s = [0]
        result = graph(s)
        assert result == {"": set()}

    def test_graph_5(self):
        s = [5]
        result = graph(s)
        assert result == {"00000": set()}

    def test_graph_2_1(self):
        s = [2, 1]
        result = graph(s)
        assert result == {"001": {"010"}, "010": {"001", "100"}, "100": {"010"}}

    def test_graph_2_2(self):
        s = [2, 2]
        result = graph(s)
        assert result == {
            "0011": {"0101"},
            "0101": {"0011", "0110", "1001"},
            "0110": {"0101", "1010"},
            "1010": {"0110", "1001", "1100"},
            "1001": {"0101", "1010"},
            "1100": {"1010"},
        }

    def test_extend_empty_list(self):
        p = []
        result = extend(p, (0,))
        assert result == []

    def test_extend_emtpy_tuple(self):
        p = [tuple()]
        result = extend(p, (0,))
        assert result == [(0,)]

    def test_extend_1(self):
        p = [(1,)]
        result = extend(p, (0,))
        assert result == [(1, 0)]

    def test_extend_3_descending(self):
        p = [(3,), (2,), (1,)]
        result = extend(p, (0,))
        assert result == [(3, 0), (2, 0), (1, 0)]

    def test_extend_2_2_with_01(self):
        p = [
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 0),
        ]
        result = extend(p, (0, 1))
        assert result == [
            (0, 0, 1, 1, 0, 1),
            (0, 1, 0, 1, 0, 1),
            (1, 0, 0, 1, 0, 1),
            (0, 1, 1, 0, 0, 1),
            (1, 0, 1, 0, 0, 1),
            (1, 1, 0, 0, 0, 1),
        ]

    def test_extend_2_2_with_54(self):
        p = [
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 0),
        ]
        result = extend(p, (5, 4, 8))
        assert result == [
            (0, 0, 1, 1, 5, 4, 8),
            (0, 1, 0, 1, 5, 4, 8),
            (1, 0, 0, 1, 5, 4, 8),
            (0, 1, 1, 0, 5, 4, 8),
            (1, 0, 1, 0, 5, 4, 8),
            (1, 1, 0, 0, 5, 4, 8),
        ]

    def test_extend_cycle_cover_empty(self):
        p = []
        with pytest.raises(AssertionError):
            extend_cycle_cover(p, (0,))

    def test_extend_cycle_cover_1(self):
        p = [[(1,)]]
        result = extend_cycle_cover(p, (0,))
        assert result == [[(1, 0)]]

    def test_extend_cycle_cover_2_2(self):
        p = [
            [
                (0, 0, 1, 1),
                (0, 1, 0, 1),
                (1, 0, 0, 1),
                (0, 1, 1, 0),
                (1, 0, 1, 0),
                (1, 1, 0, 0),
            ]
        ]
        result = extend_cycle_cover(p, (0, 1))
        assert result == [
            [
                (0, 0, 1, 1, 0, 1),
                (0, 1, 0, 1, 0, 1),
                (1, 0, 0, 1, 0, 1),
                (0, 1, 1, 0, 0, 1),
                (1, 0, 1, 0, 0, 1),
                (1, 1, 0, 0, 0, 1),
            ]
        ]

    def test_extend_cycle_cover_2_2_and_1_1(self):
        p = [
            [
                [
                    [
                        (0, 0, 1, 1),
                        (0, 1, 0, 1),
                        (1, 0, 0, 1),
                        (0, 1, 1, 0),
                        (1, 0, 1, 0),
                        (1, 1, 0, 0),
                    ]
                ]
            ],
            [[(0, 1), (1, 0)]],
        ]
        result = extend_cycle_cover(p, (0, 1))
        assert result == [
            [
                [
                    [
                        (0, 0, 1, 1, 0, 1),
                        (0, 1, 0, 1, 0, 1),
                        (1, 0, 0, 1, 0, 1),
                        (0, 1, 1, 0, 0, 1),
                        (1, 0, 1, 0, 0, 1),
                        (1, 1, 0, 0, 0, 1),
                    ]
                ]
            ],
            [[(0, 1, 0, 1), (1, 0, 0, 1)]],
        ]

    def test_extend_cycle_cover_2_2_and_1_1_and_0_0_0_2(self):
        p = [
            [
                [
                    [
                        (0, 0, 1, 1),
                        (0, 1, 0, 1),
                        (1, 0, 0, 1),
                        (0, 1, 1, 0),
                        (1, 0, 1, 0),
                        (1, 1, 0, 0),
                    ]
                ]
            ],
            [[(0, 1), (1, 0)]],
            [[[[(3,)]]]],
        ]
        result = extend_cycle_cover(p, (7,))
        assert result == [
            [
                [
                    [
                        (0, 0, 1, 1, 7),
                        (0, 1, 0, 1, 7),
                        (1, 0, 0, 1, 7),
                        (0, 1, 1, 0, 7),
                        (1, 0, 1, 0, 7),
                        (1, 1, 0, 0, 7),
                    ]
                ]
            ],
            [[(0, 1, 7), (1, 0, 7)]],
            [[[[(3, 7)]]]],
        ]

    def test_shorten_empty(self):
        p = []
        with pytest.raises(AssertionError):
            shorten(p, 0)

    def test_shorten_1_empty(self):
        p = [tuple()]
        result = shorten(p, 0)
        assert result == [tuple()]
        with pytest.raises(AssertionError):
            shorten(p, 1)

    def test_shorten_1_with_1(self):
        p = [(0,)]
        assert shorten(p, 0) == p
        result = shorten(p, 1)
        assert result == [tuple()]
        with pytest.raises(AssertionError):
            shorten(p, 2)

    def test_shorten_2_2_with_1(self):
        p = [(0, 1), (1, 0)]
        assert shorten(p, 0) == p
        result = shorten(p, 1)
        assert result == [(0,), (1,)]

    def test_shorten_long_with_2(self):
        p = [tuple([4] * 15), tuple([3] * 12)]
        result = shorten(p, 8)
        assert result == [tuple([4] * 7), tuple([3] * 4)]
        with pytest.raises(AssertionError):
            shorten(p, 13)

    def test_shorten_negative(self):
        p = [(0, 1, 2), (2, 1, 0)]
        result = shorten(p, -1)
        assert result == [(1, 2), (1, 0)]
        result = shorten(p, -2)
        assert result == [(2,), (0,)]

    def test_rotate_empty_with_0(self):
        p = []
        result = rotate(p, 0)
        assert result == []

    def test_rotate_empty_with_1(self):
        p = []
        result = rotate(p, 1)
        assert result == []

    def test_rotate_1_with_2(self):
        p = [(0,)]
        result = rotate(p, 2)
        assert result == [(0,)]

    def test_rotate_2_2_with_4(self):
        p = [
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 0),
        ]
        result = rotate(p, 4)
        assert result == [
            (1, 0, 1, 0),
            (1, 1, 0, 0),
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
        ]

    def test_rotate_2_2_out_of_bounds(self):
        p = [
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 0),
        ]
        assert rotate(p, len(p)) == p
        assert rotate(p, 7) == [
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 0),
            (0, 0, 1, 1),
        ]

    def test_rotate_2_2_negative(self):
        p = [
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 0),
        ]
        assert rotate(p, -len(p)) == p
        assert rotate(p, -7) == [
            (1, 1, 0, 0),
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
        ]
        assert rotate(p, -2) == [
            (1, 0, 1, 0),
            (1, 1, 0, 0),
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
        ]

    def test_halve_signature_empty(self):
        s = []
        result = _halveSignature(s)
        assert result == []

    def test_halve_signature_0(self):
        s = [0]
        result = _halveSignature(s)
        assert result == [0]

    def test_halve_signature_1(self):
        s = [1]
        result = _halveSignature(s)
        assert result == [0]

    def test_halve_signature_2(self):
        s = [2]
        result = _halveSignature(s)
        assert result == [1]

    def test_halve_signature_2_2_4_100_46_13(self):
        s = [2, 99, 4, 100, 46, 13]
        result = _halveSignature(s)
        assert result == [1, 49, 2, 50, 23, 6]

    def test_halve_signature_negative(self):
        s = [2, -1]
        with pytest.raises(ValueError):
            _halveSignature(s)

    def test_multiset_empty(self):
        s = []
        result = multiset(s)
        assert result == tuple()

    def test_multiset_0(self):
        s = [0]
        result = multiset(s)
        assert result == tuple()

    def test_multiset_2(self):
        s = [2]
        result = multiset(s)
        assert result == (0, 0)

    def test_multiset_2_0_1(self):
        s = [2, 0, 1]
        result = multiset(s)
        assert result == (0, 0, 2)

    def test_multiset_2_1_1_4(self):
        s = [2, 1, 1, 4]
        result = multiset(s)
        assert result == (0, 0, 1, 2, 3, 3, 3, 3)

    def test_multiset_negative(self):
        s = [2, -1]
        with pytest.raises(ValueError):
            multiset(s)

    def test_multiset_int(self):
        s = 50
        result = multiset(s)
        assert result == (0,) * 50

    def test_multiset_int_negative(self):
        s = -2
        with pytest.raises(ValueError):
            multiset(s)

    def test_permutations_empty(self):
        s = []
        result = _permutations(s)
        assert result == []

    def test_permutations_0(self):
        s = [0]
        result = _permutations(s)
        assert result == [tuple()]

    def test_permutations_2(self):
        s = [2]
        result = _permutations(s)
        assert result == [(0, 0)]

    def test_permutations_2_0_1(self):
        s = [2, 0, 1]
        result = _permutations(s)
        assert len(result) == 3 and len(set(result)) == 3
        for p in result:
            assert p in [(0, 0, 2), (0, 2, 0), (2, 0, 0)]

    def test_permutations_negative(self):
        s = [2, -1]
        with pytest.raises(ValueError):
            _permutations(s)

    def test_permutations_int(self):
        s = 3
        result = _permutations(s)
        assert result == [(0, 0, 0)]

    def test_permutations_int_negative(self):
        s = -2
        with pytest.raises(ValueError):
            _permutations(s)

    def test_stutterPermutations_empty(self):
        s = []
        result = stutterPermutations(s)
        assert result == []

    def test_stutterPermutations_0(self):
        s = [0]
        result = stutterPermutations(s)
        assert result == []

    def test_stutterPermutations_2(self):
        s = [2]
        result = stutterPermutations(s)
        assert result == [(0, 0)]

    def test_stutterPermutations_2_0_1(self):
        s = [2, 0, 1]
        result = stutterPermutations(s)
        assert result == [(0, 0, 2)]

    def test_stutterPermutations_more_odd(self):
        s = [2, 1, 1]
        assert stutterPermutations(s) == []

    def test_stutterPermutations_2_2_2(self):
        s = [2, 2, 2]
        result = stutterPermutations(s)
        assert len(result) == 6 and len(set(result)) == 6
        for p in result:
            assert p in [
                (0, 0, 1, 1, 2, 2),
                (0, 0, 2, 2, 1, 1),
                (1, 1, 0, 0, 2, 2),
                (1, 1, 2, 2, 0, 0),
                (2, 2, 0, 0, 1, 1),
                (2, 2, 1, 1, 0, 0),
            ]

    def test_stutterPermutations_negative(self):
        s = [2, -1]
        with pytest.raises(ValueError):
            stutterPermutations(s)

    def test_nonStutterPermutations_empty(self):
        s = []
        result = nonStutterPermutations(s)
        assert result == []

    def test_nonStutterPermutations_0(self):
        s = [0]
        result = nonStutterPermutations(s)
        assert result == []

    def test_nonStutterPermutations_2(self):
        s = [2]
        result = nonStutterPermutations(s)
        assert result == []

    def test_nonStutterPermutations_2_0_1(self):
        s = [2, 0, 1]
        result = nonStutterPermutations(s)
        assert result == [(0, 2, 0), (2, 0, 0)]

    def test_nonStutterPermutations_more_odd(self):
        s = [2, 1, 1]
        result = nonStutterPermutations(s)
        assert len(result) == len(set(result))
        assert len(result) == multinomial(s)

    def test_nonStutterPermutations_2_2(self):
        s = [2, 2]
        result = nonStutterPermutations(s)
        assert len(result) == 4 and len(set(result)) == 4
        for p in result:
            assert p in [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 1, 0)]

    def test_nonStutterPermutations_negative(self):
        s = [2, -1]
        with pytest.raises(ValueError):
            nonStutterPermutations(s)

    def test_stutterize_empty(self):
        s = []
        result = _stutterize(s)
        assert result == []

    def test_stutterize_0(self):
        s = [tuple()]
        result = _stutterize(s)
        assert result == [tuple()]

    def test_stutterize_2(self):
        s = [(0,)]
        result = _stutterize(s)
        assert result == [(0, 0)]

    def test_stutterize_1_1(self):
        s = [(0, 1), (1, 0)]
        result = _stutterize(s)
        assert result == [(0, 0, 1, 1), (1, 1, 0, 0)]

    def test_stutterize_2_2(self):
        s = [
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 0),
        ]
        result = _stutterize(s)
        assert result == [
            (0, 0, 0, 0, 1, 1, 1, 1),
            (0, 0, 1, 1, 0, 0, 1, 1),
            (1, 1, 0, 0, 0, 0, 1, 1),
            (0, 0, 1, 1, 1, 1, 0, 0),
            (1, 1, 0, 0, 1, 1, 0, 0),
            (1, 1, 1, 1, 0, 0, 0, 0),
        ]

    def test_select_by_tail_empty(self):
        p = []
        result = selectByTail(p, (0,))
        assert result == []

    def test_select_by_tail_0(self):
        p = [tuple()]
        result = selectByTail(p, (0,))
        assert result == []

    def test_select_by_tail_1(self):
        p = [(0,)]
        assert selectByTail(p, (0,)) == [(0,)]
        assert selectByTail(p, (1,)) == []

    def test_select_by_tail_1_1(self):
        p = [(0, 1), (1, 0)]
        assert selectByTail(p, (0,)) == [(1, 0)]
        assert selectByTail(p, (1,)) == [(0, 1)]

    def test_select_by_tail_2_0_0_2(self):
        p = [
            (0, 0, 3, 3),
            (0, 3, 0, 3),
            (3, 0, 0, 3),
            (0, 3, 3, 0),
            (3, 0, 3, 0),
            (3, 3, 0, 0),
        ]
        assert selectByTail(p, (0, 3)) == [(0, 3, 0, 3), (3, 0, 0, 3)]
        assert selectByTail(p, (0, 3, 0)) == [(3, 0, 3, 0)]
        assert selectByTail(p, (3, 3, 0, 0)) == [(3, 3, 0, 0)]
        assert selectByTail(p, (1,)) == []
        assert selectByTail(p, (0, 3, 3, 0, 0)) == []

    def test_HpathQ_empty(self):
        p = []
        result = HpathQ(p, [])
        assert result == False

    def test_HpathQ_0(self):
        p = [tuple()]
        result = HpathQ(p, [0])
        assert result == False

    def test_HpathQ_1(self):
        p = [(0,)]
        assert HpathQ(p, [0]) == False
        assert HpathQ(p, [1]) == False

    def test_HpathQ_1_1(self):
        p = [(0, 1), (1, 0)]
        assert HpathQ(p, [0, 1]) == False
        assert HpathQ(p, [1, 0]) == False
        assert HpathQ(p, [1, 1]) == True

    def test_HpathQ_2_2(self):
        p = [
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 0),
        ]
        assert HpathQ(p, [2, 2]) == False
        assert (
            HpathQ([(0, 1, 0, 1), (1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 1, 0)], [2, 2])
            == True
        )
        # contains a stutter
        assert (
            HpathQ(
                [(0, 0, 1, 1), (0, 1, 0, 1), (1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 1, 0)],
                [2, 2],
            )
            == False
        )
        # not a path
        assert (
            HpathQ([(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 1, 0)], [2, 2])
            == False
        )
        # incorrect signature
        assert (
            HpathQ([(0, 1, 0, 1), (1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 1, 0)], [2, 0, 2])
            == False
        )
