#!/usr/bin/ruby
$VERBOSE=nil

imgs = ["1_lw.jpg","2_lw.jpg","3_lw.jpg"]
doctitle = "This is the title."

# ascii below (between TXTBLK's) is the exact same as would 
# be in a .tex document except the \'s are escaped
# and the apperence of '#{title}' and '#filename}'

def getTexHeader(title)
	return <<-TXTBLK
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% imgs2pdf_latex script
% Nikon Image Template
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\documentclass{article}
\\usepackage[letterpaper,width=7in,height=9.5in]{geometry}
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


puts getTexHeader("blah blah blah")
imgs.each{|i|
	puts getTexImage(i)
}

puts getTexClosing()

exit
