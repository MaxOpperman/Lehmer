"""
Tests for Verhoef (2017)

Copyright (c) 2024 - Max Opperman - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the (To Be Supplied) License.
"""

import collections
import math
import pytest
from path_operations import pathQ
from permutation_graphs import HpathQ, binomial, stutterPermutations
from verhoeff import HpathNS

class Test_HpathNS_BaseCases():
    def test_HpathNS_0_0(self):
        result = HpathNS(0, 0)
        expected_result = []
        assert result == expected_result

    def test_HpathNS_0_1(self):
        result = HpathNS(0, 1)
        expected_result = [(1,)]
        assert result == expected_result

    def test_HpathNS_1_0(self):
        result = HpathNS(1, 0)
        expected_result = [(0,)]
        assert result == expected_result

    def test_HpathNS_1_1(self):
        result = HpathNS(1, 1)
        expected_result = [(0, 1), (1, 0)]
        assert result == expected_result

    def test_HpathNS_1_2(self):
        result = HpathNS(1, 2)
        expected_result = [(1, 0, 1), (0, 1, 1)]
        assert result == expected_result

    def test_HpathNS_2_1(self):
        result = HpathNS(2, 1)
        expected_result = [(0, 1, 0), (1, 0, 0)]
        assert result == expected_result
    
    def test_HpathNS_3_1(self):
        result = HpathNS(3, 1)
        expected_result = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]
        assert result == expected_result

    def test_HpathNS_1_3(self):
        result = HpathNS(1, 3)
        expected_result = [(1, 1, 1, 0), (1, 1, 0, 1), (1, 0, 1, 1), (0, 1, 1, 1)]
        assert result == expected_result
    
    def test_HpathNS_4_1(self):
        result = HpathNS(4, 1)
        expected_result = [(0, 0, 0, 1, 0), (0, 0, 1, 0, 0), (0, 1, 0, 0, 0), (1, 0, 0, 0, 0)]
        assert result == expected_result
    

