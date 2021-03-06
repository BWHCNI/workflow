#!/usr/bin/env ruby
###############################################################
## 2009-11-03
##
## Combine a set of neighboring nrrd files into one mosaic nrrd.
## Differences in Z can be managed by padding with zero up to the max Z,
## or by compressing into one plane with optional scaling.
##
## Two types of mosaics:
## Grid:: Placement is on a grid specified by a delimited text file.
## Fluid:: Automatic placement in X and Y.
##
## All unu commands used go to stdout, so the effect should be
## reproducible by re-running the output as a shell script.
##
## TODO:
## 1) The line containing *.nrrd.normalized prevents the scripts
##    from running in 2 different terminals simulatenously, because
##    when one is complete, it deletes ALL the .nrrd.normalized
##    files.
## 2) Make it so the header of the mosaic file has relevant Mims_* data.
###############################################################

require 'optparse'
require 'pathname'
require 'date'

Axes = {:x => 0, :y => 1, :z => 2, :mass => 3}

# nrrd utilities
module Nrrd

  Unu   = "unu" # path to unu executable
  Debug = true  # print unu commands?
  
  def self.opt_str(opts)
    opts.map do |key, val|
      key.to_s.empty? ? val.to_s : "--#{key} #{val}"
    end.join(' ')
  end

  ###############################################################
  ## make a system call to unu with the given action and arguments
  ###############################################################
  def self.unu_call(action, opts={})
    if action.is_a? Array #  pipe one to the next
      cmd = action.map { |a, o| "#{Unu} #{a} #{opt_str(o)}"}.join(' | ')
    else # a single command
      cmd = "#{Unu} #{action} #{opt_str(opts)}"
    end
    puts "#{cmd}" if Debug
    system(cmd)
    puts ""
  end

  ###############################################################
  ## return hashes of header values for nrrd file
  ###############################################################
  def self.head(filename)
    delim_nrrd = ': '
    delim_meta = ':='
    header = {}
    text = IO.popen("#{Unu} head \"#{filename}\"") {|f| f.read }
    lines = text.split($/).reject {|x| x.start_with? '#'} # ignore comments

    magic = lines.shift # nrrd identifier
    nrrd_values = lines.reject {|x| !(x.include? delim_nrrd)}.map {|x| x.split(delim_nrrd)}
    meta_values = lines.reject {|x| !(x.include? delim_meta)}.map {|x| x.split(delim_meta)}.reject {|x| x.length != 2}

    header[:magic] = magic
    header[:nrrd]  = Hash[*nrrd_values.flatten]
    header[:meta]  = Hash[*meta_values.flatten]
    return header
  end

  ###############################################################
  ## return an array of the number of planes in each of the given files
  ###############################################################
  def self.get_planes(files)  
    files.delete_if {|file| file.eql?("-")}
    files.map { |file| head(file)[:nrrd]["sizes"].split(' ')[Axes[:z]].to_i }
  end

  ###############################################################
  ## Pad a nrrd file with zero up to the given max size
  ###############################################################
  def self.pad(file_in, file_out, max, min=nil)
    min ||= [0]*max.length # default to all 0's
    pad_opts = {}
    pad_opts["minimum"]  = min.join(' ')     # min positions along each axis
    pad_opts["maximum"]  = max.join(' ')     # max positions along each axis
    pad_opts["boundary"] = "pad"             # boundary behavior; fill new areas with nothing
    pad_opts["input"]    = "\"#{file_in}\""  # input file
    pad_opts["output"]   = "\"#{file_out}\"" # output file
    unu_call("pad", pad_opts)
  end

  ###############################################################
  ## Compress input file by summing along Z (and then reinserting the Z axis).
  ###############################################################
  def self.compress(file_in, file_out=nil, axis=Axes[:z])
    file_out ||= file_in
    unu_call("project -a #{axis} -m sum -i \"#{file_in}\" | unu axinsert -a #{axis} -o \"#{file_out}\"")
  end

  ###############################################################
  ## Divide input file by a given value (or another file).
  ###############################################################
  def self.divide(file_in, value, file_out=nil)
    file_out ||= file_in
    unu_call("2op / \"#{file_in}\" #{value} -o \"#{file_out}\"")
  end
  
  ###############################################################
  ## Multiply input file by a given value (or another file).
  ###############################################################
  def self.multiply(file_in, value, file_out=nil)
    file_out ||= file_in
    unu_call("2op x \"#{file_in}\" #{value} -o \"#{file_out}\"")
  end
  
  ###############################################################
  ## Join a set of nrrd files along a given axis.
  ###############################################################  
  def self.join(files_in, file_out, axis, sizes, meta={})
    join_opts = {}
    data_opts = {}
    make_opts = {}
    join_opts["input"] = files_in.join(' ')
    join_opts["axis"]  = axis
    data_opts[""] = "-"
    make_opts["encoding"]  = "raw"
    make_opts["endian"]    = "little"
    make_opts["size"]      = sizes.join(' ')
    make_opts["kind"]      = "space space space list" # X, Y, Z, and mass
    make_opts["spacing"]   = "1 1 1 NaN"
    make_opts["centering"] = "node node node node"
    make_opts["type"]      = "float" ## Added by ZK
    make_opts["unit"]      = "pixel pixel pixel pixel"
    make_opts["output"]    = "\"#{file_out}\""
    make_opts["keyvalue"]  = meta.map{|key, val| "\"#{key}:=#{val}\""}.join(' ') unless meta.empty?
    unu_call([["join", join_opts], ["data", data_opts], ["make", make_opts]])
  end
  
  ###############################################################
  ## Copy a single mass from a nrrd file to a new file.
  ###############################################################
  def self.write_mass(file_in, file_out, mass_number)
    header = head(file_in)
    masses = header[:meta]["Mims_mass_numbers"].split(' ').map {|x| x.to_f.round}
    max    = header[:nrrd]["sizes"].split(' ').map {|x| x.to_i - 1}
    min    = [0]*max.length
    return unless mass_index = masses.index(mass_number)
    min[Axes[:mass]] = max[Axes[:mass]] = mass_index
    opts = {}
    opts["minimum"] = min.join(' ')
    opts["maximum"] = max.join(' ')
    opts["input"]   = file_in
    opts["output"]  = file_out
    unu_call("crop", opts)
  end

