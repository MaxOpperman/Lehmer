import pytest

from helper_operations.permutation_graphs import (
    HcycleQ,
    HpathQ,
    _stutterize,
    extend_cycle_cover,
    halve_signature,
    multinomial,
    multiset,
    nonStutterPermutations,
    permutations_from_sig,
    stutterPermutations,
)


class TestStutterProperties:
    # Class that tests the helper_operations.permutation_graphs module
    # In specific, the functions that are related to stutter permutations and their properties
    def test_halve_signature_empty(self):
        s = tuple()
        result = halve_signature(s)
        assert result == tuple()

    def test_halve_signature_0(self):
        s = (0,)
        result = halve_signature(s)
        assert result == (0,)

    def test_halve_signature_1(self):
        s = (1,)
        result = halve_signature(s)
        assert result == (0,)

    def test_halve_signature_2(self):
        s = (2,)
        result = halve_signature(s)
        assert result == (1,)

    def test_halve_signature_2_2_4_100_46_13(self):
        s = (2, 99, 4, 100, 46, 13)
        result = halve_signature(s)
        assert result == (1, 49, 2, 50, 23, 6)

    def test_halve_signature_negative(self):
        s = (2, -1)
        with pytest.raises(ValueError):
            halve_signature(s)

    def test_multiset_empty(self):
        s = tuple()
        result = multiset(s)
        assert result == tuple()

    def test_multiset_0(self):
        s = (0,)
        result = multiset(s)
        assert result == tuple()

    def test_multiset_2(self):
        s = (2,)
        result = multiset(s)
        assert result == (0, 0)

    def test_multiset_2_0_1(self):
        s = (2, 0, 1)
        result = multiset(s)
        assert result == (0, 0, 2)

    def test_multiset_2_1_1_4(self):
        s = (2, 1, 1, 4)
        result = multiset(s)
        assert result == (0, 0, 1, 2, 3, 3, 3, 3)

    def test_multiset_negative(self):
        s = (2, -1)
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
        s = tuple()
        result = permutations_from_sig(s)
        assert result == []

    def test_permutations_0(self):
        s = (0,)
        result = permutations_from_sig(s)
        assert result == [tuple()]

    def test_permutations_2(self):
        s = (2,)
        result = permutations_from_sig(s)
        assert result == [(0, 0)]

    def test_permutations_2_0_1(self):
        s = (2, 0, 1)
        result = permutations_from_sig(s)
        assert len(result) == 3 and len(set(result)) == 3
        for p in result:
            assert p in [(0, 0, 2), (0, 2, 0), (2, 0, 0)]

    def test_permutations_negative(self):
        s = (2, -1)
        with pytest.raises(ValueError):
            permutations_from_sig(s)

    def test_permutations_int(self):
        s = 3
        result = permutations_from_sig(s)
        assert result == [(0, 0, 0)]

    def test_permutations_int_negative(self):
        s = -2
        with pytest.raises(ValueError):
            permutations_from_sig(s)

    def test_stutterPermutations_empty(self):
        s = tuple()
        result = stutterPermutations(s)
        assert result == []

    def test_stutterPermutations_0(self):
        s = (0,)
        result = stutterPermutations(s)
        assert result == []

    def test_stutterPermutations_2(self):
        s = (2,)
        result = stutterPermutations(s)
        assert result == [(0, 0)]

    def test_stutterPermutations_2_0_1(self):
        s = (2, 0, 1)
        result = stutterPermutations(s)
        assert result == [(0, 0, 2)]

    def test_stutterPermutations_more_odd(self):
        s = (2, 1, 1)
        assert stutterPermutations(s) == []

    def test_stutterPermutations_2_2_2(self):
        s = (2, 2, 2)
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
        s = (2, -1)
        with pytest.raises(ValueError):
            stutterPermutations(s)

    def test_nonStutterPermutations_empty(self):
        s = tuple()
        result = nonStutterPermutations(s)
        assert result == []

    def test_nonStutterPermutations_0(self):
        s = (0,)
        result = nonStutterPermutations(s)
        assert result == []

    def test_nonStutterPermutations_2(self):
        s = (2,)
        result = nonStutterPermutations(s)
        assert result == []

    def test_nonStutterPermutations_2_0_1(self):
        s = (2, 0, 1)
        result = nonStutterPermutations(s)
        assert result == [(0, 2, 0), (2, 0, 0)]

    def test_nonStutterPermutations_more_odd(self):
        s = (2, 1, 1)
        result = nonStutterPermutations(s)
        assert len(result) == len(set(result))
        assert len(result) == multinomial(s)

    def test_nonStutterPermutations_2_2(self):
        s = (2, 2)
        result = nonStutterPermutations(s)
        assert len(result) == 4 and len(set(result)) == 4
        for p in result:
            assert p in [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 1, 0)]

    def test_nonStutterPermutations_negative(self):
        s = (2, -1)
        with pytest.raises(ValueError):
            nonStutterPermutations(s)

    def test_stutterize_empty(self):
        p = []
        result = _stutterize(p)
        assert result == []

    def test_stutterize_0(self):
        p = [tuple()]
        result = _stutterize(p)
        assert result == [tuple()]

    def test_stutterize_2(self):
        p = [(0,)]
        result = _stutterize(p)
        assert result == [(0, 0)]

    def test_stutterize_1_1(self):
        p = [(0, 1), (1, 0)]
        result = _stutterize(p)
        assert result == [(0, 0, 1, 1), (1, 1, 0, 0)]

    def test_stutterize_2_2(self):
        p = [
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 0),
        ]
        result = _stutterize(p)
        assert result == [
            (0, 0, 0, 0, 1, 1, 1, 1),
            (0, 0, 1, 1, 0, 0, 1, 1),
            (1, 1, 0, 0, 0, 0, 1, 1),
            (0, 0, 1, 1, 1, 1, 0, 0),
            (1, 1, 0, 0, 1, 1, 0, 0),
            (1, 1, 1, 1, 0, 0, 0, 0),
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

    def test_HpathQ_empty(self):
        p = []
        result = HpathQ(p, tuple())
        assert result == False

    def test_HpathQ_0(self):
        p = [tuple()]
        result = HpathQ(p, (0,))
        assert result == False

    def test_HpathQ_1(self):
        p = [(0,)]
        assert HpathQ(p, (0,)) == False
        assert HpathQ(p, (1,)) == False

    def test_HpathQ_1_1(self):
        p = [(0, 1), (1, 0)]
        assert HpathQ(p, (0, 1)) == False
        assert HpathQ(p, (1, 0)) == False
        assert HpathQ(p, (1, 1)) == True

    def test_HpathQ_2_2(self):
        assert (
            HpathQ(
                [
                    (0, 0, 1, 1),
                    (0, 1, 0, 1),
                    (1, 0, 0, 1),
                    (0, 1, 1, 0),
                    (1, 0, 1, 0),
                    (1, 1, 0, 0),
                ],
                (2, 2),
            )
            == False
        )
        assert (
            HpathQ([(0, 1, 0, 1), (1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 1, 0)], (2, 2))
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
            HpathQ([(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 1, 0)], (2, 2))
            == False
        )
        # incorrect signature
        assert (
            HpathQ([(0, 1, 0, 1), (1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 1, 0)], (2, 0, 2))
            == False
        )

    def test_HcycleQ_empty(self):
        p = []
        result = HcycleQ(p, tuple())
        assert result == False

    def test_HcycleQ_0(self):
        p = [tuple()]
        result = HcycleQ(p, (0,))
        assert result == False

    def test_HcycleQ_1(self):
        p = [(0,)]
        assert HcycleQ(p, (0,)) == False
        assert HcycleQ(p, (1,)) == False

    def test_HcycleQ_1_1(self):
        # a cycle must be of length at least 3
        p = [(0, 1), (1, 0)]
        assert HcycleQ(p, (0, 1)) == False
        assert HcycleQ(p, (1, 0)) == False
        assert HcycleQ(p, (1, 1)) == False

    def test_HcycleQ_2_2(self):
        assert (
            HcycleQ(
                [
                    (0, 0, 1, 1),
                    (0, 1, 0, 1),
                    (1, 0, 0, 1),
                    (0, 1, 1, 0),
                    (1, 0, 1, 0),
                    (1, 1, 0, 0),
                ],
                (2, 2),
            )
            == False
        )
        assert (
            HcycleQ([(0, 1, 0, 1), (1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 1, 0)], (2, 2))
            == True
        )
        # contains a stutter
        assert (
            HcycleQ(
                [(0, 0, 1, 1), (0, 1, 0, 1), (1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 1, 0)],
                (2, 2),
            )
            == False
        )
        # not a cycle since index 1 and 2 are not a path
        assert (
            HcycleQ([(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 1, 0)], (2, 2))
            == False
        )
        # incorrect signature
        assert (
            HcycleQ([(0, 1, 0, 1), (1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 1, 0)], (2, 0, 2))
            == False
        )

    def test_Hpath_HpathQ_vs_HcycleQ(self):
        # 001 is a stutter permutation
        assert HpathQ([(0, 1, 0), (1, 0, 0)], (2, 1)) == True
        # too short for a cycle
        assert HcycleQ([(0, 1, 0), (0, 0, 1)], (2, 1)) == False

        # [2, 1, 1] signature
        assert (
            HpathQ(
                [
                    (0, 0, 1, 2),
                    (0, 0, 2, 1),
                    (0, 2, 0, 1),
                    (0, 2, 1, 0),
                    (0, 1, 2, 0),
                    (0, 1, 0, 2),
                    (1, 0, 0, 2),
                    (1, 0, 2, 0),
                    (1, 2, 0, 0),
                    (2, 1, 0, 0),
                    (2, 0, 1, 0),
                    (2, 0, 0, 1),
                ],
                (2, 1, 1),
            )
            == True
        )
        assert (
            HcycleQ(
                [
                    (0, 0, 1, 2),
                    (0, 0, 2, 1),
                    (0, 2, 0, 1),
                    (0, 2, 1, 0),
                    (0, 1, 2, 0),
                    (0, 1, 0, 2),
                    (1, 0, 0, 2),
                    (1, 0, 2, 0),
                    (1, 2, 0, 0),
                    (2, 1, 0, 0),
                    (2, 0, 1, 0),
                    (2, 0, 0, 1),
                ],
                (2, 1, 1),
            )
            == False
        )
