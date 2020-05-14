import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import os
import numpy as np
from datetime import time

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

        probes_frame = probes[5000:7500]
        values = csv["value"].tolist()[5000:7500]
        moving_mean = np.append(np.diff(values), 0)
        moving_mean[moving_mean > 10] = 0
        moving_mean[moving_mean < -10] = 0
        moving_mean[moving_mean != 0] = 1
        moving_mean = np.multiply(moving_mean, values)
        mean = np.mean(values)
        moving_mean[moving_mean > mean] = 0
        filename = os.path.basename(file)

        plt.figure(i)
        # plt.subplot(2, 1, 1)
        plt.plot(probes_frame, values)
        plt.plot(probes_frame, moving_mean)
        plt.legend(["Normal", "Standarized"])
        plt.title(f"{filename}")
        plt.xlabel("Time")
        plt.ylabel("CO2")

        # plt.subplot(2, 1, 2)
        # plt.plot(probes, moving_mean)
        # plt.title("Standarized")
        # plt.xlabel("Time")
        # plt.ylabel("CO2")

        x=np.sum(moving_mean)
        moving_mean[moving_mean!=0]=1
        x=x/np.sum(moving_mean)
        # print(x)

# =============================================================================
#         standarized_values = csv["standarized"][5000:7500]
#         standarized_moving_mean = csv["standarized"].rolling(window=10).mean()[5000:7500]
# 
#         plt.subplot(2, 2, 3)
#         plt.plot(probes, standarized_values)
#         plt.title("Standarized moving average")
#         plt.xlabel("Time [ms]")
#         plt.ylabel("CO2")
# 
#         plt.subplot(2, 2, 4)
#         plt.plot(probes, standarized_moving_mean)
#         plt.title("Moving average")
#         plt.xlabel("Time [ms]")
#         plt.ylabel("CO2")
# 
# =============================================================================
        plt.show()
