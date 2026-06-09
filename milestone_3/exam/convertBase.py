def convert_base(num: str, from_base: int, to_base: int) -> str:
    if from_base < 2 or from_base > 36 or to_base < 2 or to_base > 36:
        return "ERROR"
    base = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    try:
        n = int(num, from_base)
        res = ""
        if n == 0:
            return "0"
        while n > 0:
            res += base[n % to_base]
            n //= to_base
        return res[::-1]
    except Exception:
        return "ERROR"


if __name__ == "__main__":
    print(convert_base("1010", 2, 10))          # → "10"
    print(convert_base("10", 10, 2))            # → "1010"
    print(convert_base("1A", 16, 10))           # → "26"
    print(convert_base("26", 10, 16))           # → "1A"
    print(convert_base("ZZZ", 36, 10))          # → "46655"
    print(convert_base("0", 10, 2))             # → "0"
    print(convert_base("000", 2, 10))           # → "0"
    print(convert_base("2", 2, 10))             # → "ERROR"
    print(convert_base("G", 16, 10))            # → "ERROR"
    