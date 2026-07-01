# reduced-input-pvt-ml

**Public code and literature-validation companion repository for the reduced-input Hybrid-PT workflow.**

## Overview
This repository contains the public, clean, and reusable codebase associated with the paper: *"Reduced-input machine-learning reconstruction of differential-liberation solution gas-oil ratio profiles from digitized PVT reports"* (submitted to Geoenergy Science and Engineering).

The objective is to document the reduced-input Hybrid-PT workflow for reconstructing discrete solution gas-oil ratio (Rs) profiles. 

## Repository Status
The core public package is implemented. The repository includes:
- feature engineering utilities;
- physical-domain validation helpers;
- regression metrics;
- unfitted Hybrid-PT pipeline factory;
- inference helpers for user-provided fitted models.

## Core package
The following modules have been created:
- `src/pvt_ml/features.py`
- `src/pvt_ml/validation.py`
- `src/pvt_ml/metrics.py`
- `src/pvt_ml/architectures.py`
- `src/pvt_ml/inference.py`

Please note that `architectures.py` only creates unfitted pipelines, and `inference.py` only uses user-provided models. This repository does not include any fitted models or proprietary data.

## Development setup
To install the public package in editable mode and run the unit tests (which use dummy values, not real data):

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix/macOS:
# source .venv/bin/activate

pip install -e .
pip install -r requirements-dev.txt
python -m pytest
```
## Public and Restricted Materials
- This repository **does not** contain proprietary Mexican PVT datasets used for training, blind validation, or additional post-development validation in the paper.
- It **does not** contain the final trained machine learning models (`.joblib` / `.pkl`) derived from proprietary data.
- It **does not** promise complete numerical reproducibility of the paper's figures and tables due to confidentiality restrictions.
- The **Literature Validation Set** exists as a prepared public dataset in `data/`, but it does not permit complete numerical reproduction of the paper because the final trained models derived from proprietary data are not published.

## Planned Structure
- `src/pvt_ml/`: Core framework and reusable code.
- `docs/`: Documentation on data availability, model scope, and repository policies.
- `data/`: Will contain approved public datasets (e.g., Literature Validation Set).
- `models/`: Reserved for future approved demonstration artifacts, if any. No models trained on proprietary data will be released.

## Citation
Please refer to the `CITATION.cff` file for the recommended software citation. The formal reference for the associated paper will be added here once it is published.
