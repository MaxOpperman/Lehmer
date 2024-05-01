import copy
import pytest
from path_operations import cycleQ
from permutation_graphs import HcycleQ, multinomial
from stachowiak import _lemma10_helper, lemma10, lemma11

class Test_Lemma11():
    """
     Test lemma 11 of Stachowiak (1992), again becomes very large so we don't check the actual paths, only the properties.
     Since HcycleQ is very slow, we use cycleQ instead.
     We check that the correct number of permutations are found and that there are no duplicates (using set).
     This way we can be sure that the permutations are all found and that they form a cycle.
    """
    l11sig_3_3_2 = lemma11([3, 3, 2])
    def test_lemma11_3_3_2(self):
        result = copy.deepcopy(self.l11sig_3_3_2)
        assert len(set(result)) == len(result)
        assert len(result) == multinomial([3, 3, 2])
        assert HcycleQ(result, [3, 3, 2])

    def test_lemma11_3_3_7(self):
        sig = [3, 3, 7]
        result = lemma11(sig)
        assert len(set(result)) == len(result)
        assert len(result) == multinomial(sig)
        assert cycleQ(result)

    def test_lemma11_3_3_10(self):
        sig = [3, 3, 10]
        result = lemma11(sig)
        assert len(set(result)) == len(result)
        assert len(result) == multinomial(sig)
        assert cycleQ(result)

    def test_lemma11_3_3_2_1(self):
        # we only have to add the last the last element (which occurs once) to the path
        result = _lemma10_helper(self.l11sig_3_3_2, 1, 3)
        assert len(set(result)) == len(result)
        assert len(result) == multinomial([3, 3, 2, 1])
        assert cycleQ(result)

    def test_lemma11_3_3_2_2(self):
        # we only have to add the last the last element (which occurs twice) to the path
        result = _lemma10_helper(self.l11sig_3_3_2, 2, 3)
        assert len(set(result)) == len(result)
        assert len(result) == multinomial([3, 3, 2, 2])
        assert cycleQ(result)

    def test_lemma11_5_3_2(self):
        sig = [5, 3, 2]
        result = lemma11(sig)
        assert len(set(result)) == len(result)
        assert len(result) == multinomial(sig)
        assert cycleQ(result)

    def test_lemma11_5_5_3(self):
        sig = [5, 5, 3]
        result = lemma11(sig)
        assert len(set(result)) == len(result)
        assert len(result) == multinomial(sig)
        assert cycleQ(result)
