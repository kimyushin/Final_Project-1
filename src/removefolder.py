import shutil
import glob2


[shutil.rmtree(f) for f in glob2.glob('./result/*')]
print('result all removed')


