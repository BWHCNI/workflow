#!/usr/bin/ruby

require 'optparse'
$VERBOSE=nil

sortbool = false
debug = false
outputfile = "output.pdf"
basename = "output"
doctitle = ""

#tex method definitions
# ascii below (between TXTBLK's) is the exact same as would 
# be in a .tex document except the \'s are escaped
# and the apperence of '#{title}' and '#filename}
def getTexHeader(title)
	return <<-TXTBLK
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% imgs2pdf_latex script
% Nikon Image Template
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\documentclass{article}
\\usepackage[letterpaper,width=7in,height=9in]{geometry}
\\usepackage{graphicx}
\\usepackage{fancyhdr}
\\usepackage[strings]{underscore}
\\pagestyle{fancy}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Headers and footers
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%		
\\chead{\\Large{\\bf{#{title}}}}
\\cfoot{}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Begin document
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\begin{document}\n
TXTBLK
end

def getTexImage(filename)
	return <<-TXTBLK
\\includegraphics[height=\\textheight]{#{filename}}
\\clearpage\\newpage
TXTBLK
end

def getTexClosing()
	return "\n\n\\end{document}"
end
#end tex method definitions


opts = OptionParser.new do |opts|
        opts.on("-s") do |s|
		sortbool = true
        end
	opts.on("-o outputfile") do |o|
		outputfile = o.to_s
		basename = outputfile.slice(0, outputfile.rindex("."))
        end
	opts.on("-t title") do |t|
		doctitle = t.to_s
	end
	opts.on("-d") do |d|
		debug = true
	end
        opts.on("-h") do |h|
                #watch the un-indentation
                puts <<-TXTBLK
Usage: imgs2pdf_latex.rb [options] img1.jpg img2.jpg ...

Options:
        -s		sort argument files based on 1st numeric substring
        -t title	define document title (default "")     
	-o outputfile	name of output file, eg "Exp_9_images.pdf" (default output.pdf)
	-d		debug flag, prevents temp files from being deleted and prints pdflatex output

Example:
	imgs2pdf_latex.rb -t "Lee 19 15N BrdU" -s -o Lee_Exp19_nikon.pdf tiled*.jpg
        \n
                TXTBLK

                exit
        end


opts.parse!(ARGV)

#which returns null if can't be found
#check for pdflatex
pdflatexPath = %x[which pdflatex]
if pdflatexPath.length == 0
	puts "ERROR: this script requires pdflatex to be in your path. Exiting..."
	exit
end
if ARGV.length == 0
	puts "ERROR: No image files passed. Use \"imgs2pdf_latex.rb -h\" for help. Exiting..."
	exit
end

imgfiles = ARGV
if sortbool
	imgfiles.sort!{|x,y|
		reg = /\d+/
		mx = reg.match(x)
		my = reg.match(y)
		ix = mx[0].to_i
		iy = my[0].to_i
		ix <=> iy
	}
end

puts "\nImage files in this order: "
imgfiles.each{|i| 
	puts i
}
puts ""
puts "Output will be saved to #{basename}.pdf and will be #{imgfiles.length} pages."

#write latex to texfile
texfile = File.open("#{basename}.tex", 'wb')
texfile << getTexHeader(doctitle)
imgfiles.each{|i|
	texfile << getTexImage(i)
}
texfile << getTexClosing()
texfile.close

#notice stder redirect
texoutput = %x[pdflatex -interaction=nonstopmode #{basename}.tex 2>&1]
puts texoutput if debug

if !File.exists?("#{basename}.pdf")
	puts "ERROR: pdf not generated. Rerun with '-d' to debug"
end

if !debug
	#system not %x[] to print any errors
	system("rm #{basename}.log")
	system("rm #{basename}.aux")
	system("rm #{basename}.tex")
end



end

