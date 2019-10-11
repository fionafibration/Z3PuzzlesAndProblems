from math import sqrt
from functools import lru_cache, reduce
from collections import Counter
from itertools import product
from pprint import *
from collections import defaultdict

MUL = int.__mul__


def prime_factors(n):
    d = _divs(n)
    d = [] if d == [n] else (d[:-1] if d[-1] == d else d)
    pf = Counter(d)
    return dict(pf)


@lru_cache(maxsize=None)
def _divs(n):
    for i in range(2, int(sqrt(n) + 1)):
        d, m = divmod(n, i)
        if not m:
            return [i] + _divs(d)
    return [n]


def proper_divs(n):
    pf = prime_factors(n)
    pfactors, occurrences = pf.keys(), pf.values()
    multiplicities = product(*(range(oc + 1) for oc in occurrences))
    divs = {reduce(MUL, (pf ** m for pf, m in zip(pfactors, multis)), 1)
            for multis in multiplicities}
    try:
        divs.remove(n)
    except KeyError:
        pass
    return divs or ({1} if n != 1 else set())


divcount = defaultdict(lambda: [])

minfactors = {}

for i in range(1, 100000):
    divcount[len(proper_divs(i))].append(i)

for i in divcount.keys():
    minfactors[i] = min(divcount[i])

indices = list(minfactors.keys())

indices.sort(reverse=True)

best = 1000000000

bestnums = {}

for i in indices:
    if minfactors[i] < best:
        best = minfactors[i]
    else:
        minfactors[i] = best

for val in minfactors.values():
    bestnums[val] = len(proper_divs(val))

pprint(bestnums)