#!/bin/bash


cd /tmp/

# Github point, need to grab ../raw/master/whatever/file
# NOT ../blob/master/whatever/file
echo -e "Downloading mosaic_nrrd.rb..."
curl https://github.com/NRIMS/workflow/raw/master/mosaic_nrrd/mosaic_nrrd.rb > mosaic_nrrd.rb

echo -e "Downloading unu from mosaic_nrrd..."
curl https://github.com/NRIMS/workflow/raw/master/mosaic_nrrd/unu-osx > unu-osx

# This gets you the page, not the file
# wget https://github.com/NRIMS/workflow/blob/master/mosaic_nrrd/unu

echo -e "Create '/usr/local/bin/' (Requires sudo)"
sudo mkdir -p /usr/local/bin/
echo -e "Move files to /usr/local/bin"
sudo mv mosaic_nrrd.rb /usr/local/bin/mosaic_nrrd
sudo mv unu-osx /usr/local/bin/unu

echo -e "Set permisions"
sudo chmod 755 /usr/local/bin/mosaic_nrrd
sudo chmod 755 /usr/local/bin/unu

echo -e "\n\nTest path:"
which unu
which mosaic_nrrd

echo -e "If you see '/usr/local/bin/unu' & '/usr/local/bin/mosaic_nrrd' above you're good."
echo -e "\n\nRun 'mosaic_nrrd -h' to see help.\nFin."
