import pandas as pd
import numpy as np
from joblib import dump
from tempfile import mkdtemp
from shutil import rmtree
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, GroupKFold, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import QuantileTransformer

X = pd.read_hdf('data/features/filtered/filtered_0.05_.h5')
y = pd.read_hdf('data/ach_at_combined_y.h5', key='y')
# y_bin = y.astype('category')
# y_bin = pd.get_dummies(y_bin)

# ADD SUBJECT COLUMN
s = 1
for i in range(1,6):
    X.loc[90*(i-1):90*i,'subject'] = s
    s += 1
for i in range(1,7):
    X.loc[450+(60*(i-1)):450+(60*i),'subject'] = s
    s+=1
assert not any(pd.isna(X['subject']))

train = X[X['subject'] != 4].index
test = X[X['subject'] == 4].index

X_train, X_test, y_train, y_test = X.iloc[train,:], X.iloc[test,:], y.iloc[train], y.iloc[test]

# # cross-validation iterator
# gkf = GroupKFold(n_splits=10)
# gkf = list(gkf.split(X_train, y_train, X_train['subject']))

skf = StratifiedKFold(n_splits=10, shuffle=True)

# one vs. rest scoring
scoring = {'AUC': 'roc_auc_ovo',
           'Accuracy': 'accuracy',
           'F1-score': 'f1_weighted',
           'Precision': 'precision_weighted',
           'Recall': 'recall_weighted',
           }
 
# define the pipeline
qt = QuantileTransformer()
clf = LogisticRegression()
cachedir = mkdtemp()
pipeline = Pipeline(steps=[('qt', qt), ('clf', clf)], memory=cachedir)

# hyperparameters
n_quantiles = [10]
output_distribution = ['normal']
penalty = ['l1', 'l2']
C = np.logspace(-4,4,20)

# parameter grid
param_grid = {'qt__n_quantiles': n_quantiles, 
              'qt__output_distribution': output_distribution,
              'clf__penalty' : penalty,
              'clf__solver' : ['saga'],
              'clf__C': C,
              'clf__max_iter': [1000]}

# replace rf with a pipeline ( quantile transform, classifier )
clf_grid = GridSearchCV(pipeline,
                        param_grid=param_grid,
                        cv=skf,
                        scoring=scoring,
                        refit=False,
                        verbose=2,
                        n_jobs=-1)

search = clf_grid.fit(X_train, y_train)

# Remove the cache directory
rmtree(cachedir)

dump(search, 'models/logreg_gridsearch_model_v2.joblib')

results = pd.DataFrame(search.cv_results_)

results.to_hdf('models/logreg_gridsearch_results_v2.h5', key='data', complevel=9)
