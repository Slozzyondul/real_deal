import tabula
import pandas as pd

# Specify the path to your PDF file
pdf_file = "/home/solo/Desktop/2022-1.pdf"

# Read tables from PDF and convert to DataFrame
dfs = tabula.read_pdf(pdf_file, pages="all", output_format="dataframe")

# Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(dfs)

# Specify the output Excel file path
excel_file = "/home/solo/Desktop/output_file1.xlsx"

# Save the combined DataFrame to Excel
combined_df.to_excel(excel_file, index=False)

print("Tables successfully extracted and saved to Excel.")
