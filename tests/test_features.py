import pytest
import pandas as pd
from pvt_ml.features import (
    compute_reduced_pressure,
    compute_reduced_rs,
    reconstruct_rs,
    add_hybrid_pt_features,
    get_hybrid_pt_input_columns,
    get_hybrid_pt_target_column
)

def test_compute_reduced_pressure():
    df = pd.DataFrame({"P": [100.0, 200.0], "Pb": [400.0, 400.0]})
    df_out = compute_reduced_pressure(df)
    assert "P_over_Pb" in df_out.columns
    assert list(df_out["P_over_Pb"]) == [0.25, 0.5]

def test_compute_reduced_rs():
    df = pd.DataFrame({"Rs_scf_stb": [125.0, 250.0], "Rsb_scf_stb": [500.0, 500.0]})
    df_out = compute_reduced_rs(df)
    assert "Rsr" in df_out.columns
    assert list(df_out["Rsr"]) == [0.25, 0.5]

def test_reconstruct_rs():
    df = pd.DataFrame({"Rsr_pred": [0.25, 0.5], "Rsb_scf_stb": [500.0, 500.0]})
    df_out = reconstruct_rs(df)
    assert "Rs_pred_scf_stb" in df_out.columns
    assert list(df_out["Rs_pred_scf_stb"]) == [125.0, 250.0]

def test_add_hybrid_pt_features():
    df = pd.DataFrame({"P": [100.0], "Pb": [400.0], "T_C": [80.0]})
    df_orig = df.copy()
    df_out = add_hybrid_pt_features(df)
    assert "P_over_Pb" in df_out.columns
    assert list(df_out["P_over_Pb"]) == [0.25]
    # Check original dataframe wasn't modified
    assert "P_over_Pb" not in df_orig.columns

def test_get_hybrid_pt_input_columns():
    assert get_hybrid_pt_input_columns() == ["P_over_Pb", "Pb", "T_C"]

def test_get_hybrid_pt_target_column():
    assert get_hybrid_pt_target_column() == "Rsr"

def test_missing_columns():
    df = pd.DataFrame({"P": [100.0]})
    with pytest.raises(ValueError, match="Missing required columns"):
        compute_reduced_pressure(df)

def test_invalid_values():
    df = pd.DataFrame({"P": [100.0], "Pb": [-400.0]})
    with pytest.raises(ValueError):
        compute_reduced_pressure(df)
