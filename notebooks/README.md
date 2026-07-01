# Notebooks Directory

This directory is currently empty by design.

- **No notebooks containing confidential outputs are permitted.**
- To avoid accidental leakage of sensitive or proprietary data (which can easily happen in cached notebook cell outputs), Jupyter Notebooks are intentionally excluded from this public repository by default.
- **Exception**: Public, audit-approved notebooks (e.g., `literature_validation_overview.ipynb`) are allowed if they:
  - use only public datasets;
  - do not contain confidential outputs;
  - do not load proprietary models;
  - do not show point-to-point proprietary data in tables;
  - are fully auditable.
- All other public examples are maintained as reproducible and auditable Python scripts (see the `examples/` directory).

To run the approved public notebook locally, you can install the optional dependencies:
```bash
pip install -r requirements-notebook.txt
```
