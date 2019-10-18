from z3 import *


s = Solver()

values = [[Int(f's_{x}_{y}') for y in range(9)] for x in range(9)]

problem = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

assert(len(problem) == 81)



for y in range(9):
    for x in range(9):

        # Index out of our problem string
        val = problem[x + 9 * y]

        # Constrain range
        if val in '123456789':
            s.add(values[x][y] == int(val))

        else:
            s.add(And(values[x][y] <= 9, values[x][y] >= 1))



# Rows must have unique values
for row in range(9):
    s.add(Distinct(
        [values[col][row] for col in range(9)]
    ))

# Same with columns
for col in range(9):
    s.add(Distinct(
        [values[col][row] for row in range(9)]
    ))

# Constrain boxes
# x, y are the upper left corner of each box
# and we then add every pair of (0, 1, 2) to them
# to get the full box
for x in range(0, 9, 3):
    for y in range(0, 9, 3):
        s.add(Distinct(
            [values[x + i][y + j] for i in range(3) for j in range(3)]
        ))


solutions = 0

while s.check() == sat:

    # Pretty print solution
    for y in range(9):
        for x in range(9):

            print('%s ' % s.model()[values[x][y]], end='')


            # Vertical box seperatators!
            if x in [2, 5]:
                print('| ', end='')

        print()
        if y in [2, 5]:
            print('------+-------+------')

    print()

    s.add(Or([values[x][y] != s.model()[values[x][y]] for x in range(9) for y in range(9)]))

    solutions += 1

if (solutions > 0):
    print('Found %s solutions!' % solutions)

else:
    print('Found no solutions!')