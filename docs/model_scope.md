# Model Scope and Methodological Details

This repository focuses on the **Hybrid-PT** formulation, the primary recommended approach from our paper.

## Formulation Overview
- The Hybrid-PT model predicts the reduced solution gas-oil ratio: **`Rsr`**.
- The physical solution gas-oil ratio (`Rs`) is then reconstructed using the formula: `Rs = Rsb * Rsr_pred`.
- The bubble-point solution gas-oil ratio (`Rsb`) is utilized as a physical scaling anchor.

## Scope and Limitations
- This model is **not** an equation of state.
- It **does not substitute** physical laboratory PVT analysis.
- It **does not impose** complete thermodynamic consistency across all possible conditions.
- Predictions **should not be extrapolated** outside the domain evaluated in the manuscript.

## Public implementation scope
This public implementation covers:
- computation of `P_over_Pb`;
- computation of `Rsr`;
- reconstruction of `Rs_pred_scf_stb = Rsb_scf_stb * Rsr_pred`;
- evaluation metrics;
- creation of unfitted Hybrid-PT pipelines;
- inference execution using a user-provided fitted model.

This public implementation **does not** cover:
- training of the final model presented in the article;
- loading of proprietary fitted models;
- full numerical reproduction of the paper;
- calibration with proprietary data.
