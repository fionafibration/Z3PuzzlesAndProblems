from math import ceil, log


def encode(num, depth):
    if num < 2048:
        return hex(num)
    return '(' + numconvert(num, depth + 1) + ')'


# Ben Kurtovic's bitshift conversion algorithm:
# https://benkurtovic.com/2014/06/01/obfuscating-hello-world.html
def numconvert(num, depth=0):
    result = ''
    while num:
        base = shift = 0
        diff = num
        span = int(ceil(log(-num if num < 0 else num, 1.1))) + (32 >> depth)
        for test_base in range(span):
            for test_shift in range(span):
                test_diff = (-num if num < 0 else num) - (test_base << test_shift)
                if (-test_diff if test_diff < 0 else test_diff) < (-diff if diff < 0 else diff):
                    diff = test_diff
                    base = test_base
                    shift = test_shift
        if result:
            result += ' + ' if num > 0 else ' - '
        elif num < 0:
            base = -base
        if shift == 0:
            result += encode(base, depth)
        else:
            result += '(%s << %s)' % (encode(base, depth),
                                      encode(shift, depth))
        num = diff if num > 0 else -diff
    return result


for num in [3274879887, 1064966938, 3639927359, 1677710747, 1825747855, 3009546298]:
    print(numconvert(num))

print()
print(numconvert(100))