import pandas as pd

# Load dataset (change name if needed)
data = pd.read_excel("PCOS_data.xlsx")

# Print columns
print("Columns in dataset:")
print(data.columns)

# Show first 5 rows
print("\nSample data:")
print(data.head())