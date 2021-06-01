import glob2
import data

path = './data/**/*LMZ*.xml'

# path = './*'
#path로 받을것 ,r 첨가
file_name=glob2.glob(path)

file_name_1=glob2.glob('../data/**/*LMZ*.xml')
#print(file_name_1)
