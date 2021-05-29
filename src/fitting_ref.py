#from importing_1 import D07 ,D08_0526,D08_0528,D08_0712,D23_0528,D23_0531,D23_0603,D24_0528,D24_0528_1,D24_0531,D24_0603
#from input_file import file_name
import numpy as np
import pandas as pd
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
from numpy import exp,sqrt,pi

import glob2 as gl
import warnings
warnings.simplefilter('ignore',np.RankWarning)
from parsing1 import ref_IL1, ref_L1,L1,L2,L3,L4,L5,L6

#ref 4,5,6차 fitting
def polyfit(x,y,degree):
    results = {}
    coeffs = np.polyfit(x,y,degree)
    results['polynomial'] = coeffs.tolist()
    # r-squared
    p = np.poly1d(coeffs)
    yhat = p(x)
    ybar = np.sum(y) / len(y)  # 평균값
    ssreg = np.sum((yhat - ybar) ** 2)  # 실제값과 예측값차이
    sstot = np.sum((y - ybar) ** 2)  # 실제값과 평균값 차이
    results['determination'] = ssreg / sstot
    return results
p4_list=[]
p5_list=[]
p6_list=[]
rsquared4_list=[]
rsquared5_list=[]
rsquared6_list=[]
p1_list_fit=[]
p2_list_fit=[]
p3_list_fit=[]
p4_list_fit=[]
p5_list_fit=[]
p6_list_fit=[]


for i in range(0,len(ref_L1)):
    #4차
    f4 =np.polyfit(ref_L1[i],ref_IL1[i],4)
    p4=np.poly1d(f4)
    rsqaured4=polyfit(ref_L1[i],ref_IL1[i],4)['determination']
    p4_list.append(p4(ref_L1[i]).tolist())
    rsquared4_list.append(rsqaured4)

    #5차
    f5 =np.polyfit(ref_L1[i],ref_IL1[i],5)
    p5=np.poly1d(f5)
    rsqaured5=polyfit(ref_L1[i],ref_IL1[i],5)['determination']
    p5_list.append(p5(ref_L1[i]).tolist())
    rsquared5_list.append(rsqaured5)
    #6차
    f6 =np.polyfit(ref_L1[i],ref_IL1[i],6)
    p6=np.poly1d(f6)
    rsqaured6=polyfit(ref_L1[i],ref_IL1[i],6)['determination']
    p6_list.append(p6(ref_L1[i]).tolist())
    rsquared6_list.append(rsqaured6)

    p1_list_fit.append(p6(L1[i]))
    p2_list_fit.append(p6(L2[i]))
    p3_list_fit.append(p6(L3[i]))
    p4_list_fit.append(p6(L4[i]))
    p5_list_fit.append(p6(L5[i]))
    p6_list_fit.append(p6(L6[i]))
    #print(p1_list_fit)
#print(rsqaured4,rsqaured5,rsqaured6)
   # print(rsqaured4)
#print(p6_list[0])
#print(rsquared4_list[0])
