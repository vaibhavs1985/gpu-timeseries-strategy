#!/usr/bin/env python
# coding: utf-8

# In[6]:

import nvsmi
import nvidia_smi
#import pandas as pd
#import numpy as np
#import pickle
#from sklearn.preprocessing import StandardScaler
#from sklearn.linear_model import LinearRegression
#from timeit import default_timer as timer
#import pickle
import sys
#import glob
#from sklearn.metrics import r2_score
import os

#from statsmodels.tsa.statespace.sarimax import SARIMAX
#from statsmodels.tsa.arima_process import ArmaProcess
#from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
#from statsmodels.tsa.stattools import adfuller
#import matplotlib.pyplot as plt

#from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

from time import sleep


#import nvidia_smi

nvidia_smi.nvmlInit()

gpu_freq = [135, 142, 150, 157, 165, 172, 180, 187, 195, 202, 210, 217, 225, 232, 240, 247, 255, 262, 270, 277, 285, 292, 300, 307, 315, 322, 330, 337, 345, 352, 360, 367, 375, 382, 390, 397, 405, 412, 420, 427, 435, 442, 450, 457, 465, 472, 480, 487, 495, 502, 510, 517, 525, 532, 540, 547, 555, 562, 570, 577, 585, 592, 600, 607, 615, 622, 630, 637, 645, 652, 660, 667, 675, 682, 690, 697, 705, 712, 720, 727, 735, 742, 750, 757, 765, 772, 780, 787, 795, 802, 810, 817, 825, 832, 840, 847, 855, 862, 870, 877, 885, 892, 900, 907, 915, 922, 930, 937, 945, 952, 960, 967, 975, 982, 990, 997, 1005, 1012, 1020, 1027, 1035, 1042, 1050, 1057, 1065, 1072, 1080, 1087, 1095, 1102, 1110, 1117, 1125, 1132, 1140, 1147, 1155, 1162, 1170, 1177, 1185, 1192, 1200, 1207, 1215, 1222, 1230, 1237, 1245, 1252, 1260, 1267, 1275, 1282, 1290, 1297, 1305, 1312, 1320, 1327, 1335, 1342, 1350, 1357, 1365, 1372, 1380, 1387, 1395, 1402, 1410, 1417, 1425, 1432, 1440, 1447, 1455, 1462, 1470, 1477, 1485, 1492, 1500, 1507, 1515, 1522, 1530]


def modeling(util_array):

    forecast = []
    for i in range(8):
        model = ARIMA(util_array[i],order=(1,1,1))
        model_fit = model.fit()
        forecast.append(model_fit.forecast(1)[0])
    return forecast


def get_gpu_util():
    gpu_util_avg = []
    for i in range(0,8):
        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)

        res = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
        gpu_util_avg.append(res.gpu)
    return gpu_util_avg
 




def get_df(prev_len, current_len):
    while True:
        df = pd.read_csv('util.csv')
        df_cpu = df['utilization.gpu [%]']
        cpu_numpy = df_cpu.to_numpy()
        cpu_numpy = cpu_numpy.reshape((-1,8))
        mycolumns = ['GPU1','GPU2','GPU3','GPU4','GPU5','GPU6','GPU7','GPU8']
        df_cpu = pd.DataFrame(data=cpu_numpy,columns=mycolumns)

        df_cpu['GPU1'] = df_cpu['GPU1'].str.replace('%','')
        df_cpu['GPU2'] = df_cpu['GPU2'].str.replace('%','')
        df_cpu['GPU3'] = df_cpu['GPU3'].str.replace('%','')
        df_cpu['GPU4'] = df_cpu['GPU4'].str.replace('%','')
        df_cpu['GPU5'] = df_cpu['GPU5'].str.replace('%','')
        df_cpu['GPU6'] = df_cpu['GPU6'].str.replace('%','')
        df_cpu['GPU7'] = df_cpu['GPU7'].str.replace('%','')
        df_cpu['GPU8'] = df_cpu['GPU8'].str.replace('%','')

        df_cpu = df_cpu.astype(float)
        print(current_len, len(df))
        if len(df)>current_len:
            current_len = len(df)
            break
        else:
            sleep(0.25)
            continue
    #df.drop(['UOPS_RETIRED  ','RESOURCE_STALLS.ANY '],axis=1,inplace=True)
    line_array = df_cpu.mean()
    #print('dataframe shape',df.shape)
    #print('line_array shape',line_array.shape)
    #print(df.columns)
    return line_array, prev_len, current_len


# In[8]:


core_freq = [x*1.0 for x in range(1200000,2300000,100000)]
uncore_freq = [x*1.0 for x in range(1300000000,2700000000,100000000)]
uncore_to_code = {}
for i,u in enumerate(uncore_freq):
    uncore_to_code[u] = hex(0x1010+257*i)



# In[13]:



