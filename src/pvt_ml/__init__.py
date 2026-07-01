"""
pvt_ml: Reduced-input machine-learning reconstruction of differential-liberation
solution gas-oil ratio profiles.
"""

from .features import (
    compute_reduced_pressure,
    compute_reduced_rs,
    reconstruct_rs,
    add_hybrid_pt_features,
    get_hybrid_pt_input_columns,
    get_hybrid_pt_target_column
)

from .metrics import (
    mean_absolute_error,
    root_mean_squared_error,
    average_absolute_percentage_relative_error,
    coefficient_of_determination,
    regression_metrics
)

from .validation import (
    require_columns,
    require_numeric,
    require_positive,
    require_non_negative,
    validate_pressure_domain,
    validate_hybrid_pt_input
)

from .architectures import (
    get_default_extra_trees_params,
    create_extra_trees_regressor,
    create_standardized_extra_trees_pipeline,
    create_hybrid_pt_pipeline,
    get_supported_formulations,
    get_architecture_metadata
)

from .inference import (
    prepare_hybrid_pt_input,
    predict_rsr,
    predict_hybrid_pt_profile,
    add_predictions_to_dataframe
)

from .literature import (
    get_literature_validation_required_columns,
    get_literature_validation_optional_columns,
    get_literature_sources_required_columns,
    validate_literature_validation_dataframe,
    validate_literature_sources_dataframe,
    check_no_restricted_columns,
    summarize_literature_dataframe
)

__all__ = [
    "compute_reduced_pressure",
    "compute_reduced_rs",
    "reconstruct_rs",
    "add_hybrid_pt_features",
    "get_hybrid_pt_input_columns",
    "get_hybrid_pt_target_column",
    "mean_absolute_error",
    "root_mean_squared_error",
    "average_absolute_percentage_relative_error",
    "coefficient_of_determination",
    "regression_metrics",
    "require_columns",
    "require_numeric",
    "require_positive",
    "require_non_negative",
    "validate_pressure_domain",
    "validate_hybrid_pt_input",
    "get_default_extra_trees_params",
    "create_extra_trees_regressor",
    "create_standardized_extra_trees_pipeline",
    "create_hybrid_pt_pipeline",
    "get_supported_formulations",
    "get_architecture_metadata",
    "prepare_hybrid_pt_input",
    "predict_rsr",
    "predict_hybrid_pt_profile",
    "add_predictions_to_dataframe",
    "get_literature_validation_required_columns",
    "get_literature_validation_optional_columns",
    "get_literature_sources_required_columns",
    "validate_literature_validation_dataframe",
    "validate_literature_sources_dataframe",
    "check_no_restricted_columns",
    "summarize_literature_dataframe"
]
