import pytest
import numpy as np
from pvt_ml.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
    average_absolute_percentage_relative_error,
    coefficient_of_determination,
    regression_metrics
)

def test_metrics_values():
    y_true = [100.0, 200.0]
    y_pred = [90.0, 210.0]
    
    mae = mean_absolute_error(y_true, y_pred)
    assert np.isclose(mae, 10.0)
    
    rmse = root_mean_squared_error(y_true, y_pred)
    assert np.isclose(rmse, 10.0)
    
    aapre = average_absolute_percentage_relative_error(y_true, y_pred)
    assert np.isclose(aapre, 7.5) # (0.1 + 0.05)/2 = 0.075 -> 7.5%
    
    r2 = coefficient_of_determination(y_true, y_pred)
    assert r2 > 0

def test_regression_metrics_dict():
    y_true = [100.0, 200.0]
    y_pred = [90.0, 210.0]
    res = regression_metrics(y_true, y_pred)
    assert "MAE" in res
    assert "RMSE" in res
    assert "AAPRE" in res
    assert "R2" in res

def test_aapre_excludes_zeros():
    y_true = [0.0, 100.0]
    y_pred = [10.0, 90.0]
    # Should only compute AAPRE for the 100 vs 90 pair (10%)
    aapre = average_absolute_percentage_relative_error(y_true, y_pred)
    assert np.isclose(aapre, 10.0)

def test_aapre_all_zeros():
    y_true = [0.0, 0.0]
    y_pred = [10.0, 10.0]
    with pytest.raises(ValueError, match="All y_true values are zero"):
        average_absolute_percentage_relative_error(y_true, y_pred)

def test_length_mismatch():
    with pytest.raises(ValueError, match="same length"):
        mean_absolute_error([1.0], [1.0, 2.0])

def test_empty_inputs():
    with pytest.raises(ValueError, match="must not be empty"):
        mean_absolute_error([], [])
