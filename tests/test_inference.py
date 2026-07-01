import pytest
import numpy as np
import pandas as pd
from pvt_ml.inference import (
    prepare_hybrid_pt_input,
    predict_rsr,
    predict_hybrid_pt_profile,
    add_predictions_to_dataframe
)

class DummyModel:
    def predict(self, X):
        return [0.25, 0.50]

class DummyModelInvalid:
    pass

def test_prepare_hybrid_pt_input():
    df = pd.DataFrame({"P": [100.0, 200.0], "Pb": [400.0, 400.0], "T_C": [80.0, 80.0]})
    X = prepare_hybrid_pt_input(df)
    assert "P_over_Pb" in X.columns
    assert list(X.columns) == ["P_over_Pb", "Pb", "T_C"]
    assert list(X["P_over_Pb"]) == [0.25, 0.50]

def test_predict_rsr():
    model = DummyModel()
    df = pd.DataFrame({"P": [100.0, 200.0], "Pb": [400.0, 400.0], "T_C": [80.0, 80.0]})
    preds = predict_rsr(model, df)
    assert isinstance(preds, np.ndarray)
    assert preds.ndim == 1
    assert list(preds) == [0.25, 0.50]

def test_predict_rsr_missing_predict():
    model = DummyModelInvalid()
    df = pd.DataFrame({"P": [100.0], "Pb": [400.0], "T_C": [80.0]})
    with pytest.raises(ValueError, match="does not have a 'predict' method"):
        predict_rsr(model, df)

def test_add_predictions_to_dataframe():
    df = pd.DataFrame({"Rsb_scf_stb": [500.0, 500.0]})
    rsr_pred = [0.25, 0.50]
    df_out = add_predictions_to_dataframe(df, rsr_pred)
    assert "Rsr_pred" in df_out.columns
    assert "Rs_pred_scf_stb" in df_out.columns
    assert list(df_out["Rs_pred_scf_stb"]) == [125.0, 250.0]

def test_add_predictions_length_mismatch():
    df = pd.DataFrame({"Rsb_scf_stb": [500.0]})
    rsr_pred = [0.25, 0.50]
    with pytest.raises(ValueError, match="Length of predictions does not match"):
        add_predictions_to_dataframe(df, rsr_pred)

def test_predict_hybrid_pt_profile():
    model = DummyModel()
    df = pd.DataFrame({"P": [100.0, 200.0], "Pb": [400.0, 400.0], "T_C": [80.0, 80.0], "Rsb_scf_stb": [500.0, 500.0]})
    df_out = predict_hybrid_pt_profile(model, df)
    assert "Rsr_pred" in df_out.columns
    assert "Rs_pred_scf_stb" in df_out.columns
    assert list(df_out["Rsr_pred"]) == [0.25, 0.50]
    assert list(df_out["Rs_pred_scf_stb"]) == [125.0, 250.0]
