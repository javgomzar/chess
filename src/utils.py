
def extract(l: list):
    if len(l) == 0:
        return None
    elif len(l) > 1:
        raise ValueError("argument must have length 1")
    else:
        return l[0] 

def sign(n: int) -> int:
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0

def uniform_distance(a: tuple[int], b: tuple[int]) -> int:
    if len(a) != len(b):
        raise ValueError("arguments must have same length")

    n = len(a)
    return max([abs(a[i] - b[i]) for i in range(0,n)])

def append_if_not_in(l: list, item) -> None:
    if item not in l:
        l.append(item)

def remove_empty(str_list: list[str]) -> str:
    return [text for text in str_list if text != '']
