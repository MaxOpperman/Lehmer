import pytest

from stachowiak import lemma11
from type_variations import stachowiak_list


class TestStachowiakList:
    def cast_list(self, x):
        # cast a list of tuples to a list of lists
        return [list(tup) for tup in x]

    def test_stachowiak_list_l11_empty(self):
        with pytest.raises(ValueError):
            stachowiak_list.lemma11([])

    def test_stachowiak_list_l11_1(self):
        assert stachowiak_list.lemma11([1]) == self.cast_list(lemma11([1]))

    def test_stachowiak_list_l11_2(self):
        assert stachowiak_list.lemma11([2]) == self.cast_list(lemma11([2]))

    def test_stachowiak_list_l11_1_1(self):
        assert stachowiak_list.lemma11([1, 1]) == self.cast_list(lemma11([1, 1]))

    def test_stachowiak_list_l11_not_enough_odd(self):
        with pytest.raises(ValueError):
            stachowiak_list.lemma11([2, 4, 14, 22, 1])
        with pytest.raises(ValueError):
            stachowiak_list.lemma11([2, 1])
        with pytest.raises(ValueError):
            stachowiak_list.lemma11([3, 2, 2])
        with pytest.raises(ValueError):
            stachowiak_list.lemma11([6, 5, 4, 20, 2])
        with pytest.raises(ValueError):
            stachowiak_list.lemma11([6, 8, 4, 18, 2])

    def test_stachowiak_list_l11_two_odd(self):
        assert stachowiak_list.lemma11([3, 3]) == self.cast_list(lemma11([3, 3]))
        assert stachowiak_list.lemma11([5, 3]) == self.cast_list(lemma11([5, 3]))
        assert stachowiak_list.lemma11([3, 5]) == self.cast_list(lemma11([3, 5]))
        assert stachowiak_list.lemma11([5, 5]) == self.cast_list(lemma11([5, 5]))
        assert stachowiak_list.lemma11([3, 7]) == self.cast_list(lemma11([3, 7]))
        assert stachowiak_list.lemma11([7, 3]) == self.cast_list(lemma11([7, 3]))

    def test_stachowiak_list_l11_two_or_more_odd(self):
        assert stachowiak_list.lemma11([3, 3, 3]) == self.cast_list(lemma11([3, 3, 3]))
        assert stachowiak_list.lemma11([3, 3, 2]) == self.cast_list(lemma11([3, 3, 2]))
        assert stachowiak_list.lemma11([3, 3, 2, 1]) == self.cast_list(
            lemma11([3, 3, 2, 1])
        )
        assert stachowiak_list.lemma11([3, 5, 2, 1]) == self.cast_list(
            lemma11([3, 5, 2, 1])
        )
        assert stachowiak_list.lemma11([5, 5, 2]) == self.cast_list(lemma11([5, 5, 2]))
