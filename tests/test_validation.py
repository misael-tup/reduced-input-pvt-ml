import pytest
import pandas as pd
from pvt_ml.validation import (
    require_columns,
    require_numeric,
    require_positive,
    require_non_negative,
    validate_pressure_domain,
    validate_hybrid_pt_input
)

def test_require_columns_passes():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    require_columns(df, ["A", "B"])

def test_require_columns_fails():
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(ValueError, match="Missing required columns"):
        require_columns(df, ["A", "B"])

def test_require_numeric_fails():
    df = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})
    with pytest.raises(ValueError, match="must contain numeric data"):
        require_numeric(df, ["A", "B"])

def test_require_positive():
    df_valid = pd.DataFrame({"A": [1.0, 2.0]})
    require_positive(df_valid, ["A"])
    
    df_invalid = pd.DataFrame({"A": [0.0, 1.0]})
    with pytest.raises(ValueError, match="strictly positive"):
        require_positive(df_invalid, ["A"])

def test_require_non_negative():
    df_valid = pd.DataFrame({"A": [0.0, 1.0]})
    require_non_negative(df_valid, ["A"])
    
    df_invalid = pd.DataFrame({"A": [-1.0, 1.0]})
    with pytest.raises(ValueError, match="non-negative"):
        require_non_negative(df_invalid, ["A"])

def test_validate_pressure_domain():
    df_valid = pd.DataFrame({"P": [100.0, 400.0], "Pb": [400.0, 400.0]})
    validate_pressure_domain(df_valid)
    
    df_invalid = pd.DataFrame({"P": [500.0], "Pb": [400.0]})
    with pytest.raises(ValueError, match="less than or equal"):
        validate_pressure_domain(df_invalid)

def test_validate_hybrid_pt_input():
    df_valid = pd.DataFrame({"P_over_Pb": [0.25], "Pb": [400.0], "T_C": [80.0]})
    validate_hybrid_pt_input(df_valid)
