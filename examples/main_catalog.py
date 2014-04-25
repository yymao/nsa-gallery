import numpy as np
from urllib2 import urlopen

def get_raw_data():
    url = "https://raw.githubusercontent.com/saga-survey/saga-data/master/masterlist.csv"
    names = "RA,Dec,PGC,NSAID,othername,vhelio,vhelio_err,distance,r,i,z,I,K".split(',')
    usecols = (3,2,7,8,9,10,11,12,5,6,0,1)
    fmts = [float]*len(names)
    conv = dict(zip(range(len(names)), [lambda s : float(s or np.nan)]*len(names)))
    for i in [2, 3]:
        fmts[i] = int
        conv[i] = lambda s : int(s or -1)
    dtype = zip(names, fmts)
    dtype = [dtype[i] for i in usecols]
    conv = {i:conv[i] for i in usecols}
    return np.loadtxt(urlopen(url), np.dtype(dtype), delimiter = ',', converters=conv, skiprows=2, usecols=usecols)

def apply_cut(df, cut_f, *fields):
    return df[cut_f(*map(df.__getitem__, fields))]

dc = get_raw_data()

#change cuts here
dc = apply_cut(dc, lambda x: x>-1, 'NSAID')
dc = apply_cut(dc, lambda x: x>7, 'K')
dc = apply_cut(dc, lambda x: x<10, 'K')
dc = apply_cut(dc, lambda x: x>20, 'distance')
dc = apply_cut(dc, lambda x: x<45, 'distance')

dc = dc[dc['K'].argsort()]
s = slice(0, -2) #to exclude RA and Dec

def tostr(v):
    return '' if v is -1 or np.isnan(v) else '%g'%v

with open('main_catalog.csv', 'w') as f:
    f.write(','.join(dc.dtype.names[s]) + '\n')
    for r in dc:
        f.write(','.join(map(tostr, r.tolist()[s])) + '\n')
