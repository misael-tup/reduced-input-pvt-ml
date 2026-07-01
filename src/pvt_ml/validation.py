import pandas as pd
from typing import List

def require_columns(df: pd.DataFrame, columns: List[str]) -> None:
    """Verifies that all specified columns are present in the DataFrame."""
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def require_numeric(df: pd.DataFrame, columns: List[str]) -> None:
    """Verifies that the specified columns contain numeric data."""
    require_columns(df, columns)
    for col in columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column '{col}' must contain numeric data.")

def require_positive(df: pd.DataFrame, columns: List[str]) -> None:
    """Verifies that the specified columns contain strictly positive values (> 0)."""
    require_numeric(df, columns)
    for col in columns:
        if not (df[col] > 0).all():
            raise ValueError(f"Column '{col}' must contain strictly positive values (> 0).")

def require_non_negative(df: pd.DataFrame, columns: List[str]) -> None:
    """Verifies that the specified columns contain non-negative values (>= 0)."""
    require_numeric(df, columns)
    for col in columns:
        if not (df[col] >= 0).all():
            raise ValueError(f"Column '{col}' must contain non-negative values (>= 0).")

def validate_pressure_domain(df: pd.DataFrame, pressure_col: str = "P", pb_col: str = "Pb", allow_equal: bool = True) -> None:
    """
    Validates the physical pressure domain for differential liberation data.
    Ensures P >= 0, Pb > 0, and P <= Pb (or P < Pb).
    """
    require_non_negative(df, [pressure_col])
    require_positive(df, [pb_col])
    
    if allow_equal:
        if not (df[pressure_col] <= df[pb_col]).all():
            raise ValueError(f"Values in '{pressure_col}' must be less than or equal to '{pb_col}'.")
    else:
        if not (df[pressure_col] < df[pb_col]).all():
            raise ValueError(f"Values in '{pressure_col}' must be strictly less than '{pb_col}'.")

def validate_hybrid_pt_input(df: pd.DataFrame) -> None:
    """Validates the input requirements for the Hybrid-PT formulation."""
    required_cols = ["P_over_Pb", "Pb", "T_C"]
    require_columns(df, required_cols)
    require_numeric(df, required_cols)
    require_positive(df, ["Pb"])
    require_non_negative(df, ["P_over_Pb"])
