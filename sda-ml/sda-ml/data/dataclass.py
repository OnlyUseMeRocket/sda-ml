from typing import TypedDict

class StatSummary(TypedDict):
    """First moment of given parameter (Mean, Standard Deviation)"""
    Mean: float
    StandardDeviation: float

class GD_LLA(TypedDict):
    """Geodedic Latitude [deg], Longitude [deg] and Altitude (either km or m)"""
    Latitude: float
    Longitude: float
    Altitude: float

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

