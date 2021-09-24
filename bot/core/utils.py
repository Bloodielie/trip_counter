from math import ceil


def parting(xs, parts):
    part_len = ceil(len(xs)/parts)
    return [xs[part_len*k:part_len*(k+1)] for k in range(parts)]
