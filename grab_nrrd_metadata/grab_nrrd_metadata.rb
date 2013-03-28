#!/usr/bin/ruby -w
require 'csv'
$VERBOSE=nil

# This is pretty basic and is gonna have to 
# be updated probably...
#
# Takes a list of nrrd's as args and writes
# all of their header metadata to metadata.csv
#

#method defs
#############################

def get_metadata_size(f)
	linecounter = 1
	skip = 1
	file = File.new(f, "r")
	
	while (line = file.gets)
		# skip the nrrd version and comment lines
        	if(line.to_s() == "\n") then break end
		if(linecounter==1 or line[0]=="#"[0]) then
			skip = skip + 1
			linecounter = linecounter + 1
			next 
		end

        	linecounter = linecounter + 1
	end

return linecounter-skip
end

def get_metadata_names(f)

	names = Array.new(get_metadata_size(f))
	linecounter = 1
	skip = 1
	file = File.new(f, "r")

	while (line = file.gets)
		# skip the nrrd version and comment lines
        	if(line.to_s() == "\n") then break end
		if(linecounter==1 or line[0]=="#"[0]) then
			linecounter = linecounter + 1
			skip = skip + 1
			next 
		end
	
		meta = line[0..(line.index(":")-1)]
		meta.rstrip!
		meta.lstrip!
		names[linecounter-skip] = meta
        	linecounter = linecounter + 1
	end

return names
end

#############################

if ARGV.length < 1 then
	puts "Error: no files passed"
	exit
end

#read first file to count number of metadata lines
puts "Counting metadata using #{ARGV[0]}"
datasize = get_metadata_size(ARGV[0])
puts "#{datasize} lines metadata"
puts "-------------"

#read first file to count number of metadata lines
puts "Grabbing metadata names using #{ARGV[0]}"
names = get_metadata_names(ARGV[0])
puts "Metadata names:"
names.each {|n|
	print "#{n}, "
}
puts "\n-------------"

outfile = File.open('metadata.csv', 'wb')


CSV::Writer.generate(outfile) do |csv|
	csv << (["file"] + names)
end


ARGV.each{|f|
        linecounter = 1
	skip = 1
        file = File.new(f, "r")
	puts f
	datalist = Array.new(datasize)
	
	while (line = file.gets)
		# skip the nrrd version and comment lines
	        if(line.to_s() == "\n") then break end
		if(linecounter==1 or line[0]=="#"[0]) then
			linecounter = linecounter + 1
			skip = skip + 1
			next 
		end
		
		#if linecounter > datasize then 
		#	puts "Error with file #{f} , More metadata than expected, skipping file..."
		#	break
		#end

		meta = line[0..(line.index(":")-1)]
		meta.rstrip!
		meta.lstrip!
		data = (line[line.index(":")+1..line.length])
		data.gsub!("=","")
		data.gsub!(",",";")
		data.rstrip!
		data.lstrip!
		#puts "#{meta}<->#{data}"
		
		datalist[linecounter-skip] = data
	        linecounter = linecounter + 1
	end
	puts "lines: #{linecounter-skip}"
	puts "Adding to csv..."

#	fname = f[f.rindex("/")+1..f.length]
	fname = f
	CSV::Writer.generate(outfile) << ([fname] + datalist)

	puts "-------------"
}

outfile.close

#the end


