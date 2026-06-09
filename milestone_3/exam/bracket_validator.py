def bracket_validator(s: str) -> bool:
    stack = []
    for i in s:
        if i in "([{":
            stack.append(i)
        elif i in ")]}":
            if not stack:
                return False
            last = stack.pop()
            if (i == ')' and last != '(') or (i == '}' and last != '{') or (i == ']' and last != '['):
                    return False
    return not stack


if __name__ == "__main__":
    print(bracket_validator("()"))                              # → True
    print(bracket_validator("()[]{}"))                          # → True
    print(bracket_validator("{[()]}"))                          # → True
    print(bracket_validator(""))                                # → True
    print(bracket_validator("hello(hhhh)world{ho}w are"))       # → True
    print(bracket_validator("(]"))                              # → False
    print(bracket_validator("([)]"))                            # → False
    print(bracket_validator("((("))                             # → False
    print(bracket_validator("())"))                             # → False
