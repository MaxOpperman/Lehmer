from abc import ABC
from collections.abc import Iterator


def swap_elements(a_list: list, i: int, j: int) -> None:
    """
    Swaps the elements at positions i and j in the given list.

    Args:
        a_list (list): The list in which the elements will be swapped.
        i (int): The index of the first element to be swapped.
        j (int): The index of the second element to be swapped.

    Returns:
        None: (the list is modified in place)
    """
    tmp = a_list[i]
    a_list[i] = a_list[j]
    a_list[j] = tmp


class SetPerm(Iterator, ABC):
    """
    This file is directly copied from the original source code of the article:
    "Multiset permutation generation by transpositions" by Rivertz
    The original source code is available at: https://doi.org/10.48550/arXiv.2309.11781

    Therefore we also did not test or document this file as it is not part of our codebase.

    References:
        - Hans Jakob Rivertz. Multiset permutation generation by transpositions. 9 2023
    """

    def __init__(self, multiplicity):
        self.m = multiplicity
        self.k = len(multiplicity)
        self.P = []
        for i in range(self.k):
            self.P += [i + 1] * multiplicity[i]
        self.n = len(self.P)
        self.D = [1] * self.n
        self.T = 0  # No active element type

    def __next__(self):
        if self.T == 0:
            self.T = 1
            return self.P.copy()
        else:
            return self.one_step(self.n).copy()

    def swap(self, i, j, df):
        swap_elements(self.P, i, j)
        swap_elements(self.D, i, j)
        for k in range(i + df, j, df):
            self.D[k] = 1
        self.T = 1

    def one_step(self, n):
        d = -1  # One iteration of the algorithm
        T = self.T
        for i in range(n - 1, -1, -1):
            if self.P[i] == T:
                d = i
                break
        df = self.D[d]
        j = d + df
        if d > -1:
            while -1 < j < self.n:
                if self.P[j] != T or self.D[j] != df:
                    if self.P[j] > T:
                        self.swap(d, j, df)
                        return self.P
                    break
                j = j + df
            self.D[d] = -self.D[d]
            return self.one_step(d)
        else:  # No elements of type T can move!
            self.T = self.T + 1  # Next type!
            if self.T >= self.k:  # No elements can move.
                raise StopIteration  # Exit!
            return self.one_step(self.n)
