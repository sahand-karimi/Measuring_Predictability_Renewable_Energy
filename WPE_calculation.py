import pandas as pd
import pyentrp.entropy as ent
import concurrent.futures  # Using multi processors


def WPE_cal(series, site_id, dimension, sampling_interval):
    resampled_series = series.resample(sampling_interval).sum()  # Resampling the time series
    WPE_output = ent.weighted_permutation_entropy(resampled_series, order=dimension, delay=1, normalize=True)
    return site_id, WPE_output


def mainfunc():
    # Reading the synthetic rooftop PV dataset and site details file associated with it
    # (Note that the results produced using the dummy dataset are likely to be different with the ones
    # shown in the research article)
    input_data = pd.read_csv("Input_data/synthetic_rooftop_data.gz", compression='gzip')
    input_data.index = pd.to_datetime(input_data["t_stamp_utc"])
    input_data = input_data.drop(columns=["t_stamp_utc"])
    all_sites = input_data.columns
    total_sites = len(all_sites)

    resampling_interval_list = ['5min', '10min', '15min', '20min', '25min', '30min']
    dimension_list = [3, 4, 5, 6]

    for sampling_interval in resampling_interval_list:
        for dimension in dimension_list:
            print("Working on a new set")
            count = 0
            wpe_dict = dict()
            # WPE calculation:
            with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
                results = [executor.submit(WPE_cal, input_data[site_id], site_id, dimension, sampling_interval)
                           for site_id in all_sites]
                for f in concurrent.futures.as_completed(results):
                    count = count + 1
                    percent = count / (total_sites + 1)
                    print('%.3f is done...' % percent)
                    site_id_temp, WPE_val_temp = f.result()
                    wpe_dict[site_id_temp] = WPE_val_temp
            print("WPE values for " + sampling_interval + ' resamp & ' + str(dimension) + " dim were calculated.")
            # This saves the final data-frame for each resampling interval and dimension
            (pd.DataFrame(list(wpe_dict.items()), columns=['ID', 'WPEVal'])).to_pickle(
                'WPEvalues_' + sampling_interval + 'minresamp_' + str(dimension) + 'dim.pkl')


if __name__ == '__main__':
    mainfunc()
