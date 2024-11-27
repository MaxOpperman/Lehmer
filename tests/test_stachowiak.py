"""
Tests for Stachowiak (1992)

Copyright (c) 2024 - Max Opperman - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the (To Be Supplied) License.
"""

import copy
import math

import numpy as np
import pytest

from helper_operations.path_operations import cycleQ, pathQ
from helper_operations.permutation_graphs import (
    HcycleQ,
    HpathQ,
    LargeHcycleQ,
    multinomial,
)
from stachowiak import (
    _lemma10_helper,
    lemma2_extended_path,
    lemma7,
    lemma8,
    lemma9,
    lemma11,
)


class Test_Lemma2:
    """
    Test lemma 2 of Stachowiak (1992), again becomes very large so we don't check the actual paths, only the properties.
    Since HcycleQ is very slow, we use cycleQ instead. Should output GE ((0 | 1) | l^p)
    We check that the correct number of permutations are found and that there are no duplicates (using set).
    This way we can be sure that the permutations are all found and that they form a cycle.
    """

    def test_lemma2_ext_path_2(self):
        chain_p = (2, 2)
        result = lemma2_extended_path(chain_p)
        assert result == [
            (0, 1, 2, 2),
            (1, 0, 2, 2),
            (1, 2, 0, 2),
            (1, 2, 2, 0),
            (2, 1, 2, 0),
            (2, 2, 1, 0),
            (2, 2, 0, 1),
            (2, 0, 2, 1),
            (0, 2, 2, 1),
            (0, 2, 1, 2),
            (2, 0, 1, 2),
            (2, 1, 0, 2),
        ]

    def test_lemma2_ext_path_3(self):
        chain_p = (2, 2, 2)
        result = lemma2_extended_path(chain_p, True)
        assert result == [
            (1, 0, 2, 2, 2),
            (1, 2, 0, 2, 2),
            (1, 2, 2, 0, 2),
            (1, 2, 2, 2, 0),
            (2, 1, 2, 2, 0),
            (2, 2, 1, 2, 0),
            (2, 2, 2, 1, 0),
            (2, 2, 2, 0, 1),
            (2, 2, 0, 2, 1),
            (2, 0, 2, 2, 1),
            (0, 2, 2, 2, 1),
            (0, 2, 2, 1, 2),
            (2, 0, 2, 1, 2),
            (2, 2, 0, 1, 2),
            (2, 2, 1, 0, 2),
            (2, 1, 2, 0, 2),
            (2, 1, 0, 2, 2),
            (2, 0, 1, 2, 2),
            (0, 2, 1, 2, 2),
            (0, 1, 2, 2, 2),
        ]

    def test_lemma2_ext_path_3_reverse(self):
        chain_p = (2, 2, 2)
        result = lemma2_extended_path(chain_p, False)
        assert result == [
            (0, 1, 2, 2, 2),
            (0, 2, 1, 2, 2),
            (0, 2, 2, 1, 2),
            (0, 2, 2, 2, 1),
            (2, 0, 2, 2, 1),
            (2, 2, 0, 2, 1),
            (2, 2, 2, 0, 1),
            (2, 2, 2, 1, 0),
            (2, 2, 1, 2, 0),
            (2, 1, 2, 2, 0),
            (1, 2, 2, 2, 0),
            (1, 2, 2, 0, 2),
            (2, 1, 2, 0, 2),
            (2, 2, 1, 0, 2),
            (2, 2, 0, 1, 2),
            (2, 0, 2, 1, 2),
            (2, 0, 1, 2, 2),
            (2, 1, 0, 2, 2),
            (1, 2, 0, 2, 2),
            (1, 0, 2, 2, 2),
        ]

    def test_lemma2_ext_path_4_different_int(self):
        chain_p = (9, 9, 9, 9)
        result = lemma2_extended_path(chain_p)
        assert result == [
            (0, 1, 9, 9, 9, 9),
            (1, 0, 9, 9, 9, 9),
            (1, 9, 0, 9, 9, 9),
            (1, 9, 9, 0, 9, 9),
            (1, 9, 9, 9, 0, 9),
            (1, 9, 9, 9, 9, 0),
            (9, 1, 9, 9, 9, 0),
            (9, 9, 1, 9, 9, 0),
            (9, 9, 9, 1, 9, 0),
            (9, 9, 9, 9, 1, 0),
            (9, 9, 9, 9, 0, 1),
            (9, 9, 9, 0, 9, 1),
            (9, 9, 0, 9, 9, 1),
            (9, 0, 9, 9, 9, 1),
            (0, 9, 9, 9, 9, 1),
            (0, 9, 9, 9, 1, 9),
            (9, 0, 9, 9, 1, 9),
            (9, 9, 0, 9, 1, 9),
            (9, 9, 9, 0, 1, 9),
            (9, 9, 9, 1, 0, 9),
            (9, 9, 1, 9, 0, 9),
            (9, 1, 9, 9, 0, 9),
            (9, 1, 9, 0, 9, 9),
            (9, 9, 1, 0, 9, 9),
            (9, 9, 0, 1, 9, 9),
            (9, 0, 9, 1, 9, 9),
            (0, 9, 9, 1, 9, 9),
            (0, 9, 1, 9, 9, 9),
            (9, 0, 1, 9, 9, 9),
            (9, 1, 0, 9, 9, 9),
        ]

    def test_lemma2_ext_path_4_different_int_reverse(self):
        chain_p = (9, 9, 9, 9)
        result = lemma2_extended_path(chain_p, False)
        assert result == [
            (1, 0, 9, 9, 9, 9),
            (0, 1, 9, 9, 9, 9),
            (0, 9, 1, 9, 9, 9),
            (0, 9, 9, 1, 9, 9),
            (0, 9, 9, 9, 1, 9),
            (0, 9, 9, 9, 9, 1),
            (9, 0, 9, 9, 9, 1),
            (9, 9, 0, 9, 9, 1),
            (9, 9, 9, 0, 9, 1),
            (9, 9, 9, 9, 0, 1),
            (9, 9, 9, 9, 1, 0),
            (9, 9, 9, 1, 9, 0),
            (9, 9, 1, 9, 9, 0),
            (9, 1, 9, 9, 9, 0),
            (1, 9, 9, 9, 9, 0),
            (1, 9, 9, 9, 0, 9),
            (9, 1, 9, 9, 0, 9),
            (9, 9, 1, 9, 0, 9),
            (9, 9, 9, 1, 0, 9),
            (9, 9, 9, 0, 1, 9),
            (9, 9, 0, 9, 1, 9),
            (9, 0, 9, 9, 1, 9),
            (9, 0, 9, 1, 9, 9),
            (9, 9, 0, 1, 9, 9),
            (9, 9, 1, 0, 9, 9),
            (9, 1, 9, 0, 9, 9),
            (1, 9, 9, 0, 9, 9),
            (1, 9, 0, 9, 9, 9),
            (9, 1, 0, 9, 9, 9),
            (9, 0, 1, 9, 9, 9),
        ]

    def test_lemma2_ext_path_5_different_int(self):
        chain_p = (8, 8, 8, 8, 8)
        result = lemma2_extended_path(chain_p)
        assert len(result) == multinomial((1, 1, len(chain_p)))
        assert cycleQ(result)
        assert result == [
            (1, 0, 8, 8, 8, 8, 8),
            (1, 8, 0, 8, 8, 8, 8),
            (1, 8, 8, 0, 8, 8, 8),
            (1, 8, 8, 8, 0, 8, 8),
            (1, 8, 8, 8, 8, 0, 8),
            (1, 8, 8, 8, 8, 8, 0),
            (8, 1, 8, 8, 8, 8, 0),
            (8, 8, 1, 8, 8, 8, 0),
            (8, 8, 8, 1, 8, 8, 0),
            (8, 8, 8, 8, 1, 8, 0),
            (8, 8, 8, 8, 8, 1, 0),
            (8, 8, 8, 8, 8, 0, 1),
            (8, 8, 8, 8, 0, 8, 1),
            (8, 8, 8, 0, 8, 8, 1),
            (8, 8, 0, 8, 8, 8, 1),
            (8, 0, 8, 8, 8, 8, 1),
            (0, 8, 8, 8, 8, 8, 1),
            (0, 8, 8, 8, 8, 1, 8),
            (8, 0, 8, 8, 8, 1, 8),
            (8, 8, 0, 8, 8, 1, 8),
            (8, 8, 8, 0, 8, 1, 8),
            (8, 8, 8, 8, 0, 1, 8),
            (8, 8, 8, 8, 1, 0, 8),
            (8, 8, 8, 1, 8, 0, 8),
            (8, 8, 1, 8, 8, 0, 8),
            (8, 1, 8, 8, 8, 0, 8),
            (8, 1, 8, 8, 0, 8, 8),
            (8, 8, 1, 8, 0, 8, 8),
            (8, 8, 8, 1, 0, 8, 8),
            (8, 8, 8, 0, 1, 8, 8),
            (8, 8, 0, 8, 1, 8, 8),
            (8, 0, 8, 8, 1, 8, 8),
            (0, 8, 8, 8, 1, 8, 8),
            (0, 8, 8, 1, 8, 8, 8),
            (8, 0, 8, 1, 8, 8, 8),
            (8, 8, 0, 1, 8, 8, 8),
            (8, 8, 1, 0, 8, 8, 8),
            (8, 1, 8, 0, 8, 8, 8),
            (8, 1, 0, 8, 8, 8, 8),
            (8, 0, 1, 8, 8, 8, 8),
            (0, 8, 1, 8, 8, 8, 8),
            (0, 1, 8, 8, 8, 8, 8),
        ]