class Test_HpathNS_Even_Even():
    def test_HpathNS_2_2(self):
        result = HpathNS(2, 2)
        expected_result = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 1, 0)]
        assert result == expected_result
    
    def test_HpathNS_2_4(self):
        result = HpathNS(2, 4)
        expected_result = [(0, 1, 1, 1, 1, 0), (1, 0, 1, 1, 1, 0), (1, 1, 0, 1, 1, 0),
                           (1, 1, 1, 0, 1, 0), (1, 1, 1, 0, 0, 1), (1, 1, 0, 1, 0, 1),
                           (1, 0, 1, 1, 0, 1), (1, 0, 1, 0, 1, 1), (1, 0, 0, 1, 1, 1),
                           (0, 1, 0, 1, 1, 1), (0, 1, 1, 0, 1, 1), (0, 1, 1, 1, 0, 1)]
        assert result == expected_result
    
    def test_HpathNS_4_4(self):
        result = HpathNS(4, 4)
        expected_result = [(1, 1, 1, 0, 0, 0, 0, 1), (1, 1, 0, 1, 0, 0, 0, 1), (1, 0, 1, 1, 0, 0, 0, 1), (0, 1, 1, 1, 0, 0, 0, 1), (0, 1, 1, 0, 1, 0, 0, 1), (0, 1, 0, 1, 1, 0, 0, 1), (0, 0, 1, 1, 1, 0, 0, 1), (0, 0, 1, 1, 0, 1, 0, 1), (0, 1, 0, 1, 0, 1, 0, 1), (0, 1, 1, 0, 0, 1, 0, 1), (1, 0, 1, 0, 0, 1, 0, 1), (1, 1, 0, 0, 0, 1, 0, 1), (1, 1, 0, 0, 1, 0, 0, 1), (1, 0, 1, 0, 1, 0, 0, 1), (1, 0, 0, 1, 1, 0, 0, 1), (1, 0, 0, 1, 0, 1, 0, 1), (1, 0, 0, 0, 1, 1, 0, 1), (0, 1, 0, 0, 1, 1, 0, 1), (0, 0, 1, 0, 1, 1, 0, 1), (0, 0, 1, 0, 1, 0, 1, 1), (0, 1, 0, 0, 1, 0, 1, 1), (0, 1, 0, 1, 0, 0, 1, 1), (0, 1, 1, 0, 0, 0, 1, 1), (1, 0, 1, 0, 0, 0, 1, 1), (1, 0, 0, 1, 0, 0, 1, 1), (1, 0, 0, 0, 1, 0, 1, 1), (1, 0, 0, 0, 0, 1, 1, 1), (0, 1, 0, 0, 0, 1, 1, 1), (0, 0, 1, 0, 0, 1, 1, 1), (0, 0, 0, 1, 0, 1, 1, 1), (0, 0, 0, 1, 1, 0, 1, 1), (0, 0, 0, 1, 1, 1, 0, 1), (0, 0, 0, 1, 1, 1, 1, 0), (0, 0, 1, 0, 1, 1, 1, 0), (0, 1, 0, 0, 1, 1, 1, 0), (1, 0, 0, 0, 1, 1, 1, 0), (1, 0, 0, 1, 0, 1, 1, 0), (1, 0, 1, 0, 0, 1, 1, 0), (1, 1, 0, 0, 0, 1, 1, 0), (1, 1, 0, 0, 1, 0, 1, 0), (1, 0, 1, 0, 1, 0, 1, 0), (1, 0, 0, 1, 1, 0, 1, 0), (0, 1, 0, 1, 1, 0, 1, 0), (0, 0, 1, 1, 1, 0, 1, 0), (0, 0, 1, 1, 0, 1, 1, 0), (0, 1, 0, 1, 0, 1, 1, 0), (0, 1, 1, 0, 0, 1, 1, 0), (0, 1, 1, 0, 1, 0, 1, 0), (0, 1, 1, 1, 0, 0, 1, 0), (1, 0, 1, 1, 0, 0, 1, 0), (1, 1, 0, 1, 0, 0, 1, 0), (1, 1, 0, 1, 0, 1, 0, 0), (1, 0, 1, 1, 0, 1, 0, 0), (1, 0, 1, 0, 1, 1, 0, 0), (1, 0, 0, 1, 1, 1, 0, 0), (0, 1, 0, 1, 1, 1, 0, 0), (0, 1, 1, 0, 1, 1, 0, 0), (0, 1, 1, 1, 0, 1, 0, 0), (0, 1, 1, 1, 1, 0, 0, 0), (1, 0, 1, 1, 1, 0, 0, 0), (1, 1, 0, 1, 1, 0, 0, 0), (1, 1, 1, 0, 1, 0, 0, 0), (1, 1, 1, 0, 0, 1, 0, 0), (1, 1, 1, 0, 0, 0, 1, 0)]
        assert result == expected_result
    
    def test_HpathNS_6_4(self):
        result = HpathNS(6, 4)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # check that there is a hamilton path on the non-stutter permutations
        assert HpathQ(result, [6, 4])
    
    def test_HpathNS_2_8(self):
        result = HpathNS(2, 8)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # check that there is a hamilton path on the non-stutter permutations
        assert HpathQ(result, [2, 8])


class Test_HpathNS_Even_Odd():    
    def test_HpathNS_2_3(self):
        result = HpathNS(2, 3)
        expected_result = [(1, 1, 1, 0, 0), (1, 1, 0, 1, 0), (1, 0, 1, 1, 0),
                           (1, 0, 1, 0, 1), (1, 0, 0, 1, 1), (0, 1, 0, 1, 1),
                           (0, 1, 1, 0, 1), (0, 1, 1, 1, 0)]
        assert result == expected_result


class Test_HpathNS_Odd_Even():   
    def test_HpathNS_3_2(self):
        result = HpathNS(3, 2)
        expected_result = [(0, 0, 0, 1, 1), (0, 0, 1, 0, 1), (0, 1, 0, 0, 1),
                           (0, 1, 0, 1, 0), (0, 1, 1, 0, 0), (1, 0, 1, 0, 0),
                           (1, 0, 0, 1, 0), (1, 0, 0, 0, 1)]
        assert result == expected_result

    def test_HpathNS_3_4(self):
        result = HpathNS(3, 4)
        expected_result = [(1, 1, 1, 0, 0, 0, 1), (1, 1, 1, 0, 0, 1, 0),
                           (1, 1, 1, 0, 1, 0, 0), (1, 1, 0, 1, 1, 0, 0),
                           (1, 0, 1, 1, 1, 0, 0), (0, 1, 1, 1, 1, 0, 0),
                           (0, 1, 1, 1, 0, 1, 0), (0, 1, 1, 0, 1, 1, 0),
                           (0, 1, 0, 1, 1, 1, 0), (1, 0, 0, 1, 1, 1, 0),
                           (1, 0, 1, 0, 1, 1, 0), (1, 0, 1, 1, 0, 1, 0),
                           (1, 1, 0, 1, 0, 1, 0), (1, 1, 0, 1, 0, 0, 1),
                           (1, 0, 1, 1, 0, 0, 1), (0, 1, 1, 1, 0, 0, 1),
                           (0, 1, 1, 0, 1, 0, 1), (0, 1, 1, 0, 0, 1, 1),
                           (0, 1, 0, 1, 0, 1, 1), (0, 0, 1, 1, 0, 1, 1),
                           (0, 0, 1, 1, 1, 0, 1), (0, 1, 0, 1, 1, 0, 1),
                           (1, 0, 0, 1, 1, 0, 1), (1, 0, 1, 0, 1, 0, 1),
                           (1, 1, 0, 0, 1, 0, 1), (1, 1, 0, 0, 0, 1, 1),
                           (1, 0, 1, 0, 0, 1, 1), (1, 0, 0, 1, 0, 1, 1),
                           (1, 0, 0, 0, 1, 1, 1), (0, 1, 0, 0, 1, 1, 1),
                           (0, 0, 1, 0, 1, 1, 1), (0, 0, 0, 1, 1, 1, 1)]
        assert result == expected_result


