#!/usr/bin/ruby

require 'optparse'
$VERBOSE=nil

sortbool = false
outputfile = "output.pdf"

opts = OptionParser.new do |opts|
        opts.on("-s") do |s|
		sortbool = true
        end
	opts.on("-o outputfile") do |o|
		outputfile = o.to_s
        end
end

opts.parse!(ARGV)

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

cleanup = Array.new
pdffiles = Array.new
k = 1

puts "Output will be saved to #{outputfile} "
puts "------------------------------------"

imgfiles.each{|img|
	puts "Convert #{img} to page#{k}.ps ..."
	system("convert -page letter #{img} /tmp/page#{k}.ps")
	puts "Convert page#{k}.ps to page#{k}.pdf ..."
	system("ps2pdf /tmp/page#{k}.ps /tmp/page#{k}.pdf")
	puts "\n"

	pdffiles << "/tmp/page#{k}.pdf"
	cleanup  << "/tmp/page#{k}.ps"
	cleanup  << "/tmp/page#{k}.pdf"
	k = k+1
}
puts "------------------------------------"
puts "Creating pdf from pages..."

pages = ""
pdffiles.each{|f| pages << " " << f.to_s}

puts pages
puts "------------------------------------"

puts "Creating full pdf with gs..."
system("gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=#{outputfile} -dBATCH #{pages}")

puts "------------------------------------"
puts "Deleting temp files..."
cleanup.each{|f|
	system("rm #{f}")
}

puts "The End."
