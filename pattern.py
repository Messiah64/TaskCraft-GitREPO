import pandas as pd

def generate_planner(data_file, output_file, days_in_month):
    # Read data from Excel file
    df = pd.read_excel(data_file, index_col=0)

    # Generate the planner for the specified month by repeating the last 8 days
    monthly_planner = pd.DataFrame(index=df.index, columns=range(1, days_in_month + 1))

    # Iterate through each rota and repeat the last 8 days for the month
    for rota in df.index:
        last_8_days = list(df.loc[rota, str(days_in_month - 7):str(days_in_month)])
        repeated_pattern = (last_8_days * ((days_in_month - 1) // 8 + 1))[:days_in_month]
        monthly_planner.loc[rota] = repeated_pattern

    # Export the result to an Excel file
    monthly_planner.to_excel(output_file)

    # Print a message to confirm the export
    print(f"Result has been exported to '{output_file}'")

# Specify the number of days in February
days_in_february = 28  # Adjust as needed

# Generate the planner for February
generate_planner('testdata.xlsx', 'result_february.xlsx', days_in_february)
