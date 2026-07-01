import argparse
import pandas as pd
import sys
from pvt_ml.literature import (
    validate_literature_validation_dataframe,
    validate_literature_sources_dataframe
)

# Public Mapping
FLUID_SOURCE_MAP = {
    'L2': {'source_key': 'standing_1958', 'citation_short': 'Standing (1958)', 'year': 1958},
    'L3': {'source_key': 'walsh_1994', 'citation_short': 'Walsh et al. (1994)', 'year': 1994},
    'L4': {'source_key': 'mccain_2002', 'citation_short': 'McCain (2002)', 'year': 2002},
    'L5': {'source_key': 'nnabuo_2014', 'citation_short': 'Nnabuo et al. (2014)', 'year': 2014},
    'L6': {'source_key': 'igwe_ujile_2015', 'citation_short': 'Igwe and Ujile (2015)', 'year': 2015},
    'L7': {'source_key': 'zhang_2024', 'citation_short': 'Zhang et al. (2024)', 'year': 2024},
    'L8': {'source_key': 'okotie_2017', 'citation_short': 'Okotie et al. (2017)', 'year': 2017},
    'L9': {'source_key': 'salehirad_2005', 'citation_short': 'Salehirad (2005)', 'year': 2005},
    'L10': {'source_key': 'salehirad_2005', 'citation_short': 'Salehirad (2005)', 'year': 2005},
    'L11': {'source_key': 'vasquez_beggs_1977', 'citation_short': 'Vasquez and Beggs (1977)', 'year': 1977},
    'L12': {'source_key': 'elias_trevisan_2016', 'citation_short': 'Elias and Trevisan (2016)', 'year': 2016},
    'L13': {'source_key': 'smith_tan_1997', 'citation_short': 'Smith and Tan (1997)', 'year': 1997},
    'L14': {'source_key': 'okotie_fasanya_2020', 'citation_short': 'Okotie and Fasanya (2020)', 'year': 2020},
    'L15': {'source_key': 'christensen_1999', 'citation_short': 'Christensen (1999)', 'year': 1999},
    'L16': {'source_key': 'klein_1959', 'citation_short': 'Klein (1959)', 'year': 1959},
    'L17': {'source_key': 'klein_1959', 'citation_short': 'Klein (1959)', 'year': 1959},
    'L18': {'source_key': 'labedi_1982', 'citation_short': 'Labedi (1982)', 'year': 1982},
    'L19': {'source_key': 'abidini_2018', 'citation_short': 'Abidini et al. (2018)', 'year': 2018},
    'L20': {'source_key': 'alagoa_2023', 'citation_short': 'Alagoa et al. (2023)', 'year': 2023},
    'L21': {'source_key': 'al_marhoun_2003', 'citation_short': 'Al-Marhoun (2003)', 'year': 2003}
}

def build_public_literature_dataset(input_path: str, output_validation_path: str, output_sources_path: str):
    # 1. Read input CSV
    df_raw = pd.read_csv(input_path)
    
    # 2. Check source columns
    required_raw_cols = ['Model', 'Fluid_ID', 'P', 'Pb', 'T', 'Rsb', 'Rs_exp']
    missing = [c for c in required_raw_cols if c not in df_raw.columns]
    if missing:
        raise ValueError(f"Input CSV is missing required columns: {missing}")
        
    # 3. Filter
    df = df_raw[df_raw['Model'] == 'Hybrid-PT'].copy()
    
    # 4. Verify filtered dataset
    if len(df) != 184:
        raise ValueError(f"Expected 184 rows after filtering, got {len(df)}")
    
    fluids = df['Fluid_ID'].unique().tolist()
    if len(fluids) != 20:
        raise ValueError(f"Expected 20 unique fluids, got {len(fluids)}")
        
    expected_fluids = {f'L{i}' for i in range(2, 22)}
    if set(fluids) != expected_fluids:
        raise ValueError(f"Unexpected set of fluid IDs. Expected L2 to L21. Got: {fluids}")
        
    if 'L1' in fluids:
        raise ValueError("L1 must not be in the validation set.")
        
    # 5 & 6. Mapping columns
    df = df.rename(columns={
        'Fluid_ID': 'literature_fluid_id',
        'T': 'T_C',
        'Rsb': 'Rsb_scf_stb',
        'Rs_exp': 'Rs_scf_stb'
    })
    
    # 7. Recalculate
    df['P_over_Pb'] = df['P'] / df['Pb']
    df['Rsr'] = df['Rs_scf_stb'] / df['Rsb_scf_stb']
    
    # 8. Create source_key
    df['source_key'] = df['literature_fluid_id'].map(lambda x: FLUID_SOURCE_MAP[x]['source_key'])
    
    # Select exact columns in order
    validation_cols = [
        'literature_fluid_id', 'source_key', 'P', 'Pb', 'T_C', 
        'Rsb_scf_stb', 'Rs_scf_stb', 'P_over_Pb', 'Rsr'
    ]
    df_val = df[validation_cols].copy()
    
    # 9. Validate
    validate_literature_validation_dataframe(df_val, require_reduced_columns=True)
    
    # 10. Save
    df_val.to_csv(output_validation_path, index=False)
    
    # 11. Create literature_sources
    source_records = []
    for source_key in df_val['source_key'].unique():
        # Get one of the fluids mapping to this source
        sample_fluid = df_val[df_val['source_key'] == source_key]['literature_fluid_id'].iloc[0]
        meta = FLUID_SOURCE_MAP[sample_fluid]
        
        # Fluids for this source
        fluids_for_source = df_val[df_val['source_key'] == source_key]['literature_fluid_id'].unique().tolist()
        n_points = len(df_val[df_val['source_key'] == source_key])
        
        source_records.append({
            'source_key': source_key,
            'citation_short': meta['citation_short'],
            'year': meta['year'],
            'literature_fluid_ids': ','.join(sorted(fluids_for_source, key=lambda x: int(x[1:]))),
            'n_points': n_points,
            'notes': "Published literature source; retained pressure points satisfy P <= Pb."
        })
        
    df_sources = pd.DataFrame(source_records)
    source_cols = ['source_key', 'citation_short', 'year', 'literature_fluid_ids', 'n_points', 'notes']
    df_sources = df_sources[source_cols]
    
    # 12. Validate sources
    validate_literature_sources_dataframe(df_sources)
    
    # 13. Save
    df_sources.to_csv(output_sources_path, index=False)
    
    # 14. Print Summary
    print("Aggregate Summary:")
    print(f"- n_points: {len(df_val)}")
    print(f"- n_fluids: {df_val['literature_fluid_id'].nunique()}")
    print(f"- n_sources: {df_sources['source_key'].nunique()}")
    print(f"- Validation Path: {output_validation_path}")
    print(f"- Sources Path: {output_sources_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Public Literature Dataset")
    parser.add_argument("--input", required=True, help="Path to original pointwise final csv")
    parser.add_argument("--output-validation", required=True, help="Output path for literature_validation.csv")
    parser.add_argument("--output-sources", required=True, help="Output path for literature_sources.csv")
    args = parser.parse_args()
    
    try:
        build_public_literature_dataset(args.input, args.output_validation, args.output_sources)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
