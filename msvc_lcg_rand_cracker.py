from z3 import *
import random

"""
MSVC rand():

state := 1 or srand() value
fun rand:
{
    state := (state * 214013) + 2531011
    return (state / >> 16) % 0x7fff
}
"""

# Size of int in platform
INTSIZE = 32

INTMAX = 2 ** INTSIZE - 1

CIntSort = lambda name: BitVec(name, INTSIZE)

# Randmax value
RANDMAX = 0x7fff

A, B = 214013, 2531011


class SimulatedRand:
    def __init__(self, seed = None):
        self.mask = 2 ** INTSIZE - 1

        if seed is not None:
            self.state = seed
        else:
            self.state = random.randrange(2 ** 32)

    def next(self):
        self.state = (self.state * A) & self.mask
        self.state = (self.state + B) & self.mask
        return (self.state >> 16) & RANDMAX

    def __repr__(self):
        return "SimulatedRand(%s)" % self.state


def find_seed(known: list, modulus: int = 100, minimize=False):
    num_states = len(known)

    states = [CIntSort("state_%s" % i) for i in range(1, num_states + 2)]

    seed_sym = CIntSort("seed_sym")

    s = Solver()

    for i in range(1, num_states + 1):
        s.add(states[i] == states[i - 1] * A + B)

    for i in range(num_states):
        s.add(known[i] == URem((states[i] >> 16) & RANDMAX, modulus))

    s.add(states[0] == seed_sym * A + B)

    possible_seeds = []

    seed_count = 0

    while s.check() == sat:
        seed = s.model()[seed_sym].as_long()

        possible_seeds.append(seed)

        if minimize:
            s.add(seed_sym < seed)
        else:
            s.add(seed_sym != seed)

        seed_count += 1
        print("Found seed: %s" % seed)

        if seed_count >= 10:
            break

    if len(possible_seeds) == 0:
        print("No seeds found!")

    return possible_seeds


def predict_next(known: list, modulus: int = INTMAX, ):
    seeds = find_seed(known, modulus)

    next_values = []

    for seed in seeds:
        sim = SimulatedRand(seed)

        for i in range(len(known)):
            sim.next()

        next_values.append(sim.next() % modulus)

    next_probability = {}

    for value in set(next_values):
        next_probability[value] = next_values.count(value) / len(next_values)

    return next_probability, seeds


seeds = find_seed([69, 69, 69, 69], 100)

print(seeds)

# [3274879887, 3212450586, 1064966938, 1492443711, 3639927359, 3825194395, 1677710747, 1825747855, 3973231503, 3009546298]