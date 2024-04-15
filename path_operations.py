import copy
from typing import List, Tuple


def adjacent(s, t):
    """"returns true if s and t adjacent, false otherwise"""
    if len(s) != len(t):
        return False
    diff = [i for i, (a, b) in enumerate(zip(s, t)) if a != b]
    return len(diff) == 2 and diff[0] + 1 == diff[1] and s[diff[0]] == t[diff[1]] and s[diff[1]] == t[diff[0]]


def pathQ(p: List[tuple], verbose=True):
    """Returns True if p a path.
    :param verbose: whether the error in the path should be printed in console
    :param p, list of vertices
    :return: true if p is a path
    """
    for i, item in enumerate(p):
        if i < len(p) - 1 and not adjacent(item, p[i + 1]):
            if verbose:
                print(f"No path: index {i}->{i+1}. See: {i-1}-{i}-{i+1}; {p[i-1]}-{item}-{p[i+1]}")
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


def pathsEdges(paths):
    """Returns lists of edges of paths."""
    return [[item, p[i + 1]] for p in paths for i, item in enumerate(p) if i < len(p) - 1]


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


def splitPath(p, a):
    """Splits a path at vertex a. Element a appears in both paths."""
    A = p.index(a)
    if len(p) == 1:
        return p
    return [p[:A + 1], p[A:]]


def splitPathIn2(p: List[tuple], a: tuple) -> Tuple[List[tuple], List[tuple]]:
    """Splits a path at vertex a. Element a appears in only the first path."""
    assert len(p) > 1
    A = p.index(a)
    return p[:A+1], p[A+1:]


def cutCycle(c, a):
    """Splits a cycle at vertex a. Vertex a appears on first place """
    if len(c) == 1 and a in c:
        return c
    try:
        assert cycleQ(c)
    except AssertionError as err:
        print(f"{repr(err)} not a cycle: {c}, should be cut to {a}")
        quit()
    A = c.index(a)
    return c[A:] + c[:A]


def spurBaseIndex(path, vertex, edges):
    try:
        return [path.index(i[(i.index(vertex) + 1) % 2]) for i in edges if vertex in i][0]
    except IndexError:
        return False


def spur(path, vertex, edges):
    try:
        s = [i for i in edges if vertex in i and i[(i.index(vertex) + 1) % 2] in path][0]
        if s[0] == vertex:
            return [s[1], s[0]]
        return s
    except IndexError:
        return False


def spurs(path, vertices, edges):
    return [spur(path, i, edges) for i in vertices]


def incorporateSpur(path, vertex, edges):
    b = spurBaseIndex(path, vertex, edges)
    if not b:
        return False
    return path[:b + 1] + [vertex] + path[b:]


def incorporateSpurs(path, vertices, edges):
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


def createZigZagPath(c: List[tuple], u: tuple, v: tuple):
    """
    :param c: cycle of even length, list of tuples
    :param u: tuple to append
    :param v: tuple to append
    :return: cycle obtained by combining two "parallel" copies of given cycle, to form a 'square wave',
            running from cycle[[1]]v to cycle[[-1]]v; the two copies are distinguished by
            appending u and v; also works for a path
    """
    assert adjacent(u, v)
    module = [u, v, v, u]  # Define the module list
    result = []
    # Map over the temporary list and join each vertex with the corresponding element from the module list
    for i, item in enumerate(c):
        for suff in module:
            result.append(item + suff)
    return result


def incorporateSpurInZigZag(path, vertex, edgeQ, e):
    # Modify path to remove last e elements except for the first one
    modified_path = [x[:-e] if i != 0 else x for i, x in enumerate(path)]
    i = spurBaseIndex(path, vertex, edgeQ(modified_path))
    pair = path[i:i+2]  # Extract the 'vertical' edge
    return path[:i] + [vertex + pair[1][:-e]] + path[i+1:]


def incorporateSpursInZigZag(path, vertices, edgeQ, e):
    for vertex in vertices:
        path = incorporateSpurInZigZag(path, vertex, edgeQ, e)
    return path


def createSquareTube(path: List[tuple], u: tuple, v: tuple):
    # interleave the elements of the four copies of the path list
    temp = [item for sublist in zip(*([path]*4)) for item in sublist]
    uu = u + u
    uv = u + v
    vu = v + u
    vv = v + v
    module1 = [uu, uv, vv, vu, vu, vv, uv, uu]
    module2 = [uu, uv, vv, vu, vu, uu, uv, vv]

    # Combine the path with modules based on the index
    result = [item + module1[i % 8] for i, item in enumerate(temp[:-8])] +\
             [item + module2[i % 8] for i, item in enumerate(temp[-8:])]
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
