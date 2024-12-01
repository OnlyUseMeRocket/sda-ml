from typing import TypedDict
from torch.utils.data import Dataset
import torch
from data.experiment import PURDUE_ARMSTRONG
from data.geo_astro import observer_ecef_to_eci, observer_gd_lla_to_ecef, kepler_to_cartesian_restricted
from astropy.time import Time

class StatSummary(TypedDict):
    """First moment of given parameter (Mean, Standard Deviation)"""
    Mean: float
    StandardDeviation: float

class Restricted_InitialOrbitStatistics(TypedDict):
    """Initial orbital parameter statistics for restricted orbits
    Inputs:
        SemiMajorAxis: Semi-Major Axis of Restricted Orbit [km or m]
        Eccentricity: Eccentricity of Restricted Orbit [NO DIM]
        ArgPeriapsis: Argument of Periapsis [deg]
        MeanAnomaly: Mean Anomaly [deg]

    NOTE: General reminder to always consider units when switching between m and km
    (I'm looking at you graviatational constant !!!!!)
    """
    SemiMajorAxis: StatSummary
    Eccentricity: StatSummary
    ArgPeriapsis: StatSummary
    MeanAnomaly: StatSummary

class RestrictedIODDataset(Dataset):
    def __init__(self) -> None:
        ...
    def __len__(self) -> int:
        ...
    
    def __getitem__(self, index: int) -> tuple[float, tuple[float, ...]]:
        ...

def generate_initial_orbit_dataset_restricted(initial_orbit_stats: Restricted_InitialOrbitStatistics, n_samples: int):
    
    # Define Data Mean and Covariance
    data_mean = torch.tensor([initial_orbit_stats['SemiMajorAxis']['Mean'],
                              initial_orbit_stats['Eccentricity']['Mean'],
                              initial_orbit_stats['ArgPeriapsis']['Mean'],
                              initial_orbit_stats['MeanAnomaly']['Mean']])

    data_st_dev = torch.tensor([initial_orbit_stats['SemiMajorAxis']['StandardDeviation'],
                              initial_orbit_stats['Eccentricity']['StandardDeviation'],
                              initial_orbit_stats['ArgPeriapsis']['StandardDeviation'],
                              initial_orbit_stats['MeanAnomaly']['StandardDeviation']])
    
    data_variance = data_st_dev ** 2
    data_cov_matrix = torch.diag(data_variance)

    # Generate Samples
    print(data_mean)
    print(data_cov_matrix)
    distribution = torch.distributions.multivariate_normal.MultivariateNormal(data_mean, data_cov_matrix)
    
    # The tuple is shaped that way as the input is a torch.Size, which is a tuple of (row, col)
    # Variables: [SMA, Eccentricity, ArgPeriapsis, MeanAnomaly]
    initial_orbit_samples = distribution.sample((n_samples, ))

    # Generate Observer Coordinates
    obs_ecef = observer_gd_lla_to_ecef(PURDUE_ARMSTRONG['Latitude'],
                                       PURDUE_ARMSTRONG['Longitude'],
                                       PURDUE_ARMSTRONG['Altitude'])
    
    obs_j2k = observer_ecef_to_eci(obs_ecef, Time.now())
    obj_j2k = kepler_to_cartesian_restricted(initial_orbit_samples)


    return (obs_j2k, obj_j2k)


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