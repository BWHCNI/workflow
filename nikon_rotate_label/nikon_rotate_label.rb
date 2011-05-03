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
printer = "astaroth"
pbool = false
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
	opts.on("-p") do |p|
		pbool = true
	end
	opts.on("-t") do |p|
		tbool = true
	end
	opts.on("-w") do |w|
		webcambool = true
		webcam = "w"
	end
end

opts.parse!(ARGV)

csv = Array.new()
CSV.open(labelfile, 'r') do |row|
	csv << row
end

csv.each {|r| r.each {|c| print c+" " }; puts ""; }

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
	
	barcommand = ""
	if webcambool 
		barcommand = case csv[i][3].upcase
			when "5X": "-draw 'rectangle 75,175,335,185' -gravity none -pointsize 50 -draw \"text 75,165 '200um'\""
			when "10X": "-draw 'rectangle 75,175,335,185' -gravity none -pointsize 50 -draw \"text 75,165 '100um'\""
			when "20X": "-draw 'rectangle 75,175,545,185' -gravity none -pointsize 50 -draw \"text 75,165 '100um'\""
			when "50X": "-draw 'rectangle 75,175,335,185' -gravity none -pointsize 50 -draw \"text 75,165 '20um'\""
			when "100X": "-draw 'rectangle 75,175,335,185' -gravity none -pointsize 50 -draw \"text 75,165 '10um'\""
		end
	else
		barcommand = case csv[i][3].upcase
			when "5X": "-draw 'rectangle 75,175,235,185' -gravity none -pointsize 50 -draw \"text 75,165 '200um'\""
			when "10X": "-draw 'rectangle 75,175,235,185' -gravity none -pointsize 50 -draw \"text 75,165 '100um'\""
			when "20X": "-draw 'rectangle 75,175,397,185' -gravity none -pointsize 50 -draw \"text 75,165 '100um'\""
			when "50X": "-draw 'rectangle 75,175,235,185' -gravity none -pointsize 50 -draw \"text 75,165 '20um'\""
			when "100X": "-draw 'rectangle 75,175,235,185' -gravity none -pointsize 50 -draw \"text 75,165 '10um'\""
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

		if pbool
			puts "Printing #{names}.jpg on #{printer}"
			system("lp -d #{printer} -o scaling=100 ./labeled/#{names}.jpg")
		end

		puts "-----------------"
	}
end

puts "\n\nThe End\n\n"