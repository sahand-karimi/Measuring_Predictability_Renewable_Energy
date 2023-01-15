import pandas as pd
import pyentrp.entropy as ent
import concurrent.futures  # Using multi processors
from datetime import timedelta
from datetime import datetime


def wpe_calculation_over_time(series, site_id, dimension, delay, window_size, resamp_int, datapoint_in_eachday):
    wpe_list = list()
    counter = 0

    a_year = timedelta(days=365)

    resampled_series = series.resample(resamp_int).sum()  # Resampling the time series
    for timeindex in resampled_series.index + window_size:
        if timeindex == resampled_series.index[0] + a_year:
            break
        if (counter % datapoint_in_eachday) == 0:  # calculates the WPE even one day
            windowed_series = resampled_series[timeindex - window_size:timeindex]
            wpe_list.append(ent.weighted_permutation_entropy(windowed_series,
                                                             order=dimension, delay=delay, normalize=True))
        counter = counter + 1
    return site_id, wpe_list


def mainfunc():
    # Reading the synthetic rooftop PV dataset and site details file associated with it
    # (Note that the results produced using the dummy dataset are likely to be different with the ones
    # shown in the research article)
    input_data = pd.read_csv("Input_data/synthetic_rooftop_data.gz", compression='gzip')
    input_data.index = pd.to_datetime(input_data["t_stamp_utc"])
    input_data = input_data.drop(columns=["t_stamp_utc"])
    all_sites = input_data.columns
    total_sites = len(all_sites)

    # Set the parameters:
    dimension = 6
    delay = 1
    count = 0
    resamp_int = '10min'
    rolling_window_size = 60  # in days (about 2 months)

    window = timedelta(days=rolling_window_size)
    datapoint_in_eachday = int(timedelta(days=1) / timedelta(minutes=datetime.strptime(resamp_int, '%Mmin').minute))
    wpe_lists_dictionary = dict()

    # WPE calculation:
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        results = [executor.submit(wpe_calculation_over_time, input_data[site_id], site_id, dimension, delay,
                                   window, resamp_int, datapoint_in_eachday) for site_id in all_sites]
        for f in concurrent.futures.as_completed(results):
            count = count + 1
            percent = count / (total_sites + 1)
            print('%.3f is done...' % percent)
            site_id_read, wpe_list = f.result()
            wpe_lists_dictionary[site_id_read] = wpe_list
    print("WPE values of " + str(count) + " houses were calculated.")

    # Creating the datetime index for the final data-frame:
    index_list = list()
    a_year = timedelta(days=365)
    for site_id in all_sites:
        series = input_data.loc[:, site_id].resample(resamp_int).sum()
        counter = 0
        for timeindex in series.index + window:
            if timeindex == series.index[0] + a_year:
                break
            if (counter % datapoint_in_eachday) == 0:
                index_list.append(timeindex)
            counter = counter + 1
        break

    # Producing the final data frame that can be worked on
    fina_wpe_over_time_df = pd.DataFrame(wpe_lists_dictionary)
    fina_wpe_over_time_df['newcol'] = index_list
    fina_wpe_over_time_df.index = pd.to_datetime(fina_wpe_over_time_df['newcol'])
    fina_wpe_over_time_df = fina_wpe_over_time_df.drop(columns=['newcol'])

    # Saving the final data-frame
    fina_wpe_over_time_df.to_pickle('WPE_over_one_Year_windows_of' + str(rolling_window_size) + 'days_'
                                    + str(dimension) + '_' + resamp_int + '.pkl')


if __name__ == '__main__':
    mainfunc()
