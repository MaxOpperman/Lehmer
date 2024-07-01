"""
Smoke test for permutation graphs

Copyright (c) 2018 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the (To Be Supplied) License.
"""

import pytest

from helper_operations.permutation_graphs import (
    binomial,
    count_inversions,
    defect,
    generate_adj,
    get_num_of_inversions,
    graph,
    multinomial,
    perm,
    signature,
)


class TestPermutationGraphs:
    # Class that tests the helper_operations.permutation_graphs module
    # In specific, the functions are used to manipulate permutations
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

    def test_generate_adj_multiple_0s1(self):
        p = (0, 0, 0, 0, 0, 0, 1)
        result = generate_adj(p)
        assert result == [(0, 0, 0, 0, 0, 1, 0)]

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
