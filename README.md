nsa-gallery
===========

A web app to quickly browse through a list of NSA objects.

## Bulid the web app

To use this web app, first you need to create a csv file which contains a list of NSA IDs:

- The first row in this csv file MUST be the header.
- The first column in this csv file MUST be the NSA IDs.
- All other columns in this csv file will be displayed on the webpage.

Once you have the csv file in the correct format, please run
If you just have a list of NSA IDs, you can simply create a text file and write in:

```
NSA
123
7045
2239
2832
```

There is also an example catalog `example_catalog.csv` so you can see how to format a catalog file.

Once you have the csv file in the correct format, please run

    python2 build.py /path/to/your/catalog.csv

or 

    python2 build.py http://url/to/your/catalog.csv

This will download all the needed images (which takes some time, and you need Internet connection) and build a javascript file for your catalog. Once it's done, simply open `index.html` in your non-IE browser and you can look through all the NSA objects in your catalog.


## While you are browsing

Use the `left` and `right` arrow keys (or `j` and `k`) to flip through objects. Press `/` or `f` to search for a specific NSA ID (it needs to be present in your catalog).

This app is not to replace the NSA or SDSS website but just for the convienence of view many objects. To find more about the objects, please click the buttons on the top of the page and it will bring you to corresponding websites. 

