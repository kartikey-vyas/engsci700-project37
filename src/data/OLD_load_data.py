# -*- coding: utf-8 -*-
# import click
# import logging
# from pathlib import Path
# from dotenv import find_dotenv, load_dotenv
import os
import numpy as np
import pandas as pd
from scipy.io import loadmat

## THIS WAS IN HERE FROM THE COOKIECUTTER DATA SCIENCE TEMPLATE
# @click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
# def main(input_filepath, output_filepath):
#     """ Runs data processing scripts to turn raw data from (../raw) into
#         cleaned data ready to be analyzed (saved in ../processed).
#     """
#     logger = logging.getLogger(__name__)
#     logger.info('making final data set from raw data')


# if __name__ == '__main__':
#     log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     logging.basicConfig(level=logging.INFO, format=log_fmt)

#     # not used in this stub but often useful for finding various files
#     project_dir = Path(__file__).resolve().parents[2]

#     # find .env automagically by walking up directories until it's found, then
#     # load up the .env entries as environment variables
#     load_dotenv(find_dotenv())

#     main()
# get a list of the file names


def load_MEA_data_OLD(folder = "data/raw",method = "means"):
    """ This function loads the raw data from .mat files.
        All raw data must be placed in data/raw

        Arguments
        ---------
        folder: specifies the root folder where the data to be loaded will be put
                default = "data/raw"
                
        method: specifies how to process the data before exporting it. 
                default = "means" 
                    only keeps the mean signal for each MEA
    """
    d = folder
    filenames = []

    # get all the paths of the files to be loaded in
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith(".mat"):
                filenames.append(os.path.join(root, file))

    # initialise time vectors
    t0 = {'time': np.arange(60001, 240001, 1)}
    t1 = {'time': np.arange(420001, 600001, 1)}
    t2 = {'time': np.arange(780001, 960001, 1)}

    # set up dataframes to add the values into
    # baseline (0), first drug administered (1), second drug administered (2)

    df_baseline = pd.DataFrame(t0)
    df_first = pd.DataFrame(t1)
    df_second = pd.DataFrame(t2)

    for file in filenames:
        matfile = loadmat(file)
        MEA_data = pd.DataFrame(matfile['filt_data'])
        if method == "means":
            MEA_data = pd.DataFrame(MEA_data.mean(axis=0))
            # the name of the file will be the column header
            colname = os.path.split(file)[1]
            colname = colname[:-4]
            MEA_data.columns = [colname]
        elif method == "all":
            pass
        
        # concatenate appropriate dataframe
        if colname.endswith("0"):
            df_baseline = pd.concat([df_baseline, MEA_data], axis=1)
        elif colname.endswith("1"):
            df_first = pd.concat([df_first, MEA_data], axis=1)
        else:
            df_second = pd.concat([df_second, MEA_data], axis=1)

    # export to csv
    export_path = "data/interim/"
    if method == "means":
        ext = "_means.csv"
    
    df_baseline.to_csv(export_path+"baseline"+ext)
    df_first.to_csv(export_path+"first"+ext)
    df_second.to_csv(export_path+"second"+ext)