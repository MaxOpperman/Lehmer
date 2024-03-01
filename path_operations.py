def adjacent(s, t):
    """"returns true if s and t adjacent, false otherwise"""
    if len(s) != len(t):
        return False
    diff = [i for i, (a, b) in enumerate(zip(s, t)) if a != b]
    return len(diff) == 2 and diff[0] + 1 == diff[1] and s[diff[0]] == t[diff[1]] and s[diff[1]] == t[diff[0]]


def pathQ(p):
    """Returns True if p a path.
    :param p, list of vertices
    :return: true if p is a path
    """
    for i, item in enumerate(p):
        if i < len(p) - 1 and not adjacent(item, p[i + 1]):
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
    """Stiches two parallel paths by gluing the end vertices."""
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
    """Splits a path at vertex a. Element a appers in both paths."""
    A = p.index(a)
    if len(p) == 1:
        return p
    return [p[:A + 1], p[A:]]


def cutCycle(c, a):
    """Splits a cycle at vertex a. Vertex a appears on first place """
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
    for i in sez:
        i.append(e)
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


def createZigZagPath(c, d):
    """c and d are the same cycles. both are needed because
     mul(c, 0) changes te cycle c, so if you do mul(c, 1) you get mul(c, 01). This alg returns path."""

    c0 = pathEdges(mul(c, 0))
    c1 = pathEdges(mul(d, 1))
    C = []
    for i, item in enumerate(c0):
        if i % 2 == 0:
            C.extend(item)
        if i % 2 == 1:
            C.extend(c1[i])
    C.append(c1[-1][1])
    C.append(c1[0][0])
    return C


def incorporateSpurInZigZag(c, d, s, ss, edges0):
    """c and d are the same cycles. both are needed because
     mul(c, 0) changes te cycle c, so if you do mul(c, 1) you get mul(c, 01)"""
    sp = 2 * spurBaseIndex(c, s[0], edges0)
    C = createZigZagPath(c, d)
    C = C[:sp] + mul(s, 0) + mul(ss, 1) + C[sp:]
    return C


def incorporateSpursInZigZag(c, d, s, ss, edges):
    C = createZigZagPath(c, d)
    e = [mul(i, 0) for i in edges]
    for i, item in enumerate(s):
        sp = spurBaseIndex(c, mul(item, 0)[0], e)
        c = c[:sp] + ss[i] + c[sp:]
        C = C[:sp * 2] + s[i] + mul(ss[i], 1) + C[sp * 2:]

    return C


def createSquareTube(p, q, r, s):
    p00 = mul(mul(p, 0), 0)
    p10 = mul(mul(r, 1), 0)
    p01 = mul(mul(q, 0), 1)
    p11 = mul(mul(s, 1), 1)

    P = []
    P.extend([p00[0], p10[0], p01[0], p11[0], p11[1]])
    for i, item in enumerate(p00):
        if i + 1 < len(p00):
            if i % 2 == 0 and i > 0:
                P.extend([p10[i], p00[i], p11[i], p11[i + 1]])
            elif i % 2 == 1:
                P.extend([p00[i], p10[i], p01[i], p01[i + 1]])
        else:
            P.extend([p00[i], p10[i], p01[i]])
            # Paths have to be of even length so this is not needed, but if you would want a square tube of paths of odd length this might be useful
            # if i%2 == 0 :
            #    P.extend([p10[i], p00[i], p11[i]])
            # elif i%2 ==1:
            #    P.extend([p00[i], p10[i], p01[i]])
    return P


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
