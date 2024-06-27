import numpy as np


def adjacent(s: tuple[int, ...], t: tuple[int, ...]) -> bool:
    """returns true if s and t adjacent, false otherwise"""
    if len(s) != len(t):
        return False
    if isinstance(s, np.ndarray):
        diff = np.where(s != t)[0]
        return (
            diff.size == 2
            and diff[0] + 1 == diff[1]
            and s[diff[0]] == t[diff[1]]
            and s[diff[1]] == t[diff[0]]
        )
    diff = [i for i, (a, b) in enumerate(zip(s, t)) if a != b]
    return (
        len(diff) == 2
        and diff[0] + 1 == diff[1]
        and s[diff[0]] == t[diff[1]]
        and s[diff[1]] == t[diff[0]]
    )


def pathQ(p: list[tuple[int, ...]], verbose=True) -> bool:
    """Returns True if p a path.
    :param verbose: whether the error in the path should be printed in console
    :param p, list of vertices
    :return: true if p is a path
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
    """Returns True if c a cycle."""
    if len(c) <= 2:
        return False
    for i, item in enumerate(c):
        if not adjacent(item, c[(i + 1) % len(c)]):
            return False
    return True


def pathEdges(p: list[tuple[int, ...]]) -> list[list[tuple[int, ...]]]:
    """Returns a list of edges of a path. (Path is given as a list of adjacent vertices)"""
    if not pathQ(p):
        return []
    return [[item, p[i + 1]] for i, item in enumerate(p) if i < len(p) - 1]


def stichPaths(
    p1: list[tuple[int, ...]], p2: list[tuple[int, ...]]
) -> list[tuple[int, ...]]:
    """Stitches two parallel paths by gluing the end vertices."""
    if adjacent(p1[-1], p2[0]):
        return p1 + p2
    elif adjacent(p1[0], p2[-1]):
        return p2 + p1
    elif adjacent(p1[-1], p2[-1]):
        return p1 + p2[::-1]
    elif adjacent(p1[0], p2[0]):
        return p1[::-1] + p2
    return False


def splitPathIn2(
    p: list[tuple[int, ...]], a: tuple[int, ...]
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """Splits a path at vertex a. Element a appears in only the first path."""
    assert len(p) > 1
    assert a in p
    assert pathQ(p)
    A = p.index(a)
    return p[: A + 1], p[A + 1 :]


def cutCycle(c: list[tuple[int, ...]], a: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Splits a cycle at vertex a. Vertex a appears on first place"""
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
    """Determines index of base of spur for given path and spur tip. Returns the index of the base of the spur or raises an error."""
    for i, item in enumerate(path):
        print(f"item: {item}, vertex: {vertex}")
        if neighbor(item, vertex):
            return i
    raise ValueError(f"No vertex adjacent to {vertex} in the path: {path}")


def neighbor(p: tuple[int, ...], q: tuple[int, ...]) -> bool:
    """Returns True if p and q differ by a swap of two adjacent elements, False otherwise."""
    if len(p) != len(q):
        return False
    diff = [i for i, (a, b) in enumerate(zip(p, q)) if a != b]
    return (
        len(diff) == 2
        and diff[0] + 1 == diff[1]
        and p[diff[0]] == q[diff[1]]
        and p[diff[1]] == q[diff[0]]
    )


def mul(sez: list[tuple[int, ...]], e: int) -> list[tuple[int, ...]]:
    """Adds 'e' to all elements(lists) in list sez"""
    if not sez:
        return [(e,)]
    for i, el in enumerate(sez):
        sez[i] = el + (e,)
    return sez


def createZigZagPath(
    c: list[tuple[int, ...]], u: tuple[int, ...], v: tuple[int, ...]
) -> list[tuple[int, ...]]:
    """
    :param c: cycle as a list of tuples
    :param u: tuple to append
    :param v: tuple to append
    :return: cycle obtained by combining two "parallel" copies of given cycle, to form a 'square wave',
            running from cycle[[1]]v to cycle[[-1]]v; the two copies are distinguished by
            appending u and v; also works for a path
    """
    assert adjacent(u, v)
    assert pathQ(c)
    assert len(c) > 0
    temp = [item for sublist in zip(c, c) for item in sublist]
    module = [u, v, v, u]
    return [item + module[i % 4] for i, item in enumerate(temp)]


