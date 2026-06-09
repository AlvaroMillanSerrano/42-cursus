def isPalindrome(s: str) -> bool:
    p = ""
    for c in s:
        if s.isalnum():
            p += c
    return p == p[::-1]


if __name__ == "__main__":

    print(isPalindrome("madam"))                           # → True
    print(isPalindrome("racecar"))                         # → True
    print(isPalindrome("A man, a plan, a canal: Panama"))  # → True
    print(isPalindrome("No 'x' in Nixon"))                 # → True
    print(isPalindrome(""))                                # → True
    print(isPalindrome("hello"))                           # → False
    print(isPalindrome("12321"))                           # → True
    print(isPalindrome("12345"))                           # → False
    print(isPalindrome("Able was I ere I saw Elba"))       # → True