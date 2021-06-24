class 我:
    def __init__(self, n=None):
        self.n = n
        self.depth = 0


def 非(a):
    h = 我()
    h.depth = a
    return h


def 常(a):
    return a.depth


def 需(a):
    return a


def 要(a, b):
    h = 我()
    h.depth = a.depth + b.depth
    return h


def 放(a, b):
    h = 我()
    h.depth = a.depth - b.depth
    return h


def 屁(a, b):
    h = 我()
    h.depth = a.depth * b.depth
    return h


def 然(a, b):
    h = 我()
    h.depth = a.depth % b.depth
    return h


def 後(a, b):
    h = 我()
    h.depth = pow(a.depth, b.depth)
    return h


def 睡(a, b, m):
    h = 我()
    h.depth = pow(a.depth, b.depth, m.depth)
    return h


def 覺(n):
    print(chr(常(n)), end="", flush=True)

