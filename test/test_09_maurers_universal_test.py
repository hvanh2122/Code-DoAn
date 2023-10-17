import math

def pattern2int(pattern):
    l = len(pattern)
    n = 0
    for bit in pattern:
        n = (n << 1) + int(bit)
    return n


def maurer_s_universal_test(bits, pattern_len=None, init_blocks=None):
    n = len(bits)

    # Step 1. Choose the block size
    if pattern_len is not None:
        l = pattern_len
    else:
        ns = [904960, 2068480, 4654080, 10342400,
              22753280, 49643520, 107560960,
              231669760, 496435200, 1059061760]
        l = 6
        if n < 387840:
            return False, 0.0
        for threshold in ns:
            if n >= threshold:
                l += 1

    # Step 2 Split the data into Q and K blocks
    nblocks = int(math.floor(n / l))
    if init_blocks is not None:
        q = init_blocks
    else:
        q = 10 * (2 ** l)
    k = nblocks - q

    # Step 3 Construct Table
    nsymbols = (2 ** l)
    t = [0 for x in range(nsymbols)]  # zero out the table
    for i in range(q):  # Mark final position of
        pattern = bits[i * l:(i + 1) * l]  # each pattern
        idx = pattern2int(pattern)
        t[idx] = i + 1  # +1 to number indexes 1..(2**L)+1
        # instead of 0..2**L
    # Step 4 Iterate
    sum = 0.0
    for i in range(q, nblocks):
        pattern = bits[i * l:(i + 1) * l]
        j = pattern2int(pattern)
        dist = i + 1 - t[j]
        t[j] = i + 1
        sum = sum + math.log(dist, 2)
    print("  sum =", sum)

    # Step 5 Compute the test statistic
    fn = sum / k
    print("  fn =", fn)

    # Step 6 Compute the P Value
    # Tables from https://static.aminer.org/pdf/PDF/000/120/333/
    # a_universal_statistical_test_for_random_bit_generators.pdf
    ev_table = [0, 0.73264948, 1.5374383, 2.40160681, 3.31122472,
                4.25342659, 5.2177052, 6.1962507, 7.1836656,
                8.1764248, 9.1723243, 10.170032, 11.168765,
                12.168070, 13.167693, 14.167488, 15.167379]
    var_table = [0, 0.690, 1.338, 1.901, 2.358, 2.705, 2.954, 3.125,
                 3.238, 3.311, 3.356, 3.384, 3.401, 3.410, 3.416,
                 3.419, 3.421]

    # sigma = math.sqrt(var_table[l])
    mag = abs((fn - ev_table[l]) / (
                (0.7 - 0.8 / l + (4 + 32 / l) * (pow(k, -3 / l)) / 15) * (math.sqrt(var_table[l] / k)) * math.sqrt(2)))
    p = math.erfc(mag)

    success = (p >= 0.01)
    return success, p


if __name__ == "__main__":
    bits = '01001001010110100010001111010101101001110010100100111000101000010010101000101111011111110111000011011110111101000010111110111011'
    success, p, _ = maurer_s_universal_test(bits, pattern_len=2, init_blocks=4)

    print("success =", success)
    print("p       = ", p)