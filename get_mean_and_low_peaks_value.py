import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import os
import numpy as np
from datetime import time
from scipy.signal import argrelextrema

if __name__ == "__main__":
    files = fd.askopenfilenames()

    for i, file in enumerate(files, 1):
        csv = pd.read_csv(file, delimiter=" ",
                          names=["date", "time", "nothing", "trashZ",
                                    "standarized", "trashz", "value"], index_col=False)

        times = csv["time"].to_list()
        start_time = times[0]
        stop_time = times[-1]
        probes = csv.index.tolist()
        probes_count = len(probes)


# =============================================================================
#         #dynamically creates size of graph
#         middle=np.shape(probes)[0]//2
#         end=middle*3//2
#         probes_frame = probes[middle:end]
#         func=np.vectorize(lambda x:x/20)
#         probes_frame=func(probes_frame)
# =============================================================================
        
        
        starting_time,ending_time=4800,6000
        probes_frame = probes[starting_time:ending_time]
        func=np.vectorize(lambda x:x/20)
        probes_frame=func(probes_frame)
        
        #initialization of important parameters
        values = csv["value"].tolist()[starting_time:ending_time]
        filename = os.path.basename(file)

        #old way of getting minimas
# =============================================================================
#         function to get the minimum values of peaks
#         moving_mean = np.append(np.diff(values), 0)
#         moving_mean[moving_mean > 10] = 0
#         moving_mean[moving_mean < -10] = 0
#         moving_mean[moving_mean != 0] = 1
#         moving_mean = np.multiply(moving_mean, values)
#         mean = np.mean(values)
#         moving_mean[moving_mean > mean] = 0
# =============================================================================
        


        values=np.array(values)
        minimas=argrelextrema(values, np.less)
        local_minimas=np.zeros(np.shape(values)[0])

        for i in range (0,np.shape(minimas)[1]):
            local_minimas[minimas[0][i]]=1
        
        local_minimas = np.multiply(local_minimas, values)
        mean = np.mean(values)
        local_minimas[local_minimas > mean] = 0
        number_of_low_peaks=0
        min_peak_mean=0
        for i in range (0,np.shape(local_minimas)[0]):
            if(local_minimas[i]!=0):
                number_of_low_peaks+=1
                min_peak_mean+=local_minimas[i]
        min_peak_mean/=number_of_low_peaks

        plt.figure(i)
        plt.plot(probes_frame, values)
        plt.plot(probes_frame, local_minimas)
        plt.legend(["Wartoci surowe", "lokalne minima"])
        plt.xlabel("Time[s]")
        plt.ylabel("CO2")
        plt.title(f'{filename} \n mean value = {mean},\n local minimas = {min_peak_mean}')

        plt.show()