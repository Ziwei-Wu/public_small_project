#Script to untar data retrieved from the LTA by using wget
#It will DELETE the .tar file after extracting it.

import os
import glob

for filename in glob.glob("SRM*.tar"):
  outname=filename.split("%")[-1]
  os.rename(filename, outname)
  os.system('tar -xvf '+outname)
  os.system('rm -r '+outname )

  print outname+' untarred.'
