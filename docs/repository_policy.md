# Repository Policy

This repository strictly enforces confidentiality and reproducibility policies.

## Permitted Content
- Clean and reusable source code.
- Framework documentation.
- Approved data from published literature.
- Public results derived strictly from literature validation.
- Scripts and examples designed for public validation.

## Prohibited Content
- **Proprietary Data:** No proprietary datasets, including CSV, Excel, or other tabular files derived from restricted sources.
- **Proprietary Models:** No trained models (`.joblib`, `.pkl`) derived from proprietary data.
- **PVT Reports:** No original PVT reports (Mexican or otherwise).
- **Local Paths:** No hardcoded local paths (e.g., `C:\Users\...`).
- **Credentials:** No API keys, passwords, or tokens.
- **Dirty Notebooks:** No Jupyter Notebooks containing outputs of confidential data.
- **Proprietary Figures/Tables:** No visualizations or tables that expose proprietary data points.
- **Manuscript Files:** No Word or PDF files corresponding to the submitted manuscript.
- **Bulk Copies:** No unreviewed bulk copying of entire folders from the original research project.
- **Inference Scripts:** `inference.py` must not be modified to automatically load proprietary models from disk.
