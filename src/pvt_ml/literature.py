import pandas as pd
from typing import List, Dict, Any
from .validation import (
    require_columns,
    require_numeric,
    require_positive,
    require_non_negative,
    validate_pressure_domain
)

def get_literature_validation_required_columns() -> List[str]:
    """Returns the required columns for the literature_validation.csv schema."""
    return ["literature_fluid_id", "source_key", "P", "Pb", "T_C", "Rsb_scf_stb", "Rs_scf_stb"]

def get_literature_validation_optional_columns() -> List[str]:
    """Returns the optional columns for the literature_validation.csv schema."""
    return ["P_over_Pb", "Rsr"]

def get_literature_validation_allowed_columns() -> List[str]:
    """Returns all allowed columns for the literature_validation.csv schema."""
    return get_literature_validation_required_columns() + get_literature_validation_optional_columns()

def get_literature_sources_required_columns() -> List[str]:
    """Returns the required columns for the literature_sources.csv schema."""
    return ["source_key", "citation_short", "year", "literature_fluid_ids", "n_points", "notes"]

def get_literature_sources_allowed_columns() -> List[str]:
    """Returns all allowed columns for the literature_sources.csv schema."""
    return get_literature_sources_required_columns()

def check_allowed_columns(df: pd.DataFrame, allowed_columns: List[str]) -> None:
    """
    Checks that the DataFrame only contains allowed columns.
    Raises ValueError if any unexpected columns are present.
    """
    unexpected = [c for c in df.columns if c not in allowed_columns]
    if unexpected:
        raise ValueError(f"Unexpected columns detected: {unexpected}. Only allowed columns are permitted.")

def check_no_restricted_columns(df: pd.DataFrame) -> None:
    """
    Checks that the DataFrame does not contain columns forbidden due to confidentiality.
    Matching is case-insensitive.
    """
    restricted_keywords = [
        "field", "field_name", "well", "well_name", "asset", "asset_name",
        "report", "report_id", "pemex", "operator", "confidential", "proprietary"
    ]
    
    df_cols_lower = [str(c).lower() for c in df.columns]
    
    for col in df_cols_lower:
        for keyword in restricted_keywords:
            if keyword in col:
                raise ValueError(f"Restricted column detected: '{col}' (matches keyword '{keyword}'). Dataset cannot be validated.")

def validate_literature_validation_dataframe(df: pd.DataFrame, require_reduced_columns: bool = False) -> bool:
    """
    Validates a DataFrame against the expected public literature validation schema.
    """
    check_no_restricted_columns(df)
    check_allowed_columns(df, get_literature_validation_allowed_columns())
    
    required_cols = get_literature_validation_required_columns()
    require_columns(df, required_cols)
    
    numeric_cols = ["P", "Pb", "T_C", "Rsb_scf_stb", "Rs_scf_stb"]
    require_numeric(df, numeric_cols)
    
    require_non_negative(df, ["P", "Rs_scf_stb"])
    require_positive(df, ["Pb", "Rsb_scf_stb"])
    
    validate_pressure_domain(df, pressure_col="P", pb_col="Pb", allow_equal=True)
    
    if require_reduced_columns:
        optional_cols = get_literature_validation_optional_columns()
        require_columns(df, optional_cols)
        require_numeric(df, optional_cols)
        require_non_negative(df, optional_cols)
    else:
        # Check them if they exist
        for col in get_literature_validation_optional_columns():
            if col in df.columns:
                require_numeric(df, [col])
                require_non_negative(df, [col])
                
    return True

def validate_literature_sources_dataframe(df: pd.DataFrame) -> bool:
    """
    Validates a DataFrame against the expected public literature sources schema.
    """
    check_no_restricted_columns(df)
    check_allowed_columns(df, get_literature_sources_allowed_columns())
    
    required_cols = get_literature_sources_required_columns()
    require_columns(df, required_cols)
    
    require_numeric(df, ["year", "n_points"])
    require_positive(df, ["n_points"])
    
    return True

def summarize_literature_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generates a basic statistical summary of the literature validation DataFrame.
    """
    validate_literature_validation_dataframe(df, require_reduced_columns=False)
    
    return {
        "n_fluids": df["literature_fluid_id"].nunique(),
        "n_sources": df["source_key"].nunique(),
        "n_points": len(df),
        "min_P": float(df["P"].min()),
        "max_P": float(df["P"].max()),
        "min_Pb": float(df["Pb"].min()),
        "max_Pb": float(df["Pb"].max())
    }
