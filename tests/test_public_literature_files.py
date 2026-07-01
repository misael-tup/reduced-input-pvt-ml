import os
import pandas as pd
from pvt_ml.literature import (
    validate_literature_validation_dataframe,
    validate_literature_sources_dataframe
)

def test_public_literature_files_exist_and_valid():
    val_path = os.path.join('data', 'literature_validation.csv')
    src_path = os.path.join('data', 'literature_sources.csv')
    
    assert os.path.exists(val_path), f"File {val_path} does not exist"
    assert os.path.exists(src_path), f"File {src_path} does not exist"
    
    df_val = pd.read_csv(val_path)
    df_src = pd.read_csv(src_path)
    
    # Validation logic from module
    assert validate_literature_validation_dataframe(df_val, require_reduced_columns=True)
    assert validate_literature_sources_dataframe(df_src)
    
    # Extra verifications
    assert len(df_val) == 184
    
    fluids = df_val["literature_fluid_id"].unique().tolist()
    assert len(fluids) == 20
    
    expected_fluids = {f'L{i}' for i in range(2, 22)}
    assert set(fluids) == expected_fluids
    assert 'L1' not in fluids
    
    # Column exactness and order
    expected_val_cols = [
        'literature_fluid_id', 'source_key', 'P', 'Pb', 'T_C', 
        'Rsb_scf_stb', 'Rs_scf_stb', 'P_over_Pb', 'Rsr'
    ]
    assert df_val.columns.tolist() == expected_val_cols
    
    expected_src_cols = [
        'source_key', 'citation_short', 'year', 'literature_fluid_ids', 'n_points', 'notes'
    ]
    assert df_src.columns.tolist() == expected_src_cols
