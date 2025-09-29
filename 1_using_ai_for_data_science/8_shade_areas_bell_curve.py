# Modify this plot below so we shade the probability/area
# of a golden retriever's weight being between 64 and 70 lbs.

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

mu, sigma = 64, 3
x = np.linspace(mu - sigma * 4, mu + sigma * 4, 1000)
y = norm.pdf(x, mu, sigma)
plt.plot(x, y)

plt.title("Weight Distribution of Golden Retrievers")
plt.xlabel("Weight (lbs)")
plt.ylabel("Probability Density")
plt.grid(True, alpha=0.3)
plt.show()
