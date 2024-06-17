import numpy as np


def adjacent(s, t):
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


def pathQ(p: list[tuple], verbose=True):
    """Returns True if p a path.
    :param verbose: whether the error in the path should be printed in console
    :param p, list of vertices
    :return: true if p is a path
    """
    for i, item in enumerate(p):
        if i < len(p) - 1 and not adjacent(item, p[i + 1]):
            if verbose:
                print(
                    f"No path: index {i}->{i+1}. See: {i-1}-{i}-{i+1}; {p[i-1]}-{item}-{p[i+1]}"
                )
            return False
    return True


def cycleQ(c):
    """Returns True if c a cycle."""
    if len(c) <= 2:
        return False
    for i, item in enumerate(c):
        if not adjacent(item, c[(i + 1) % len(c)]):
            return False
    return True


def pathEdges(p):
    """Returns a list of edges of a path. (Path is given as a list of adjacent vertices)"""
    return [[item, p[i + 1]] for i, item in enumerate(p) if i < len(p) - 1]


def stichPaths(p1, p2):
    """Stitches two parallel paths by gluing the end vertices."""
    if adjacent(p1[-1], p2[0]):
        return p1 + p2
    elif adjacent(p1[0], p2[-1]):
        return p2 + p1
    elif adjacent(p1[-1], p2[-1]):
        return p1 + list(reversed(p2))
    elif adjacent(p1[0], p2[0]):
        return list(reversed(p1)) + p2
    return False


