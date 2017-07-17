
import os
import numpy as np
from isochrones import StarModel
from isochrones.mist import MIST_Isochrone
from astropy.table import Table

DATA_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

data = Table.read(os.path.join(DATA_FOLDER, "literature.csv"), format="csv")
mist = MIST_Isochrone()

N = len(data)

for i, star in data:

    print("{}/{}: {}".format(i, N, star["Name"]))

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
    # - APASS
    


    # Update kwds with parallax if available.
    if np.isfinite(star["parallax"]):
        kwds["parallax"] = (star["parallax"], star["parallax_error"])

    model = StarModel(mist, **kwds)

    # Update uniform priors on age and distance.
    model._bounds["age"] = (np.log10(10.0e9), np.log10(13.721e9))
    model._bounds["distance"] = (0, 30000.0)
    model.fit(refit=True, n_live_points=1000, evidence_tolerance=0.5)
    model.samples.to_csv(
        os.path.join(DATA_FOLDER, "{}_mist_samples.csv".format(star["Name"])))


    # Print out quantile summaries for each star.
    raise a