# Presentation Notes

## Intro

  - Present SDA Problem
  - Present IOD
  - Current Research Areas
    - Mention current implementation of IOD relies of simplifying assumptions
  - Present ML Function Approximation
  
## Justification

  - present current problems of simplifying assumptions again
  - initial IOD heavily reliant on orbit improvement (LUMVE, Kalman Filtering) to yield acceptable approximations of an orbit
  - ML provides the unique opportunity to approximate the difficult dynamics of an orbit model
  - ML works best with expanded feature availability, which is becoming more viable as more SSA/SDA observable capabilities are going online

## Research Context

  - Chosen author selected for lit review performed an introductory experiment on potential viability of function approximation
  - Worked with a very small subset of orbits
    - Planar GEO ($0^{o}$ inclination)
    - Almost zero eccentricity
    - GEO orbit
  - Feature space: 1 variable (Right Ascension)
  - Label space: Poincare Orbit Elements 

## Methodology and Results (Paper)
  - Use of Extreme Learning Machine model
    - Quick computations
    - single hidden layer fully connected layer
    - Some academic heritage on its success at function approximation
  
  - Training data is not real (simulated)
    - initial states generated from normal distribution
    - angular right ascension measurements are calculated
    - measurement noise is added - approx 1.5 arc seconds

  - 1000 samples generated, 900 used for training, 100 used for validation
  - inference results compared with directly calculated poincare elements
  - Most results have high 90th percentile $R^{2}$ values (comparing inference to analytical poincare elements)

## Methodology and Results (Experiment)
  - No existing code base to use to reproduce results
  - created python scripts to reproduce results
  - number of nodes in the fully connected layer is changed to see difference in accuracy
  - ELM model definition
  - dataloader, training loop
  - plots

## Observations
 - Restricted orbit IOD better off with linear regression rather the deep learning, as linear regression is orders of magnitude more computationally efficient
 - single variable feature space leaves no room to effectively isolate non-linear effects. consider adding more observational parameters to the feature space
 - Consider use of real observations from various observer locations
 - consider use of neural ODE to approximate continuous time model instead of discrete inferences based on learned prior distribution

## Conclusion