[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7538884.svg)](https://doi.org/10.5281/zenodo.7538884)
# Code and Data for a study on measuring the predictability of renewable generation data
This repository contains the code and data for the following paper:

Sahand Karimi-Arpanahi, S. Ali Pourmousavi, and Nariman Mahdavi. "Renewable generation predictability and its applications: A missing piece of the puzzle."

Abstract: Currently, various decisions in the power systems domain are made based on renewable generation prediction as a decisive factor. Thus, numerous sophisticated forecasting methods have been developed to improve the prediction accuracy of renewable generation. However, the accuracy of forecasting methods is limited by the inherent predictability of the data used for prediction. Additionally, the prediction techniques cannot measure the inherent predictability of a given time series. Therefore, this important measure has been entirely overlooked in theory and practice. In this paper, we systematically assess the suitability of various predictability measures for renewable generation time series, revealing the best method and providing instructions to tune it. Then, using real-world examples, we illustrate how predictability could save end users and investors millions of dollars in the electricity sector.

# Folders and files
The main folder includes the codes used to produce the figures in the paper.
Input_data folder includes all the relevant input data that we can share. It also includes a synthetic rooftop PV generation dataset.
Processed_data folder includes most of the outputs of our codes, which were used to create the figures. 


# Important notes about the input data
The original rooftop PV generation data from Solar Analytics, used in this study, cannot be shared. However, we have added a synthetic dataset with a similar structure to our rooftop PV generation to this repository. This dataset is synthesized by interpolating hourly solar irradiance data to 5-minute resolution in different locations of Australia in 2015, which is gathered from BOM. While this synthetic dataset does not meet the criteria for the application described in our study, it guides the users to prepare their own dataset in the correct structure that can be used by our code. Also, it can be used as an example to study the code. Please note that a renewable generation dataset should satisfy the following three conditions for the applications described in this paper: 1) it should have at least a temporal resolution of 10 minutes (it can differ depending on the electricity market and compliance rules); 2) the measured or estimated data should not be systematically affected by the external factors, such as generation curtailment, export limits, etc.; and 3) the length of data should be at least six months, and the dataset should cover a wide geographical area such as a country.

The solar irradiance data (GTI) from SolCast, used in this study, cannot be shared publicly, but university students and researchers can freely access the data on SolCast.com to reproduce our results. To do so, one should create a ‘Student or public researcher’ account. Then, submit a ‘Time Series Request’ with the following details. Enter all the locations of the (potential) solar farms as in our study (the exact latitude and longitude of each location are available in the public repository). Set the ‘Data period’ as mentioned in the relevant analysis, ‘Time granularity’ to 5 minutes and ‘File format’ to Solcast. Select `GTI Horizontal Single-Axis Tracker’ as one of the parameters in their request. Finally, download the GTI data and use it as input for the relevant analyses (the codes of which are shared in this repository).


# How to use the codes to produce the figures shown in the paper
We have tried our best to share as much processed data as possible so that others can firstly check out the output of the functions on our PV generation data, and, secondly produce some of the figures. If a figure can be fully created without any dependency on the input PV generation data, then it is possible to reproduce the exact figure shown in the paper. 

Regarding the analyses and figures associated with the solar irradiance data from Solcast, we have provided the exact locations of the solar farms (studied in our analyses) in the relevant codes. Thus, it is possible to download (from Solcast.com) the exact solar irradiance data we used and reproduce the relevant figures shown in the paper.


# How to run the Jupyter Notebooks
In all notebooks, if the appropriate input data is available, one can run all the cells from top to bottom in the notebook to do the relevant analysis or create the figure. In some notebooks, one can use the processed data to directly produce the figures without needing to process the input data (as the data used in our study is not publicly available in most cases).

If the user wants to use the code on their own data, first, they should run the Python codes with their own data as the input in order to create the datasets of entropy measures and prediction errors for their own renewable generation data. Then, they can run the Jupyter Notebooks to do the analyses.