class Test_Lemma7:
    """
    Test lemma 7 of Stachowiak (1992), again becomes very large so we don't check the actual paths, only the properties.
    Outputs G=((0 | 1)(k^q | l^p))
    """

    def test_lemma7_1_1_1_1(self):
        signature = (1, 1, 1, 1)
        result = lemma7(signature)
        assert len(result) == 2 * multinomial(signature[2:])
        assert result == [(0, 1, 2, 3), (0, 1, 3, 2), (1, 0, 3, 2), (1, 0, 2, 3)]

    def test_lemma7_1_1_1_2(self):
        signature = (1, 1, 1, 2)
        result = lemma7(signature)
        assert len(result) == 2 * multinomial(signature[2:])
        assert result == [
            (1, 0, 2, 3, 3),
            (1, 0, 3, 2, 3),
            (1, 0, 3, 3, 2),
            (0, 1, 3, 3, 2),
            (0, 1, 3, 2, 3),
            (0, 1, 2, 3, 3),
        ]

    def test_lemma7_1_1_2_1(self):
        signature = (1, 1, 2, 1)
        result = lemma7(signature)
        assert len(result) == 2 * multinomial(signature[2:])
        assert result == [
            (0, 1, 2, 2, 3),
            (0, 1, 2, 3, 2),
            (0, 1, 3, 2, 2),
            (1, 0, 3, 2, 2),
            (1, 0, 2, 3, 2),
            (1, 0, 2, 2, 3),
        ]

    def test_lemma7_1_1_2_2(self):
        signature = (1, 1, 2, 2)
        result = lemma7(signature)
        assert len(result) == 2 * multinomial(signature[2:])
        assert result == [
            (1, 0, 2, 2, 3, 3),
            (1, 0, 2, 3, 2, 3),
            (1, 0, 2, 3, 3, 2),
            (0, 1, 2, 3, 3, 2),
            (0, 1, 3, 2, 3, 2),
            (0, 1, 3, 3, 2, 2),
            (1, 0, 3, 3, 2, 2),
            (1, 0, 3, 2, 3, 2),
            (1, 0, 3, 2, 2, 3),
            (0, 1, 3, 2, 2, 3),
            (0, 1, 2, 3, 2, 3),
            (0, 1, 2, 2, 3, 3),
        ]

    def test_lemma7_1_1_3_2(self):
        signature = (1, 1, 3, 2)
        result = lemma7(signature)
        assert len(result) == 2 * multinomial(signature[2:])
        assert result == [
            (1, 0, 2, 2, 2, 3, 3),
            (1, 0, 2, 2, 3, 2, 3),
            (1, 0, 2, 2, 3, 3, 2),
            (0, 1, 2, 2, 3, 3, 2),
            (0, 1, 2, 3, 2, 3, 2),
            (0, 1, 2, 3, 3, 2, 2),
            (1, 0, 2, 3, 3, 2, 2),
            (1, 0, 2, 3, 2, 3, 2),
            (1, 0, 2, 3, 2, 2, 3),
            (1, 0, 3, 2, 2, 2, 3),
            (1, 0, 3, 2, 2, 3, 2),
            (1, 0, 3, 2, 3, 2, 2),
            (1, 0, 3, 3, 2, 2, 2),
            (0, 1, 3, 3, 2, 2, 2),
            (0, 1, 3, 2, 3, 2, 2),
            (0, 1, 3, 2, 2, 3, 2),
            (0, 1, 3, 2, 2, 2, 3),
            (0, 1, 2, 3, 2, 2, 3),
            (0, 1, 2, 2, 3, 2, 3),
            (0, 1, 2, 2, 2, 3, 3),
        ]

    def test_lemma7_1_1_3_4(self):
        signature = (1, 1, 3, 4)
        result = lemma7(signature)
        assert len(result) == 2 * multinomial(signature[2:])
        assert len(result) == len(set(result))
        assert cycleQ(result)
        for p in result:
            assert p[0] in [0, 1]
            assert p[1] in [0, 1]

    def test_lemma7_1_1_8_8(self):
        signature = (1, 1, 8, 8)
        result = lemma7(signature)
        assert len(result) == 2 * multinomial(signature[2:])
        assert len(result) == len(set(result))
        assert cycleQ(result)
        for p in result:
            assert p[0] in [0, 1]
            assert p[1] in [0, 1]

    def test_lemma7_1_1_7_10(self):
        signature = (1, 1, 7, 10)
        result = lemma7(signature)
        assert len(result) == 2 * multinomial(signature[2:])
        assert len(result) == len(set(result))
        assert cycleQ(result)
        for p in result:
            assert p[0] in [0, 1]
            assert p[1] in [0, 1]


