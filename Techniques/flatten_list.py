
def flatten1(S):
    """Flattening a list recursively from http://stackoverflow.com/questions/12472338/flattening-a-list-recursively"""
    if len(S) == 0:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])


def flatten(S):
    """Flattening a list recursively from http://stackoverflow.com/questions/12472338/flattening-a-list-recursively"""
    flatten=lambda l: sum(map(flatten,l),[]) if isinstance(l, list) else [l]
    return flatten(S)