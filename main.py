import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the Excel file
exelFile = "CarDataset.xlsx"
data = pd.read_excel(exelFile)

varNames = data.columns.values.tolist()

j = 0


for i in varNames:
    if i != "MPG":
        plt.subplot(3, 2, j+1)
        plt.plot(data[i], data["MPG"], ".m")
        plt.title(f"MPG vs {i}")
        plt.xlabel(i)
        plt.ylabel("MPG")
        j += 1
        
    if j >= 6:
        break

# Ajustar layout
plt.subplots_adjust(hspace=1.4)
plt.subplots_adjust(wspace=0.5)

plt.show()
dd
