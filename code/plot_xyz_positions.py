

"""
Plot XYZ positions of r-process stars.
"""


import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
from astropy.table import Table
from glob import glob
from matplotlib.ticker import MaxNLocator
from matplotlib import cm


here = os.path.dirname(__file__)
DATA_FOLDER = os.path.join(here, "../data/")
FIGURES_FOLDER = os.path.join(here, "../article/figures/")

sample_paths = glob(os.path.join(DATA_FOLDER, "*_samples.pkl"))

literature = Table.read(os.path.join(DATA_FOLDER, "literature.csv"), format="csv")

ignore_object_names = (
    "BPS CS 29497-004",
    "BPS CS 22892-052",
    "J203843.2-002333"
)

N = 100 # Number of samples to draw
x_col, y_col, z_col, R_col = range(4)
kwds = dict(alpha=0.1, label="_")


for i, sample_path in enumerate(sample_paths):

    fig, axes = plt.subplots(2)

    color = cm.Set1(i)

    with open(sample_path, "rb") as fp:
        positions, properties = pickle.load(fp)

    indices = np.random.choice(np.arange(positions.shape[0]), N, replace=False)

    for index in indices:
        axes[0].plot(positions[index, x_col], positions[index, y_col],
            c=color, **kwds)

        axes[1].plot(positions[index, x_col], positions[index, z_col],
            c=color, **kwds)

    axes[0].set_title(sample_path)
    # Draw for legend?

# Draw satellite positions.

axes[0].set_xlabel(r"$x$ $({\rm kpc})$")
axes[0].set_ylabel(r"$y$ $({\rm kpc})$")
axes[1].set_xlabel(r"$x$ $({\rm kpc})$")
axes[1].set_ylabel(r"$z$ $({\rm kpc})$")

for ax in axes:
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(5))


raise a