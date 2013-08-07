import sys

import com.nrims as nrims

ui = nrims.UI.getInstance()
if ui==None:
  print "ui==None"
else:
  print "ui exists"

rm = RoiManager.getInstance()
if rm==None:
  print "rm==None"
else:
  print "rm exists"