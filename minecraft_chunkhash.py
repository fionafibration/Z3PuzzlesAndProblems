import z3
from arybo.lib import MBA
import PIL

x1, z1 = z3.BitVecs('x1 z1', 64)

def chhash(x):
    #x *= 0x9E3779B97F4A7C15
    x ^= x >> 32
    x ^= (x >> 16)

    return x


def get_hashcode(x, z):
    i1 = 1664525 * x + 1013904223
    i2 = 1664525 * (z ^ -559038737) + 1013904223
    # return i1 ^ i2
    return i2


out = get_hashcode(x1, z1)

print(z3.simplify(out))

print(z3.simplify(z3.URem((2 ** 64) - 1, out)))

"""
mba = MBA(64)

h = mba.var('h')

x = mba.var('x')
z = mba.var('z')

hashed = get_hashcode(x, 0)

app = hashed.vectorial_decomp([x])

print(hashed)
print(app)
"""