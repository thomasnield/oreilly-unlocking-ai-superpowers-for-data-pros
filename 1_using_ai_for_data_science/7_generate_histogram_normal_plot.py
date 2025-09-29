# Take this code below and add a histogram with a normal distribution bell curve
# overlaid on top of it.


import numpy as np

x = np.array([27, 22, 28, 27, 26, 28, 31, 25, 25, 33, 24, 28, 28, 30,
              26, 25, 29, 28, 30, 30, 22, 28, 36, 27, 26, 31, 30, 25,
              27, 32, 25, 23, 27, 24, 28, 24, 27, 28, 30, 26, 33, 29,
              31, 29, 27, 31, 20, 23, 25, 29, 30, 24, 29, 28, 25, 25,
              30, 30, 27, 36, 26, 31, 24, 29, 34, 27, 23, 29, 27, 19,
              28, 30, 26, 29, 27, 30, 29, 28])

mean, median, std = np.mean(x), np.median(x), np.std(x, ddof=1)
