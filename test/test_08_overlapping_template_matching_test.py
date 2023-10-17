import math
from scipy.special import gamma, gammaincc

def lgamma(x):
    return math.log(gamma(x))


def Pr(u, eta):
    if u == 0:
        p = math.exp(-eta)
    else:
        sum = 0.0
        for l in range(1, u + 1):
            sum += math.exp(
                -eta - u * math.log(2) + l * math.log(eta) - lgamma(l + 1) + lgamma(u) - lgamma(l) - lgamma(u - l + 1))
        p = sum
    return p


def overlapping_template_matching_test(bits):
    m = 10
    # Build the template B as a random list of bits
    B = [1 for x in range(m)]

    N = 968  # The number of blocks as specified in SP800-22rev1a
    K = 5  # The number of degrees of freedom
    M = 1062  # Length of each block as specified in SP800-22rev1a
    if len(bits) < (M * N):
        return False, 0.0

    blocks = list()  # Split into N blocks of M bits
    for i in range(N):
        blocks.append(bits[i * M:(i + 1) * M])

    # Count the distribution of matches of the template across blocks: Vj
    v = [0 for x in range(K + 1)]
    for block in blocks:
        count = 0
        for position in range(M - m):
            if block[position:position + m] == B:
                count += 1

        if count >= (K):
            v[K] += 1
        else:
            v[count] += 1

    # pi = [0.324652,0.182617,0.142670,0.106645,0.077147,0.166269] # From spec
    pi = [0.364091, 0.185659, 0.139381, 0.100571, 0.0704323, 0.139865]  # From STS

    lambd = (M - m + 1.0) / (2.0 ** m)
    eta = lambd / 2.0
    sum = 0.0
    for i in range(K):  # Compute Probabilities
        pi[i] = Pr(i, eta)
        sum += pi[i]

    pi[K] = 1 - sum

    sum = 0
    chisq = 0.0
    for i in range(K + 1):
        chisq += ((v[i] - (N * pi[i])) ** 2) / (N * pi[i])
        sum += v[i]

    p = gammaincc(5.0 / 2.0, chisq / 2.0)  # Compute P value

    success = (p >= 0.01)
    return success, p

if __name__ == "__main__":
    bits = [0, 0, 1, 1, 0, 1, 1, 1, 0, 1]
    success, plist = overlapping_template_matching_test(bits)