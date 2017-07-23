

"""
Plot generalised histograms of eccentricities that we beleive for r-process stars.
"""


import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
from astropy.table import Table
from glob import glob
from matplotlib.ticker import MaxNLocator


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
    
fig, ax = plt.subplots()

kwds = dict(histtype="step", normed=True, bins=np.linspace(0, 1, 100),
    alpha=0.9, lw=2)

for i, sample_path in enumerate(sample_paths):

    object_name = os.path.basename(sample_path).split("_")[0]

    mist_path = sample_path.replace("orbit_samples.pkl", "mist_samples.csv")
    mist_samples = Table.read(mist_path, format="csv")

    literature_match = literature[literature["Name"] == object_name]
    literature_logg = literature_match["logg"][0]
    literature_e_logg = literature_match["e_logg"][0]


    if object_name in ignore_object_names:
        dists = np.percentile(mist_samples["distance_0"], [16, 50, 84]) * 1e-3
        print("Ignoring {} (dist @ {:.2f} ({:+.2f}, {:+.2f})".format(
            object_name, dists[1], dists[2] - dists[1], dists[1] - dists[0]))

        continue


    print(object_name, literature_logg, np.median(mist_samples["logg_0_0"]))

    with open(sample_path, "rb") as fp:
        positions, properties = pickle.load(fp)

    eccentricities = properties[:, 2]
    if not np.all(np.isfinite(eccentricities)):
        print("Not showing {} because not all eccentricities were finite"\
            .format(object_name))
        continue

    _ = ax.hist(eccentricities, label="_", **kwds)
    color = _[2][0].get_edgecolor()
    ax.plot([0], [-1], c=color, label=object_name)

ax.set_ylim(0, ax.get_ylim()[1])

ax.set_xlabel(r"${\rm Eccentricity,}$ $e$")

ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(5))

plt.legend(loc="upper left", frameon=False, fontsize=10, ncol=1)

fig.tight_layout()

fig.savefig(os.path.join(FIGURES_FOLDER, "eccentricities_pdf.pdf"), dpi=300)
fig.savefig(os.path.join(FIGURES_FOLDER, "eccentricities_pdf.png"), dpi=300)
