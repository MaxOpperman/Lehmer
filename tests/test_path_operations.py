import pytest

from helper_operations.path_operations import (
    adjacent,
    createSquareTube,
    createZigZagPath,
    cutCycle,
    cycleQ,
    get_transformer,
    incorporateSpurInZigZag,
    incorporateSpursInZigZag,
    mul,
    neighbor,
    pathEdges,
    pathQ,
    recursive_cycle_check,
    splitPathIn2,
    spurBaseIndex,
    transform,
    transform_cycle_cover,
)


class TestPathOperations:
    def test_adjacent_true(self):
        s = (1, 2)
        t = (2, 1)
        assert adjacent(s, t)

    def test_adjacent_same(self):
        s = (1, 2)
        assert adjacent(s, s) == False

    def test_adjacent_different_length(self):
        s = (1, 2)
        t = (2, 3, 4)
        assert adjacent(s, t) == False

    def test_adjacent_empty(self):
        s = tuple()
        t = tuple()
        assert adjacent(s, t) == False

    def test_pathQ_path(self):
        path = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]
        assert pathQ(path)

    def test_pathQ_empty(self):
        assert pathQ([]) == False

    def test_pathQ_one_permutation(self):
        assert pathQ([(0,)]) == True

    def test_pathQ_no_path(self):
        path = [(0, 0, 0, 1), (0, 0, 1, 0), (1, 0, 0, 0), (0, 1, 0, 0)]
        assert pathQ(path) == False

    def test_cycleQ_path(self):
        path = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]
        assert cycleQ(path) == False

    def test_cycleQ_cycle(self):
        cycle = [(0, 1, 2), (0, 2, 1), (2, 0, 1), (2, 1, 0), (1, 2, 0), (1, 0, 2)]
        assert cycleQ(cycle)

    def test_cycleQ_empty(self):
        assert cycleQ([]) == False

    def test_cycleQ_no_cycle(self):
        cycle = [(0, 1, 2), (0, 2, 1), (2, 0, 1), (2, 1, 0), (1, 0, 2), (1, 2, 0)]
        assert cycleQ(cycle) == False

    def test_pathEdges_path(self):
        path = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]
        result = pathEdges(path)
        expected_result = [
            [(0, 0, 0, 1), (0, 0, 1, 0)],
            [(0, 0, 1, 0), (0, 1, 0, 0)],
            [(0, 1, 0, 0), (1, 0, 0, 0)],
        ]
        assert result == expected_result

    def test_pathEdges_empty(self):
        assert pathEdges([]) == []

    def test_pathEdges_no_path(self):
        path = [(0, 0, 0, 1), (0, 0, 1, 0), (1, 0, 0, 0), (0, 1, 0, 0)]
        assert pathEdges(path) == []

    def test_splitPathIn2_path(self):
        path = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]
        result = splitPathIn2(path, (0, 0, 1, 0))
        expected_result = ([(0, 0, 0, 1), (0, 0, 1, 0)], [(0, 1, 0, 0), (1, 0, 0, 0)])

        assert result == expected_result

    def test_splitPathIn2_empty(self):
        with pytest.raises(AssertionError):
            splitPathIn2([], (0, 0, 1, 0))

    def test_splitPathIn2_empty(self):
        with pytest.raises(AssertionError):
            splitPathIn2(
                [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)], (0, 0, 0, 0)
            )

    def test_splitPathIn2_no_path(self):
        path = [(0, 0, 0, 1), (0, 0, 1, 0), (1, 0, 0, 0), (0, 1, 0, 0)]
        with pytest.raises(AssertionError):
            splitPathIn2(path, (0, 0, 1, 0))

    def test_splitPathIn2_first_element(self):
        path = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]
        expected_result = ([(0, 0, 0, 1)], [(0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)])
        result = splitPathIn2(path, (0, 0, 0, 1))

        assert result == expected_result

    def test_splitPathIn2_last_element(self):
        path = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]
        expected_result = ([(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)], [])
        result = splitPathIn2(path, (1, 0, 0, 0))

        assert result == expected_result

    def test_cutCycle_already_correct(self):
        cycle = [(0, 1, 2), (0, 2, 1), (2, 0, 1), (2, 1, 0), (1, 2, 0), (1, 0, 2)]
        assert cutCycle(cycle, (0, 1, 2)) == cycle

    def test_cutCycle_cut(self):
        cycle = [(0, 1, 2), (0, 2, 1), (2, 0, 1), (2, 1, 0), (1, 2, 0), (1, 0, 2)]
        result = cutCycle(cycle, (1, 0, 2))
        expected_result = [
            (1, 0, 2),
            (0, 1, 2),
            (0, 2, 1),
            (2, 0, 1),
            (2, 1, 0),
            (1, 2, 0),
        ]
        assert result == expected_result

    def test_cutCycle_not_in_cycle(self):
        cycle = [(0, 1, 2), (0, 2, 1), (2, 0, 1), (2, 1, 0), (1, 2, 0), (1, 0, 2)]
        with pytest.raises(AssertionError):
            cutCycle(cycle, (0, 0, 0))

    def test_cutCycle_empty_cycle(self):
        with pytest.raises(AssertionError):
            cutCycle([], (0, 1, 2))

    def test_cutCycle_middle(self):
        cycle = [(0, 1, 2), (0, 2, 1), (2, 0, 1), (2, 1, 0), (1, 2, 0), (1, 0, 2)]
        result = cutCycle(cycle, (2, 1, 0))
        expected_result = [
            (2, 1, 0),
            (1, 2, 0),
            (1, 0, 2),
            (0, 1, 2),
            (0, 2, 1),
            (2, 0, 1),
        ]
        assert result == expected_result

    def test_cutCycle_one_element(self):
        cycle = [(0, 1, 2)]
        result = cutCycle(cycle, (0, 1, 2))
        assert result == cycle

    def test_cutCycle_two_elements(self):
        cycle = [(0, 1), (1, 0)]
        result = cutCycle(cycle, (1, 0))
        assert result == cycle[::-1]

    def test_spurBaseIndex_first(self):
        path = [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 1, 0), (1, 0, 0, 1)]
        result = spurBaseIndex(path, (0, 0, 1, 1))
        expected_result = 0
        assert result == expected_result

    def test_spurBaseIndex_different(self):
        path = [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 1, 0), (1, 0, 0, 1)]
        result = spurBaseIndex(path, (1, 1, 0, 0))
        expected_result = 2
        assert result == expected_result

    def test_spurBaseIndex_empty(self):
        with pytest.raises(ValueError):
            spurBaseIndex([], (0, 0, 1, 1))

    def test_spurBaseIndex_no_neighbor(self):
        path = [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 1, 0), (1, 0, 0, 1)]
        with pytest.raises(ValueError):
            spurBaseIndex(path, (0, 0, 0, 0))

    def test_neighbor_different_length(self):
        s = (0, 1, 0, 1)
        t = (0, 1, 1, 0, 1)
        assert neighbor(s, t) == False

    def test_neighbor_different_signatures(self):
        s = (0, 1, 0, 1, 0)
        t = (0, 1, 1, 0, 1)
        assert neighbor(s, t) == False

    def test_neighbor_same(self):
        s = (0, 1, 0, 1)
        assert neighbor(s, s) == False

    def test_neighbor_true(self):
        s = (0, 1, 0, 1)
        t = (0, 1, 1, 0)
        assert neighbor(s, t)

    def test_neighbor_false(self):
        s = (0, 1, 0, 1)
        t = (1, 1, 0, 0)
        assert neighbor(s, t) == False

    def test_neighbor_empty(self):
        s = tuple()
        t = tuple()
        assert neighbor(s, t) == False

    def test_mul_empty(self):
        assert mul([], 1) == [(1,)]

    def test_mul_one_element(self):
        assert mul([(0,)], 1) == [(0, 1)]

    def test_mul_multiple_elements(self):
        assert mul([(0, 1), (1, 0)], 1) == [(0, 1, 1), (1, 0, 1)]

    def test_mul_different_number(self):
        assert mul([(0, 1), (1, 0)], 9) == [(0, 1, 9), (1, 0, 9)]

    def test_incorporateSpurInZigZag_path(self):
        path = [
            (0, 1, 0, 1, 0, 1),
            (0, 1, 0, 1, 1, 0),
            (0, 1, 1, 0, 1, 0),
            (0, 1, 1, 0, 0, 1),
            (1, 0, 1, 0, 0, 1),
            (1, 0, 1, 0, 1, 0),
            (1, 0, 0, 1, 1, 0),
            (1, 0, 0, 1, 0, 1),
        ]
        spur_pair = ((0, 0, 1, 1, 0, 1), (0, 0, 1, 1, 1, 0))
        result = incorporateSpurInZigZag(path, spur_pair)
        expected_result = [
            (0, 1, 0, 1, 0, 1),
            spur_pair[0],
            spur_pair[1],
            (0, 1, 0, 1, 1, 0),
            (0, 1, 1, 0, 1, 0),
            (0, 1, 1, 0, 0, 1),
            (1, 0, 1, 0, 0, 1),
            (1, 0, 1, 0, 1, 0),
            (1, 0, 0, 1, 1, 0),
            (1, 0, 0, 1, 0, 1),
        ]
        assert result == expected_result

    def test_incorporateSpurInZigZag_empty(self):
        spur_pair = ((0, 0, 1, 1, 0, 1), (0, 0, 1, 1, 1, 0))
        with pytest.raises(ValueError):
            incorporateSpurInZigZag([], spur_pair)

    def test_incorporateSpurInZigZag_no_neighbor(self):
        path = [
            (0, 1, 0, 1, 0, 1),
            (0, 1, 0, 1, 1, 0),
            (0, 1, 1, 0, 1, 0),
            (0, 1, 1, 0, 0, 1),
            (1, 0, 1, 0, 0, 1),
            (1, 0, 1, 0, 1, 0),
            (1, 0, 0, 1, 1, 0),
            (1, 0, 0, 1, 0, 1),
        ]
        spur_pair = ((1, 0, 1, 1, 0, 1), (1, 0, 1, 1, 1, 0))
        with pytest.raises(ValueError):
            print(incorporateSpurInZigZag(path, spur_pair))

    def test_createZigZagPath_from_cycle(self):
        c = [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 1, 0), (1, 0, 0, 1)]
        u = (0, 1)
        v = (1, 0)
        result = createZigZagPath(c, u, v)
        expected_result = [
            (0, 1, 0, 1, 0, 1),
            (0, 1, 0, 1, 1, 0),
            (0, 1, 1, 0, 1, 0),
            (0, 1, 1, 0, 0, 1),
            (1, 0, 1, 0, 0, 1),
            (1, 0, 1, 0, 1, 0),
            (1, 0, 0, 1, 1, 0),
            (1, 0, 0, 1, 0, 1),
        ]
        assert result == expected_result

    def test_createZigZagPath_from_path(self):
        c = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]
        u = (0, 1)
        v = (1, 0)
        result = createZigZagPath(c, u, v)
        expected_result = [
            (0, 0, 0, 1, 0, 1),
            (0, 0, 0, 1, 1, 0),
            (0, 0, 1, 0, 1, 0),
            (0, 0, 1, 0, 0, 1),
            (0, 1, 0, 0, 0, 1),
            (0, 1, 0, 0, 1, 0),
            (1, 0, 0, 0, 1, 0),
            (1, 0, 0, 0, 0, 1),
        ]
        assert result == expected_result

    def test_createZigZagPath_not_adjacent(self):
        c = [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 1, 0), (1, 0, 0, 1)]
        u = (0, 0)
        v = (0, 1)
        with pytest.raises(AssertionError):
            createZigZagPath(c, u, v)

    def test_createZigZagPath_empty(self):
        c = []
        u = (0, 1)
        v = (1, 0)
        with pytest.raises(AssertionError):
            createZigZagPath(c, u, v)

    def test_createZigZagPath_not_path(self):
        c = [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 1, 0)]
        u = (0, 1)
        v = (1, 0)
        with pytest.raises(AssertionError):
            createZigZagPath(c, u, v)

    def test_incorporateSpursInZigZag_path(self):
        path = [
            (0, 1, 0, 1, 0, 1),
            (0, 1, 0, 1, 1, 0),
            (0, 1, 1, 0, 1, 0),
            (0, 1, 1, 0, 0, 1),
            (1, 0, 1, 0, 0, 1),
            (1, 0, 1, 0, 1, 0),
            (1, 0, 0, 1, 1, 0),
            (1, 0, 0, 1, 0, 1),
        ]
        vertices = [(0, 0, 1, 1), (1, 1, 0, 0)]
        spur_suffixes = [(0, 1), (1, 0)]
        result = incorporateSpursInZigZag(path, vertices, spur_suffixes)
        expected_result = [
            (0, 1, 0, 1, 0, 1),
            vertices[0] + spur_suffixes[0],
            vertices[0] + spur_suffixes[1],
            (0, 1, 0, 1, 1, 0),
            (0, 1, 1, 0, 1, 0),
            (0, 1, 1, 0, 0, 1),
            (1, 0, 1, 0, 0, 1),
            vertices[1] + spur_suffixes[0],
            vertices[1] + spur_suffixes[1],
            (1, 0, 1, 0, 1, 0),
            (1, 0, 0, 1, 1, 0),
            (1, 0, 0, 1, 0, 1),
        ]
        assert result == expected_result

    def test_incorporateSpursInZigZag_empty(self):
        vertices = [(0, 0, 1, 1), (1, 1, 0, 0)]
        spur_suffixes = [(0, 1), (1, 0)]
        with pytest.raises(ValueError):
            incorporateSpursInZigZag([], vertices, spur_suffixes)

    def test_incorporateSpursInZigZag_no_neighbor(self):
        path = [
            (0, 1, 0, 1, 0, 1),
            (0, 1, 0, 1, 1, 0),
            (0, 1, 1, 0, 1, 0),
            (0, 1, 1, 0, 0, 1),
            (1, 0, 1, 0, 0, 1),
            (1, 0, 1, 0, 1, 0),
            (1, 0, 0, 1, 1, 0),
            (1, 0, 0, 1, 0, 1),
        ]
        vertices = [(1, 0, 1, 1), (0, 1, 0, 0)]
        spur_suffixes = [(0, 1), (1, 0)]
        with pytest.raises(ValueError):
            incorporateSpursInZigZag(path, vertices, spur_suffixes)

    def test_createSquarTube_path(self):
        path = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]
        u, v = (0, 1), (1, 0)
        result = createSquareTube(path, u, v)
        # Everything should be uu, uv, vv, vu, vu, vv, uv, uu
        # Except the last two nodes uu, uv, vv, vu, vu, uu, uv, vv
        expected_result = [
            (0, 0, 0, 1, 0, 1, 0, 1),
            (0, 0, 0, 1, 0, 1, 1, 0),
            (0, 0, 0, 1, 1, 0, 1, 0),
            (0, 0, 0, 1, 1, 0, 0, 1),
            (0, 0, 1, 0, 1, 0, 0, 1),
            (0, 0, 1, 0, 1, 0, 1, 0),
            (0, 0, 1, 0, 0, 1, 1, 0),
            (0, 0, 1, 0, 0, 1, 0, 1),
            (0, 1, 0, 0, 0, 1, 0, 1),
            (0, 1, 0, 0, 0, 1, 1, 0),
            (0, 1, 0, 0, 1, 0, 1, 0),
            (0, 1, 0, 0, 1, 0, 0, 1),
            (1, 0, 0, 0, 1, 0, 0, 1),
            (1, 0, 0, 0, 0, 1, 0, 1),
            (1, 0, 0, 0, 0, 1, 1, 0),
            (1, 0, 0, 0, 1, 0, 1, 0),
        ]
        assert result == expected_result

    def test_createSquarTube_empty(self):
        with pytest.raises(AssertionError):
            createSquareTube([], (0, 1), (1, 0))

    def test_createSquarTube_not_adjacent(self):
        path = [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 1, 0), (1, 0, 0, 1)]
        u, v = (0, 0), (0, 1)
        with pytest.raises(AssertionError):
            createSquareTube(path, u, v)

    def test_createSquarTube_not_path(self):
        path = [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 1, 0)]
        u, v = (0, 1), (1, 0)
        with pytest.raises(AssertionError):
            createSquareTube(path, u, v)

    def test_createSquarTube_odd_length_path(self):
        path = [(0, 0, 1), (0, 1, 0), (1, 0, 0)]
        u, v = (0, 1), (1, 0)
        with pytest.raises(AssertionError):
            createSquareTube(path, u, v)

    def test_createSquarTube_different_colors_uv(self):
        path = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]
        u, v = (2, 3, 2), (3, 2, 2)
        result = createSquareTube(path, u, v)
        # Everything should be uu, uv, vv, vu, vu, vv, uv, uu
        # Except the last two nodes uu, uv, vv, vu, vu, uu, uv, vv
        expected_result = [
            (0, 0, 0, 1) + u + u,
            (0, 0, 0, 1) + u + v,
            (0, 0, 0, 1) + v + v,
            (0, 0, 0, 1) + v + u,
            (0, 0, 1, 0) + v + u,
            (0, 0, 1, 0) + v + v,
            (0, 0, 1, 0) + u + v,
            (0, 0, 1, 0) + u + u,
            (0, 1, 0, 0) + u + u,
            (0, 1, 0, 0) + u + v,
            (0, 1, 0, 0) + v + v,
            (0, 1, 0, 0) + v + u,
            (1, 0, 0, 0) + v + u,
            (1, 0, 0, 0) + u + u,
            (1, 0, 0, 0) + u + v,
            (1, 0, 0, 0) + v + v,
        ]
        assert result == expected_result

    def test_transform_empty(self):
        assert transform([], [1, 2, 3]) == []

    def test_transform_empty_transformer(self):
        with pytest.raises(ValueError):
            transform([(0, 1), (1, 0)], [5])

    def test_transform_one_element(self):
        assert transform([(0,)], [1, 2, 3]) == [(1,)]

    def test_transform_multiple_elements(self):
        assert transform([(0, 1), (1, 0)], [1, 2, 3]) == [(1, 2), (2, 1)]

    def test_transform_different_number(self):
        assert transform([(0, 1), (1, 0)], [9, 8, 7]) == [(9, 8), (8, 9)]

    def test_transform_not_path(self):
        assert transform([(0, 1), (1, 2)], [1, 2, 3]) == [(1, 2), (2, 3)]

    def test_get_transformer_empty(self):
        assert get_transformer([], lambda x: x[0]) == ([], [])
        assert get_transformer([], lambda x: [x[0] % 2, x[0]]) == ([], [])

    def test_get_transformer_negative_signature(self):
        with pytest.raises(ValueError):
            get_transformer([-2], lambda x: x[0])
        with pytest.raises(ValueError):
            get_transformer([3, 4, 5, -3], lambda x: x[0])
        with pytest.raises(ValueError):
            get_transformer([3, -1, 5, 4], lambda x: [x[0] % 2, x[0]])

    def test_get_transformer_one_element(self):
        assert get_transformer([1], lambda x: x[0]) == ([1], [0])
        assert get_transformer([2], lambda x: [x[0] % 2, x[0]]) == ([2], [0])

    def test_get_transformer_with_zero(self):
        assert get_transformer([0], lambda x: [x[0] % 2, x[0]]) == ([], [])
        assert get_transformer([0, 3, 2], lambda x: x[0]) == ([3, 2], [1, 2])
        assert get_transformer([0, 3, 2], lambda x: -x[0]) == ([2, 3], [2, 1])

    def test_get_transformer_function_not_callable(self):
        assert get_transformer([], 0) == ([], [])
        with pytest.raises(ValueError):
            get_transformer([0], 0)
        with pytest.raises(ValueError):
            get_transformer([0], [0])
        with pytest.raises(ValueError):
            get_transformer([1, 2, 3], None)

    def test_get_transformer_multiple_elements_odd_first(self):
        assert get_transformer([2, 3, 4, 5], lambda x: [x[0] % 2, x[0]]) == (
            [5, 3, 4, 2],
            [3, 1, 2, 0],
        )
        assert get_transformer([9, 4, 4, 9], lambda x: [x[0] % 2, x[0]]) == (
            [9, 9, 4, 4],
            [0, 3, 1, 2],
        )
        assert get_transformer([4, 9, 9, 4], lambda x: [x[0] % 2, x[0]]) == (
            [9, 9, 4, 4],
            [1, 2, 0, 3],
        )
        assert get_transformer([5, 0, 3, 4, 7, 6], lambda x: [x[0] % 2, x[0]]) == (
            [7, 5, 3, 6, 4],
            [4, 0, 2, 5, 3],
        )

    def test_get_transformer_multiple_elements_even_first(self):
        assert get_transformer([3, 4, 5, 6], lambda x: [x[0] % 2 == 0, x[0]]) == (
            [6, 4, 5, 3],
            [3, 1, 2, 0],
        )
        assert get_transformer([4, 9, 9, 4], lambda x: [x[0] % 2 == 0, x[0]]) == (
            [4, 4, 9, 9],
            [0, 3, 1, 2],
        )
        assert get_transformer([9, 4, 4, 9], lambda x: [x[0] % 2 == 0, x[0]]) == (
            [4, 4, 9, 9],
            [1, 2, 0, 3],
        )
        assert get_transformer([0, 5, 6, 7, 4, 3], lambda x: [x[0] % 2 == 0, x[0]]) == (
            [6, 4, 7, 5, 3],
            [2, 4, 3, 1, 5],
        )

    def test_get_transformer_multiple_elements_descending(self):
        assert get_transformer([4, 5, 6, 7, 8], lambda x: x[0]) == (
            [8, 7, 6, 5, 4],
            [4, 3, 2, 1, 0],
        )
        assert get_transformer([8, 7, 6, 5, 4], lambda x: x[0]) == (
            [8, 7, 6, 5, 4],
            [0, 1, 2, 3, 4],
        )
        assert get_transformer([8, 6, 7, 2, 5], lambda x: x[0]) == (
            [8, 7, 6, 5, 2],
            [0, 2, 1, 4, 3],
        )
        assert get_transformer([6, 6, 8, 8], lambda x: x[0]) == (
            [8, 8, 6, 6],
            [2, 3, 0, 1],
        )

    def test_get_transformer_multiple_elements_ascending(self):
        assert get_transformer([8, 7, 6, 5, 4], lambda x: -x[0]) == (
            [4, 5, 6, 7, 8],
            [4, 3, 2, 1, 0],
        )
        assert get_transformer([4, 5, 6, 7, 8], lambda x: -x[0]) == (
            [4, 5, 6, 7, 8],
            [0, 1, 2, 3, 4],
        )
        assert get_transformer([8, 6, 7, 2, 5], lambda x: -x[0]) == (
            [2, 5, 6, 7, 8],
            [3, 4, 1, 2, 0],
        )
        assert get_transformer([8, 8, 6, 6], lambda x: -x[0]) == (
            [6, 6, 8, 8],
            [2, 3, 0, 1],
        )

    def test_transformCycleCover_depth1(self):
        assert transform_cycle_cover([[(0, 1), (1, 0)]], [1, 2, 3]) == [
            [(1, 2), (2, 1)]
        ]

    def test_transformCycleCover_depth2(self):
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
        assert transform_cycle_cover(p, [4, 2]) == [
            [
                [
                    [
                        (4, 4, 2, 2),
                        (4, 2, 4, 2),
                        (2, 4, 4, 2),
                        (4, 2, 2, 4),
                        (2, 4, 2, 4),
                        (2, 2, 4, 4),
                    ]
                ]
            ],
            [[(4, 2), (2, 4)]],
        ]

    def test_transformCycleCover_depth3(self):
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
        assert transform_cycle_cover(p, [2, 1, 3, 0]) == [
            [
                [
                    [
                        (2, 2, 1, 1),
                        (2, 1, 2, 1),
                        (1, 2, 2, 1),
                        (2, 1, 1, 2),
                        (1, 2, 1, 2),
                        (1, 1, 2, 2),
                    ]
                ]
            ],
            [[(2, 1), (1, 2)]],
            [[[[(0,)]]]],
        ]

    def test_transformCycleCover_empty_transformer(self):
        with pytest.raises(ValueError):
            transform_cycle_cover([[(0, 1), (1, 0)]], [])

    def test_transformCycleCover_empty(self):
        with pytest.raises(AssertionError):
            transform_cycle_cover([], [1, 2, 3])

    def test_recursiveCycleCheck_empty(self):
        with pytest.raises(AssertionError):
            recursive_cycle_check([])

    def test_recursiveCycleCheck_one_node(self):
        with pytest.raises(AssertionError):
            recursive_cycle_check([[(0, 1, 2)]])

    def test_recursiveCycleCheck_one_cycle(self):
        assert (
            recursive_cycle_check(
                [[(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 1, 0), (1, 0, 0, 1)]]
            )
            == 4
        )