class Test_Lemma8:
    """
    Test lemma 8 of Stachowiak (1992), again becomes very large so we don't check the actual paths, only the properties.
    Outputs G=(((0 | 1)k^q ) | l^p)
    """

    def test_lemma8_1_1_1_1(self):
        signature = (1, 1, 1, 1)
        result = lemma8(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[3])
        assert result == [
            (0, 1, 2, 3),
            (1, 0, 2, 3),
            (1, 0, 3, 2),
            (1, 3, 0, 2),
            (3, 1, 0, 2),
            (3, 0, 1, 2),
            (0, 3, 1, 2),
            (0, 1, 3, 2),
        ]

    def test_lemma8_1_1_2_1(self):
        signature = (1, 1, 2, 1)
        result = lemma8(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[3])
        assert result == [
            (0, 1, 2, 3, 2),
            (0, 1, 2, 2, 3),
            (1, 0, 2, 2, 3),
            (1, 0, 2, 3, 2),
            (1, 0, 3, 2, 2),
            (1, 3, 0, 2, 2),
            (3, 1, 0, 2, 2),
            (3, 0, 1, 2, 2),
            (0, 3, 1, 2, 2),
            (0, 1, 3, 2, 2),
        ]

    def test_lemma8_1_1_1_2(self):
        signature = (1, 1, 1, 2)
        result = lemma8(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[3])
        assert result == [
            (0, 3, 1, 2, 3),
            (3, 0, 1, 2, 3),
            (3, 0, 1, 3, 2),
            (3, 1, 0, 3, 2),
            (3, 1, 0, 2, 3),
            (1, 3, 0, 2, 3),
            (1, 3, 0, 3, 2),
            (1, 3, 3, 0, 2),
            (3, 1, 3, 0, 2),
            (3, 3, 1, 0, 2),
            (3, 3, 0, 1, 2),
            (3, 0, 3, 1, 2),
            (0, 3, 3, 1, 2),
            (0, 3, 1, 3, 2),
            (0, 1, 3, 3, 2),
            (1, 0, 3, 3, 2),
            (1, 0, 3, 2, 3),
            (1, 0, 2, 3, 3),
            (0, 1, 2, 3, 3),
            (0, 1, 3, 2, 3),
        ]

    def test_lemma8_1_1_2_2(self):
        signature = (1, 1, 2, 2)
        result = lemma8(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[3])
        assert result == [
            (0, 3, 1, 2, 3, 2),
            (0, 3, 1, 2, 2, 3),
            (3, 0, 1, 2, 2, 3),
            (3, 0, 1, 2, 3, 2),
            (3, 0, 1, 3, 2, 2),
            (3, 1, 0, 3, 2, 2),
            (3, 1, 0, 2, 3, 2),
            (3, 1, 0, 2, 2, 3),
            (1, 3, 0, 2, 2, 3),
            (1, 3, 0, 2, 3, 2),
            (1, 3, 0, 3, 2, 2),
            (1, 3, 3, 0, 2, 2),
            (3, 1, 3, 0, 2, 2),
            (3, 3, 1, 0, 2, 2),
            (3, 3, 0, 1, 2, 2),
            (3, 0, 3, 1, 2, 2),
            (0, 3, 3, 1, 2, 2),
            (0, 3, 1, 3, 2, 2),
            (0, 1, 3, 3, 2, 2),
            (1, 0, 3, 3, 2, 2),
            (1, 0, 3, 2, 3, 2),
            (1, 0, 3, 2, 2, 3),
            (0, 1, 3, 2, 2, 3),
            (0, 1, 2, 3, 2, 3),
            (0, 1, 2, 2, 3, 3),
            (1, 0, 2, 2, 3, 3),
            (1, 0, 2, 3, 2, 3),
            (1, 0, 2, 3, 3, 2),
            (0, 1, 2, 3, 3, 2),
            (0, 1, 3, 2, 3, 2),
        ]

    def test_lemma8_1_1_3_4(self):
        signature = (1, 1, 3, 4)
        result = lemma8(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[3])
        assert len(result) == len(set(result))
        assert cycleQ(result)
        for p in result:
            assert p[0] in [0, 1, 3]
            assert p[1] in [0, 1, 3]

    def test_lemma8_1_1_4_5(self):
        signature = (1, 1, 4, 5)
        result = lemma8(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[3])
        assert len(result) == len(set(result))
        assert cycleQ(result)
        for p in result:
            assert p[0] in [0, 1, 3]
            assert p[1] in [0, 1, 3]

    def test_lemma8_1_1_7_7(self):
        signature = (1, 1, 7, 7)
        result = lemma8(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[3])
        assert len(result) == len(set(result))
        assert cycleQ(result)
        for p in result:
            assert p[0] in [0, 1, 3]
            assert p[1] in [0, 1, 3]

    def test_lemma8_1_1_6_9(self):
        signature = (1, 1, 6, 9)
        result = lemma8(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[3])
        assert len(result) == len(set(result))
        assert cycleQ(result)
        for p in result:
            assert p[0] in [0, 1, 3]
            assert p[1] in [0, 1, 3]


