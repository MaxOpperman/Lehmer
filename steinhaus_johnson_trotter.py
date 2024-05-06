# From https://www.geeksforgeeks.org/johnson-trotter-algorithm/
# This Code is Contributed by Prasad Kandekar(prasad264)

class SteinhausJohnsonTrotter:
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

    # To end the algorithm for efficiency it ends
    # at the factorial of n because number of
    # permutations possible is just n!.
    def fact(self, n):
        res = 1
        for i in range(1, n + 1):
            res = res * i
        return res

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

    # Prints a single permutation
    def printOnePerm(self, a, dir, n):
        mobile = self.getMobile(a, dir, n)
        pos = self.searchArr(a, n, mobile)

        # swapping the elements according to
        # the direction i.e. dir[]
        if dir[a[pos - 1] - 1] == self.RIGHT_TO_LEFT:
            a[pos - 1], a[pos - 2] = a[pos - 2], a[pos - 1]

        elif dir[a[pos - 1] - 1] == self.LEFT_TO_RIGHT:
            a[pos], a[pos - 1] = a[pos - 1], a[pos]

        # changing the directions for elements
        # greater than largest mobile integer
        for i in range(n):
            if a[i] > mobile:
                if dir[a[i] - 1] == self.LEFT_TO_RIGHT:
                    dir[a[i] - 1] = self.RIGHT_TO_LEFT
                elif dir[a[i] - 1] == self.RIGHT_TO_LEFT:
                    dir[a[i] - 1] = self.LEFT_TO_RIGHT

        for i in range(n):
            print(a[i], end='')
        print("")

    # This function mainly calls printOnePerm()
    # one by one to print all permutations.
    def printPermutation(self, n):
        # To store current permutation
        # storing the elements from 1 to n and
        a = [i for i in range(n)]

        # Printing the first permutation
        for i in range(n):
            print(a[i], end='')
        print("")

        # To store current directions
        # initially all directions are set
        # to RIGHT TO LEFT i.e. 0.
        dir = [self.RIGHT_TO_LEFT for i in range(n)]

        # for generating permutations in the order.
        for i in range(1, self.fact(n)):
            self.printOnePerm(a, dir, n)
    
    def get_sjt_permutations(self, n):
        """
        Generate permutations using the Steinhaus-Johnson-Trotter algorithm.

        Args:
            n (int): The number of elements in the permutation.

        Returns:
            list: A list of permutations generated using the Steinhaus-Johnson-Trotter algorithm.
        """
        perms = []
        a = [i for i in range(n)]
        perms.append(tuple(a.copy()))
        dir = [self.RIGHT_TO_LEFT for i in range(n)]

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

            perms.append(tuple(a.copy()))
        return perms
