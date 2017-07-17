
import numpy as np
import os
import pickle
from astropy import units
from astropy.table import Table
from galpy.orbit import Orbit
from galpy.potential import MWPotential2014 as mw

np.random.seed(42)


DATA_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

data = Table.read(os.path.join(DATA_FOLDER, "literature.csv"), format="csv")

# Number of realizations to do per star
N, ro, vo = (1000, 8.0, 220.0)
ts = np.linspace(0, 10, 10000) * units.Gyr

for i, star in enumerate(data):

    star_name = star["Name"]
    output_path = os.path.join(DATA_FOLDER, "{}_orbit_samples.pkl".format(star_name))

    print("On {}: {}".format(i, star_name))
    
    if os.path.exists(output_path) and not CLOBBER:
        print("Skipping because {} exists".format(output_path))
        continue

    posterior_path = os.path.join(DATA_FOLDER, "{}_mist_samples.csv".format(star_name))

    if not os.path.exists(posterior_path):
        print("Skipping because {} does not exist".format(posterior_path))
        continue

    posterior = Table.read(posterior_path, format="csv")

    orbits = []
    for i in range(N):
        print("Integrating {}/{} for {}".format(i, N, star_name))

        distance = np.random.choice(posterior["distance_0"]) / 1000.0 # [kpc]

        # If we have parallax, then take Gaia proper motions. Otherwise, UCAC5.
        if np.isfinite(star["parallax"]):
            pmra, e_pmra = ("pmra_gaia", "pmra_error")
            pmdec, e_pmdec = ("pmdec_gaia", "pmdec_error")

        else:
            pmra, e_pmra = ("pmRA", "e_pmRA")
            pmdec, e_pmdec = ("pmDE", "e_pmDE")

        pm_ra = np.random.normal(star[pmra], star[e_pmra])
        pm_dec = np.random.normal(star[pmdec], star[e_pmdec])
        v_hel = np.random.normal(star["vrad"], star["e_vrad"])

        orbit = Orbit(
            vxvv=[star["RA"], star["DEC"], distance, pm_ra, pm_dec, v_hel],
            radec=True, ro=ro, vo=vo)
        orbit.integrate(ts, mw)
        orbits.append(orbit)

    # Save the xyrz values.
    positions \
        = np.array([[o.x(ts), o.y(ts), o.z(ts), o.R(ts)] for o in orbits])
    properties = np.array([[o.rap(), o.rperi(), o.e(), o.zmax()] for o in orbits])

    with open(output_path, "wb") as fp:
        pickle.dump((positions, properties), fp, -1)

    # Print some summary things.
    properties = {
        "r_apocenter": np.array([o.rap() for o in orbits]),
        "r_pericenter": np.array([o.rperi() for o in orbits]),
        "eccentricity": np.array([o.e() for o in orbits]),
        "z_max": np.array([o.zmax() for o in orbits])
    }

    contents = []
    for key, values in properties.items():
        q = np.percentile(values, [16, 50, 84])
        cen, pos, neg = (q[1], q[2] - q[1], q[0] - q[1])
        contents.append("{0}: {1:.2f} ({2:+.2f} {3:.2f})".format(key, cen, pos, neg))

    print("\n".join([star_name] + contents))

    output_path = os.path.join(DATA_FOLDER, "{}_orbit_summary.txt".format(star_name))
    with open(output_path, "w") as fp:
        fp.write("\n".join(contents))

