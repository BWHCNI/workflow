This folders contains our Fiji scripts.

The sub dir 'OpenMIMS Scripts' can be symlinked to from within your local 
'Fiji.app/plugins/Scripts/Plugins/' directory for easy development within
the Fiji script editor/menu system.

Do something analogous to:
cd ~/Fiji.app/plugins/Scripts/Plugins/
ln -s ~/workflow_scripts/fiji-scripts/OpenMIMS\ Scripts/ OpenMIMS\ Scripts

Random notes:

This -package- import: import com.nrims as nrims 
Will only work if fiji is started with this flag 
./ImageJ-linux64 -Dpython.cachedir.skip=false 

Run script from command line:
./ImageJ-linux64 -Dpython.cachedir.skip=false --allow-multiple /nrims/home3/cpoczatek/Fiji_test/Tables_test_.py
