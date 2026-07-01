import pytest
import pandas as pd
from pvt_ml.literature import (
    get_literature_validation_required_columns,
    get_literature_validation_optional_columns,
    get_literature_sources_required_columns,
    get_literature_validation_allowed_columns,
    get_literature_sources_allowed_columns,
    validate_literature_validation_dataframe,
    validate_literature_sources_dataframe,
    check_no_restricted_columns,
    summarize_literature_dataframe
)

def test_get_columns():
    req_val = get_literature_validation_required_columns()
    assert "P" in req_val
    assert "Pb" in req_val
    assert "Rsb_scf_stb" in req_val
    
    opt_val = get_literature_validation_optional_columns()
    assert "P_over_Pb" in opt_val
    assert "Rsr" in opt_val
    
    req_src = get_literature_sources_required_columns()
    assert "source_key" in req_src
    assert "year" in req_src

def test_allowed_columns():
    allow_val = get_literature_validation_allowed_columns()
    assert "P" in allow_val
    assert "P_over_Pb" in allow_val
    
    allow_src = get_literature_sources_allowed_columns()
    assert "source_key" in allow_src
    assert "year" in allow_src

def test_check_no_restricted_columns():
    df_valid = pd.DataFrame({"P": [100.0], "Pb": [400.0]})
    check_no_restricted_columns(df_valid)
    
    df_invalid = pd.DataFrame({"P": [100.0], "field_name": ["some_field"]})
    with pytest.raises(ValueError, match="Restricted column detected.*field"):
        check_no_restricted_columns(df_invalid)

    df_invalid_2 = pd.DataFrame({"P": [100.0], "FieldCode": ["some_field"]})
    with pytest.raises(ValueError, match="Restricted column detected.*field"):
        check_no_restricted_columns(df_invalid_2)

    df_invalid_3 = pd.DataFrame({"P": [100.0], "operator_name": ["PEMEX"]})
    with pytest.raises(ValueError, match="Restricted column detected.*operator"):
        check_no_restricted_columns(df_invalid_3)

def test_validate_literature_validation_dataframe_success():
    df = pd.DataFrame({
        "literature_fluid_id": ["L1"],
        "source_key": ["ref1"],
        "P": [100.0],
        "Pb": [400.0],
        "T_C": [80.0],
        "Rsb_scf_stb": [500.0],
        "Rs_scf_stb": [125.0]
    })
    assert validate_literature_validation_dataframe(df)

def test_validate_literature_validation_dataframe_unexpected_column():
    df = pd.DataFrame({
        "literature_fluid_id": ["L1"],
        "source_key": ["ref1"],
        "P": [100.0],
        "Pb": [400.0],
        "T_C": [80.0],
        "Rsb_scf_stb": [500.0],
        "Rs_scf_stb": [125.0],
        "API": [35.0]  # Unexpected
    })
    with pytest.raises(ValueError, match="Unexpected columns detected"):
        validate_literature_validation_dataframe(df)

def test_validate_literature_validation_dataframe_p_gt_pb():
    df = pd.DataFrame({
        "literature_fluid_id": ["L1"],
        "source_key": ["ref1"],
        "P": [500.0],  # P > Pb is invalid
        "Pb": [400.0],
        "T_C": [80.0],
        "Rsb_scf_stb": [500.0],
        "Rs_scf_stb": [125.0]
    })
    with pytest.raises(ValueError, match="less than or equal"):
        validate_literature_validation_dataframe(df)

def test_validate_literature_validation_dataframe_rsb_zero():
    df = pd.DataFrame({
        "literature_fluid_id": ["L1"],
        "source_key": ["ref1"],
        "P": [100.0],
        "Pb": [400.0],
        "T_C": [80.0],
        "Rsb_scf_stb": [0.0],  # Rsb must be strictly positive
        "Rs_scf_stb": [125.0]
    })
    with pytest.raises(ValueError, match="strictly positive"):
        validate_literature_validation_dataframe(df)

def test_validate_literature_sources_dataframe_success():
    df = pd.DataFrame({
        "source_key": ["ref1"],
        "citation_short": ["Author (2020)"],
        "year": [2020],
        "literature_fluid_ids": ["L1, L2"],
        "n_points": [10],
        "notes": ["Public data"]
    })
    assert validate_literature_sources_dataframe(df)

def test_validate_literature_sources_dataframe_unexpected_column():
    df = pd.DataFrame({
        "source_key": ["ref1"],
        "citation_short": ["Author (2020)"],
        "year": [2020],
        "literature_fluid_ids": ["L1, L2"],
        "n_points": [10],
        "notes": ["Public data"],
        "extra_col": [1] # Unexpected
    })
    with pytest.raises(ValueError, match="Unexpected columns detected"):
        validate_literature_sources_dataframe(df)

def test_summarize_literature_dataframe():
    df = pd.DataFrame({
        "literature_fluid_id": ["L1", "L1", "L2"],
        "source_key": ["ref1", "ref1", "ref2"],
        "P": [100.0, 200.0, 300.0],
        "Pb": [400.0, 400.0, 500.0],
        "T_C": [80.0, 80.0, 90.0],
        "Rsb_scf_stb": [500.0, 500.0, 600.0],
        "Rs_scf_stb": [125.0, 250.0, 300.0]
    })
    summary = summarize_literature_dataframe(df)
    assert summary["n_fluids"] == 2
    assert summary["n_sources"] == 2
    assert summary["n_points"] == 3
    assert summary["min_P"] == 100.0
    assert summary["max_Pb"] == 500.0

def test_summarize_literature_dataframe_restricted_column():
    df = pd.DataFrame({
        "literature_fluid_id": ["L1"],
        "source_key": ["ref1"],
        "P": [100.0],
        "Pb": [400.0],
        "T_C": [80.0],
        "Rsb_scf_stb": [500.0],
        "Rs_scf_stb": [125.0],
        "well_id": [1]
    })
    with pytest.raises(ValueError, match="Restricted column detected"):
        summarize_literature_dataframe(df)
