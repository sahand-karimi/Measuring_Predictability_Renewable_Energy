import pandas as pd
from datetime import timedelta
import concurrent.futures  # Using multi processors
import numpy as np
from statsmodels.tsa.arima.model import ARIMA


def _error(actual: np.ndarray, predicted: np.ndarray):
    """ Simple error """
    return actual - predicted


def mse(actual: np.ndarray, predicted: np.ndarray):
    """ Mean Squared Error """
    return np.mean(np.square(_error(actual, predicted)))


def mae(actual: np.ndarray, predicted: np.ndarray):
    """ Mean Absolute Error """
    return np.mean(np.abs(_error(actual, predicted)))


def error_calculation(series, site_id, train_len, test_len, forecast_horizon_list):
    MSE_naive_dict = dict()
    MAE_naive_dict = dict()

    MSE_ARIMA_dict = dict()
    MAE_ARIMA_dict = dict()

    for forecast_horizon in forecast_horizon_list:
        MSE_naive_dict[forecast_horizon] = list()
        MAE_naive_dict[forecast_horizon] = list()

        MSE_ARIMA_dict[forecast_horizon] = list()
        MAE_ARIMA_dict[forecast_horizon] = list()

    # this loop calculates the forecast errors of minutes-day ahead predictions using a rolling window
    # over 1 year (365 days):
    for i in list(range(0, len(series) - train_len - test_len)):

        train = series[i:i + train_len].values
        test = series[i + train_len:i + train_len + test_len].values

        model = ARIMA(train, order=(1, 1, 0), enforce_invertibility=False)
        model.initialize_approximate_diffuse()
        model_fit = model.fit(method_kwargs={"warn_convergence": False})
        y_pred_arima = model_fit.forecast(steps=test_len)
        leng = 0

        for forecast_horizon in forecast_horizon_list:
            MSE_naive_dict[forecast_horizon].append(round(mse(test[leng], train[-1]), 3))
            MAE_naive_dict[forecast_horizon].append(round(mae(test[leng], train[-1]), 3))
            MSE_ARIMA_dict[forecast_horizon].append(round(mse(test[leng], y_pred_arima[leng]), 3))
            MAE_ARIMA_dict[forecast_horizon].append(round(mae(test[leng], y_pred_arima[leng]), 3))

            leng += 1

    return site_id, MSE_ARIMA_dict, MAE_ARIMA_dict, MSE_naive_dict, MAE_naive_dict


def mainfunc():
    # Reading the synthetic rooftop PV dataset and site details file associated with it
    # (Note that the results produced using the dummy dataset are likely to be different with the ones
    # shown in the research article)
    input_data = pd.read_csv("Input_data/synthetic_rooftop_data.gz", compression='gzip')
    input_data.index = pd.to_datetime(input_data["t_stamp_utc"])
    input_data = input_data.drop(columns=["t_stamp_utc"])
    all_sites = input_data.columns
    total_sites = len(all_sites)

    datapoint_in_eachhour = int(timedelta(hours=1) / input_data.index.to_series().diff().median())

    forecast_horizon_list = ['5min', '10min', '15min', '20min']
    train_hours = 3
    test_data_length = int(forecast_horizon_list[-1] / input_data.index.to_series().diff().median())
    train_data_length = train_hours * datapoint_in_eachhour

    count = 0

    MSE_ARIMA_dict = dict()
    MAE_ARIMA_dict = dict()

    MSE_naive_dict = dict()
    MAE_naive_dict = dict()

    print('START')

    # Parallel calculation of forecast errors: (max_workers sets the numer of threads to be used for the calculations)
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        results = [
            executor.submit(error_calculation, input_data[site_id], site_id, train_data_length, test_data_length,
                            forecast_horizon_list)
            for site_id in all_sites]
        for f in concurrent.futures.as_completed(results):
            count = count + 1
            percent = count / (total_sites + 1)
            print('%.2f is done...' % percent)
            site_temp, MSE_ARIMA_val, MAE_ARIMA_val, MSE_naive_val, MAE_naive_val = f.result()

            MSE_ARIMA_dict[site_temp] = MSE_ARIMA_val
            MAE_ARIMA_dict[site_temp] = MAE_ARIMA_val

            MSE_naive_dict[site_temp] = MSE_naive_val
            MAE_naive_dict[site_temp] = MAE_naive_val

    # For saving the DFs of error metrics, where each DF is for a particular forecast horizon and method:
    for forecast_horizon in forecast_horizon_list:

        MSE_naive_dict_2 = dict()
        MAE_naive_dict_2 = dict()

        MSE_ARIMA_dict_2 = dict()
        MAE_ARIMA_dict_2 = dict()

        for site_id in all_sites:
            MSE_ARIMA_dict_2[site_id] = MSE_ARIMA_dict[site_id][forecast_horizon]
            MAE_ARIMA_dict_2[site_id] = MAE_ARIMA_dict[site_id][forecast_horizon]

            MSE_naive_dict_2[site_id] = MSE_naive_dict[site_id][forecast_horizon]
            MAE_naive_dict_2[site_id] = MAE_naive_dict[site_id][forecast_horizon]

        (pd.DataFrame(MSE_ARIMA_dict_2)).to_pickle('ARIMA_' + str(train_hours) + 'hr_' + forecast_horizon + '_MSE.pkl')
        (pd.DataFrame(MAE_ARIMA_dict_2)).to_pickle('ARIMA_' + str(train_hours) + 'hr_' + forecast_horizon + '_MAE.pkl')
        (pd.DataFrame(MSE_naive_dict_2)).to_pickle('naive_' + str(train_hours) + 'hr_' + forecast_horizon + '_MSE.pkl')
        (pd.DataFrame(MAE_naive_dict_2)).to_pickle('naive_' + str(train_hours) + 'hr_' + forecast_horizon + '_MAE.pkl')

    print("All DFs are now saved!")


if __name__ == '__main__':
    mainfunc()
