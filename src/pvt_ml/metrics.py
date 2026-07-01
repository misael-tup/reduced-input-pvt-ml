import numpy as np
from typing import Dict, Any

def _check_inputs(y_true: Any, y_pred: Any) -> tuple:
    """Converts inputs to numpy float arrays, flattens them, and ensures matching lengths."""
    try:
        y_true_np = np.asarray(y_true, dtype=float).ravel()
        y_pred_np = np.asarray(y_pred, dtype=float).ravel()
    except ValueError as e:
        raise ValueError("Inputs must be convertible to numeric arrays.") from e
        
    if y_true_np.size == 0 or y_pred_np.size == 0:
        raise ValueError("Inputs must not be empty.")
        
    if y_true_np.shape[0] != y_pred_np.shape[0]:
        raise ValueError("y_true and y_pred must have the same length.")
    
    return y_true_np, y_pred_np

def mean_absolute_error(y_true: Any, y_pred: Any) -> float:
    """Calculates the Mean Absolute Error (MAE)."""
    y_true_np, y_pred_np = _check_inputs(y_true, y_pred)
    return float(np.mean(np.abs(y_true_np - y_pred_np)))

def root_mean_squared_error(y_true: Any, y_pred: Any) -> float:
    """Calculates the Root Mean Squared Error (RMSE)."""
    y_true_np, y_pred_np = _check_inputs(y_true, y_pred)
    return float(np.sqrt(np.mean(np.square(y_true_np - y_pred_np))))

def average_absolute_percentage_relative_error(y_true: Any, y_pred: Any) -> float:
    """
    Calculates the Average Absolute Percentage Relative Error (AAPRE).
    Excludes instances where y_true = 0 to avoid division by zero.
    Raises ValueError if all y_true values are zero.
    """
    y_true_np, y_pred_np = _check_inputs(y_true, y_pred)
    
    mask = y_true_np != 0
    if not np.any(mask):
        raise ValueError("All y_true values are zero. AAPRE cannot be computed.")
    
    y_true_filtered = y_true_np[mask]
    y_pred_filtered = y_pred_np[mask]
    
    absolute_relative_error = np.abs((y_true_filtered - y_pred_filtered) / y_true_filtered)
    return float(np.mean(absolute_relative_error) * 100.0)

def coefficient_of_determination(y_true: Any, y_pred: Any) -> float:
    """Calculates the Coefficient of Determination (R2 Score)."""
    y_true_np, y_pred_np = _check_inputs(y_true, y_pred)
    
    ss_res = np.sum(np.square(y_true_np - y_pred_np))
    ss_tot = np.sum(np.square(y_true_np - np.mean(y_true_np)))
    
    if ss_tot == 0:
        if np.allclose(y_true_np, y_pred_np):
            return 1.0
        else:
            return 0.0
            
    return float(1 - (ss_res / ss_tot))

def regression_metrics(y_true: Any, y_pred: Any) -> Dict[str, float]:
    """
    Computes a standard set of regression metrics: MAE, RMSE, AAPRE, and R2.
    Returns a dictionary of the calculated metrics.
    """
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": root_mean_squared_error(y_true, y_pred),
        "AAPRE": average_absolute_percentage_relative_error(y_true, y_pred),
        "R2": coefficient_of_determination(y_true, y_pred)
    }
