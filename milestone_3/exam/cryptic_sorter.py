def get_vowels(s: str):
        count = 0
        vowels = "aeiouAEIOU"
        for i in s:
            if i in vowels:
                count += 1
        return count


def cryptic_sorter(tlist: list) -> list:
    return sorted(tlist, key=lambda word: (
        get_vowels(word),
        len(word),
        word.lower()
    ))


if __name__ == "__main__":
    print(cryptic_sorter(["apple", "bat", "car", "ae", "b"]))  # → ['b', 'bat', 'car', 'ae', 'apple']
    print(cryptic_sorter(["dog", "cat", "hi", "a"]))           # → ['a', 'hi', 'cat', 'dog']
    print(cryptic_sorter(["bat", "cat", "ant"]))               # → ['ant', 'bat', 'cat']
    print(cryptic_sorter(["bbb", "ccc", "ddd"]))               # → ['bbb', 'ccc', 'ddd']
    print(cryptic_sorter([]))                                  # → []