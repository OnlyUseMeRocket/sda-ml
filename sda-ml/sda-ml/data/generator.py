from data.dataclass import Restricted_InitialOrbitStatistics
import torch
import numpy as np
from experiment.constants import PURDUE_ARMSTRONG
from data.geo_astro import (
    observer_ecef_to_eci, 
    observer_gd_lla_to_ecef, 
    kepler_to_cartesian_restricted,
    calculate_poincare_elements
)
from ml.data import RestrictedIODDataset
from astropy.time import Time


def generate_initial_orbit_dataset_restricted(initial_orbit_stats: Restricted_InitialOrbitStatistics, n_samples: int) -> RestrictedIODDataset:
    
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

    # Generate Object Coordinates and Poincar Elements
    obj_j2k = kepler_to_cartesian_restricted(initial_orbit_samples)
    poincare = calculate_poincare_elements(initial_orbit_samples)

    # Generate Geocentric Right Ascension
    right_ascension: list[float] = []
    geocentric_range = obj_j2k - obs_j2k
    for row in geocentric_range:
        x = row[0]
        y = row[1]
        ra = np.atan2(y, x)
        right_ascension.append(np.rad2deg(ra))
    
    ra_tensor = torch.tensor(right_ascension)
    ra_tensor = ra_tensor.reshape(-1, 1)
    IOD_Dataset = RestrictedIODDataset(ra_tensor, poincare)

    return IOD_Dataset


