import math
import numpy as np
from scipy.stats import norm


def disp_entropy(series, dimension, cls, delay=1, normalise=True):
    norm_values = norm.cdf(series, loc=np.mean(series), scale=np.std(series))
    mapped_values = np.array([round(cls * i + 0.5) for i in norm_values])
    mapped_perms = np.array([[mapped_values[i + dim * delay] for dim in range(dimension)] for i in
                             range(len(mapped_values) - (dimension - 1) * delay)])
    str_perms = list(map(str, mapped_perms))

    perm_indices = []
    for perm in set(str_perms):
        indexes = [i for i, e in enumerate(str_perms) if e == perm]
        perm_indices.append(indexes)

    perm_freq = np.zeros(len(perm_indices))
    for i, index in enumerate(perm_indices):
        perm_freq[i] = len(index)
    perm_freq = perm_freq / (len(series) - dimension + 1)

    entropy = 0
    for freq in perm_freq:
        entropy += freq * math.log2(freq)
    de = -entropy

    if normalise:
        de = de / math.log2(cls ** dimension)

    return de
