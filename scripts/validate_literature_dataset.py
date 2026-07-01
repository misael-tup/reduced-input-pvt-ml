import argparse
import sys
import pandas as pd
from pvt_ml.literature import (
    validate_literature_validation_dataframe,
    validate_literature_sources_dataframe,
    summarize_literature_dataframe
)

def main():
    parser = argparse.ArgumentParser(description="Validate Literature Dataset CSVs for public release.")
    parser.add_argument("--validation", type=str, required=True, help="Path to literature_validation.csv")
    parser.add_argument("--sources", type=str, required=True, help="Path to literature_sources.csv")
    args = parser.parse_args()

    try:
        print(f"Loading {args.validation}...")
        df_val = pd.read_csv(args.validation)
        
        print(f"Loading {args.sources}...")
        df_src = pd.read_csv(args.sources)
        
        print("Validating literature sources...")
        validate_literature_sources_dataframe(df_src)
        print("OK.")
        
        print("Validating literature validation data...")
        validate_literature_validation_dataframe(df_val, require_reduced_columns=False)
        print("OK.")
        
        print("\n--- Summary ---")
        summary = summarize_literature_dataframe(df_val)
        for k, v in summary.items():
            print(f"{k}: {v}")
            
        print("\nSUCCESS: The literature dataset conforms to the public schema.")
        
    except Exception as e:
        print(f"\nERROR during validation:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