class Test_Lemma9:
    """
    Test lemma 8 of Stachowiak (1992), again becomes very large so we don't check the actual paths, only the properties.
    Outputs G=( (k^r (0|1) k^s) | l^p) )
    """

    def test_lemma9_1_1_1_0_1(self):
        signature = (1, 1, 1, 0, 1)
        result = lemma9(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[4])
        assert result == [
            (3, 2, 1, 0),
            (3, 2, 0, 1),
            (2, 3, 0, 1),
            (2, 0, 3, 1),
            (2, 0, 1, 3),
            (2, 1, 0, 3),
            (2, 1, 3, 0),
            (2, 3, 1, 0),
        ]

    def test_lemma9_1_1_0_1_1(self):
        signature = (1, 1, 0, 1, 1)
        result = lemma9(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[4])
        assert result == [
            (0, 1, 2, 3),
            (1, 0, 2, 3),
            (1, 0, 3, 2),
            (1, 3, 0, 2),
            (3, 1, 0, 2),
            (3, 0, 1, 2),
            (0, 3, 1, 2),
            (0, 1, 3, 2),
        ]

    def test_lemma9_1_1_1_1_1(self):
        signature = (1, 1, 1, 1, 1)
        result = lemma9(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[4])
        assert result == [
            (2, 3, 0, 1, 2),
            (3, 2, 0, 1, 2),
            (3, 2, 1, 0, 2),
            (2, 3, 1, 0, 2),
            (2, 1, 3, 0, 2),
            (2, 1, 0, 3, 2),
            (2, 1, 0, 2, 3),
            (2, 0, 1, 2, 3),
            (2, 0, 1, 3, 2),
            (2, 0, 3, 1, 2),
        ]

    def test_lemma9_1_1_1_1_4(self):
        signature = (1, 1, 1, 1, 4)
        result = lemma9(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[4])
        assert cycleQ(result)
        assert len(result) == len(set(result))

    def test_lemma9_1_1_3_1_3(self):
        signature = (1, 1, 3, 1, 3)
        result = lemma9(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[4])
        assert cycleQ(result)
        assert len(result) == len(set(result))

    def test_lemma9_1_1_2_4_5(self):
        signature = (1, 1, 2, 4, 5)
        result = lemma9(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[4])
        assert cycleQ(result)
        assert len(result) == len(set(result))

    def test_lemma9_1_1_4_7_4(self):
        signature = (1, 1, 4, 7, 4)
        result = lemma9(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[4])
        assert cycleQ(result)
        assert len(result) == len(set(result))

    def test_lemma9_1_1_8_7_5(self):
        signature = (1, 1, 8, 7, 5)
        result = lemma9(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[4])
        assert cycleQ(result)
        assert len(result) == len(set(result))

    def test_lemma9_1_1_6_6_6(self):
        signature = (1, 1, 6, 6, 6)
        result = lemma9(signature)
        assert len(result) == 2 * math.comb(sum(signature), signature[4])
        assert cycleQ(result)
        assert len(result) == len(set(result))


