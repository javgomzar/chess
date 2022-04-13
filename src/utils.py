
def extract(l: list):
    if len(l) == 0:
        return None
    elif len(l) > 1:
        raise Exception("")
    else:
        return l[0] 

def sign(n: int) -> int:
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0