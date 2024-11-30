from typing import TypedDict
from torch.utils.data import Dataset

class StatSummary(TypedDict):
    """First moment of given parameter (Mean, Standard Deviation)"""
    Mean: float
    StandardDeviation: float

class Restricted_InitialOrbitStatistics(TypedDict):
    """Initial orbital parameter statistics for restricted orbits"""
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

def generate_initial_orbit_samples_restricted(initial_orbit_stats: Restricted_InitialOrbitStatistics, n_samples: int) -> RestrictedIODDataset:
    ...
