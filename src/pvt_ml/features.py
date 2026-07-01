import pandas as pd
from typing import List
from .validation import require_columns, require_numeric, require_positive, require_non_negative

def compute_reduced_pressure(df: pd.DataFrame, pressure_col: str = "P", pb_col: str = "Pb", output_col: str = "P_over_Pb") -> pd.DataFrame:
    """
    Computes the reduced pressure (P / Pb).
    Returns a copy of the DataFrame with the new column added.
    """
    require_columns(df, [pressure_col, pb_col])
    require_numeric(df, [pressure_col, pb_col])
    require_non_negative(df, [pressure_col])
    require_positive(df, [pb_col])
    
    df_out = df.copy()
    df_out[output_col] = df_out[pressure_col] / df_out[pb_col]
    return df_out

def compute_reduced_rs(df: pd.DataFrame, rs_col: str = "Rs_scf_stb", rsb_col: str = "Rsb_scf_stb", output_col: str = "Rsr") -> pd.DataFrame:
    """
    Computes the reduced solution gas-oil ratio (Rs / Rsb).
    Returns a copy of the DataFrame with the new column added.
    """
    require_columns(df, [rs_col, rsb_col])
    require_numeric(df, [rs_col, rsb_col])
    require_non_negative(df, [rs_col])
    require_positive(df, [rsb_col])
    
    df_out = df.copy()
    df_out[output_col] = df_out[rs_col] / df_out[rsb_col]
    return df_out

def reconstruct_rs(df: pd.DataFrame, rsr_pred_col: str = "Rsr_pred", rsb_col: str = "Rsb_scf_stb", output_col: str = "Rs_pred_scf_stb") -> pd.DataFrame:
    """
    Reconstructs the absolute solution gas-oil ratio from its reduced form (Rsb * Rsr_pred).
    Returns a copy of the DataFrame with the reconstructed column added.
    """
    require_columns(df, [rsr_pred_col, rsb_col])
    require_numeric(df, [rsr_pred_col, rsb_col])
    require_positive(df, [rsb_col])
    
    df_out = df.copy()
    df_out[output_col] = df_out[rsb_col] * df_out[rsr_pred_col]
    return df_out

def add_hybrid_pt_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares input features for the Hybrid-PT formulation by calculating P_over_Pb.
    Returns a copy containing the base columns plus P_over_Pb.
    Does not compute Rsr to allow usage on datasets lacking the target variable.
    """
    df_out = compute_reduced_pressure(df, pressure_col="P", pb_col="Pb", output_col="P_over_Pb")
    return df_out

def get_hybrid_pt_input_columns() -> List[str]:
    """Returns the expected list of input features for the Hybrid-PT formulation."""
    return ["P_over_Pb", "Pb", "T_C"]

def get_hybrid_pt_target_column() -> str:
    """Returns the name of the target variable for the Hybrid-PT formulation."""
    return "Rsr"
