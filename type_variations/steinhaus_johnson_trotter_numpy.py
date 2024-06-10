# From https://www.geeksforgeeks.org/johnson-trotter-algorithm/
# This Code is Contributed by Prasad Kandekar(prasad264)
import numpy as np


class SteinhausJohnsonTrotter:
    LEFT_TO_RIGHT = True
    RIGHT_TO_LEFT = False

    def searchArr(self, a: np.ndarray, n: int, mobile: int) -> int:
        return np.where(a == mobile)[0][0] + 1

    def fact(self, n: int) -> int:
        return np.math.factorial(n)

    def getMobile(self, a: np.ndarray, dir: np.ndarray, n: int) -> int:
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

    def printOnePerm(self, a: np.ndarray, dir: np.ndarray, n: int) -> None:
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

        for i in range(n):
            print(a[i], end="")
        print("")

    def printPermutation(self, n: int) -> None:
        a = np.arange(n)
        dir = np.full(n, self.RIGHT_TO_LEFT)

        for i in range(n):
            print(a[i], end="")
        print("")

        for i in range(1, self.fact(n)):
            self.printOnePerm(a, dir, n)

    def get_sjt_permutations(self, n: int) -> np.ndarray:
        perms = np.empty((0, n), dtype=int)
        a = np.arange(n)
        perms = np.vstack((perms, a.copy()))
        dir = np.full(n, self.RIGHT_TO_LEFT)

        for i in range(1, self.fact(n)):
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

            perms = np.vstack((perms, a.copy()))
        return perms