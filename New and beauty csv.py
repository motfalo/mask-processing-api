import pandas as pd
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    files = fd.askopenfilenames()

    for i, file in enumerate(files, 1):
        csv = pd.read_csv(file, delimiter=';', skiprows=lambda x: x % 2, names=['time[ms]', 'Zz'])
        csv = pd.DataFrame(csv.Zz.str.split('z ',1).tolist(),
                           columns=['Z','unfiltered'])
        # csv['unfiltered'] = csv['unfiltered'].astype(int)

        # times = csv['time[ms]'].tolist()
        values = csv['unfiltered'].tolist()
        values = list(filter(None, values))
        values = list(map(int, values))

        # probes = csv.index.tolist()

        # print(probes)
        # print(values)
        # print(len(probes))
        probes = range(len(values))
        print(len(values))

        plt.figure()
        plt.plot(probes, values)
        plt.show()

        # print(csv)
        # csv = pd.read_csv(file, delimiter=" ",
        #                   names=["date", "time", "nothing", "trashZ",
        #                             "standarized", "trashz", "value"], index_col=False)
