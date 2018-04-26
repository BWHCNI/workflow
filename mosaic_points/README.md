This is a Python3 script that will go through .chk_im files and gather the NanoSIMS Stage Coordinates for each, then output them into a csv file.
The points gathered mark the center of a tile, and are useful for quick reference against a constructed mosaic image.



```
usage: mosaic_points.py [-h] [-t TITLE] [files [files ...]]

A script for parsing .chk_im files for NanoSIMS stage position data, and
returning a tab-separated CSV file presenting [source, tile number, x, y, z]
and titled according to the chk_im file name or as given. Can be passed files
explicitly, via a directory, or via an expression.

positional arguments:
  files                 Files that will be used.

optional arguments:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        Title for the output csv file. Default is based on the
                        given chk_im's
```

