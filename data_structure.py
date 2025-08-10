import pandas as pd

# Define the expected headers and their data types
# Assuming 'CTNS' is the 'TOTAL' column in the header row
# And 'TOTAL' is a calculated field
# NW and GW are given as numbers, but will be used in calculations
# The image provided only shows 'POWER SUPPLY' as an item, so this is just a placeholder.

DATA_HEADERS = {
    'ITEM': str,
    'MODEL': str,
    'QTY/CTN': int,
    'CTNS': int, # This is the 'CTNS' from the header, which is a quantity
    'TOTAL': float, # This will be calculated as QTY/CTN * CTNS
    'NW': float,
    'GW': float,
    'TOTAL NW': float, # Calculated as CTNS * NW
    'TOTAL GW': float # Calculated as CTNS * GW
}

# Example of how the data might look after retrieval
# This will be replaced by actual data from Google Sheets
example_data = [
    {'ITEM': 'POWER SUPPLY', 'MODEL': 'Power supply', 'QTY/CTN': 10, 'CTNS': 5, 'NW': 18, 'GW': 20},
    {'ITEM': 'POWER SUPPLY', 'MODEL': '12V400W', 'QTY/CTN': 10, 'CTNS': 3, 'NW': 18, 'GW': 20},
    {'ITEM': 'CABLE', 'MODEL': 'HDMI Cable', 'QTY/CTN': 50, 'CTNS': 10, 'NW': 0.5, 'GW': 0.6},
    {'ITEM': 'CABLE', 'MODEL': 'USB Cable', 'QTY/CTN': 100, 'CTNS': 7, 'NW': 0.2, 'GW': 0.25},
]

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Processes the DataFrame: calculates TOTAL, TOTAL NW, TOTAL GW."""
    df['TOTAL'] = df['QTY/CTN'] * df['CTNS']
    df['TOTAL NW'] = df['CTNS'] * df['NW']
    df['TOTAL GW'] = df['CTNS'] * df['GW']
    return df

def sort_and_subtotal(df: pd.DataFrame) -> pd.DataFrame:
    """Sorts by ITEM and calculates subtotals and grand totals."""
    df_sorted = df.sort_values(by='ITEM').reset_index(drop=True)

    # Calculate subtotals
    subtotals = df_sorted.groupby('ITEM').agg({
        'CTNS': 'sum',
        'TOTAL': 'sum',
        'TOTAL NW': 'sum',
        'TOTAL GW': 'sum'
    }).reset_index()
    subtotals['ITEM'] = subtotals['ITEM'] + ' Subtotal'

    # Calculate grand totals
    grand_total = pd.DataFrame([{
        'ITEM': 'Grand Total',
        'CTNS': df_sorted['CTNS'].sum(),
        'TOTAL': df_sorted['TOTAL'].sum(),
        'TOTAL NW': df_sorted['TOTAL NW'].sum(),
        'TOTAL GW': df_sorted['TOTAL GW'].sum()
    }])

    # Combine original data with subtotals and grand total
    # This part needs careful handling to insert subtotals correctly
    # For now, let's just append them for simplicity, and refine later for display
    result_df = pd.DataFrame(columns=df_sorted.columns)
    for item in df_sorted['ITEM'].unique():
        item_data = df_sorted[df_sorted['ITEM'] == item]
        result_df = pd.concat([result_df, item_data])
        sub_total_row = subtotals[subtotals['ITEM'] == item + ' Subtotal']
        result_df = pd.concat([result_df, sub_total_row], ignore_index=True)

    result_df = pd.concat([result_df, grand_total], ignore_index=True)

    return result_df

if __name__ == '__main__':
    df = pd.DataFrame(example_data)
    df_processed = process_data(df)
    df_final = sort_and_subtotal(df_processed)
    print(df_final.to_string())


