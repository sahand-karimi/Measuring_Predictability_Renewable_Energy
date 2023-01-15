import antropy as ant
import pyentrp.entropy as ent
from DE_function import disp_entropy


def WPE_over_time(series, series_length, window_len, step_size=288, dimension=3, delay=1):
    entropy_list = list()
    counter = 0
    for i in series.index + window_len:
        if i == series.index[0] + series_length:
            break
        if counter % step_size == 0:
            windowed_series = series[i - window_len:i]
            entropy_val = ent.weighted_permutation_entropy(windowed_series, order=dimension, delay=delay, normalize=True)
            entropy_list.append(entropy_val)
        counter = counter + 1
    return entropy_list


def PE_over_time(series, series_length, window_len, step_size=1, dimension=3, delay=1):
    entropy_list = list()
    counter = 0
    for i in series.index + window_len:
        if i == series.index[0] + series_length:
            break
        if counter % step_size == 0:
            windowed_series = series[i - window_len:i]
            WPEtemp = ent.permutation_entropy(windowed_series, order=dimension, delay=delay, normalize=True)
            entropy_list.append(WPEtemp)
        counter = counter + 1
    return entropy_list


def SpE_over_time(series, series_length, window_len, step_size=1):
    entropy_list = list()
    counter = 0
    for i in series.index + window_len:
        if i == series.index[0] + series_length:
            break
        if counter % step_size == 0:
            windowed_series = series[i - window_len:i]
            entropy_val = ant.spectral_entropy(windowed_series, sf=1, method='fft',  normalize=True)
            entropy_list.append(entropy_val)
        counter = counter + 1
    return entropy_list


def DE_over_time(series, series_length, window_len, step_size=1, dimension=3, cls=3, delay=1):
    entropy_list = list()
    counter = 0
    for i in series.index + window_len:
        if i == series.index[0] + series_length:
            break
        if counter % step_size == 0:
            windowed_series = series[i - window_len:i]
            entropy_val = disp_entropy(windowed_series, dimension, cls, delay=delay, normalise=True)
            entropy_list.append(entropy_val)
        counter = counter + 1
    return entropy_list


def SaE_over_time(series, series_length, window_len, step_size=1, order = 3):
    entropy_list = list()
    counter = 0
    for i in series.index + window_len:
        if i == series.index[0] + series_length:
            break
        if counter % step_size == 0:
            windowed_series = series[i - window_len:i]
            entropy_val = ant.sample_entropy(windowed_series, order=order)
            entropy_list.append(entropy_val)
        counter = counter + 1
    return entropy_list

#%%
