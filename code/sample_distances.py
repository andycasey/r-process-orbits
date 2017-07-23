
import os
import numpy as np
from isochrones import StarModel
from isochrones.mist import MIST_Isochrone
from astropy.table import Table

CLOBBER = False
DATA_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

data = Table.read(os.path.join(DATA_FOLDER, "literature.csv"), format="csv")
mist = MIST_Isochrone()

# minimum bound on distances of some stars to be 1 kppc
distance_bounds = {
    #"BPS CS 22183-031": (1000.0, 50000.0),
    "BPS CS 22892-052": (1000.0, 50000.0),
    "BPS CS 29497-004": (1000.0, 50000.0),
    "BPS CS 30306-132": (1000.0, 50000.0),
    "BPS CS 31078-018": (1000.0, 50000.0),
    "CS 29491-069": (1000.0, 50000.0),
    "J203843.2-002333": (1000.0, 50000.0),
}

N = len(data)

for i, star in enumerate(data):

    #if star["Name"] != "BPS CS 22183-031": continue
    if star["Name"] not in distance_bounds: continue

    print("{}/{}: {}".format(i, N, star["Name"]))

    output_path = os.path.join(DATA_FOLDER, "{}_mist_samples.csv".format(star["Name"]))

    if os.path.exists(output_path) and not CLOBBER:
        print("Skipping because {} exists".format(output_path))
        continue

    # Common keywords to all stars.
    kwds = dict(
        Teff=(star["teff"], star["e_teff"]),
        logg=(star["logg"], star["e_logg"]),
        feh=(star["feh"], star["e_feh"]) 
    )
    # Update kwds with magnitudes if available:
    # - 2MASS
    # - WISE
    # - SDSS

    columns = [
        ("J", "j_m_2mass", "j_msig_2mass"),
        ("H", "h_m_2mass", "h_msig_2mass"),
        ("K", "k_m_2mass", "k_msig_2mass"),
        #("W1", "w1mpro", "w1sigmpro"),
        #("W2", "w2mpro", "w2sigmpro"),
        #("W3", "w3mpro", "w3sigmpro"),
        #("G", "G", "ERR_G"),
        #("R", "R", "ERR_R"),
        #("I", "I", "ERR_I")
        ]

    for magnitude, column, error_column in columns:
        if np.isfinite(star[column]) and np.isfinite(star[error_column]):
            kwds[magnitude] = (star[column], star[error_column])

    # Update kwds with parallax if available.
    if np.isfinite(star["parallax"]):
        kwds["parallax"] = (star["parallax"], star["parallax_error"])

    print(kwds)
    model = StarModel(mist, **kwds)

    # Update uniform priors on age and distance.
    model._bounds["age"] = (np.log10(5.0e9), np.log10(13.721e9))
    model._bounds["distance"] = distance_bounds.get(star["Name"], (0, 50000.0))


    model.fit(refit=True, n_live_points=1000, evidence_tolerance=0.5)

    model.samples.to_csv(output_path)

    fig_output_path = os.path.join(
        DATA_FOLDER, "{}_mist_samples.pdf".format(star["Name"]))
    fig = model.corner_physical()
    try:
        fig.savefig(fig_output_path)
    except:
        continue

