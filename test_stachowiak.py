import collections
import math
import pytest
from path_operations import pathQ
from permutation_graphs import HpathQ
from stachowiak import HpathNS

class Test_HpathNS():
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
    
    def test_HpathNS_2_2(self):
        result = HpathNS(2, 2)
        expected_result = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 1, 0)]
        assert result == expected_result
    
    def test_HpathNS_2_3(self):
        result = HpathNS(2, 3)
        expected_result = [(1, 1, 1, 0, 0), (1, 1, 0, 1, 0), (1, 0, 1, 1, 0),
                           (1, 0, 1, 0, 1), (1, 0, 0, 1, 1), (0, 1, 0, 1, 1),
                           (0, 1, 1, 0, 1), (0, 1, 1, 1, 0)]
        assert result == expected_result
    
    def test_HpathNS_3_2(self):
        result = HpathNS(3, 2)
        expected_result = [(0, 0, 0, 1, 1), (0, 0, 1, 0, 1), (0, 1, 0, 0, 1),
                           (0, 1, 0, 1, 0), (0, 1, 1, 0, 0), (1, 0, 1, 0, 0),
                           (1, 0, 0, 1, 0), (1, 0, 0, 0, 1)]
        assert result == expected_result
    
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
    
    def test_HpathNS_2_4(self):
        result = HpathNS(2, 4)
        expected_result = [(0, 1, 1, 1, 1, 0), (1, 0, 1, 1, 1, 0), (1, 1, 0, 1, 1, 0),
                           (1, 1, 1, 0, 1, 0), (1, 1, 1, 0, 0, 1), (1, 1, 0, 1, 0, 1),
                           (1, 0, 1, 1, 0, 1), (1, 0, 1, 0, 1, 1), (1, 0, 0, 1, 1, 1),
                           (0, 1, 0, 1, 1, 1), (0, 1, 1, 0, 1, 1), (0, 1, 1, 1, 0, 1)]
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

    def test_HpathNS_5_5(self):
        result = HpathNS(5, 5)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == math.comb(5 + 5, 5)
        # check that there is a hamilton path
        assert HpathQ(result, [5, 5])

    def test_HpathNS_5_9(self):
        result = HpathNS(5, 9)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == math.comb(14, 9)
        # check that there is a hamilton path
        assert pathQ(result)

    def test_HpathNS_9_5(self):
        result = HpathNS(9, 5)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == math.comb(14, 5)
        # check that there is a hamilton path
        assert pathQ(result)

    def test_HpathNS_7_7(self):
        result = HpathNS(7, 7)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == math.comb(14, 7)
        # check that there is a hamilton path
        assert pathQ(result)

    def test_HpathNS_9_13(self):
        result = HpathNS(9, 13)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == math.comb(9 + 13, 13)
        # check that there is a hamilton path
        assert pathQ(result)


    def test_HpathNS_11_11(self):
        result = HpathNS(11, 11)
        # make sure there are no duplicates
        dups = [item for item, count in collections.Counter(result).items() if count > 1]
        assert len(dups) == 0
        # make sure that all combinations have been found
        assert len(result) == math.comb(22, 11)
        # check that there is a hamilton path
        assert pathQ(result)