from astropy.io import fits
from urllib import urlopen
import os
import sqlite3
from scipy.constants import c

ch = c*1.0e-5 #in Mpc/h
 
f = urlopen("http://sdss.physics.nyu.edu/mblanton/v0/catalogs/nsa_v0_1_2.fits")
ff = fits.open(f)
nsa = ff[1].data
ff.close()

f = urlopen("http://sdss.physics.nyu.edu/mblanton/v0/catalogs/ned_atlas.fits")
ff = fits.open(f)
ned = ff[1].data
ff.close()

db_path = 'nsa.sqlite3'
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

