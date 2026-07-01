import pytest
from pvt_ml.architectures import (
    get_default_extra_trees_params,
    create_extra_trees_regressor,
    create_standardized_extra_trees_pipeline,
    create_hybrid_pt_pipeline,
    get_supported_formulations,
    get_architecture_metadata
)
from sklearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesRegressor

def test_get_default_extra_trees_params():
    params = get_default_extra_trees_params()
    assert params["n_estimators"] == 100
    assert params["max_depth"] == 5
    assert params["min_samples_leaf"] == 2
    assert params["random_state"] == 42

def test_create_extra_trees_regressor():
    model = create_extra_trees_regressor()
    assert isinstance(model, ExtraTreesRegressor)
    # Check it's unfitted (using a common sklearn heuristic or just checking type is enough for our test rules)
    
def test_create_standardized_extra_trees_pipeline():
    pipeline = create_standardized_extra_trees_pipeline()
    assert isinstance(pipeline, Pipeline)
    assert "scaler" in pipeline.named_steps
    assert "regressor" in pipeline.named_steps

def test_create_hybrid_pt_pipeline():
    pipeline = create_hybrid_pt_pipeline()
    assert isinstance(pipeline, Pipeline)

def test_get_supported_formulations():
    assert get_supported_formulations() == ["Hybrid-PT"]

def test_get_architecture_metadata():
    meta = get_architecture_metadata()
    assert meta["primary_formulation"] == "Hybrid-PT"
    assert "P_over_Pb" in meta["input_columns"]
    assert meta["target_column"] == "Rsr"
    assert "reconstruction" in meta
    assert meta["regressor"] == "ExtraTreesRegressor"
    assert meta["preprocessing"] == "StandardScaler"
