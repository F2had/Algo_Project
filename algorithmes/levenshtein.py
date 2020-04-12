import numpy as np


def levenshtein(query, locations):
    st = ""
    diff = -1
    for s in locations:
        size_x = len(query) + 1
        size_y = len(s) + 1
        matrix = np.zeros((size_x, size_y))

        for x in range(size_x):
            matrix[x, 0] = x
        for y in range(size_y):
            matrix[0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if query[x - 1] == s[y - 1]:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1],
                        matrix[x, y - 1] + 1
                    )
                else:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1] + 1,
                        matrix[x, y - 1] + 1
                    )
        tmp = matrix[size_x - 1, size_y - 1]
        if diff == -1:
            diff = tmp
            st = s
        elif tmp <= diff:
            diff = tmp
            st = s
        else:
            pass
    return st


location = ['str',  'pantai panorama','pantai hill park']
print(levenshtein('pantai panor', location))
