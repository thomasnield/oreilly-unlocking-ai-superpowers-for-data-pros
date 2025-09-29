# Modify this code below so we can perform a logarithmic transformation
# to this tornado width data

import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("./data/tornado.csv")

x = df['TOR_WIDTH'].values

plt.hist(x,bins=30, color='#002d8b')
plt.title('Histogram of Tornado Width')
plt.xlabel('Tornado Width')
plt.ylabel('Frequency')
plt.show()
