"""This script runs feature selection on extracted features from the MEA data.
The Mann-Whitney U test is used to determine whethere a feature provides good separation between
all 3 categories of target variable.

Output
-------
Generates a design matrix with the selected features for each set of extracted features in data/features/.
Saves as an hdf (.h5) file in data/features/filtered/

Author: Kartikey Vyas"""

## IMPORTS ----------------------------------------------------------------------------------------------
import argparse
import logging
import time
from datetime import datetime
import os
import subprocess
import pandas as pd
from tsfresh.feature_selection.significance_tests import target_binary_feature_real_test

## INITIALISE ARGPARSER FOR COMMAND LINE HELP -----------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
args = parser.parse_args()

## INITIALISE LOGGING -----------------------------------------------------------------------------------
# use current time as a unique identifier
now = datetime.now()
job_id = now.strftime("%d%m%y_%H%M%S")

# create directories if not already there
if not os.path.isdir('logs/feature_selection/'):
    subprocess.run(['mkdir', 'logs/feature_selection'],
    check=True, text=True)

if not os.path.isdir('data/features/filtered/'):
    subprocess.run(['mkdir', 'data/features/filtered'],
    check=True, text=True)

# create log file
logging.basicConfig(filename='logs/feature_selection/feature_selection_'\
    +'_'+job_id+'.txt', level=logging.DEBUG)

## LOADING DATA -----------------------------------------------------------------------------------------
start = time.process_time()

y = pd.read_hdf('data/features/achat_y.h5')
y_bin = y.astype('category')
y_bin = pd.get_dummies(y_bin)

logging.info("Loaded target variable")

## FEATURE SELECTION ------------------------------------------------------------------------------------
# get all the paths of the files to be loaded in
for root, dirs, files in os.walk('data/features/'):
    for file in files:
        if file.endswith("_eff.h5"):
            # load feature dataframe
            X = pd.read_hdf(os.path.join(root, file))
            X_filt = pd.DataFrame()
            logging.info("Loaded Features from: "+file)

            # test each feature with Mann-Whitney U Test
            logging.info("Selecting Features...")
            for feature in X:
                p = []
                try:
                    p.append(target_binary_feature_real_test(X[feature],y_bin[0],'mann'))
                    p.append(target_binary_feature_real_test(X[feature],y_bin[1],'mann'))
                    p.append(target_binary_feature_real_test(X[feature],y_bin[2],'mann'))
                except ValueError:
                    p.append(1000)
            if all(x <= 0.05 for x in p):
                X_filt = pd.concat([X_filt, X[feature]], axis=1)

            # Save selected features
            logging.info(msg = str(X_filt.shape[1])+" features selected")
            X_filt.to_hdf('data/features/filtered/'+'filt_'+file, key='features', complevel=9)
            logging.info('Features saved to filt_'+file)

logging.info('time taken = '+str(time.process_time() - start))            