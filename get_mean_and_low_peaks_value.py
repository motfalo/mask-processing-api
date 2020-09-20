import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import os
import numpy as np
from datetime import time
from scipy.signal import argrelextrema
from scipy.interpolate import interp1d
from scipy.signal import hilbert, chirp
import re

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


        # plt.figure(i)
        # plt.plot(probes_frame, values)
        # plt.plot(probes_frame, local_minimas)
        # plt.legend(["Wartoci surowe", "lokalne minima"])
        # plt.xlabel("Time[s]")
        # plt.ylabel("CO2")
        # plt.title(f'{filename} \n mean value = {mean},\n local minimas = {min_peak_mean}')

        # plt.show()
        
        #amplitude envelope
        analytic_signal = hilbert(values,None)
        amplitude_envelope = np.abs(analytic_signal)
        instantaneous_phase = np.unwrap(np.angle(analytic_signal))
        
        
        #getting minimas from amplitude envelope
        minimas=argrelextrema(amplitude_envelope, np.less)
        local_minimas=np.zeros(np.shape(values)[0])

        for j in range (0,np.shape(minimas)[1]):
            local_minimas[minimas[0][j]]=1
        
        local_minimas = np.multiply(local_minimas, values)
        mean = np.mean(values)
        local_minimas[local_minimas > mean] = 0
        number_of_low_peaks=0
        min_peak_mean=0
        for j in range (0,np.shape(local_minimas)[0]):
            if(local_minimas[j]!=0):
                number_of_low_peaks+=1
                min_peak_mean+=local_minimas[j]
        min_peak_mean/=number_of_low_peaks
        
        
        #create and interpolate vector of values
        interpolated_time=np.array([])
        interpolated_minimas=np.array([])
        for j in range (np.shape(local_minimas)[0]-1,-1,-1):
            if(local_minimas[j]!=0):
                interpolated_minimas=np.append(interpolated_minimas,local_minimas[j])
                interpolated_time=np.append(interpolated_time,[j])
                
        interpolated_time=np.flip(interpolated_time)
        
        interpolation = interp1d(interpolated_minimas, interpolated_time)
        #,bounds_error=False
        newx = probes_frame
        newy = interpolation(newx)
        plt.plot(newx, newy)
        plt.scatter(interpolated_minimas, interpolated_time, s=20)
        plt.show()
        
        fig = plt.figure(i)
        ax0 = fig.add_subplot(211)
        ax0.plot(probes_frame, values, label='signal')
        ax0.plot(probes_frame, amplitude_envelope, label='envelope')
        ax0.plot(probes_frame, newy, label='local_minimas')
        ax0.set_xlabel("time in seconds")
        ax0.set_ylabel("CO2")
        ax0.legend(["Wartosci surowe", "obwiednia", "newy"])
        ax0.set_title(f'{filename} \n mean value = {mean},\n local minimas = {min_peak_mean}')
        ax1 = fig.add_subplot(212)
        ax1.plot(probes_frame, values, label='signal')
        ax1.set_xlabel("time in seconds")
        ax1.legend(["Wartosci surowe", "obwiednia"])
        #ax1.set_ylim(0.0, 120.0)
        
        text = '--1--4-----5-3-22---55-'
        parts = [c for c in re.split(r'(-|\d+)', text) if c]
        data = np.array([(x, int(y)) for x, y in enumerate(parts) if y != '-'])
        x, y = data.T
        f = interp1d(x, y, kind='cubic')