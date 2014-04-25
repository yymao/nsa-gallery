from urllib2 import urlopen
import pandas as pd

url = "https://raw.githubusercontent.com/saga-survey/saga-data/master/masterlist.csv"
d = pd.read_csv(urlopen(url), skiprows=[1])

def apply_cut(df, cut_f, *fields):
    return df[cut_f(*map(df.__getitem__, fields))]

dc = d
dc = apply_cut(dc, lambda x: ~x.isnull(), 'NSAID')
dc = apply_cut(dc, lambda x: x>7, 'K')
dc = apply_cut(dc, lambda x: x<10, 'K')
dc = apply_cut(dc, lambda x: x>20, 'distance')
dc = apply_cut(dc, lambda x: x<45, 'distance')
dc.sort(columns='K', inplace=True)
dc.to_csv('my_catalog.csv', cols=['NSAID', 'PGC#', 'distance', 'r','i','z','I','K','vhelio','vhelio_err'], float_format="%g", index=False)

