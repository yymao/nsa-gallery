import os
from urllib import urlopen

_db_cols = ['nsa', 'ra', 'dec', 'dist', 'iau', 'ned']
_db_fmts = ['%d', '%.7f', '%.7f', '%g', '%s', '%s']

_img_url = "http://skyservice.pha.jhu.edu/DR10/ImgCutout/getjpeg.aspx?ra=%s&dec=%s&scale=%s&width=512&height=512&opt=G"

def query_nsa(nsa, db):
    res = db.execute("select * from nsa where nsa==?", (nsa,))
    row = res.fetchone()
    if row is None:
        return None
    else:
        d = {}
        for k, fmt, v in zip(_db_cols, _db_fmts, row):
            if v != '':
                d[k] = fmt%v
        return d

def get_images(d, scales, path, skip_exists=False):
    for name, scale in scales:
        fname = path%(name, d['nsa'])
        if not (skip_exists and os.path.isfile(fname)):
            with open(fname, 'wb') as fo:
                fo.write(urlopen(_img_url%(d['ra'], d['dec'], scale)).read())

if __name__ == "__main__":
    import sys
    import csv
    import json
    import sqlite3

    try:
        f_csv = sys.argv[1]
    except IndexError:
        raise ValueError("Usage: python bulid.py file.csv")

    img_dir = 'images'
    img_path = img_dir + '/%s_%s.jpg'
    img_scales = [('wide', '14.06250'), ('zoom', '0.7031250')]
    js_path = 'app/data.js'
    db_path = 'app/nsa.sqlite3'

    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)
    nsa_map = {}
    db = sqlite3.connect(db_path)
    with open(js_path, 'w') as f:
        with open(f_csv, 'r') as fi:
            rd = csv.reader(fi)
            for i, row in enumerate(rd):
                if i==0:
                    f.write('var ud_header = %s;\n'%json.dumps(row[1:]))
                    f.write('var d = [\n')
                    continue
                d = query_nsa(row[0], db)
                if d is None:
                    print 'Warning: Cannot find NSA ID', row[0]
                    continue
                d['userdata'] = list(row[1:])
                get_images(d, img_scales, img_path, True)
                f.write(',\n' if i > 1 else '')
                f.write(json.dumps(d))
                nsa_map[d['nsa']] = i-1
        f.write('\n];\n')
        f.write('var nsa_map = %s;\n'%json.dumps(nsa_map))
    db.close()
