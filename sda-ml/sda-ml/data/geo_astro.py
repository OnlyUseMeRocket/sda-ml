from experiment.constants import MU_EARTH_KM
import numpy as np
import torch
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as unit

def calculate_poincare_elements(orbit_samples: torch.Tensor) -> torch.Tensor:
    poincare_tensor = torch.Tensor()
    for row in orbit_samples:    
        sma = row[0]
        ecc = row[1]
        argp = np.deg2rad(row[2])
        ta = np.deg2rad(row[3])

        # Poincare Elements
        L = np.sqrt(MU_EARTH_KM * sma)
        I = np.rad2deg(argp + ta)
        g = np.sqrt(2 * L * (1 - np.sqrt(1 - (ecc ** 2)))) * np.cos(argp)

        # Append to Larger Tensor
        tensor_row = torch.Tensor([L, I, g])
        poincare_tensor = torch.cat((poincare_tensor, tensor_row.unsqueeze(0)), dim=0)
        
    return poincare_tensor


def observer_gd_lla_to_ecef(GD_LAT: float, GD_LONG: float, alt: float) -> EarthLocation:
    """Calculate topocentric position vector of observer in ECEF frame calculations done
        in meters
    
        Inputs:
            GD_LAT: float - Geodedic Latitude       [deg]
            GD_LONG: float - Geodedic Longitude     [deg]
            alt: float - Altitude                   [m]
    
        Outputs:
            R_ECEF: torch.Tensor (3,)               [km]
    """

    # Convert Angles to Radians
    GD_LAT = np.deg2rad(GD_LAT)
    GD_LONG = np.deg2rad(GD_LONG)

    distance_to_surface = 6378.137
    f = 1.0 / 298.257223563

    # Earth Eccentricity
    e = np.sqrt((2 * f) - (f ** 2))

    # Geodedic Radius
    N = distance_to_surface / np.sqrt(1 - (e ** 2) * (np.sin(GD_LAT) ** 2))

    # Calculate ECEF Position
    R_ECEF = torch.Tensor([
        (N + alt) * np.cos(GD_LAT) * np.cos(GD_LONG),
        (N + alt) * np.cos(GD_LAT) * np.sin(GD_LONG),
        (N * (1 - (e ** 2)) + alt) * np.sin(GD_LAT)
    ])

    obs_itrs = EarthLocation(
        x=R_ECEF[0] * unit.km,
        y=R_ECEF[1] * unit.km,
        z=R_ECEF[2] * unit.km
    )

    return obs_itrs

def observer_ecef_to_eci(observer_location: EarthLocation, J2K_Time: Time) -> torch.Tensor:
    obs_j2k = observer_location.get_gcrs(obstime=J2K_Time).represent_as('cartesian')
    obs_j2k = obs_j2k.get_xyz().value
    return torch.Tensor(obs_j2k)

def kepler_to_cartesian_restricted(orbit_samples: torch.Tensor) -> torch.Tensor:
    obj_cart = torch.Tensor()
    for row in orbit_samples:
        # Initialize Vars
        inc = 0
        raan = 0
        sma = row[0]
        ecc = row[1]
        argp = np.deg2rad(row[2])
        ta = np.deg2rad(row[3])
        orbital_param = sma * (1 - (ecc ** 2))

        # Define Perifocal State
        r_perifocal = torch.Tensor([
            (orbital_param * np.cos(ta)) / (1 + (ecc * np.cos(ta))),
            (orbital_param * np.sin(ta)) / (1 + (ecc * np.cos(ta))),
            0
        ]).reshape(3,1)

        # Rotation Matrices
        r3_raan = torch.Tensor([[np.cos(-raan), np.sin(-raan), 0],
                               [-1 * np.sin(-raan), np.cos(-raan), 0],
                               [0, 0, 1]])
        r1_inc = torch.Tensor([[1, 0, 0],
                              [0, np.cos(-inc), np.sin(-inc)],
                              [0, -1 * np.sin(-inc), np.cos(-inc)]])
        r3_argp = torch.Tensor([[np.cos(-argp), np.sin(-argp), 0],
                               [-1 * np.sin(-argp), np.cos(-argp), 0],
                               [0, 0, 1]])
        
        r_cartesian = torch.matmul(torch.matmul(torch.matmul(r3_raan, r1_inc), r3_argp), r_perifocal).reshape(1,3)

        obj_cart = torch.cat((obj_cart, r_cartesian.unsqueeze(0)), dim=0)
        
    obj_cart = obj_cart.reshape(obj_cart.shape[0], 3)
    return obj_cart


        



