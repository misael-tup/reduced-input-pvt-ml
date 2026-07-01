from typing import Dict, Any, List
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import ExtraTreesRegressor
from .features import get_hybrid_pt_input_columns, get_hybrid_pt_target_column

def get_default_extra_trees_params() -> Dict[str, Any]:
    """Returns the default configuration parameters for the ExtraTreesRegressor."""
    return {
        "n_estimators": 100,
        "max_depth": 5,
        "min_samples_leaf": 2,
        "random_state": 42
    }

def create_extra_trees_regressor(**overrides) -> ExtraTreesRegressor:
    """
    Constructs an unfitted ExtraTreesRegressor using default parameters,
    allowing for explicit parameter overrides.
    """
    params = get_default_extra_trees_params()
    params.update(overrides)
    return ExtraTreesRegressor(**params)

def create_standardized_extra_trees_pipeline(**overrides) -> Pipeline:
    """
    Creates an unfitted scikit-learn Pipeline with a StandardScaler and an ExtraTreesRegressor.
    """
    return Pipeline([
        ("scaler", StandardScaler()),
        ("regressor", create_extra_trees_regressor(**overrides))
    ])

def create_hybrid_pt_pipeline(**overrides) -> Pipeline:
    """
    Returns an unfitted standardized ExtraTrees pipeline intended for the Hybrid-PT formulation.
    Expected input columns: ["P_over_Pb", "Pb", "T_C"]
    """
    return create_standardized_extra_trees_pipeline(**overrides)

def get_supported_formulations() -> List[str]:
    """Returns a list of supported model formulations."""
    return ["Hybrid-PT"]

def get_architecture_metadata() -> Dict[str, Any]:
    """Returns methodological metadata about the framework's architecture."""
    return {
        "primary_formulation": "Hybrid-PT",
        "input_columns": get_hybrid_pt_input_columns(),
        "target_column": get_hybrid_pt_target_column(),
        "reconstruction": "Rs_pred_scf_stb = Rsb_scf_stb * Rsr_pred",
        "regressor": "ExtraTreesRegressor",
        "preprocessing": "StandardScaler"
    }
