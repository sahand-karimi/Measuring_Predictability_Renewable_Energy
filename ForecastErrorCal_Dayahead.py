import pandas as pd
from datetime import timedelta
import concurrent.futures  # Using multi processors
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def _error(actual: np.ndarray, predicted: np.ndarray):
    """ Simple error """
    return actual - predicted


def mse(actual: np.ndarray, predicted: np.ndarray):
    """ Mean Squared Error """
    return np.mean(np.square(_error(actual, predicted)))


def mae(actual: np.ndarray, predicted: np.ndarray):
    """ Mean Absolute Error """
    return np.mean(np.abs(_error(actual, predicted)))


def RMSE(actual: np.ndarray, predicted: np.ndarray):
    """ Root Mean Squared Error """
    return np.sqrt(mse(actual, predicted))


def NRMSE(actual: np.ndarray, predicted: np.ndarray):
    """ Normalized Root Mean Squared Error """
    return RMSE(actual, predicted) / (actual.max() - actual.min() + 0.01)  # adding an epsilon to avoid division by 0


def NMAE(actual: np.ndarray, predicted: np.ndarray):
    """ Normalized Root Mean Squared Error """
    return mae(actual, predicted) / (actual.max() - actual.min() + 0.01)  # adding an epsilon to avoid division by 0


def error_calculation(series, site_id, train_len, test_len, datapoint_in_eachhour, seasonality):
    NRMSE_RF_list = list()
    NMAE_RF_list = list()

    NRMSE_naive_list = list()
    NMAE_naive_list = list()

    # this loop calculates the forecast errors of 1-day ahead predictions using a rolling window over 1 year (365 days):
    for i in list(range(0, (24 * datapoint_in_eachhour * 365) - test_len - train_len, seasonality)):
        train = series[i:i + train_len].values
        test = series[i + train_len:i + train_len + test_len].values
        train_x = list(range(i, i + train_len))
        test_x = list(range(i, i + test_len))
        train_x  = np.asarray(train_x)
        test_x = np.asarray(test_x)
        train_x = np.reshape(train_x, (-1, 1))
        train_x = train_x % (24 * datapoint_in_eachhour)
        test_x = np.reshape(test_x, (-1, 1))
        test_x = test_x % (24 * datapoint_in_eachhour)

        rf = RandomForestRegressor(n_estimators=100)
        rf.fit(train_x, train)
        y_pred = rf.predict(test_x)

        NRMSE_RF_list.append(NRMSE(test, y_pred))
        NMAE_RF_list.append(NMAE(test, y_pred))

        NRMSE_naive_list.append(NRMSE(test, train[train_len - seasonality:]))
        NMAE_naive_list.append(NMAE(test, train[train_len - seasonality:]))

    return site_id, NRMSE_RF_list, NMAE_RF_list, NRMSE_naive_list, NMAE_naive_list


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

    train_days = 9
    test_days = 1

    train_len = train_days * 24 * datapoint_in_eachhour
    test_len = test_days * 24 * datapoint_in_eachhour
    seasonality = 24 * datapoint_in_eachhour

    count = 0

    NRMSE_RF_dict = dict()
    NMAE_RF_dict = dict()
    NRMSE_naive_dict = dict()
    NMAE_naive_dict = dict()

    # Parallel calculation of forecast errors: (max_workers sets the numer of threads to be used for the calculations)
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        results = [executor.submit(error_calculation, input_data[site_id], site_id, train_len, test_len,
                                   datapoint_in_eachhour, seasonality) for site_id in all_sites]
        for f in concurrent.futures.as_completed(results):
            count = count + 1
            percent = count / (total_sites + 1)
            print('%.2f is done...' % percent)
            site_temp, NRMSE_RF_val, NMAE_RF_val, NRMSE_naive_val, NMAE_naive_val = f.result()

            NRMSE_RF_dict[site_temp] = NRMSE_RF_val
            NMAE_RF_dict[site_temp] = NMAE_RF_val
            NRMSE_naive_dict[site_temp] = NRMSE_naive_val
            NMAE_naive_dict[site_temp] = NMAE_naive_val

    # For saving the final data-frame
    (pd.DataFrame(NRMSE_RF_dict)).to_pickle('RF_' + str(train_days) + 'train_' + str(test_days) + 'test_NRMSE.pkl')
    (pd.DataFrame(NMAE_RF_dict)).to_pickle('RF_' + str(train_days) + 'train_' + str(test_days) + 'test_NMAE.pkl')

    (pd.DataFrame(NRMSE_naive_dict)).to_pickle('naive_'+ str(train_days) + 'train_' + str(test_days) + 'test_NRMSE.pkl')
    (pd.DataFrame(NMAE_naive_dict)).to_pickle('naive_' + str(train_days) + 'train_' + str(test_days) + 'test_NMAE.pkl')

    print("All forecast errors are now saved!")


if __name__ == '__main__':
    mainfunc()