class Test_HpathNS_Odd_Odd():   
    def test_HpathNS_3_3(self):
        result = HpathNS(3, 3)
        expected_result = [(0, 0, 0, 1, 1, 1), (0, 0, 1, 0, 1, 1), (0, 1, 0, 0, 1, 1),
                           (1, 0, 0, 0, 1, 1), (1, 0, 0, 1, 0, 1), (1, 0, 0, 1, 1, 0),
                           (1, 0, 1, 0, 1, 0), (1, 1, 0, 0, 1, 0), (1, 1, 0, 0, 0, 1),
                           (1, 0, 1, 0, 0, 1), (0, 1, 1, 0, 0, 1), (0, 1, 0, 1, 0, 1),
                           (0, 0, 1, 1, 0, 1), (0, 0, 1, 1, 1, 0), (0, 1, 0, 1, 1, 0),
                           (0, 1, 1, 0, 1, 0), (0, 1, 1, 1, 0, 0), (1, 0, 1, 1, 0, 0),
                           (1, 1, 0, 1, 0, 0), (1, 1, 1, 0, 0, 0)]
        assert result == expected_result

    def test_HpathNS_5_5(self):
        result = HpathNS(5, 5)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == binomial(5, 5)
        # check that there is a hamilton path
        assert HpathQ(result, [5, 5])

    def test_HpathNS_5_9(self):
        result = HpathNS(5, 9)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == binomial(5, 9)
        # check that there is a hamilton path
        assert pathQ(result)

    def test_HpathNS_9_5(self):
        result = HpathNS(9, 5)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == binomial(9, 5)
        # check that there is a hamilton path
        assert pathQ(result)

    def test_HpathNS_7_7(self):
        result = HpathNS(7, 7)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == binomial(7, 7)
        # check that there is a hamilton path
        assert pathQ(result)


@pytest.mark.slow
class Test_HpathNS_Large():
    """
     Test for large values of k0 and k1.
     Since HpathQ is very slow, we use pathQ instead.
     We check that the correct number of permutations are found and that there are no duplicates.
     This way we can be sure that the permutations are all found and that they form a path.
    """
    def test_HpathNS_9_13(self):
        result = HpathNS(9, 13)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == binomial(9, 13)
        # check that there is a hamilton path
        assert pathQ(result)


    def test_HpathNS_11_11(self):
        result = HpathNS(11, 11)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == binomial(11, 11)
        # check that there is a hamilton path
        assert pathQ(result)
    
    def test_HpathNS_10_5(self):
        result = HpathNS(10, 5)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == binomial(10, 5)-len(stutterPermutations([10, 5]))
        # check that there is a hamilton path
        assert pathQ(result)
    
    def test_HpathNS_9_6(self):
        result = HpathNS(9, 6)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == binomial(9, 6)-len(stutterPermutations([9, 6]))
        # check that there is a hamilton path
        assert pathQ(result)
    
    def test_HpathNS_10_6(self):
        result = HpathNS(10, 6)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == binomial(10, 6)-len(stutterPermutations([10, 6]))
        # check that there is a hamilton path
        assert pathQ(result)
    
    def test_HpathNS_4_12(self):
        result = HpathNS(4, 12)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == binomial(4, 12)-len(stutterPermutations([4, 12]))
        # check that there is a hamilton path
        assert pathQ(result)
