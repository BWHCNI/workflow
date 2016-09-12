This script takes the images captured with the [quick capture script](https://github.com/BWHCNI/workflow/tree/master/micro-manager) snd applys the labes in the csv file. It trys to be self documenting, if you call it with the *-h* argument you get this:

```
cpoczatek@grepon:nikon_rotate_label$ ./nikon_rotate_label.rb -h
Usage: nikon_rotate_label.rb -l labelfile.csv [options] img1.jpg img2.jpg ...

Options:
	-n	rotate for new machine, 50L (default prototype)
	-c	rotate for Curie Institute machine
	-t	tile labeled images 2x2
	-w	use for webcam images (otherwise defaults to scale bars for Nikon ccd)
	-h	prints this message
	-d	debug flag, print more information

Example:
	nikon_rotate_label.rb -l xy.points.csv -n -t -w *.jpg
	This will label all jpg's (from the webcam) with the proper 
	orientation for the 50L, and tile.

	Note: use imgs2pdf_latex.rb to make pdf.
```

You can see that the script is called, passed labels in a file `-l labelfile.csv` (most commonly the gererated xy.points.csv), a set of options, and then all images to label. The `-l labelfile.csv` argument is **manditory**, the options are truely options.