def incorporateSpurInZigZag(
    path: list[tuple[int, ...]], vertex_pair: tuple[tuple[int, ...], tuple[int, ...]]
) -> list[tuple[int, ...]]:
    """
    Incorporates a spur in a zigzag path.
    @param path: list of vertices, a zigzag path
    @param vertex_pair: a pair of vertices to incorporate
    @return: list of vertices, the zigzag path with the spur incorporated
    """
    # Modify path to remove last e elements except for the first one
    i = spurBaseIndex(path, vertex_pair[0])
    return path[: i + 1] + list(vertex_pair) + path[i + 1 :]


def incorporateSpursInZigZag(
    path: list[tuple[int, ...]],
    vertices: list[tuple[int, ...]],
    spur_suffixes: list[tuple[int, ...]],
) -> list[tuple[int, ...]]:
    """
    Incorporates a list of spurs in a zigzag path.
    @param path: list of vertices, a zigzag path
    @param vertices: list of vertices to incorporate
    @param spur_suffixes: list of spur suffixes (suffixes for the vertices variable)
    @return: list of vertices, the zigzag path with the spurs incorporated
    """
    C = [stut + suff for stut in vertices for suff in spur_suffixes]
    for vertex_index in range(0, len(C), 2):
        path = incorporateSpurInZigZag(path, (C[vertex_index], C[vertex_index + 1]))
    return path


def createSquareTube(path: list[tuple], u: tuple, v: tuple) -> list[tuple[int, ...]]:
    """
    Creates a square tube from a path by appending combinations of `u` and `v` like so:
    `uu, uv, vv, vu, vu, vv, uv, uu` and ending with `uu, uv, vv, vu, vu, uu, uv, vv`
    @param path: list of vertices, a path
    @param u: tuple to append
    @param v: tuple adjacent to u to append
    @return: list of vertices, the square tube. Every vertex in the original path is repeated 4 times.
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


def get_transformer(s: list[int], func: callable) -> tuple[list[int], list[int]]:
    """
    Sorts the signature using a given function and provides array to transform it back
    @param s: signature as a list of integers
    @param func: lambda function of tuples of form (value, index) to sort the signature
    @return: tuple of two lists of integers;
        the first list is the sorted signature,
        the second list is the transformation array (used in `tranform`)
    """
    if len(s) == 0:
        return [], []
    elif any(s_i < 0 for s_i in s):
        raise ValueError("Signature must be a list of non-negative integers.")
    elif not callable(func):
        raise ValueError("Function must be callable.")
    # index the numbers in the signature such that we can transform them back later
    indexed_sig = [(value, idx) for idx, value in enumerate(s)]
    # put the odd numbers first in the signature
    indexed_sig.sort(reverse=True, key=func)
    return [x[0] for x in indexed_sig if x[0] != 0], [x[1] for x in indexed_sig]


def transform(lis: list[tuple[int, ...]], tr: list[int]) -> list[tuple[int, ...]]:
    """
    Transforms a list of permutations as tuples according to the given renaming.
    @param lis: list of permutations
    @param tr: transformation list, int at index i is the new name for i
    @return: list of lists of transformed permutations
    """
    l = []
    for i in lis:
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


def transform_cycle_cover(
    lis3d: list[list[tuple[int, ...]]], tr: list[int]
) -> list[list[tuple[int, ...]]]:
    """
    Transforms a list of unknown depth holding a list of permutations according to the given renaming. Used for the cycle cover.
    @param lis: list of lists of permutations
    @param tr: transformation list, int at index i is the new name for i
    @return: list of lists of transformed permutations
    """
    assert len(lis3d) > 0
    if isinstance(lis3d[0][0][0], int):
        return [transform(l, tr) for l in lis3d]
    elif not isinstance(lis3d, list):
        raise ValueError("The input is not a list")
    else:
        return [transform_cycle_cover(l, tr) for l in lis3d]


def recursive_cycle_check(cycle, total_length=0) -> int:
    """
    Recursively check whether the given list is a cycle.
    @param cycle: list of cycles
    @param total_length: total length of the cycle, starts at 0.
    @return: total length of the list of cycles
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
