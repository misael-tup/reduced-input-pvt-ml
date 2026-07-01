# Literature Dataset Schema

The **Literature Validation Set** aims to provide a safe, reproducible, and fully public validation dataset for the `pvt_ml` framework, composed strictly of data extracted from published, non-proprietary sources.

**CRITICAL NOTE**: This dataset must **never** be mixed with the proprietary Development Set, the Blind External Validation Set, or the Additional Mexican PVT validation set.

## `literature_validation.csv`

This file contains the individual PVT data points.

### Allowed Columns
- **`literature_fluid_id`**: Anonymized public identifier (e.g., L2, L3).
- **`source_key`**: Short key matching the source in `literature_sources.csv`.
- **`P`**: Pressure stage (psia).
- **`Pb`**: Bubble-point pressure (psia).
- **`T_C`**: Reservoir temperature (°C).
- **`Rsb_scf_stb`**: Bubble-point solution gas-oil ratio (SCF/STB).
- **`Rs_scf_stb`**: Experimental solution gas-oil ratio (SCF/STB).
- **`P_over_Pb`** *(Optional)*: Reduced pressure.
- **`Rsr`** *(Optional)*: Reduced solution gas-oil ratio.

*Note: Optional columns may be omitted in the raw CSV, as they can be reconstructed mathematically.*

## `literature_sources.csv`

This file contains the metadata and traceability information for the literature data.

### Allowed Columns
- **`source_key`**: Short key for the source.
- **`citation_short`**: Short citation string.
- **`year`**: Publication year.
- **`literature_fluid_ids`**: The fluid IDs associated with this source.
- **`n_points`**: Number of retained data points.
- **`notes`**: Public notes for traceability.

**Note:** No additional columns are allowed unless the public schema is updated and reviewed.

## Prohibited Columns
To ensure no proprietary data leaks, the following columns (and variations) are strictly prohibited and will cause validation to fail:
- `field`, `field_name`
- `well`, `well_name`
- `asset`, `asset_name`
- `report`, `report_id`
- `pemex`, `operator`
- `confidential`, `proprietary`

## Traceability Criteria
All identifiers used must be completely public and anonymous. Traceability must refer only to the publicly available literature source and not to any internal databases.