end

###############################################################
##
###############################################################
def group_masses(fileset, masses, suffix_out="tmp")
  return fileset unless masses
  fileset.map do |files|
    files.map do |file|
      file_out = "#{file}.#{suffix_out}"
      header = Nrrd.head(file)
      sizes = header[:nrrd]["sizes"].split(' ')
      sizes[Axes[:mass]] = masses.length 
      header[:meta]["Mims_mass_numbers"] = ""
      tmps = []
      masses.each do |name, values|
        header[:meta]["Mims_mass_numbers"] += "#{name} "
        tmps << "#{file}.#{name}.tmp"
        values.each {|val| Nrrd.write_mass(file, tmps.last, val) }
      end
      Nrrd.join(tmps, "#{file}.#{suffix_out}", Axes[:mass], sizes, header[:meta])
      tmps.each {|tmp| File.delete(tmp) }
      
      file_out
    end
  end
end

###############################################################
## Compensate for varying numbers of planes between the given files,
## either by padding or compressing in Z.
## Returns the resulting filenames.
###############################################################
def normalize(fileset, opts={})
  opts[:compress]        ||= false
  opts[:scale_by_planes] ||= false
  opts[:suffix_out]      ||= "normalized"
  max_planes = Nrrd.get_planes(fileset.flatten).sort.last
  fileset.map do |files|    
    files.map do |file|
      if File.basename(file).eql?("-")
         file_out = "#{file}"
      else
         file_out = "#{file}.#{opts[:suffix_out]}"
         sizes = Nrrd.head(file)[:nrrd]["sizes"].split(' ')      
         if opts[:compress] # sum along z-axis
            Nrrd.compress(file, file_out)
            scale_factor = sizes[Axes[:z]].to_f/max_planes
            Nrrd.divide(file_out, scale_factor) if opts[:scale_by_planes]
         else # otherwise, pad in z
            sizes[Axes[:z]] = max_planes
            Nrrd.pad(file, file_out, sizes.map{|x| x.to_i-1})
         end
      end
      file_out
    end
  end
end

###############################################################
## Join input files together on a grid in X and Y.
## (Assumes dimensions already match between files.)
## Returns the output filename.
###############################################################
def tile(fileset, file_out)
  header = []
  ref_file = ""
  background_image_created = false
  # get a legit header
  fileset.each do |filenames|
    filenames.each do |file|
      if File.exists?(file)
          header  = Nrrd.head(file)
          ref_file = file
          break
      end
    end
  end
  size    = header[:nrrd]["sizes"].split(' ').map{|x| x.to_i}
  rows    = fileset.each_index.map {|i| "row#{i+1}.nrrd"}
  max_row = fileset.map {|row| row.length}.sort.last
  
  # create a background image if necessary
  fileset.each do |filenames|
    if filenames.include?("-")
       Nrrd.multiply(ref_file, 0, "background.nrrd")
       background_image_created = true
       break
    end
  end
  
  x = Axes[:x]; y = Axes[:y]
  fileset.each_index do |i|
    while fileset[i].index("-") != nil
       fileset[i][fileset[i].index("-")] = "background.nrrd"
    end
    size_row = size.clone
    size_row[x] = size[x]*fileset[i].length
    Nrrd.join(fileset[i], rows[i], x, size_row)
    size_row[x] = size[x]*max_row
    Nrrd.pad(rows[i], rows[i], size_row.map{|i|i-1})
  end
  size[x] *= max_row
  size[y] *= fileset.length
  Nrrd.join(rows, file_out, y, size, header[:meta])
  if background_image_created
    File.delete("background.nrrd")
  end
  fileset.each_index.map {|i| File.delete("row#{i+1}.nrrd")}
  
  file_out
end

###############################################################
## Load a grid of tab-delimited input nrrd filenames from the given text file.
## Each line specifies one row (rows can vary in length).
## Returns an array of arrays of filenames.
###############################################################
def load_layout(filename, delim_col = "\t", delim_row = $/)
  dir = File.dirname(Pathname.new(filename).realpath.to_s)
  fileset = File.open(filename,'r') {|f| f.read }.split(delim_row).map{|r| r.split(delim_col)}  
  unless Pathname.new(fileset[0][0]).absolute? 
    fileset.map! {|files| files.map! {|f| 
      if !f.eql?("-")
        "#{dir}/#{f}"
      else
        "#{f}"
      end}
    }
  end
end

###############################################################
## Return array of relative (to top left) horizontal and 
## vertical positions, in pixels, for the given nrrd files.
###############################################################
def get_pixel_positions(files, prototype, reverse) ## DJ:17/09/2014 : "reverse" argument added
  positions    = []
  um_per_px    = []
  
  horizontal_direction = 1
  if prototype
    horizontal_direction = -1 
  end

  # DJ: 09/17/2014
  vertical_direction = 1
  if reverse
    vertical_direction = -1 
  end
      
  files.each do |file|
    mims = Nrrd.head(file)[:meta]
    positions << mims["Mims_position"].split(',').reverse.map{|c| c.to_i}

    positions.last[0] *= horizontal_direction
    positions.last[1] *= vertical_direction  ## DJ: 09/14/2014

    um_per_px << mims["Mims_pixel_width"].to_f/1000
  end

  min_pos = positions.transpose.map{|c| c.sort.first}

  positions.each_with_index.map do |p, i|
    p.zip(min_pos).map{|c,m| ((c-m)/um_per_px[i]).round }
  end
end

