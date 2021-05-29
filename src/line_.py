import numpy as np
import pandas as pd
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
from numpy import exp,sqrt,pi
import lmfit
from lmfit import Model
import glob2 as gl
import warnings
warnings.simplefilter('ignore',np.RankWarning)
from input_file import file_name
Batch=[]
Wafer=[]
Mask=[]



#----
data = {'Lot': [],
        'Wafer': [],
        'Mask': [],
        'TestSite': [],
        'Name': [],
        'Date': [],
        'Script ID': [],
        'Script Version': [],
        'Script Owner': [],
        'Operator': [],
        'Row': [],
        'Column': [],
        'ErrorFlag': [],
        'Error description': [],
        'Analysis Wavelength': [],
        'Rsq of Ref.spectrum (6th)': [],
        'Max trnasmission Ref.spec.(dB)': [],
        'Rsq of IV': [],
        'I at -1V': [],
        'I at 1V': []}

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.DataFrame(data)
#----
def polyfit(x, y, degree):
        results = {}
        coeffs = np.polyfit(x, y, degree)

        results['polynomial'] = coeffs.tolist()
        # r-squared
        p = np.poly1d(coeffs)
        yhat = p(x)
        ybar = np.sum(y) / len(y)  # 평균값
        ssreg = np.sum((yhat - ybar) ** 2)  # 실제값과 예측값차이
        sstot = np.sum((y - ybar) ** 2)  # 실제값과 평균값 차이
        results['determination'] = ssreg / sstot
        return results


for i in range(0,len(file_name)):

        tree = et.parse(file_name[i])
        root = tree.getroot()
        ModulatorSite = tree.findall('ElectroOpticalMeasurements/ModulatorSite')
        Modulator = tree.findall('ElectroOpticalMeasurements/ModulatorSite/Modulator')
        PortCombo = tree.findall('ElectroOpticalMeasurements/ModulatorSite/Modulator/PortCombo')
        TestSiteInfo_ = root.find("TestSiteInfo")
        WavelengthSweep = tree.findall('ElectroOpticalMeasurements/ModulatorSite/Modulator/PortCombo/WavelengthSweep')
        L = tree.findall('ElectroOpticalMeasurements/ModulatorSite/Modulator/PortCombo/WavelengthSweep/L')
        IL = tree.findall('ElectroOpticalMeasurements/ModulatorSite/Modulator/PortCombo/WavelengthSweep/IL')
        Voltage = tree.find('ElectroOpticalMeasurements/ModulatorSite/Modulator/PortCombo/IVMeasurement/Voltage')
        Current = tree.find('ElectroOpticalMeasurements/ModulatorSite/Modulator/PortCombo/IVMeasurement/Current')
        TestSiteInfo = TestSiteInfo_.attrib
        DesignParameter = tree.findall('ElectroOpticalMeasurements/ModulatorSite/Modulator/DeviceInfo/DesignParameters/DesignParameter')

        #---------rsq

        L_6 = L[6].text.split(',')
        IL_6 = IL[6].text.split(',')

        x = list(map(float, L_6))
        y = list(map(float, IL_6))

        f6 = np.polyfit(x, y, 6)
        p6 = np.poly1d(f6)
        # -----iv r
        Voltage = Voltage.text.split(',')
        Current = Current.text.split(',')

        Voltage = list(map(float, Voltage))
        Current_float = map(float, Current)
        Current = list(map(abs, Current_float))

        x_cut = Voltage[:10]
        y_cut = Current[:10]

        polyIV = polyfit(x_cut, y_cut, 13)['polynomial']
        poly1dIV = np.poly1d(polyIV)


        def foo(x, amp, b):
                return abs(amp * (exp(b * x) - 1)) + poly1dIV(x)


        my_model = Model(foo)
        result = my_model.fit(Current, x=Voltage, amp=0.1, b=0.1)

        best_f = result.best_fit.tolist()
        poly1dIV_list = list(poly1dIV(x_cut))

        yhat = best_f
        ybar = np.sum(Current) / len(Current)  # 평균값
        ssreg = np.sum((yhat - ybar) ** 2)  # 실제값과 예측값차이
        sstot = np.sum((Current - ybar) ** 2)  # 실제값과 평균값 차이
        results = ssreg / sstot

        if results > 0.95:
                Error = 'Ref.spec.Error'
                ErrorFlag = 1
        else:
                Error = 'No error'
                ErrorFlag = 0

        # -----------------------------------------
        data = {'Lot': TestSiteInfo['Batch'],
                'Wafer': TestSiteInfo['Wafer'],
                'Mask': TestSiteInfo['Maskset'],
                'TestSite': TestSiteInfo['TestSite'],
                'Name': Modulator[0].attrib['Name'],
                'Date': PortCombo[0].attrib['DateStamp'],
                'Script ID': 'process LMZ',
                'Script Version': '0.1',
                'Script Owner': 'B2',
                'Operator': ModulatorSite[0].attrib['Operator'],
                'Row': TestSiteInfo['DieRow'],
                'Column': TestSiteInfo['DieColumn'],
                'ErrorFlag': ErrorFlag,
                'Error description': Error,
                'Analysis Wavelength': DesignParameter[1].text,
                'Rsq of Ref.spectrum (6th)': polyfit(x, y, 6)['determination'],
                'Max trnasmission Ref.spec.(dB)': max(p6(x)),
                'Rsq of IV': results,
                'I at -1V': poly1dIV_list[4],
                'I at 1V': best_f[12]}

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        dfs = df.append(data, ignore_index=True)


        dfs.to_csv('./result.csv')


