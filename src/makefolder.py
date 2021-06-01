import os
import glob2
from input_file import file_name


def createfolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('ERROR')

for i in range(0,len(file_name)):
    file_name_list = file_name[i].split('/')
    path_file = file_name_list[-1].split('\\')
    #print(path_file)
    createfolder('./result/{}/{}/{}'.format(path_file[-4], path_file[-3], path_file[-2]))
    createfolder('./result/{}'.format('csv'))