import numpy as np
from astropy.io import fits
from urllib import urlretrieve
import os
import sqlite3
from scipy.constants import c
ch = c*1.0e-5 #in Mpc/h

def fits_open_url(url):
    tmp = urlretrieve(url)[0]
    try:
        ff = fits.open(tmp)
        X = ff[1].data
        ff.close()
    finally:
        os.unlink(tmp)
    return X

nsa = fits_open_url('http://sdss.physics.nyu.edu/mblanton/v0/nsa_v0_1_2.fits')

ned_name = fits_open_url('http://sdss.physics.nyu.edu/mblanton/v0/catalogs/ned_atlas.fits')
ned_name = ned_name['NAME1'].strip() + ned_name['NAME2'].strip()

sdss_id = fits_open_url('http://sdss.physics.nyu.edu/mblanton/v0/catalogs/sdss_atlas.fits')
sdss_id = sdss_id['ID']

sdss_objid = sdss_id[nsa['isdss']].astype(np.int64) \
        | nsa['field'].astype(np.int64) << 16 \
        | nsa['camcol'].astype(np.int64) << 29 \
        | nsa['run'].astype(np.int64) << 32 \
        | np.array(nsa['rerun'], dtype=np.int64) << 48 \
        | 2 << 59

db_path = 'nsa.sqlite3'

if os.path.isfile(db_path):
    os.unlink(db_path)

db = sqlite3.connect(db_path)
db.execute('create table nsa (nsa int unique, ra real, dec real, dist real, sersic_n real, sdss_objid int, iau text, ned text)')
db.commit()

stmt = 'insert into nsa values (%s)'%(','.join(['?']*8))
for i, row in enumerate(nsa):
    db.execute(stmt, (int(row['nsaid']), row['ra'], row['dec'], \
            float(row['ZDIST']*ch), float(row['sersic_n']), \
            sdss_objid[i] if row['isdss'] > -1 else -1, \
            unicode(row['iauname']), \
            u'' if row['ined'] == -1 else unicode(ned_name[row['ined']])))
db.commit()
db.close()

