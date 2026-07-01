import os
import pandas as pd
from pvt_ml.literature import (
    validate_literature_validation_dataframe,
    validate_literature_sources_dataframe,
    summarize_literature_dataframe
)

def main():
    val_path = os.path.join('data', 'literature_validation.csv')
    src_path = os.path.join('data', 'literature_sources.csv')
    
    # 1. Load data
    df_val = pd.read_csv(val_path)
    df_src = pd.read_csv(src_path)
    
    # 2. Validate
    validate_literature_validation_dataframe(df_val, require_reduced_columns=True)
    validate_literature_sources_dataframe(df_src)
    
    # 3. Summarize
    summary = summarize_literature_dataframe(df_val)
    
    # 4. Verify assertions
    assert summary['n_points'] == 184
    assert summary['n_fluids'] == 20
    assert summary['n_sources'] == 18
    assert 'L1' not in df_val['literature_fluid_id'].unique()
    assert all(f"L{i}" in df_val['literature_fluid_id'].unique() for i in range(2, 22))
    
    expected_val_cols = [
        'literature_fluid_id', 'source_key', 'P', 'Pb', 'T_C', 
        'Rsb_scf_stb', 'Rs_scf_stb', 'P_over_Pb', 'Rsr'
    ]
    assert df_val.columns.tolist() == expected_val_cols
    
    # 5. Print Output
    print("- Literature validation data: OK")
    print("- Sources metadata: OK")
    print(f"- Number of fluids: {summary['n_fluids']}")
    print(f"- Number of pressure points: {summary['n_points']}")
    print(f"- Number of sources: {summary['n_sources']}")
    print("- Fluid IDs: L2-L21")
    print("- No proprietary columns detected")

if __name__ == "__main__":
    main()
