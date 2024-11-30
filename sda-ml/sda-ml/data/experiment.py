from data.generator import Restricted_InitialOrbitStatistics
from data.geo_astro import GD_LLA

INITIAL_ORBIT_PARAMS: Restricted_InitialOrbitStatistics = {
    'SemiMajorAxis': {
        'Mean': 42164.,
        'StandardDeviation': 100.
    },
    'ArgPeriapsis': {
        'Mean': 0.,
        'StandardDeviation': 90.
    },
    'Eccentricity': {
        'Mean': 0.015,
        'StandardDeviation': 0.001
    },
    'MeanAnomaly': {
        'Mean': 0.,
        'StandardDeviation': 90.
    }
}

# Altitude in meters
PURDUE_ARMSTRONG: GD_LLA = {
        'Latitdue': 40.43157,
        'Longitude': 273.085549,
        'Altitude': 192.5
}

