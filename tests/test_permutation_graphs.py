"""
Smoke test for permutation graphs

Copyright (c) 2018 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the (To Be Supplied) License.
"""

import pytest

from helper_operations.permutation_graphs import binomial, multinomial, perm, signature


class TestMain:
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

    def test_signature_empty(self):
        p = []
        result = signature(p)
        assert not result

    def test_signature_0(self):
        p = [0]
        result = signature(p)
        assert result == [1]

    def test_signature_2(self):
        p = [2]
        result = signature(p)
        assert result == [0, 0, 1]

    def test_signature_3_2_1(self):
        p = [2, 0, 1, 0, 1, 0]
        result = signature(p)
        assert result == [3, 2, 1]

    def check_permutations(self, s: list[int], ps: list[list[int]]):
        """Check that all permutations in ps differ,  none are missing, and all have signature s"""
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
        """Four objects of tree colors"""
        s = [2, 1, 1]
        result = perm(s)
        self.check_permutations(s, result)
