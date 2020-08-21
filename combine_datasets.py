import pandas as pd

achat = pd.read_hdf('data/processed/ach_at_full_6000.h5')
achhex = pd.read_hdf('data/processed/ach_hex_full_6000.h5')

achhex = achhex[achhex['y'] < 3]
achhex['window_id'] += 1000

df = pd.concat([achat,achhex])

df.to_hdf('data/processed/ach_at_combined_6000.h5', key='data', complevel=9)

y = (df[['window_id','y']]
     .drop_duplicates('window_id')
     .set_index('window_id')
     .T
     .squeeze()
     .sort_index(0))

y.to_hdf('data/ach_at_combined_y.h5', key='data', complevel=9)

subject = (df[['window_id','subject']]
     .drop_duplicates('window_id')
     .set_index('window_id')
     .T
     .squeeze()
     .sort_index(0))

subject.to_hdf('data/ach_at_combined_subject.h5', key='data', complevel=9)