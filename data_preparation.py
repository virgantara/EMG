import os
import numpy as np
import pandas as pd
import math
from digital_processing import bp_filter, notch_filter, plot_signal
from feature_extraction_v2 import features_estimation, time_features_estimation,frequency_features_estimation
import re

base_path = 'FileTXTMyomes2023/G3'


features_names = ['VAR', 'RMS', 'IEMG', 'MAV', 'LOG', 'WL', 'ACC', 'DASDV', 'ZC', 'WAMP', 'MYOP', "FR", "MNP", "TP",
                      "MNF", "MDF", "PKF", "WENT"]

sampling_frequency = 1024
frame = 120
step = 60
x_gm, x_ta, x_vm = [],[],[]
x = []
# writer = pd.ExcelWriter('output_sampling'+str(sampling_frequency)+'_frame'+str(frame)+'_step'+str(step)+'.xlsx')
df = pd.DataFrame(columns=features_names)
for folder_class in sorted(os.listdir(base_path)):
    subpaths = os.path.join(base_path,folder_class)
    print(folder_class)
    for subpath in sorted(os.listdir(subpaths)):
        
        file_path = os.path.join(base_path,folder_class,subpath)
#         print(file_path)
#         tmp = []
        emg_signal = []
        file1 = open(file_path, 'r', encoding='iso-8859-1')
        lines = file1.readlines()
        counter = 1
        for line in lines:
            
            tmp = line.replace("\n","")
            tmp = re.findall(r"[-+]?\d*\.\d+|\d+", tmp)
            
            if len(tmp) == 1:
                tmp = tmp[0]
                emg_signal.append(tmp)
                
        signal = np.array(emg_signal).astype(np.float32)
        signal = signal.reshape((signal.size,))
        filtered_signal = signal
        emg_features, features_names = features_estimation(filtered_signal, '',sampling_frequency, frame, step)
        emg_features = emg_features.T
        d = pd.DataFrame(emg_features)
        d.columns = features_names
        d['target'] = folder_class
#             print(path)
        df = df.append([d],ignore_index = True)
        

                
df.to_csv('cls_sampling_'+str(sampling_frequency)+'_frame'+str(frame)+'_step'+str(step)+'.csv')
# writer.save()               