###############################################################
## Return array of min and max strings for padding the given nrrd files.
###############################################################
def get_pad_values(files, compress, prototype, reverse) ## DJ:17/09/2014 : "reverse" argument added
  pos_pixels = get_pixel_positions(files, prototype, reverse) ## DJ:17/09/2014 : "reverse" argument added
  max_px     = pos_pixels.transpose.map{|x| x.sort.last}  
  maxes      = files.map { |f| Nrrd.head(f)[:nrrd]["sizes"].split(' ').map{|s| s.to_i - 1} }
  max_planes = 0
  if !compress
     max_planes = maxes.transpose[Axes[:z]].sort.last
  end   
  maxes.map {|max| max[Axes[:z]] = max_planes}

  pos_pixels.zip(maxes).map do |pix, max|
    pad_min = (pix.map{|c| 0-c} + [0, 0]) * ' '
    pad_max = (pix.zip(max_px).map{|c,m| m-c+max[0]} + max[2,2]) * ' '
    "-min #{pad_min} -max #{pad_max}"
  end
end

###############################################################
## Sum input files together with specified positioning.
## Returns the output filename.
###############################################################
def merge(files, pads, file_out)
  tmp_file = file_out + ".tmp"
  Nrrd.unu_call("pad -b pad #{pads.shift} -i \"#{files.shift}\" -o \"#{tmp_file}\"") # create canvas with first file

  files.zip(pads) do |file, pad| # combine with each subsequent file
    Nrrd.unu_call("pad -b pad #{pad} -i \"#{file}\" | #{Nrrd::Unu} 2op + \"#{tmp_file}\" - -o \"#{tmp_file}\"")
  end
  tmp_file
end

###############################################################
# Clean up any temp files.
###############################################################
def cleanup(files)
  files.each do |file|
    File.delete(file)
  end
end

###############################################################
# Sets the "Mims_position:=" meta data for the mosaic.
###############################################################
def set_positions_strings(files, file_out, tmp_out_file, prototype)
  positions    = []
  pos_x        = []
  pos_y        = []
  locations    = ""
      
  ## Build the list of tile positions.
  size = files.length
  i = 0
  files.each do |file|
    mims = Nrrd.head(file)[:meta]
    positions << mims["Mims_position"].split(',').reverse.map{|c| c.to_i}
    if mims.has_key?("Mims_tile_positions")
       locations << mims["Mims_tile_positions"]
    else
       locations << file << "," << positions.last[1].to_s() << "," << positions.last[0].to_s()
    end
    if !(i==size-1)
       locations << ";"
    end
    i+=1
  end

  ## Calculate the center position of the mosaic
  min_pos = positions.transpose.map{|c| c.sort.first}
  max_pos = positions.transpose.map{|c| c.sort.last}
  pos_x = (min_pos[1] + max_pos[1])/2
  pos_y = (min_pos[0] + max_pos[0])/2
  
  ## Caluculate the raster size.
  mims = Nrrd.head(tmp_out_file)  
  um_per_px = mims[:meta]["Mims_pixel_width"].to_f/1000
  x = mims[:nrrd]["sizes"].split(' ')[Axes[:x]].to_f
  y = mims[:nrrd]["sizes"].split(' ')[Axes[:y]].to_f
  raster_x = (um_per_px * x).round
  raster_y = (um_per_px * y).round
  
  ## Create the new header.
  header = IO.popen("unu head \"#{tmp_out_file}\"") {|f| f.read }
  data = IO.popen("unu data #{tmp_out_file}") {|f| f.read }
  
  #Works in v1.8
  #header.to_a()
  # to_a() depricated in ruby 1.9
  # this works in quick test
  headerlines = header.split("\n")
  # need to test a little more before changing, maybe add a version check

  File.open(file_out, 'w') {|f|
  puts "-----------------------------------------"

  headerlines.each do |line|
    #puts line
    if line.start_with?("Mims_position:=")
       f.write("Mims_position:="+pos_x.to_s()+","+pos_y.to_s())
       f.write("\n")
    elsif line.start_with?("Mims_tile_positions:=")
       # do nothing
    elsif line.start_with?("Mims_raster:=")
       #puts "RASTER!"
       f.write("Mims_raster:="+raster_x.to_s()+","+raster_y.to_s())
       f.write("\n")
    else
       f.write("#{line}\n")   
    end    
  end

  if prototype
    f.write("Mims_prototype:=true\n")
  end
  f.write("Mims_tile_positions:="+locations)
  f.write("\n")
  f.write("\n")
  puts "-----------------------------------------"
  f.write(data)
  }
