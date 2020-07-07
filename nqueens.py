from z3 import *

N = 12

UNICODE = True

s = Solver()

# Stores the file (x) of the queen for each rank (y)
board = [Int('q_%s' % y) for y in range(N)]

# Queens have to be within the chessboard's bounds
for x in range(N):
    s.add(0 <= board[x], board[x] <= (N - 1))

# Queens cannot share the same file
s.add(Distinct(board))


def zabs(x):
    return If(x >= 0, x, -x)

for i in range(N):
    for j in range(N):
        if i == j:
            continue

        s.add(And(
            board[i] - board[j] != i - j,
            board[i] - board[j] != j - i
        ))


solutions = 0

while s.check() == sat:

    for y in range(N):
        col = s.model()[board[y]].as_long()

        print('. ' * col, end='')

        if UNICODE:
            print("♕ ", end='')
        else:
            print("@ ", end='')

        print('. ' * (N - col - 1))

    print('\n')

    s.add(Or(
        [board[i] != s.model()[board[i]] for i in range(N)]
    ))

    solutions += 1

if (solutions > 0):
    print('Found %s solutions!' % solutions)

else:
    print('Found no solutions!')