def splitPathIn2(
    p: list[tuple[int, ...]], a: tuple[int, ...]
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """Splits a path at vertex a. Element a appears in only the first path."""
    assert len(p) > 1
    A = p.index(a)
    return p[: A + 1], p[A + 1 :]


def cutCycle(c, a):
    """Splits a cycle at vertex a. Vertex a appears on first place"""
    if len(c) == 1 and a in c:
        return c
    try:
        assert a in c
    except AssertionError as err:
        print(f"{repr(err)} cycle: {c}, should be cut to {a}")
        quit()
    # if the array is a numpy array, use numpy functions
    if isinstance(c, np.ndarray):
        # check whether a is in c
        if not np.any(np.all(c == a, axis=1)):
            print(f"Vertex {a} not in numpy cycle {c}")
            quit()
        index = np.where(np.all(c == a, axis=1))[0][0]
        return np.roll(c, -index, axis=0)
    # if the array is a list, use list functions (index instead of where)
    A = c.index(a)
    return c[A:] + c[:A]


def spurBaseIndex(path, vertex):
    """Determines index of base of spur for given path and spur tip."""
    for i, item in enumerate(path):
        if neighbor(item, vertex):
            return i
    return False


def neighbor(p, q):
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


def incorporateSpur(path, vertex, edges):
    """Incorporates spur into path. Returns False if spur cannot be incorporated (no adjacent vertex available)."""
    b = spurBaseIndex(path, vertex, edges)
    if not b:
        return False
    return path[: b + 1] + [vertex] + path[b:]


def incorporateSpurs(path, vertices, edges):
    """Incorporates multiple spurs into path."""
    for i in vertices:
        a = incorporateSpur(path, i, edges)
        path = a
    return path


def mul(sez, e):
    """Adds 'e' to all elements(lists) in list sez"""
    if not sez:
        return [e]
    for i, el in enumerate(sez):
        sez[i] = el + (e,)
    return sez


def createZigZagPathE(c, d):
    """c and d are the same cycles/paths. both are needed
    because mul(c, 0) changes te cycle c, so if you do mul(
    c, 1) you get mul(c, 01). This alg returns edges of a path"""
    c0 = pathEdges(mul(c, 0))
    c1 = pathEdges(mul(d, 1))
    C = []
    for i, item in enumerate(c0):
        if i % 2 == 0:
            C.append(item)
            C.append([item[1], c1[i][1]])
        if i % 2 == 1:
            C.append(c1[i])
            C.append([c1[i][1], item[1]])
    C.append([c1[-1][1], c1[0][0]])
    C.append([c1[0][0], c0[0][0]])
    return C


def createZigZagPath(
    c: list[tuple[int, ...]], u: tuple[int, ...], v: tuple[int, ...]
) -> list[tuple[int, ...]]:
    """
    :param c: cycle of even length, list of tuples
    :param u: tuple to append
    :param v: tuple to append
    :return: cycle obtained by combining two "parallel" copies of given cycle, to form a 'square wave',
            running from cycle[[1]]v to cycle[[-1]]v; the two copies are distinguished by
            appending u and v; also works for a path
    """
    assert adjacent(u, v)
    temp = [item for sublist in zip(c, c) for item in sublist]
    module = [u, v, v, u]
    return [item + module[i % 4] for i, item in enumerate(temp)]


def incorporateSpurInZigZag(path, vertex_pair) -> list[tuple[int, ...]]:
    # Modify path to remove last e elements except for the first one
    i = spurBaseIndex(path, vertex_pair[0])
    return path[: i + 1] + vertex_pair + path[i + 1 :]


def incorporateSpursInZigZag(path, vertices, spur_suffixes) -> list[tuple[int, ...]]:
    C = [stut + suff for stut in vertices for suff in spur_suffixes]
    for vertex_index in range(0, len(C), 2):
        path = incorporateSpurInZigZag(path, [C[vertex_index], C[vertex_index + 1]])
    return path


def createSquareTube(path: list[tuple], u: tuple, v: tuple) -> list[tuple[int, ...]]:
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


def parallelEdgesQ(e1, e2, edges):
    """e1, e2 edges, edges a list of edges (in graph),
    returns True if in edges exist edges f1, f2 st e1, f1, e2, f2 form a 4-cycle"""
    p = 1
    r = 1
    if e1[0] == e2[0] or e1[0] == e2[1] or e1[1] == e2[0] or e1[1] == e2[1]:
        return False

    for i in edges:
        if i == [e1[0], e2[1]] or i == [e2[1], e1[0]]:
            p *= 2
        elif i == [e1[1], e2[0]] or i == [e2[0], e1[1]]:
            p *= 3
        if i == [e1[0], e2[0]] or i == [e2[0], e1[0]]:
            r *= 2
        elif i == [e1[1], e2[1]] or i == [e2[1], e1[1]]:
            r *= 3

    if p == 6 or r == 6:
        return True
    return False


def parallelEdges(edges):
    """Returns a list of parallel edges."""
    P = []
    for i, item in enumerate(edges):
        for j in edges[i:]:
            if parallelEdgesQ(item, j, edges):
                P.append([item, j])
    return P


def transform(lis: list[tuple[int, ...]], tr: list[int]) -> list[tuple[int, ...]]:
    """
    Transforms the permutation(s) according to the given renaming.
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
                return "list of transformations is too short"
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
    if isinstance(lis3d[0][0][0], int):
        return [transform(l, tr) for l in lis3d]
    elif not isinstance(lis3d, list):
        raise ValueError("The input is not a list")
    else:
        return [transform_cycle_cover(l, tr) for l in lis3d]


def conditionHpath(sig):
    """Condition for existence of Hamiltonian path on all permutations of the given signature."""
    sig = [i for i in sig if i != 0]
    if len(sig) == 1:
        return True
    if len(sig) == 2 and sig[0] == 1 or sig[1] == 1:
        return True
    st = 0
    for i in sig:
        if i % 2 == 1:
            st += 1
    if st >= 2:
        return True
    return False


def recursive_cycle_check(cycle, total_length=0) -> int:
    """
    Recursively check whether the given list is a cycle.
    @param cycle: list of cycles
    @param total_length: total length of the cycle, starts at 0.
    @return: total length of the list of cycles
    """
    assert isinstance(cycle, list)
    if isinstance(cycle[0][0], int):
        assert cycleQ(cycle)
        assert len(cycle) == len(set(cycle))
        total_length += len(cycle)
    else:
        for sub_cycle in cycle:
            total_length = recursive_cycle_check(sub_cycle, total_length)
    return total_length
