#!/usr/bin/python

import fnmatch
import os
import hashlib
import time

matches = []
paths = []
md5sums = []

start = "/nrims/home3/cpoczatek/Pictures/"
extensions = ('.jpg', '.jpeg', '.gif', '.png')

for root, dirnames, filenames in os.walk(start):
  for filename in filenames:
    if filename.endswith(extensions):
      
      # found a matching file
      matches.append(filename)
      
      # get full path
      fullpath = os.path.join(root, filename)
      paths.append(fullpath)

      # both this and the method below compute the same hash
      #
      #file_md5sum = hashlib.md5(open(fullpath, 'r').read()).hexdigest()
      #md5sums.append(file_md5sum)

      # computing the hash bit by bit is more memory efficient
      md5 = hashlib.md5()
      f = open(fullpath, 'r')
      while True:
        data = f.read(2**14)
        if not data:
            break
        md5.update(data)
      psum = md5.hexdigest()

      # get file metadata
      info = os.stat(fullpath)
      # format modification time
      modtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(info.st_mtime))
      
      # get ownership and permissions
      own = info.st_uid
      perm = oct(info.st_mode)[-3:]
      stats = (filename, fullpath, info.st_size, modtime, own, perm, psum)
      print stats

print "\n\nfin.\n"



