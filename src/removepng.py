import os
import glob2

pngfile ='./result/*.png'
[os.remove(f) for f in glob2.glob(pngfile)]
