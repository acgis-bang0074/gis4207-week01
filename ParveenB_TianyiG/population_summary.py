import sys
import os
import pandas as pd


def main(in_census_csv, out_summary_csv):
    # Check if input file exists
    # If the input census CSV file does not exist, print an error message
    # and exit the program with error code 1
    if not os.path.exists(in_census_csv):
        print(f"Error: Input file '{in_census_csv}' does not exist.")
        sys.exit(1)
    
    df = pd.read_csv(in_census_csv)
    
    # Step 4 — Filter the DataFrame
    # Overwrite the original DataFrame (saves memory)
    df = df[
            df["DIM: Profile of Census Subdivisions (2247)"] 
            == "Total - Age groups and average age of the population - 100% data"
    ]
    
    # Step 5
    df = df[[ "GEO_CODE (POR)", "GEO_NAME", "Dim: Sex (3): Member ID: [1]: Total - Sex", "Dim: Sex (3): Member ID: [2]: Male", "Dim: Sex (3): Member ID: [3]: Female" ]]
    
    # Step 6
    df = df.rename(columns={
        "GEO_CODE (POR)": "GEOCODE",
        "GEO_NAME": "GEONAME",
        "Dim: Sex (3): Member ID: [1]: Total - Sex": "Total Pop.",
        "Dim: Sex (3): Member ID: [2]: Male": "Male",
        "Dim: Sex (3): Member ID: [3]: Female": "Female"
    })
    
    # Step 7 & 8
    invalid_values = ["x", "F", ".."]
    
    df = df[
        ~df["Total Pop."].isin(invalid_values) &
        ~df["Male"].isin(invalid_values) &
        ~df["Female"].isin(invalid_values)
    ]
    
    # Instead of astype(int), use pd.to_numeric() with errors='coerce'.
    # This handles:'13150.00', '200',' 300 ' (extra spaces),'12,500' (commas)
    df["Total Pop."] = pd.to_numeric(df["Total Pop."], errors="coerce")
    df["Male"] = pd.to_numeric(df["Male"], errors="coerce")
    df["Female"] = pd.to_numeric(df["Female"], errors="coerce")
    
    # Convert to integer
    df["Total Pop."] = df["Total Pop."].astype(int)
    df["Male"] = df["Male"].astype(int)
    df["Female"] = df["Female"].astype(int)
    
    # Step 9 - Export DataFrame to CSV
    df.to_csv(out_summary_csv, index=False)
    print(f"Output saved to {out_summary_csv}")


if __name__ == '__main__':
    # Check if the correct number of command-line arguments are provided
    # The script requires exactly 2 arguments: in_census_csv and out_summary_csv
    # If the number of arguments is not 3 (script name + 2 arguments),
    # print the usage message and exit with error code 1
    if len(sys.argv) != 3:
        print("Usage: population_summary.py in_census_csv out_summary_csv")
        sys.exit(1)
    
    in_census_csv = sys.argv[1]
    out_summary_csv = sys.argv[2]
    
    main(in_census_csv, out_summary_csv)



