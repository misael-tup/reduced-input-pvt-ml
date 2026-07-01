import numpy as np
import pandas as pd
from typing import Any
from .features import (
    add_hybrid_pt_features,
    get_hybrid_pt_input_columns,
    reconstruct_rs
)
from .validation import (
    require_columns,
    require_numeric,
    require_positive
)

def prepare_hybrid_pt_input(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares the input DataFrame for Hybrid-PT inference by ensuring P_over_Pb exists
    and selecting the required columns.
    Returns a new DataFrame containing only the required input columns.
    """
    input_cols = get_hybrid_pt_input_columns()
    
    if "P_over_Pb" not in df.columns:
        df_processed = add_hybrid_pt_features(df)
    else:
        df_processed = df.copy()
        
    require_columns(df_processed, input_cols)
    require_numeric(df_processed, input_cols)
    
    return df_processed[input_cols]

def predict_rsr(model: Any, df: pd.DataFrame) -> np.ndarray:
    """
    Generates predictions for Rsr using the provided model or pipeline.
    Expects a fitted model with a 'predict' method.
    Returns a numpy array of predictions.
    """
    if not hasattr(model, "predict"):
        raise ValueError("The provided model does not have a 'predict' method.")
        
    X = prepare_hybrid_pt_input(df)
    predictions = model.predict(X)
    try:
        return np.asarray(predictions, dtype=float).ravel()
    except ValueError as exc:
        raise ValueError("Model predictions must be numeric.") from exc

def add_predictions_to_dataframe(df: pd.DataFrame, rsr_pred: Any, rsb_col: str = "Rsb_scf_stb") -> pd.DataFrame:
    """
    Adds Rsr_pred to the DataFrame and reconstructs the absolute Rs_pred_scf_stb.
    Returns a copy of the DataFrame with the new columns.
    """
    try:
        rsr_pred_np = np.asarray(rsr_pred, dtype=float).ravel()
    except ValueError as exc:
        raise ValueError("Predictions array must be numeric.") from exc
        
    if rsr_pred_np.size == 0:
        raise ValueError("Predictions array cannot be empty.")
    if len(df) != len(rsr_pred_np):
        raise ValueError("Length of predictions does not match number of rows in DataFrame.")
        
    require_columns(df, [rsb_col])
    require_numeric(df, [rsb_col])
    require_positive(df, [rsb_col])
    
    df_out = df.copy()
    df_out["Rsr_pred"] = rsr_pred_np
    
    df_out = reconstruct_rs(df_out, rsr_pred_col="Rsr_pred", rsb_col=rsb_col, output_col="Rs_pred_scf_stb")
    
    return df_out

def predict_hybrid_pt_profile(model: Any, df: pd.DataFrame) -> pd.DataFrame:
    """
    Executes the full Hybrid-PT inference workflow:
    1. Prepares features.
    2. Predicts Rsr.
    3. Reconstructs Rs_pred_scf_stb.
    Returns a copy of the original DataFrame augmented with the predictions.
    """
    rsr_pred = predict_rsr(model, df)
    return add_predictions_to_dataframe(df, rsr_pred)
