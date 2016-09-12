This script takes the images and converts them to a multi page pdf with title. It is most often used on the output of the [nikon_rotate_lable script](https://github.com/BWHCNI/workflow/tree/master/nikon_rotate_label). It trys to be self documenting, if you call it with the -h argument you get this:

```
cpoczatek@grepon:nikon_rotate_label$ imgs2pdf_latex.rb -h
Usage: imgs2pdf_latex.rb [options] img1.jpg img2.jpg ...

Options:
        -s		sort argument files based on 1st numeric substring
        -t title	define document title (default "")     
	      -o outputfile	name of output file, eg "Exp_9_images.pdf" (default output.pdf)
	      -d		debug flag, prevents temp files from being deleted and prints pdflatex output

Example:
	imgs2pdf_latex.rb -t "Lee 19 15N BrdU" -s -o Lee_Exp19_nikon.pdf tiled*.jpg
```

Here you can see that you specify a title, can sort numerically (not lexigraphically) if desired, and name the output file for the set of images passed to the script, in ths case `tiled*.jpg`