end

###############################################################
## Combine a set of nrrd files into one, in one of two ways:
## * by joining files specified in layout file opts[:layout] together in X and Y.
## * by padding opts[:files] with extra space in X and Y and then summing together.
###############################################################
def mosaic(opts)
  if opts[:type] == :grid
    files = load_layout(opts[:layout])
    files2 = group_masses(files, opts[:masses])
    files2 = normalize(files2, opts)
    tile(files2, opts[:file_out])
  else
    pads = get_pad_values(opts[:files], opts[:compress], opts[:prototype], opts[:reverse]) ## DJ:09/17/2014 : "opts[:reverse]" argument was added.
    nrrd_files = group_masses(opts[:files], opts[:masses])    
    normalize_files = normalize([nrrd_files], opts)[0]
    files_to_delete = normalize_files.dup  
    tmp_out_file = merge(normalize_files, pads, opts[:file_out])
    set_positions_strings(opts[:files], opts[:file_out], tmp_out_file, opts[:prototype])
    cleanup(files_to_delete << tmp_out_file)
  end 
end

###############################################################
## Create a mosaic based on the given array of command-line arguments.
###############################################################
def main(args)
  options = {}
  parser = OptionParser.new do |opts|
    opts.banner = "Usage: #{File.basename($0)} [options] file1.nrrd file2.nrrd ..."
    opts.on("-t", "--type mosaic_type", [:grid, :fluid], "Choose type of mosaic to create ('grid' or 'fluid').") {|t| options[:type] = t}
    opts.on("-p", "--prototype", "Data from prototype, reverse x-axis ('fluid' mode only).") {|p| options[:prototype] = true}
    opts.on("-c", "--[no-]compress", "Compress each input file to a single-plane image.") { |c| options[:compress] = c }
    opts.on("-s", "--[no-]scale", "Scale counts by number of planes in each input file.") { |s| options[:scale_by_planes] = s }
    opts.on("-l", "--layout layout_filename", "Specify grid layout file.",
            "  (A text file containg input nrrd filenames; columns tab-separated, rows newline-separated)") { |f| options[:layout] = f }

    # DJ: 09/17/2014 : to reverse option
    opts.on("-r", "--reverse", "Reverse the tile rows ('fluid mode only')") { |r| options[:reverse] = true}

    opts.on("-o", "--output output_filename", "Specify output nrrd file.") { |f| options[:file_out] = f }
    opts.on_tail("-h", "--help", "Show this help message.") {STDERR.puts opts; exit}
  end
  if args.empty?
    STDERR.puts parser
    exit
  end
  parser.parse!(args)
  options[:files] = args unless args.empty?
  options[:file_out] ||= "mosaic.nrrd"
  
  unless options[:type]
    options[:type] = :grid
    options[:type] = :fluid if options[:files]
  end
  
  if options[:compress].nil?
     options[:compress] = true
  end
  
  if options[:prototype].nil? || options[:type] == :grid
     options[:prototype] = false
  end  

  ## DJ: 09/17/2014
  if options[:reverse].nil? || options[:type] == :grid
     options[:reverse] = false
  end  
  
  options[:layout] ||= "grid.txt" if options[:type] == :grid

  mosaic(options)
end

# Returns number of seconds since epoch
time1 = Time.now.to_i
main(ARGV) if __FILE__ == $0
time2 = Time.now.to_i
time_diff = time2 - time1
print "TOTAL_time = ", time_diff, " seconds.\n"
