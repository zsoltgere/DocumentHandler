#  -*- coding: utf-8 -*-

from numpy import zeros, inf
import time


class Utils:
    """
        The origin of the following three function and the comments is: https://github.com/nltk/nltk/blob/develop/nltk/metrics/distance.py
        It has edited slightly to fit only the requirements of this program.
        Distance Metrics.
        Compute the distance between two items (usually strings).
        As metrics, they must satisfy the following three requirements:
        1. d(a, a) = 0
        2. d(a, b) >= 0
        3. d(a, c) <= d(a, b) + d(b, c)
    """
    def _edit_dist_init(len1, len2):
        lev = []
        for i in range(len1):
            lev.append([0] * len2)  # initialize 2D array to zero
        for i in range(len1):
            lev[i][0] = i           # column 0: 0,1,2,3,4,...
        for j in range(len2):
            lev[0][j] = j           # row 0: 0,1,2,3,4,...
        return lev

    def _edit_dist_step(lev, i, j, s1, s2):
        c1 = s1[i - 1]
        c2 = s2[j - 1]

        a = lev[i - 1][j] + 1
        b = lev[i][j - 1] + 1

        c = lev[i - 1][j - 1] + (1 if c1 != c2 else 0)

        d = c + 1

        lev[i][j] = min(a, b, c, d)

    def edit_distance(s1, s2):
        """
        Calculate the Levenshtein edit-distance between two strings.
        The edit distance is the number of characters that need to be
        substituted, inserted, or deleted, to transform s1 into s2.  For
        example, transforming "rain" to "shine" requires three steps,
        consisting of two substitutions and one insertion:
        "rain" -> "sain" -> "shin" -> "shine".  These operations could have
        been done in other orders, but at least three steps are needed.

        Allows specifying the cost of substitution edits (e.g., "a" -> "b"),
        because sometimes it makes sense to assign greater penalties to substitutions.

        This also optionally allows transposition edits (e.g., "ab" -> "ba"),
        though this is disabled by default.

        :param s1, s2: The strings to be analysed
        :type s1: str
        :type s2: str
        """
        len1 = len(s1)
        len2 = len(s2)
        lev = Utils._edit_dist_init(len1 + 1, len2 + 1)

        for i in range(len1):
            for j in range(len2):
                Utils._edit_dist_step(lev, i + 1, j + 1, s1, s2)

        return lev[len1][len2]

    def dtw(x, y):
        """
            Computes Dynamic Time Warping (DTW) of two sequences.
            The origin of this function is: https://github.com/pierre-rouanet/dtw/blob/master/dtw.py
            It has edited to fit only the requirements of this program.
            :param array x: N1*M array
            :param array y: N2*M array
            Returns the cost matrix
        """
        assert len(x)
        assert len(y)
        r, c = len(x), len(y)
        D0 = zeros((r + 1, c + 1))
        D0[0, 1:] = inf
        D0[1:, 0] = inf
        D1 = D0[1:, 1:]

        for i in range(r):
            for j in range(c):
                D1[i, j] = Utils.edit_distance(x[i], y[j])

        return D1

# tool to measure execution time
class ExecutionMeter():

    def __init__(self):
        self.start()

    # start the watch
    def start(self):
        self.startime = time.time()

    # stop the watch, and return the elapsed time in formatted string
    def stop(self):
        return ("--- %s seconds ---" % (time.time() - self.startime))

# costum exception class
class DocumentHandlerException(Exception):
    # constructor
    def __init__(self, value):
        self.value = value

    # return the string representation of self.value
    def __str__(self):
        return repr(self.value)

def getTime():
    return time.strftime("%Y-%m-%dT%H:%M:%S")