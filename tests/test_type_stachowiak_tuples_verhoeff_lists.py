import pytest

from stachowiak import lemma11
from type_variations import stachowiak_tuple_verhoeff_list


class TestStachowiakListVerhoeffTuple:
    def test_stachowiak_list_l11_empty(self):
        with pytest.raises(ValueError):
            stachowiak_tuple_verhoeff_list.lemma11([])

    def test_stachowiak_list_l11_1(self):
        assert stachowiak_tuple_verhoeff_list.lemma11([1]) == lemma11((1,))

    def test_stachowiak_list_l11_2(self):
        assert stachowiak_tuple_verhoeff_list.lemma11([2]) == lemma11((2,))

    def test_stachowiak_list_l11_1_1(self):
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1]) == lemma11((1, 1))

    def test_stachowiak_list_l11_not_enough_odd(self):
        with pytest.raises(ValueError):
            stachowiak_tuple_verhoeff_list.lemma11([2, 4, 14, 22, 1])
        with pytest.raises(ValueError):
            stachowiak_tuple_verhoeff_list.lemma11([2, 1])
        with pytest.raises(ValueError):
            stachowiak_tuple_verhoeff_list.lemma11([3, 2, 2])
        with pytest.raises(ValueError):
            stachowiak_tuple_verhoeff_list.lemma11([6, 5, 4, 20, 2])
        with pytest.raises(ValueError):
            stachowiak_tuple_verhoeff_list.lemma11([6, 8, 4, 18, 2])

    def test_stachowiak_list_l11_two_odd(self):
        assert stachowiak_tuple_verhoeff_list.lemma11([3, 3]) == lemma11((3, 3))
        assert stachowiak_tuple_verhoeff_list.lemma11([5, 3]) == lemma11((5, 3))
        assert stachowiak_tuple_verhoeff_list.lemma11([3, 5]) == lemma11((3, 5))
        assert stachowiak_tuple_verhoeff_list.lemma11([5, 5]) == lemma11((5, 5))
        assert stachowiak_tuple_verhoeff_list.lemma11([3, 7]) == lemma11((3, 7))
        assert stachowiak_tuple_verhoeff_list.lemma11([7, 3]) == lemma11((7, 3))

    def test_stachowiak_list_l11_two_or_more_odd(self):
        assert stachowiak_tuple_verhoeff_list.lemma11([3, 3, 3]) == lemma11((3, 3, 3))
        assert stachowiak_tuple_verhoeff_list.lemma11([3, 3, 2]) == lemma11((3, 3, 2))
        assert stachowiak_tuple_verhoeff_list.lemma11([3, 3, 2, 1]) == lemma11(
            (3, 3, 2, 1)
        )
        assert stachowiak_tuple_verhoeff_list.lemma11([3, 5, 2, 1]) == lemma11(
            (3, 5, 2, 1)
        )
        assert stachowiak_tuple_verhoeff_list.lemma11([5, 5, 2]) == lemma11((5, 5, 2))


class TestStachowiakListSJT:
    def test_stachowiak_list_l11_only_1s(self):
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1, 1]) == lemma11((1, 1, 1))
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1, 1, 1]) == lemma11(
            (1, 1, 1, 1)
        )
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1, 1, 1, 1]) == lemma11(
            (1, 1, 1, 1, 1)
        )

    def test_stachowiak_list_l11_1_1_1_even(self):
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1, 1, 2]) == lemma11(
            (1, 1, 1, 2)
        )
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1, 1, 4, 2]) == lemma11(
            (1, 1, 1, 4, 2)
        )
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1, 1, 6]) == lemma11(
            (1, 1, 1, 6)
        )
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1, 1, 1, 2]) == lemma11(
            (1, 1, 1, 1, 2)
        )


class TestStachowiakListVerhoeffTupleLemma2:
    def test_stachowiak_list_l11_lemma2(self):
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1, 2]) == lemma11((1, 1, 2))
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1, 4]) == lemma11((1, 1, 4))
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1, 8]) == lemma11((1, 1, 8))
        assert stachowiak_tuple_verhoeff_list.lemma11([1, 1, 14]) == lemma11((1, 1, 14))
