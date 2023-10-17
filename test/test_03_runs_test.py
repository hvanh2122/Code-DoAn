import math

def runs_test(input):
    n = len(input)
    ones = input.count('1')  # number of ones
    prop = float(ones) / float(n)
    tau = 2.0 / math.sqrt(n)

    if abs(prop - 0.5) > tau:
        p = 0
    else:
        vobs = 1.0
        for i in range(n - 1):
            if input[i] != input[i + 1]:
                vobs += 1.0
        p = math.erfc(abs(vobs - (2.0 * n * prop * (1.0 - prop))) / (2.0 * math.sqrt(2.0 * n) * prop * (1 - prop)))

    success = (p >= 0.01)
    return success,p