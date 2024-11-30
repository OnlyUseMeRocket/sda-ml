from typing import TypedDict
import numpy as np
import torch

class GD_LLA(TypedDict):
    """Geodedic Latitude [deg], Longitude [deg] and Altitude (either km or m)"""
    Latitude: float
    Longitude: float
    Altitude: float

def calculate_poincare_elements() -> torch.Tensor:
    ...

def gd_lla_to_ecef(GD_LAT: float, GD_LONG: float, alt: float) -> torch.Tensor:
    """Calculate topocentric position vector of observer in ECEF frame calculations done
        in meters
    
        Inputs:
            GD_LAT: float - Geodedic Latitude       [deg]
            GD_LONG: float - Geodedic Longitude     [deg]
            alt: float - Altitude                   [m]
    
        Outputs:
            R_ECEF: torch.Tensor (3,)               [m]
    """

    # Convert Angles to Radians
    GD_LAT = np.deg2rad(GD_LAT)
    GD_LONG = np.deg2rad(GD_LONG)

    distance_to_surface = 6378.137e3
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

    return R_ECEF

