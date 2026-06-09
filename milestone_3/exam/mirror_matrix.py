def reverseMatrix(s: list) -> list:
    res = []
    for val in s[::-1]:
        res.append(val[::-1])
    return res


if __name__ == "__main__":
    print(reverseMatrix([[1, 2], [3, 4]]))                   # → [[4, 3], [2, 1]]
    print(reverseMatrix([[1, 2, 3], [4, 5, 6]]))             # → [[6, 5, 4], [3, 2, 1]]
    print(reverseMatrix([[1, 2, 3, 4]]))                     # → [[4, 3, 2, 1]]
    print(reverseMatrix([[1], [2], [3]]))                    # → [[3], [2], [1]]
    print(reverseMatrix([[1]]))                              # → [[1]]
    print(reverseMatrix([]))                                 # → []
    print(reverseMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))  # → [[9,8,7],[6,5,4],[3,2,1]]