def sculptor(text: str) -> str:
    res = ""
    upper = -1
    for c in text:
        if c.isalpha():
            if upper > 0:
                nc = c.upper()
            else: 
                nc = c.lower()
            upper = -upper
            res += nc
        else:
            res += c
    return res


if __name__ == "__main__":
    print((sculptor("Hello world")))    # → "hElLo WoRlD"
    print(sculptor("Hello, world!"))  # → "hElLo, WoRlD!"
    print(sculptor("123abcDEF"))      # → "123aBcDeF"
    print(sculptor("a-bC-dEf-ghIj"))  # → "a-Bc-DeF-gHiJ"
    print(sculptor(""))               # → ""
    print(sculptor("12345"))          # → "12345"
    print(sculptor("A"))              # → "a"
    print(sculptor("ab"))             # → "aB"