class Test_Lemma10_and_11:
    """
    Test lemma 10 and 11 of Stachowiak (1992), again becomes very large so we don't check the actual paths, only the properties.
    Since HcycleQ is very slow, we use cycleQ instead. Outputs all permutations of the given signature.
    We check that the correct number of permutations are found and that there are no duplicates (using set).
    This way we can be sure that the permutations are all found and that they form a cycle.
    """

    l11sig_3_3_2 = lemma11((3, 3, 2))

    def test_lemma11_empty(self):
        with pytest.raises(ValueError):
            lemma11(tuple())

    def test_lemma11_2(self):
        # only one element -> stutter permutation
        result = lemma11((2,))
        assert result == []

    def test_lemma11_5(self):
        result = lemma11((5,))
        assert result == []

    def test_lemma11_1_1(self):
        result = lemma11((1, 1))
        assert HpathQ(result, (1, 1))

    # at least two odd numbers
    def test_lemma11_not_enough_odd_numbers(self):
        with pytest.raises(ValueError):
            lemma11((1, 2))
        with pytest.raises(ValueError):
            lemma11((5, 4))
        with pytest.raises(ValueError):
            lemma11((6, 7))
        with pytest.raises(ValueError):
            lemma11((2, 2))

    def test_lemma11_different_order_1_1_4(self):
        assert HpathQ(lemma11((4, 1, 1)), (4, 1, 1))
        assert HpathQ(lemma11((1, 4, 1)), (1, 4, 1))
        assert HpathQ(lemma11((5, 1, 1)), (5, 1, 1))
        assert HpathQ(lemma11((1, 5, 1)), (1, 5, 1))

    def test_lemma11_4_2_3_1(self):
        assert HpathQ(lemma11((4, 2, 3, 1)), (4, 2, 3, 1))

    def test_lemma11_3_2_3_1(self):
        assert HpathQ(lemma11((3, 2, 3, 1)), (3, 2, 3, 1))

    def test_lemma11_1_2_3_5(self):
        assert HpathQ(lemma11((1, 2, 3, 5)), (1, 2, 3, 5))

    def test_lemma11_3_3_2(self):
        result = copy.deepcopy(self.l11sig_3_3_2)
        assert HcycleQ(result, (3, 3, 2))

    def test_lemma11_3_3_1_2(self):
        sig = (3, 3, 1, 2)
        result = lemma11(sig)
        assert LargeHcycleQ(result, sig)

    def test_lemma11_3_3_7(self):
        sig = (3, 3, 7)
        result = lemma11(sig)
        assert LargeHcycleQ(result, sig)

    def test_lemma11_3_3_10(self):
        sig = (3, 3, 10)
        result = lemma11(sig)
        assert LargeHcycleQ(result, sig)

    def test_lemma11_3_3_2_1(self):
        # we only have to add the last element (which occurs once) to the path
        result = _lemma10_helper(self.l11sig_3_3_2, 1, 3)
        assert LargeHcycleQ(result, (3, 3, 2, 1))

    def test_lemma11_3_3_2_2(self):
        # we only have to add the last the last element (whihc occurs twice) to the path
        result = _lemma10_helper(self.l11sig_3_3_2, 2, 3)
        assert LargeHcycleQ(result, (3, 3, 2, 2))

    def test_lemma11_5_3_2(self):
        sig = (5, 3, 2)
        result = lemma11(sig)
        assert LargeHcycleQ(result, sig)

    def test_lemma11_5_5_3(self):
        sig = (5, 5, 3)
        result = lemma11(sig)
        assert LargeHcycleQ(result, sig)

    def test_lemma11_5_5_4(self):
        sig = (5, 5, 4)
        result = lemma11(sig)
        assert LargeHcycleQ(result, sig)

    def test_lemma11_3_5_6(self):
        sig = (3, 5, 6)
        result = lemma11(sig)
        assert LargeHcycleQ(result, sig)


@pytest.mark.slow
class Test_Lemma11_Large:
    def test_lemma11_7_7_2(self):
        sig = (7, 7, 2)
        result = lemma11(sig)
        assert LargeHcycleQ(result, sig)

    def test_lemma11_5_5_1_3(self):
        sig = (5, 5, 1, 3)
        result = lemma11(sig)
        assert LargeHcycleQ(result, sig)
