import pandas as pd
import antropy as ant

# Reading the synthetic rooftop PV dataset and site details file associated with it
# (Note that the results produced using the dummy dataset are likely to be different with the ones
# shown in the research article)
input_data = pd.read_csv("Input_data/synthetic_rooftop_data.gz", compression='gzip')
input_data.index = pd.to_datetime(input_data["t_stamp_utc"])
input_data = input_data.drop(columns=["t_stamp_utc"])
all_sites = input_data.columns
total_sites = len(all_sites)

resampling_interval_list = ['5min', '10min', '15min', '20min', '25min', '30min']

for sampling_interval in resampling_interval_list:
    SpE_dict = dict()
    for site_id in all_sites:
        series = input_data[site_id].resample(sampling_interval).sum()
        SpE_dict[site_id] = ant.spectral_entropy(series, sf=1, method='fft', normalize=True)

    # This saves the final data-frame for each resampling interval
    (pd.DataFrame(list(SpE_dict.items()), columns=['ID', 'SpEVal'])).to_pickle(
        'SpEvalues_' + sampling_interval + '.pkl')

#%%
