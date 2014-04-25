from astropy.io import fits
from urllib import urlopen
from tempfile import TemporaryFile
import os
import sqlite3
from scipy.constants import c

ch = c*1.0e-5 #in Mpc/h
 
def fits_open_url(url):
    f = urlopen(url)
    with TemporaryFile() as ftmp:
        ftmp.write(f.read())
        ftmp.seek(0,0)
        ff = fits.open(ftmp)
        X = ff[1].data
        ff.close()
    return X

nsa = fits_open_url("http://sdss.physics.nyu.edu/mblanton/v0/nsa_v0_1_2.fits")
ned = fits_open_url("http://sdss.physics.nyu.edu/mblanton/v0/catalogs/ned_atlas.fits")

db_path = 'nsa.sqlite3'

if os.path.isfile(db_path):
    os.unlink(db_path)
db = sqlite3.connect(db_path)
db.execute('create table nsa (nsa int unique, ra real, dec real, dist real, iau text, ned text)')
db.commit()

for i in nsa:
    ined = i.field('ined')
    t = (int(i.field('nsaid')), float(i.field('ra')), float(i.field('dec')), \
            float(i.field('ZDIST')*ch), \
            unicode(i.field('iauname')), \
            u'' if ined == -1 else unicode(ned[ined].field('NAME1').strip() \
                    + ned[ined].field('NAME2').strip()))
    db.execute('insert into nsa values (?,?,?,?,?,?)', t)

db.commit()
db.close()

