#!/usr/bin/ruby

require 'optparse'
require 'csv'
$VERBOSE=nil

labelfile = ""
rotate = "-90"
curie = ""
newmach = ""
flip = "-flip "
webcam = ""
tbool = false
webcambool = false

opts = OptionParser.new do |opts|
	opts.on("-l labelfile") do |l|
		puts "label file:   "+l.to_s()
		labelfile = l.to_s()
	end
	opts.on("-c") do |c|
		curie = "c"
		rotate = "90"
	end
	opts.on("-n") do |n|
		newmach = "n"
		flip = ""
	end
	opts.on("-t") do |p|
		tbool = true
	end
	opts.on("-w") do |w|
		webcambool = true
		webcam = "w"
	end
	opts.on("-h") do |h|
		#watch the un-indentation
		puts <<-TXTBLK
Usage: nikon_rotate_label.rb -l labelfile.csv [options] img1.jpg img2.jpg ...

Options:
	-n	rotate for new machine, 50L (default prototype)
	-c	rotate for Curie Institute machine
	-t	tile labeled images 2x2
	-w	use for webcam images (otherwise defaults to scale bars for Nikon ccd)
	-h	prints this message

Example:
	nikon_rotate_label.rb -l xy.points.csv -n -t -w *.jpg
	This will label all jpg's (from the webcam) with the proper 
	orientation for the 50L, and tile.

	Note: use imgs2pdf_latex.rb to make pdf.\n
		TXTBLK

		exit
	end
end

opts.parse!(ARGV)

#external commands checks
#which returns null if can't be found
#check for convert
convertPath = %x[which convert]
if convertPath.length == 0
	puts "ERROR: this script requires ImageMagik's \"convert\" command to be in your path. Exiting..."
	exit
end
#check for montage
montagePath = %x[which montage]
if montagePath.length == 0
	puts "ERROR: this script requires ImageMagik's \"montage\" command to be in your path. Exiting..."
	exit
end
#check for args
if ARGV.length == 0
	puts "No files passed. Use \"nikon_rotate_label.rb -h\" for help."
	exit
end

#read the label file
csv = Array.new()
#for Ruby 1.8
if CSV.const_defined? :Reader
	CSV.open(labelfile, 'r') do |row|
		csv << row
	end
else
#for Ruby 1.9
	CSV.foreach(labelfile) do |row|
		csv << row	
	end
end

#print label file just because
csv.each {|r| r.each {|c| print c+" " }; puts ""; }

#gather all file names and file extension
nameindex = Hash.new(-1)
csv.each_index {|i| nameindex.store(csv[i][0].to_s, i)}

extension = ARGV[0].slice(ARGV[0].rindex("."),ARGV[0].length-1)
nolable = ""
puts "\n"

puts "\n\n**************************************************************"
ARGV.each {|f| 
	ext = f.slice(f.rindex("."),f.length-1)
	name = f.slice(0, f.rindex("."))
	
	# puts "name: #{name}"
	if ext!=extension
		puts "Warning: more than one file type!"
	end
	if !nameindex.has_key?(name)
		puts "Warning: #{f} #{name} has no label information (printing ignored)"
		pbool = false
	end
}
puts "**************************************************************\n\n"

puts "Creating ./labeled directory"
system("mkdir ./labeled")
puts "\n"

filelist = Array.new
namelist = Array.new
passedfiles = Array.new
ext = ""

ARGV.each {|f|
	ext = f.slice(f.rindex("."),f.length-1)
	name = f.slice(0, f.rindex("."))
	i=nameindex[name]
	
	#find correct scale bar size
	barcommand = ""
	if webcambool 
		barcommand = case csv[i][3].upcase
			when "5X"; "-draw 'rectangle 75,175,335,185' -gravity none -pointsize 50 -draw \"text 75,165 '200um'\""
			when "10X"; "-draw 'rectangle 75,175,335,185' -gravity none -pointsize 50 -draw \"text 75,165 '100um'\""
			when "20X"; "-draw 'rectangle 75,175,545,185' -gravity none -pointsize 50 -draw \"text 75,165 '100um'\""
			when "50X"; "-draw 'rectangle 75,175,335,185' -gravity none -pointsize 50 -draw \"text 75,165 '20um'\""
			when "100X"; "-draw 'rectangle 75,175,335,185' -gravity none -pointsize 50 -draw \"text 75,165 '10um'\""
		end
	else
		barcommand = case csv[i][3].upcase
			when "5X"; "-draw 'rectangle 75,175,235,185' -gravity none -pointsize 50 -draw \"text 75,165 '200um'\""
			when "10X"; "-draw 'rectangle 75,175,235,185' -gravity none -pointsize 50 -draw \"text 75,165 '100um'\""
			when "20X"; "-draw 'rectangle 75,175,397,185' -gravity none -pointsize 50 -draw \"text 75,165 '100um'\""
			when "50X"; "-draw 'rectangle 75,175,235,185' -gravity none -pointsize 50 -draw \"text 75,165 '20um'\""
			when "100X"; "-draw 'rectangle 75,175,235,185' -gravity none -pointsize 50 -draw \"text 75,165 '10um'\""
		end
	end
	
	puts "Rotating and Labeling: #{name}#{ext} -> #{name}_l#{newmach}#{curie}#{webcam}#{ext}"

	if nameindex.has_key?(name)
		label = "ISEE:#{csv[i][0]} (#{csv[i][1]}, #{csv[i][2]}) #{csv[i][3]} chip:#{csv[i][4]} #{csv[i][5]}"
		if curie != "" then label << " (curie)" end
		if newmach == "" then label << " (proto)" else label << " (50L)" end
	else
		label = " "
		barcommand = " "
	end
	
	
	system("convert #{name}#{ext} -quiet #{flip} -resize 1600x1200\! -rotate #{rotate}  -gravity North  -background White  -splice 0x100 +repage -depth 8 ./labeled/#{name}_l#{newmach}#{curie}#{webcam}#{ext};   width=`identify -format %w ./labeled/#{name}_l#{newmach}#{curie}#{webcam}#{ext}`;  convert -quiet -background '#0000' -fill black -gravity center -size ${width}x100 caption:\"#{label}\" +size ./labeled/#{name}_l#{newmach}#{curie}#{webcam}#{ext} +swap -gravity North -composite -fill red #{barcommand} -depth 8 ./labeled/#{name}_l#{newmach}#{curie}#{webcam}#{ext}")

	passedfiles << name+"_l#{newmach}#{curie}#{webcam}"+ext

}
puts "\n"

if tbool
	1.upto(csv.length-1) {|k|
		filelist << "./labeled/" + csv[k][0] + "_l#{newmach}#{curie}#{webcam}"+ext
		namelist << csv[k][0] + "_l#{newmach}#{curie}#{webcam}"
	}

	0.step(filelist.length, 4) {|i|
		files=""
		names="tiled_"
		0.upto(3) {|j| if filelist[i+j].to_s != "" then files << filelist[i+j].to_s << " " end}
		0.upto(3) {|j| if namelist[i+j].to_s != "" then names << namelist[i+j].to_s << "_" end}
		names.chomp!("_");
	
		if files!="    "
			puts "Tiling "+files+" -> #{names}.jpg"
			system("montage #{files} -mode Concatenate  -tile 2x2  -geometry +5+5 ./labeled/#{names}.jpg")
		end

		puts "-----------------"
	}
end

puts "\n\nThe End\n\n"
