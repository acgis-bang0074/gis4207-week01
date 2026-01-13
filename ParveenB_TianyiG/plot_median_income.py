import sys
import os
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams


def main(in_csv, out_png):
    # Check if input file exists
    # If the input CSV file does not exist, print an error message
    # and exit the program with error code 1
    if not os.path.exists(in_csv):
        print(f"Error: Input file '{in_csv}' does not exist.")
        sys.exit(1)
    
    df = pd.read_csv(in_csv)
    
    # Step 3 - Filter for Median Income
    # Filter 'DIM: Profile of Census Subdivisions (2247)' for 
    # 'Median total income in 2015 among recipients ($)'
    df = df[
        df["DIM: Profile of Census Subdivisions (2247)"] 
        == "Median total income in 2015 among recipients ($)"
    ]
    
    # Step 4 - Filter for the required columns
    df = df[["GEO_CODE (POR)", "Dim: Sex (3): Member ID: [1]: Total - Sex"]]
    
    # Step 5 - Rename columns
    df = df.rename(columns={
        "GEO_CODE (POR)": "GEOCODE",
        "Dim: Sex (3): Member ID: [1]: Total - Sex": "Median Income"
    })
    
    # Step 6 - Set index to GEOCODE column
    df = df.set_index("GEOCODE")
    
    # Step 7 - Filter out invalid values
    invalid_values = ["x", "F", ".."]
    df = df[~df["Median Income"].isin(invalid_values)]
    
    # Step 8 - Convert Median Income to numeric values
    df["Median Income"] = pd.to_numeric(df["Median Income"], errors="coerce")
    
    # Step 9 & 10 - Create histogram using seaborn histplot method
    histo = sns.histplot(data=df, x="Median Income", bins=30, kde=True)
    
    # Step 11 - Get figure from the AxesSubplot object
    fig = histo.get_figure()
    
    # Step 12 - Save figure to PNG file
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    print(f"Histogram saved to {out_png}")


if __name__ == '__main__':
    # Check if the correct number of command-line arguments are provided
    # The script requires exactly 2 arguments: in_csv and out_png
    # If the number of arguments is not 3 (script name + 2 arguments),
    # print the usage message and exit with error code 1
    if len(sys.argv) != 3:
        print("Usage: plot_median_income.py in_csv out_png")
        sys.exit(1)
    
    in_csv = sys.argv[1]
    out_png = sys.argv[2]
    
    main(in_csv, out_png)