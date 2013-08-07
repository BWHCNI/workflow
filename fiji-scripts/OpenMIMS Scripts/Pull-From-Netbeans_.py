from subprocess import call

IJ.log("copy: /nrims/home3/cpoczatek/NetBeansProjects/OpenMIMS/trunk/dist/Open_MIMS.jar")
call(["cp", "/nrims/home3/wang2/NetBeansProjects/trunk/dist/Open_MIMS.jar", "/nrims/home3/wang2/Fiji.app/plugins/Open_MIMS.jar"])
IJ.log("to: /nrims/home3/cpoczatek/Fiji.app/plugins/Open_MIMS.jar")
IJ.doCommand("Refresh Menus")
IJ.log("call: \"Refresh Menus\" (update jars)")