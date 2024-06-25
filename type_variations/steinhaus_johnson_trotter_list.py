# From https://www.geeksforgeeks.org/johnson-trotter-algorithm/
# This Code is Contributed by Prasad Kandekar(prasad264)

import math


class SteinhausJohnsonTrotterList:
    # Python program to print all permutations
    # using Johnson and Trotter algorithm.
    LEFT_TO_RIGHT = True
    RIGHT_TO_LEFT = False

    # Utility functions for finding the
    # position of largest mobile integer in a[].
    def searchArr(self, a, n, mobile):
        for i in range(n):
            if a[i] == mobile:
                return i + 1

    # To carry out step 1 of the algorithm i.e.
    # to find the largest mobile integer.
    def getMobile(self, a, dir, n):
        mobile_prev = 0
        mobile = 0
        for i in range(n):
            # direction 0 represents RIGHT TO LEFT.
            if dir[a[i] - 1] == self.RIGHT_TO_LEFT and i != 0:
                if a[i] > a[i - 1] and a[i] > mobile_prev:
                    mobile = a[i]
                    mobile_prev = mobile
            # direction 1 represents LEFT TO RIGHT.
            if dir[a[i] - 1] == self.LEFT_TO_RIGHT and i != n - 1:
                if a[i] > a[i + 1] and a[i] > mobile_prev:
                    mobile = a[i]
                    mobile_prev = mobile
        if mobile == 0 and mobile_prev == 0:
            return 0
        else:
            return mobile

    def get_sjt_permutations(self, n: int) -> list[list[int]]:
        """
        Generate permutations using the Steinhaus-Johnson-Trotter algorithm.

        Args:
            n (int): The number of elements in the permutation.

        Returns:
            list: A list of permutations generated using the Steinhaus-Johnson-Trotter algorithm.
        """
        perms = []
        a = [i for i in range(n)]
        perms.append(a.copy())
        dir = [self.RIGHT_TO_LEFT for i in range(n)]

        for i in range(1, math.factorial(n)):
            mobile = self.getMobile(a, dir, n)
            pos = self.searchArr(a, n, mobile)

            if dir[a[pos - 1] - 1] == self.RIGHT_TO_LEFT:
                a[pos - 1], a[pos - 2] = a[pos - 2], a[pos - 1]

            elif dir[a[pos - 1] - 1] == self.LEFT_TO_RIGHT:
                a[pos], a[pos - 1] = a[pos - 1], a[pos]

            for i in range(n):
                if a[i] > mobile:
                    if dir[a[i] - 1] == self.LEFT_TO_RIGHT:
                        dir[a[i] - 1] = self.RIGHT_TO_LEFT
                    elif dir[a[i] - 1] == self.RIGHT_TO_LEFT:
                        dir[a[i] - 1] = self.LEFT_TO_RIGHT

            perms.append(a.copy())
        return perms
