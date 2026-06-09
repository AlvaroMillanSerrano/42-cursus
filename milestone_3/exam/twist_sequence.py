def twister(nums: list, n: int) -> list:
    if not nums:
        return []
    n = n % len(nums)
    return nums[-n:] + nums[:-n]


if __name__ == "__main__":
    print(twister([1, 2, 3, 4, 5], 2))      # [4, 5, 1, 2, 3]
    print(twister([4, 2, 1, -1, 'a'], 4))   # [2, 1, -1, 'a', 4]
    print(twister([1, 2, 3], 3))            # [1, 2, 3]
    print(twister([1, 2, 3], 5))            # [2, 3, 1]
    print(twister([1, 2, 3, 4], -1))        # [2, 3, 4, 1]
    print(twister([], 3))                   # []
    print(twister([1], 10))                 # [1]