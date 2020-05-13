import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import os

if __name__ == "__main__":
    files = fd.askopenfilenames()

    for i, file in enumerate(files, 1):
        csv = pd.read_csv(file, delimiter=" ",
                          names=["date", "time", "nothing", "trashZ",
                                    "standarized", "trashz", "value"], index_col=False)

        probes = csv.index.tolist()[5000:7500]
        values = csv["value"].tolist()[5000:7500]

        filename = os.path.basename(file)

        plt.figure(i)
        plt.subplot(2, 2, 1)
        plt.plot(probes, values)
        plt.title(f"Normal {filename}")
        plt.xlabel("Time [ms]")
        plt.ylabel("CO2")

        moving_mean = csv["value"].rolling(window=23).mean()[5000:7500]

        plt.subplot(2, 2, 2)
        plt.plot(probes, moving_mean)
        plt.title("Standarized")
        plt.xlabel("Time [ms]")
        plt.ylabel("CO2")

        standarized_values = csv["standarized"][5000:7500]
        standarized_moving_mean = csv["standarized"].rolling(window=10).mean()[5000:7500]

        plt.subplot(2, 2, 3)
        plt.plot(probes, standarized_values)
        plt.title("Standarized moving average")
        plt.xlabel("Time [ms]")
        plt.ylabel("CO2")

        plt.subplot(2, 2, 4)
        plt.plot(probes, standarized_moving_mean)
        plt.title("Moving average")
        plt.xlabel("Time [ms]")
        plt.ylabel("CO2")

        plt.show()
