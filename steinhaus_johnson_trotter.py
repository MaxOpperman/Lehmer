import math


class SteinhausJohnsonTrotter:
    """
    Class representing the Steinhaus-Johnson-Trotter algorithm for generating permutations.

    The Steinhaus-Johnson-Trotter algorithm is an algorithm for generating all permutations of a given set of elements.

    References:
        - From https://www.geeksforgeeks.org/johnson-trotter-algorithm/. This Code is Contributed by Prasad Kandekar (prasad264).
        - Hugo Steinhaus. One Hundred Problems In Elementary Mathematics. Dover, New York, 1979.
        - Selmer M. Johnson. Iterative Solution of Linear Systems of Functional Equations. Technical Report 2, 1962.
        - H. F. Trotter. Algorithm 115: Perm. Communications of the ACM, 5(8):434-435, 8 1962
    """

    LEFT_TO_RIGHT = True
    """
    bool: The direction of the mobile element to move left to right.
    """
    RIGHT_TO_LEFT = False
    """
    bool: The direction of the mobile element to move right to left.
    """

    # Utility functions for finding the
    # position of largest mobile integer in a[].
    def searchArr(self, a, n, mobile):
        """
        Search for the given mobile element in the array.

        Args:
            a (list): The array to search in.
            n (int): The length of the array.
            mobile (int): The mobile element to search for.

        Returns:
            int: The index of the mobile element in the array, if found.

        Raises:
            ValueError: If the mobile element is not found in the array.
        """
        for i in range(n):
            if a[i] == mobile:
                return i + 1
        raise ValueError(f"Mobile element {mobile} not found in array {a}.")

    # To carry out step 1 of the algorithm i.e.
    # to find the largest mobile integer.
    def getMobile(self, a, dir, n):
        """
        Returns the largest mobile element in the given permutation.

        Args:
            a (list): The permutation of numbers.
            dir (list): The direction of each element in the permutation.
            n (int): The length of the permutation.

        Returns:
            int: The largest mobile element in the permutation.

        """
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

    def get_sjt_permutations(self, n):
        """
        Generate permutations using the Steinhaus-Johnson-Trotter algorithm.

        Args:
            n (int): The number of elements in the permutation.

        Returns:
            list: A list of permutations generated using the Steinhaus-Johnson-Trotter algorithm.
        """
        print(
            f"\033[1m\033[92mSTEINHAUS-JOHNSON-TROTTER USED FOR SIGNATURE {(1,) * n} \033[0m\033[0m"
        )
        perms = []
        a = [i for i in range(n)]
        perms.append(tuple(a.copy()))
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

            perms.append(tuple(a.copy()))
        return perms
