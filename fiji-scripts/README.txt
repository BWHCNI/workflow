This folders contains our Fiji scripts.

The sub dir 'OpenMIMS Scripts' can be symlinked to from within your local 
'Fiji.app/plugins/Scripts/Plugins/' directory for easy development within
the Fiji script editor/menu system.

Do something analogous to:
cd ~/Fiji.app/plugins/Scripts/Plugins/
ln -s ~/workflow_scripts/fiji-scripts/OpenMIMS\ Scripts/ OpenMIMS\ Scripts

Development should occur in 'OpenMIMS_Scripts_devel'.

"Proper" development:
1) check out workflow_scripts/fiji-scripts/ (this is obviously already done).
2) create symlink as above.
3) Start your IDE (Fiji!), open 'Script Editor', create myScript_.py in 'OpenMIMS_Scripts_devel' and hack away.
4) Don't forget 'svn add'.
5) Commit as needed.
6) When ready for enduser consumption 'svn move myScript_.py ../OpenMIMS\ Scripts/' .
7) Push to update site, update enduser installs (e.g. common) as needed.
8) When fixing bugs, edit files -in place- in 'OpenMIMS Scripts', committing as needed.  Repeat 7.


#############################################
Random notes:

This -package- import: import com.nrims as nrims 
Will only work if fiji is started with this flag 
./ImageJ-linux64 -Dpython.cachedir.skip=false 

Run script from command line:
./ImageJ-linux64 -Dpython.cachedir.skip=false --allow-multiple /nrims/home3/cpoczatek/Fiji_test/Tables_test_.py


If you want to clear the "Open Recent" menu in the script editor
open ~/.imagej/IJ_Prefs.txt and cut the lines begining with:
".script.editor.recent"


