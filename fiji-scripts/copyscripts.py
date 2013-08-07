#!/usr/bin/python
import sys
import shutil
import os

sourceFiles = os.listdir("OpenMIMS Scripts")
for i in range(len(sourceFiles)):
	sourceName = sourceFiles[i]
	if (sourceName != "README.txt"):
		shutil.copy2("OpenMIMS Scripts/" + sourceName, "/nrims/common/local/Fiji.app/plugins/Scripts/Plugins/OpenMIMS Scripts/")

