# Reviewer Guide

## 1. Purpose of this repository
This is a **public code and literature-validation companion repository** for the paper *"Reduced-input machine-learning reconstruction of differential-liberation solution gas-oil ratio profiles from digitized PVT reports"*. It provides a clean, reusable, and inspectable version of the core Hybrid-PT framework and its associated public literature dataset.

## 2. What reviewers can verify
Reviewers can inspect and verify the following components:
- The structure and unfitted pipeline of the **Hybrid-PT framework** (`src/pvt_ml/architectures.py`).
- The calculation of reduced pressure `P_over_Pb` and reduced Rs `Rsr` (`src/pvt_ml/features.py`).
- The reconstruction of absolute Rs via `Rs_pred_scf_stb = Rsb_scf_stb * Rsr_pred` (`src/pvt_ml/inference.py`).
- The validation logic and structure of the **Literature Validation Set** (`src/pvt_ml/literature.py`).
- The unit tests that ensure code integrity (`tests/`).
- The public data schema dictating mandatory formats and strict confidentiality checks (`docs/literature_schema.md`).
- The traceability of literature sources (`data/literature_sources.csv`).

## 3. What reviewers cannot reproduce from this public repository
Due to strict confidentiality agreements regarding Mexican PVT data, reviewers **cannot** reproduce the following elements from the paper:
- The training of the final machine learning model.
- The complete numerical metrics and parity plots presented in the paper.
- The Blind External Validation Set.
- The Additional Mexican PVT validation set.
- The proprietary trained models (`.joblib` / `.pkl`).
- The original, raw Mexican PVT reports.

## 4. Quickstart commands
To set up the repository, run the tests, and validate the public literature dataset, run the following commands from the root directory:

```bash
# Install the package in editable mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Validate the literature dataset using the strict CLI
python scripts/validate_literature_dataset.py --validation data/literature_validation.csv --sources data/literature_sources.csv

# Run the overview example script
python examples/literature_dataset_overview.py

# Run all unit tests
python -m pytest
```

## 5. Interpretation
The **Literature Validation Set** is fully public and allows reviewers to check the consistency, physical domain boundaries, and origin of the published dataset. However, it does not substitute the proprietary Mexican PVT datasets that were fundamentally used to train the final model presented in the paper.
