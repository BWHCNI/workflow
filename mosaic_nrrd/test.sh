#!/bin/bash

# This is a quick and dirty test script since I introduced a bug and didn't
# realize it.
#
# All this does is runs the script on the test data and diffs the headers 
# and the md5 hash of the data.


mkdir -p tmp

echo -e "Making nrrd's...."

# We need to cd into test_data to keep the tile_positions field in the header
# the same as the example nrrd's.
# Note, in the scripts calls there are some sub-shells made that aren't 
# redirecting stderr...

cd test_data
echo -e "--------------------------------" >> ../tmp/log
echo -e "Make grid mosaic:" >> ../tmp/log
echo -e "--------------------------------" >> ../tmp/log
../mosaic_nrrd.rb -t grid -l grid.txt -o ../tmp/new_grid.nrrd 090708-2-1_1*.nrrd 2>&1 >> ../tmp/log

echo -e "--------------------------------" >> ../tmp/log
echo -e "Make fluid mosaic:" >> ../tmp/log
echo -e "--------------------------------" >> ../tmp/log
../mosaic_nrrd.rb -t fluid -o ../tmp/new_fluid.nrrd 090708-2-1_1*.nrrd 2>&1 >> ../tmp/log
cd ..

echo -e "diffing grid nrrd's..."

# grid mosaic
echo -e "--------------------------------" >> ./tmp/log
echo -e "diff headers: new_grid.nrrd <---> mosaic_grid.nrrd " >> ./tmp/log
echo -e "--------------------------------"  >> ./tmp/log
diff -sy <(unu head ./tmp/new_grid.nrrd) <(unu head ./test_data/mosaic_grid.nrrd ) 2>&1 >> ./tmp/log

echo -e "--------------------------------" >> ./tmp/log
echo -e "diff md5 of data: new_grid.nrrd <---> mosaic_grid.nrrd " >> ./tmp/log
echo -e "--------------------------------"  >> ./tmp/log
diff -sy <(unu data ./tmp/new_grid.nrrd | md5sum) <(unu data ./test_data/mosaic_grid.nrrd | md5sum) 2>&1 >> ./tmp/log

echo -e "diffing fluid nrrd's..."

# fluid mosaic
echo -e "--------------------------------" >> ./tmp/log
echo -e "diff headers: new_fluid.nrrd <---> mosaic_fluid.nrrd" >> ./tmp/log
echo -e "--------------------------------"  >> ./tmp/log
diff -sy <(unu head ./tmp/new_fluid.nrrd) <(unu head ./test_data/mosaic_fluid.nrrd ) 2>&1 >> ./tmp/log

echo -e "--------------------------------" >> ./tmp/log
echo -e "diff md5 of data: new_fluid.nrrd <---> mosaic_fluid.nrrd" >> ./tmp/log
echo -e "--------------------------------"  >> ./tmp/log
diff -sy <(unu data ./tmp/new_fluid.nrrd | md5sum) <(unu data ./test_data/mosaic_fluid.nrrd | md5sum) 2>&1 >> ./tmp/log


