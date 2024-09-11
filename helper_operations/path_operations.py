import numpy as np


def adjacent(s: tuple[int, ...], t: tuple[int, ...]) -> bool:
    """
    Check if two tuples are adjacent. They are adjacent if they differ by a swap of two adjacent elements.

    Args:
        s (tuple[int, ...]): The first tuple.
        t (tuple[int, ...]): The second tuple.

    Returns:
        bool: True if the tuples are adjacent, False otherwise.
    """
    if len(s) != len(t) or len(s) < 2:
        return False
    if isinstance(s, np.ndarray):
        diff = np.where(s != t)[0]
        return (
            diff.size == 2
            and diff[0] + 1 == diff[1]
            and s[diff[0]] == t[diff[1]]
            and s[diff[1]] == t[diff[0]]
        )
    for i in range(len(s) - 1):
        if s[i] != t[i]:
            return (
                s[i] == t[i + 1]
                and s[i + 1] == t[i]
                and s[:i] == t[:i]
                and s[i + 2 :] == t[i + 2 :]
            )
    return False


def pathQ(p: list[tuple[int, ...]], verbose=True) -> bool:
    """
    Checks if the given list of vertices represents a path. So True if all vertices are adjacent, False otherwise.

    Args:
        p (list[tuple[int, ...]]): List of permutations (vertices). The order of the vertices is checked.
        verbose (bool, optional): Whether the error in the path should be printed in console. Defaults to True.

    Returns:
        bool: True if p is a path, False otherwise.
    """
    if len(p) == 0:
        return False
    elif len(p) == 1:
        return True
    for i, item in enumerate(p):
        if i < len(p) - 1 and not adjacent(item, p[i + 1]):
            if verbose:
                print(
                    f"No path: index {i}->{i+1}. See: {i-1}-{i}-{i+1}; {p[i-1]}-{item}-{p[i+1]}"
                )
            return False
    return True


def cycleQ(c: list[tuple[int, ...]]) -> bool:
    """
    Checks if a list of tuples represents a cycle. The list represents a cycle if all vertices are adjacent and the first and last vertices are adjacent.

    Args:
        c (list[tuple[int, ...]]): A list of tuples representing a cycle.

    Returns:
        bool: True if the list represents a cycle, False otherwise.
    """
    if len(c) <= 2:
        return False
    for i, item in enumerate(c):
        if not adjacent(item, c[(i + 1) % len(c)]):
            print(f"not a cycle: {item} and {c[(i + 1) % len(c)]}")
            return False
    return True


