import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import os
import numpy as np

#program shows raw data from second to third minute

if __name__ == "__main__":
    files = fd.askopenfilenames()
    graph_elements=np.shape(files)
    
    values=[]
    filename=[]
    

    for i, file in enumerate(files, 1):
        csv = pd.read_csv(file, delimiter=" ",
                          names=["date", "time", "nothing", "trashZ",
                                    "standarized", "trashz", "value"], index_col=False)

        filename.append(os.path.basename(file))
        probes = csv.index.tolist()
        probes_count = len(probes)



        probes_frame = probes[2400:3800]
        values.append(csv["value"].tolist()[2400:3800])
        func=np.vectorize(lambda x:x/20)
        probes_frame=func(probes_frame)
        
        
    
    plt.figure(1)
    for i in range (0,graph_elements[0]):
        plt.plot(probes_frame, values[i], linewidth =0.5)
        plt.legend(filename)
        plt.title("porównanie rozwiązań")
        plt.xlabel("Time[s]")
        plt.ylabel("CO2")
        plt.show()
        
