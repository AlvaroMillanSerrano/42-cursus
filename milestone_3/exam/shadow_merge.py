def mergeList(list1: list, list2: list) -> list:
    res = []
    if list1:
        for element in list1:
            res.append(element)
    if list2:
        for element in list2:
            res.append(element)
    return sorted(res)


if __name__ == "__main__":
    print(mergeList([1, 3, 5, -1], [0, 8, 2, 1]))       # → [-1, 0, 1, 1, 2, 3, 5, 8]
    print(mergeList([99, -22, 10, 9], []))              # → [-22, 9, 10, 99]
    print(mergeList(None, [5, 3, 1]))                   # → [1, 3, 5]
    print(mergeList([7, 6, 8], None))                   # → [6, 7, 8]
    print(mergeList([], []))                            # → []
    print(mergeList([1, 1, 1], [1, 1]))                 # → [1, 1, 1, 1, 1]
    print(mergeList([-5, -2], [-3, -1]))                # → [-5, -3, -2, -1]