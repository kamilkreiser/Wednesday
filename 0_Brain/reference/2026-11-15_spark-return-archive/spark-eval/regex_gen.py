
import re as _re

def matches(pattern: str, text: str) -> bool:
    # Build a regex from the pattern, translating our syntax to Python's re
    # We need to handle: literals, '.', '*', '+', '?', '[abc]', '[a-z]', '[^abc]'
    # Quantifiers apply to the single preceding element.
    # We'll parse the pattern and construct a regex string.

    regex = _translate(pattern)
    return _re.fullmatch(regex, text) is not None

def _translate(pattern: str) -> str:
    result = []
    i = 0
    n = len(pattern)
    while i < n:
        c = pattern[i]
        if c == '\\':
            # Escape next character (literal)
            if i + 1 < n:
                result.append(_escape_literal(pattern[i+1]))
                i += 2
            else:
                # Trailing backslash: treat as literal backslash
                result.append(r'\\')
                i += 1
        elif c == '.':
            result.append('.')
            i += 1
        elif c == '*':
            # Quantifier: apply to previous element
            if not result:
                # Invalid: * at start, treat as literal
                result.append(r'\*')
            else:
                # Make previous element a group and add *
                # We need to ensure the previous element is a single unit.
                # We'll wrap the last element in a non-capturing group.
                # But since we only have single elements, we can just append '*'
                # However, if the previous element was a class, it's already a group.
                # For simplicity, we'll just append '*'
                result.append('*')
            i += 1
        elif c == '+':
            if not result:
                result.append(r'\+')
            else:
                result.append('+')
            i += 1
        elif c == '?':
            if not result:
                result.append(r'\?')
            else:
                result.append('?')
            i += 1
        elif c == '[':
            # Parse character class
            j = i + 1
            negate = False
            if j < n and pattern[j] == '^':
                negate = True
                j += 1
            # Find closing bracket
            class_content = []
            while j < n and pattern[j] != ']':
                if pattern[j] == '\\':
                    # Escape next char
                    if j + 1 < n:
                        class_content.append('\\' + pattern[j+1])
                        j += 2
                    else:
                        class_content.append('\\')
                        j += 1
                else:
                    class_content.append(pattern[j])
                    j += 1
            if j >= n:
                # No closing bracket: treat '[' as literal
                result.append(r'\[')
                i += 1
                continue
            # Build class string
            class_str = ''.join(class_content)
            if negate:
                result.append('[^' + class_str + ']')
            else:
                result.append('[' + class_str + ']')
            i = j + 1
        else:
            # Literal character
            result.append(_escape_literal(c))
            i += 1
    return ''.join(result)

def _escape_literal(ch: str) -> str:
    # Escape regex metacharacters except those we handle specially
    if ch in '.^$*+?{}[]\\|()':
        return '\\' + ch
    return ch
