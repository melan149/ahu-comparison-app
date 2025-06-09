
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Function to extract data for a specific quarter
def extract_quarter_data(df, quarter):
    quarter_data = df[df['Quarter'] == quarter]
    unit_sizes = quarter_data['Unit size'].unique()
    recovery_types = [col.split('_')[-1] for col in quarter_data.columns if 'Recovery type' in col]
    
    data = []
    for unit_size in unit_sizes:
        for recovery_type in recovery_types:
            min_airflow_col = f'Minimum airflow_recovery type{recovery_type}'
            max_airflow_col = f'Maximum airflow_recovery type{recovery_type}'
            if min_airflow_col in quarter_data.columns and max_airflow_col in quarter_data.columns:
                min_airflow = quarter_data[quarter_data['Unit size'] == unit_size][min_airflow_col].values[0]
                max_airflow = quarter_data[quarter_data['Unit size'] == unit_size][max_airflow_col].values[0]
                data.append([unit_size, recovery_type, min_airflow, max_airflow])
    
    return pd.DataFrame(data, columns=['Unit size', 'Recovery type', 'Min airflow', 'Max airflow'])

# Function to plot airflow range chart
def plot_airflow_chart(df, title):
    fig, ax = plt.subplots()
    for i, row in df.iterrows():
        ax.barh(row['Unit size'], row['Max airflow'] - row['Min airflow'], left=row['Min airflow'], label=row['Recovery type'])
    ax.set_xlabel('Airflow')
    ax.set_title(title)
    ax.legend()
    st.pyplot(fig)

# Streamlit app
st.title('AHU Airflow Comparison')

# File upload
left_file = st.file_uploader("Upload the first Excel file", type=["xlsx"], key="left")
right_file = st.file_uploader("Upload the second Excel file", type=["xlsx"], key="right")

if left_file and right_file:
    left_df = pd.read_excel(left_file, sheet_name='data', engine='openpyxl')
    right_df = pd.read_excel(right_file, sheet_name='data', engine='openpyxl')
    
    # Quarter selection
    left_quarter = st.selectbox("Select Quarter for the first file", ['Q1', 'Q2', 'Q3', 'Q4'], key="left_quarter")
    right_quarter = st.selectbox("Select Quarter for the second file", ['Q1', 'Q2', 'Q3', 'Q4'], key="right_quarter")
    
    # Extract data for selected quarters
    left_data = extract_quarter_data(left_df, left_quarter)
    right_data = extract_quarter_data(right_df, right_quarter)
    
    # Plot charts
    st.subheader('Airflow Range for the First File')
    plot_airflow_chart(left_data, f'Airflow Range for {left_quarter}')
    
    st.subheader('Airflow Range for the Second File')
    plot_airflow_chart(right_data, f'Airflow Range for {right_quarter}')