def pathEdges(
    p: list[tuple[int, ...]]
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """
    Returns a list of edges of a path. T

    Args:
        p (list[tuple[int, ...]]): The path represented as a list of adjacent vertices.

    Returns:
        list[list[tuple[int, ...]]]: A list of edges, where each edge is represented as a tuple of two adjacent vertices.

    Raises:
        ValueError: If the given list of vertices does not represent a path.
    """
    if not pathQ(p) or len(p) < 2:
        raise ValueError(f"Path {p} is not a path.")
    return [(item, p[i + 1]) for i, item in enumerate(p) if i < len(p) - 1]


def splitPathIn2(
    p: list[tuple[int, ...]], a: tuple[int, ...]
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """
    Splits a path in two parts at vertex `a`. Element `a` appears in only the first path.

    Args:
        p (list[tuple[int, ...]]): The path to be split.
        a (tuple[int, ...]): The vertex at which to split the path.

    Returns:
        tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
            A tuple containing two lists representing the split paths.\n
            - The first list contains the vertices from the start of the original path up to and including vertex `a`.
            - The second list contains the vertices from vertex `a+1` to the end of the original path.

    Raises:
        AssertionError: If the length of the path is less than or equal to 1.
        AssertionError: If the vertex `a` is not present in the path.
        AssertionError: If the list `p` does not represent a path.
    """
    assert len(p) > 1
    if not a in p:
        raise AssertionError(f"Vertex {a} not in path {p}")
    assert pathQ(p)
    A = p.index(a)
    return p[: A + 1], p[A + 1 :]


def cutCycle(c: list[tuple[int, ...]], a: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Splits a cycle at vertex `a` and rotates it such that vertex `a` apprears first in the returned path.

    Args:
        c (list[tuple[int, ...]]): The cycle to be split. Can also be a numpy array.
        a (tuple[int, ...]): The vertex at which to split the cycle. Must be present in the cycle.

    Returns:
        list[tuple[int, ...]]: The cycle `c` but rotated such that vertex `a` appears first.

    Raises:
        AssertionError: If the vertex a is not present in the cycle c.
        ValueError: If the vertex a is not present in the numpy cycle c (if c is a numpy array).

    """
    if len(c) == 1 and a in c:
        return c
    try:
        assert a in c
    except AssertionError as err:
        print(f"{repr(err)} cycle: {c}, should be cut to {a}")
        raise err
    # if the array is a numpy array, use numpy functions
    if isinstance(c, np.ndarray):
        # check whether a is in c
        if not np.any(np.all(c == a, axis=1)):
            print(f"Vertex {a} not in numpy cycle {c}")
            raise ValueError(f"Vertex {a} not in numpy cycle {c}")
        index = np.where(np.all(c == a, axis=1))[0][0]
        return np.roll(c, -index, axis=0)
    # if the array is a list, use list functions (index instead of where)
    A = c.index(a)
    return c[A:] + c[:A]


def spurBaseIndex(path: list[tuple[int, ...]], vertex: tuple[int, ...]) -> int:
    """
    Determines the index of the base of the spur for a given path and spur tip.

    Args:
        path (list[tuple[int, ...]]): The path to search for the base of the spur.
        vertex (tuple[int, ...]): The spur tip vertex.

    Returns:
        int: The index of the base of the spur.

    Raises:
        ValueError: If no vertex adjacent to `vertex` is found in the `path`.
    """
    for i, item in enumerate(path):
        if adjacent(item, vertex):
            return i
    raise ValueError(f"No vertex adjacent to {vertex} in the path: {path}")


def find_last_distinct_adjacent_index(perm: tuple[int, ...]) -> int:
    """
    Find the last pair of distinct adjacent elements in a permutaiton (tuple).

    Args:
        perm (tuple[int, ...]): Permutation as a tuple of integers.

    Returns:
        int: The index of the first element in the last pair of distinct adjacent

    Raises:
        ValueError: If no distinct adjacent elements are found in the permutation.
    """
    # Loop through the tuple from the second last element to the first
    for i in range(len(perm) - 2, -1, -1):
        # Check if adjacent elements are distinct
        if perm[i] != perm[i + 1]:
            # Return the index of the first element in the distinct pair
            return i
    # Return None if no distinct adjacent elements are found
    raise ValueError(f"No distinct adjacent elements found in the permutation: {perm}")


def mul(sez: list[tuple[int, ...]], e: int) -> list[tuple[int, ...]]:
    """
    Adds 'e' to all elements (tuples) in the list `sez`.

    Args:
        sez (list[tuple[int, ...]]): The list of tuples to be modified.
        e (int): The value to be appended to each element in sez.

    Returns:
        list[tuple[int, ...]]: The modified list with 'e' added to each element.
    """
    if not sez:
        return [(e,)]
    for i, el in enumerate(sez):
        sez[i] = el + (e,)
    return sez


def createZigZagPath(
    p: list[tuple[int, ...]], u: tuple[int, ...], v: tuple[int, ...]
) -> list[tuple[int, ...]]:
    """
    Create a zigzag path by combining two "parallel" copies of a given path.
    The zig zag path runs from `p[0]u` to `p[-1]u`. Obtained by appending `u` and `v` to each vertex in the path.
    Then for the following vertex in the path, append `v` and `u` to it. Then `u` and `v`, again `v` and `u` and so on.

    Args:
        p (list[tuple[int, ...]]): Path as a list of tuples.
        u (tuple[int, ...]): Tuple to append.
        v (tuple[int, ...]): Tuple to append.

    Returns:
        list[tuple[int, ...]]:
            Path obtained by combining two "parallel" copies of the given path `p`.

    Raises:
        AssertionError: If the path `p` is not a path.
        AssertionError: If the length of the path is less than 1.
        AssertionError: If the vertices `u` and `v` are not adjacent.
    """
    assert adjacent(u, v)
    assert pathQ(p)
    assert len(p) > 0
    temp = [item for sublist in zip(p, p) for item in sublist]
    module = [u, v, v, u]
    return [item + module[i % 4] for i, item in enumerate(temp)]


def incorporateSpurInZigZag(
    path: list[tuple[int, ...]], vertex_pair: tuple[tuple[int, ...], tuple[int, ...]]
) -> list[tuple[int, ...]]:
    """
    Incorporates a spur in a zigzag path. A spur consists of two vertices,
    both ending with two trailing elements that are the same as in the zigzag path.
    The spur is incorporated by finding the base of the spur in the zigzag path,
    i.e. the vertex adjacent to the spur tip which is in the "zig" part.
    Then the spur is inserted in the path at that index. Then the path continues with the "zag" part.

    Args:
        path (list[tuple[int, ...]]): List of vertices, a zigzag path.
        vertex_pair (tuple[tuple[int, ...], tuple[int, ...]]):
            A pair of vertices to incorporate. The pair consists of two vertices,
            both ending with two trailing elements that are the same as in the zigzag path.
            The parts prior to the trailing elements are stutters.


    Returns:
        list[tuple[int, ...]]: List of vertices, the zigzag path with the spur incorporated.
    """
    # Modify path to remove last e elements except for the first one
    i = spurBaseIndex(path, vertex_pair[0])
    return path[: i + 1] + list(vertex_pair) + path[i + 1 :]


def createSquareTube(path: list[tuple], u: tuple, v: tuple) -> list[tuple[int, ...]]:
    """
    Creates a square tube from a path by appending combinations of `u` and `v` like so:\n
    - The first vertices with `uu, uv, vv, vu, vu, vv, uv, uu`
    - Only the last one with `uu, uv, vv, vu, vu, uu, uv, vv`\n
    Every vertex in the original path is repeated 4 times. Once for each combination of `u` and `v` above.

    Args:
        path (list[tuple]): List of vertices, a path.
        u (tuple): Tuple to append.
        v (tuple): Tuple adjacent to `u` to append.

    Returns:
        list[tuple[int, ...]]: List of vertices, the square tube. Every vertex in the original path is repeated 4 times.
    """
    assert adjacent(u, v)
    assert pathQ(path)
    assert len(path) > 0 and len(path) % 2 == 0
    # interleave the elements of the four copies of the path list
    temp = [item for sublist in zip(*([path] * 4)) for item in sublist]
    uu = u + u
    uv = u + v
    vu = v + u
    vv = v + v
    module1 = [uu, uv, vv, vu, vu, vv, uv, uu]
    module2 = [uu, uv, vv, vu, vu, uu, uv, vv]

    # Combine the path with modules based on the index
    result = [item + module1[i % 8] for i, item in enumerate(temp[:-8])] + [
        item + module2[i % 8] for i, item in enumerate(temp[-8:])
    ]
    return result


def get_transformer(s: tuple[int], func: callable) -> tuple[tuple[int], list[int]]:
    """
    Sorts the signature using a given function and provides array to transform it back.
    The transformer array is built by indexing the numbers. See ``transform`` for more details on the format.

    Args:
        s (tuple[int]): The signature as a tuple of integers.
        func (callable): The lambda function of tuples of form (value, index) to sort the signature.

    Returns:
        tuple[tuple[int], list[int]]:
            A tuple of a tuple and a list of integers:
            - the first is a tuple: the sorted signature.
            - the second is a list: the transformation array (used in the ``tranform`` function).
    """
    if len(list(s)) == 0:
        return tuple(), []
    elif any(s_i < 0 for s_i in s):
        raise ValueError("Signature must be a tuple of non-negative integers.")
    elif not callable(func):
        raise ValueError("Function must be callable.")
    # index the numbers in the signature such that we can transform them back later
    indexed_sig = [(value, idx) for idx, value in enumerate(s)]
    # put the odd numbers first in the signature
    indexed_sig.sort(reverse=True, key=func)
    return tuple([x[0] for x in indexed_sig if x[0] != 0]), [
        x[1] for x in indexed_sig if x[0] != 0
    ]


def transformer_to_sorted(
    unsorted_signature: tuple[int, ...], func=lambda x: x[0]
) -> list[int]:
    """
    Get the transformer to go from unsorted to sorted signature.
    Works using a separate function to get 0's in the signature as well.

    Args:
        unsorted_signature (tuple[int, ...]): The unsorted signature.
        func (callable, optional): The lambda function of tuples of form (value, index) to sort the signature. Defaults to lambda x: x[0].

    Returns:
        list[int]: The transformer to go from unsorted to sorted signature.
    """
    # get the transformer (has to be done separately to get 0's in signature as well)
    indexed_sig = [(value, idx) for idx, value in enumerate(unsorted_signature)]
    indexed_sig.sort(reverse=True, key=func)
    transformer_list = [x[1] for x in indexed_sig]
    # get the transformer to go from unsorted to sorted -> reverse transformer
    temp_dict = {i: s for s, i in enumerate(transformer_list)}
    return [temp_dict[k] for k in sorted(temp_dict.keys())]


def transform(perms: list[tuple[int, ...]], tr: list[int]) -> list[tuple[int, ...]]:
    """
    Transforms a list of permutations as tuples according to the given renaming.
    The transformer list `tr` is a list of integers where the integer at index `i` is the new name for element `i`.
    See the example below.\n
    The function raises a ValueError if `lis` contains an element whose index is larger than the length `tr`.
    So the transformation list should be at least as long as the largest index in the permutations.

    Args:
        perms (list[tuple[int, ...]]): List of permutations.
        tr (list[int]): Transformation list, int at index `i` is the new name for `i`.

    Returns:
        list[tuple[int, ...]]: List of tuples of integers. The transformed permutations.

    Raises:
        ValueError: If the index of an element in the permutation is larger than the length of the transformation list.

    Example:
        >>> transform([(0, 1, 2), (1, 0, 2)], [4, 5, 6])
        [(4, 5, 6), (5, 4, 6)]
    """
    l = []
    for i in perms:
        v = []
        for j in i:
            try:
                v.append(tr[j])
            except IndexError:
                raise ValueError(
                    f"Index {j} is larger than the length of the transformation list {tr}"
                )
        l.append(tuple(v))
    return l


def transform_cycle_cover(perms3d: list[list], tr: list[int]) -> list[list]:
    """
    Transforms a list of unknown depth holding a list of permutations according to the given renaming. Used for the cycle cover.
    The transformer list `tr` is a list of integers where the integer at index `i` is the new name for element `i`.
    The depth is at least 2 and determined by the cycle cover function.

    Args:
        perms3d (list[list[tuple[int, ...]]]):
            List of lists of permutations. Does not have a fixed depth. The depth is determined by the cycle cover function.
            If the depth is 2 (list of lists of permutations, where permutations are tuples), the function will transform the permutations.
        tr (list[int]):
            Transformation list, int at index `i` is the new name for `i`.

    Returns:
        list[list[tuple[int, ...]]]: The same structure of lists as the input, but with the permutations transformed.
    Raises:
        AssertionError: If the input list does not have a length greater than 0.
        ValueError: If the input is not a list.
    """
    try:
        assert isinstance(perms3d, list) and len(perms3d) > 0
        assert isinstance(perms3d[0], list) and len(perms3d[0]) > 0
        assert (
            isinstance(perms3d[0][0], list) or isinstance(perms3d[0][0], tuple)
        ) and len(perms3d[0][0]) > 0
    except AssertionError:
        raise AssertionError(f"The input could not be parsed: {perms3d}")
    if isinstance(perms3d[0][0][0], int):
        return [transform(l, tr) for l in perms3d]
    elif not isinstance(perms3d, list):
        raise ValueError(f"The input is not a list: {perms3d}")
    else:
        return [transform_cycle_cover(l, tr) for l in perms3d]


def shorten_cycle_cover(lis3d: list[list], elements: tuple[int, ...]) -> list[list]:
    """
    Shortens a list of unknown depth holding a list of permutations by the given elements. Used for the cycle cover.
    The elements are removed from the permutations in the lists of tuples. Also checks whether all tuples end with the given elements.

    Args:
        lis3d (list[list]):
            List of lists of permutations. Does not have a fixed depth. The depth is determined by the cycle cover function.
            If the depth is 2 (list of lists of permutations, where permutations are tuples), the function will shorten the permutations.
        elements (tuple[int, ...]):
            Tuple of integers to remove from the permutations.

    Returns:
        list[list[tuple[int, ...]]]:
            The same structure of lists as the input, but with the permutations shortened by `elements`.

    Raises:
        AssertionError: If the input list does not have a length greater than 0.
        AssertionError: If a permutation does not end with the given elements.
    """
    assert len(lis3d) > 0
    if len(elements) == 0:
        return lis3d
    elif (
        not isinstance(lis3d, list)
        or len(lis3d) == 0
        or not isinstance(lis3d[0], list)
        or len(lis3d[0]) == 0
        or len(lis3d[0][0]) == 0
    ):
        raise ValueError("The input is not a list")
    elif isinstance(lis3d[0][0][0], int):
        assert all(tup[-len(elements) :] == elements for l in lis3d for tup in l)
        return [[tup[: -len(elements)] for l in lis3d for tup in l]]
    else:
        return [shorten_cycle_cover(l, elements) for l in lis3d]


def recursive_cycle_check(cycle: list[list], total_length=0) -> int:
    """
    Recursively check whether the given list is a cycle. The input is a list of cycles of unknown depth.
    The function will check the depth and return the total number of permutations in the lists of permutations.
    For each list, the cycle property is checked (and whether it has duplicates).
    Then the length of the cycle is added to the total length. The total length is returned.

    Args:
        cycle (list): List of cycles.
        total_length (int): Total length of the cycle, starts at 0.

    Returns:
        int: Total length of the list of cycles.

    Raises:
        AssertionError: If the input is not a list of length greater than 0.
        AssertionError: If the input is not a list of cycles.
        AssertionError: If the subcycles contain duplicates.
    """
    assert len(cycle) > 0
    assert isinstance(cycle, list)
    if isinstance(cycle[0][0], int):
        assert cycleQ(cycle)
        assert len(cycle) == len(set(cycle))
        total_length += len(cycle)
    else:
        for sub_cycle in cycle:
            total_length = recursive_cycle_check(sub_cycle, total_length)
    return total_length


def get_first_element(nested_list: list, element=0) -> tuple[int, ...]:
    """
    Recursively retrieves the first element of a nested list.

    Args:
        nested_list (list): The nested list. Ultimately a tuple of integers (the permutations).
        element (int, optional): The element to retrieve. Defaults to 0.

    Returns:
        tuple[int, ...]: The first element of the nested list.
    """
    if isinstance(nested_list, list):
        return get_first_element(nested_list[element])
    else:
        return nested_list


def non_stutter_cycleQ(sig: tuple[int]) -> bool:
    """
    Return whether a cycle on the non-stutter permutations is possible for the given signature.
    This cycle is not possible for the following signatures:\n
    - Linear neighbor-swap graphs (even-1 or odd-1)
    - Odd-odd
    - Odd-even / even-odd
    - Even-1-1

    Args:
        sig (tuple[int]): The signature of the multiset permutations.

    Returns:
        bool: True if a cycle on the non-stutter permutations is possible, False if only a path is possible.
    """
    if len(list(sig)) == 0:
        # empty signature cannot be a cycle
        return False
    if len(list(sig)) == 1:
        # one element cannot be a cycle
        return False
    if len(list(sig)) == 2 and 1 in sig:
        # this is a linear graph
        return False
    if len(list(sig)) == 2 and (
        sig[0] % 2 != sig[1] % 2 or (sig[0] % 2 == 1 and sig[1] % 2 == 1)
    ):
        # odd-even or even-odd or odd-odd
        return False
    # sort the signature
    sorted_sig, _ = get_transformer(sig, lambda x: [x[0] % 2, x[0]])
    if len(list(sig)) == 3 and (
        sorted_sig[0] == 1 and sorted_sig[1] == 1 and sorted_sig[2] % 2 == 0
    ):
        # Even-1-1
        return False
    return True


def stutterPermutationQ(perm: tuple[int, ...]) -> bool:
    """
    Check whether a given permutation is a stutter permutation.
    A stutter permutation is a permutation where all elements are the same except for the last two elements.

    Args:
        perm (tuple[int, ...]): The permutation to check.

    Returns:
        bool: True if the permutation is a stutter permutation, False otherwise.
    """
    if len(perm) < 2:
        return True
    return all(perm[i] == perm[i + 1] for i in range(0, len(perm) - 1, 2))


def glue(
    cycle1: list[tuple[int, ...]],
    cycle2: list[tuple[int, ...]],
    vertex_pair_c1: tuple[tuple[int, ...], tuple[int, ...]],
    vertex_pair_c2: tuple[tuple[int, ...], tuple[int, ...]],
) -> list[tuple[int, ...]]:
    """
    Glue two cycles together by using the cross edges instead of the parallel edges
    The cycles must contain the vertices and the vertices must be adjacent (in the cycle)

    Args:
        cycle1 (list[tuple[int, ...]]): The first cycle.
        cycle2 (list[tuple[int, ...]]): The second cycle.
        vertex_pair_c1 (tuple[tuple[int, ...], tuple[int, ...]]): The pair of vertices in the first cycle.
        vertex_pair_c2 (tuple[tuple[int, ...], tuple[int, ...]]): The pair of vertices in the second cycle.

    Returns:
        list[tuple[int, ...]]: The glued cycles.
    """
    # rotate the first cycle to start with the first vertex
    cycle1 = cutCycle(cycle1, vertex_pair_c1[0])
    # make sure it ends with the second vertex
    if cycle1[-1] != vertex_pair_c1[1]:
        cycle1 = cycle1[:1] + cycle1[1:][::-1]
    if not cycle1[-1] == vertex_pair_c1[1]:
        v2index = cycle1.index(vertex_pair_c1[1])
        print(f"Second vertex pair: {vertex_pair_c2}")
        raise ValueError(
            f"In the first cycle, the vertices {vertex_pair_c1} are not adjacent in cycle:\n{[cycle1[-1]] + cycle1[:2]} and {cycle1[v2index-1:v2index+2]} (index {v2index})."
        )
    # rotate the second cycle to start with the first vertex
    cycle2 = cutCycle(cycle2, vertex_pair_c2[0])
    # make sure it ends with the second vertex
    if cycle2[-1] != vertex_pair_c2[1]:
        cycle2 = cycle2[:1] + cycle2[1:][::-1]
    if not cycle2[-1] == vertex_pair_c2[1]:
        v2index = cycle2.index(vertex_pair_c2[1])
        raise ValueError(
            f"In the second cycle, the vertices {vertex_pair_c2} are not adjacent in cycle:\n{[cycle2[-1]] + cycle2[:2]} and {cycle2[v2index-1:v2index+2]}."
        )
    # glue the cycles together
    if adjacent(vertex_pair_c1[0], vertex_pair_c2[0]) and adjacent(
        vertex_pair_c1[1], vertex_pair_c2[1]
    ):
        return cycle1 + cycle2[::-1]
    elif adjacent(vertex_pair_c1[0], vertex_pair_c2[1]) and adjacent(
        vertex_pair_c1[1], vertex_pair_c2[0]
    ):
        return cycle1 + cycle2
    raise ValueError(
        f"The vertices {vertex_pair_c1} and {vertex_pair_c2} are not adjacent."
    )
