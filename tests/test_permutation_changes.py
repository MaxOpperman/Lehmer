import pytest

from helper_operations.permutation_graphs import extend, rotate, selectByTail, shorten, swapPair


class TestPermutationChanges:
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
