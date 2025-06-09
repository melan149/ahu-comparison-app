
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def extract_quarter_data(df, quarter):
    # Drop the first two rows to set the correct header
    df = df.drop([0, 1])
    df.columns = df.iloc[0]
    df = df[1:]
    
    # Extract data for the specified quarter
    quarter_data = df[df['Quarter'] == quarter]
    
    # Extract unit sizes and airflow data
    unit_sizes = quarter_data['Unit size'].unique()
    recovery_types = ['Recovery type1', 'Recovery type2']
    min_airflow_cols = [f'Minimum airflow_{rt}' for rt in recovery_types]
    max_airflow_cols = [f'Maximum airflow_{rt}' for rt in recovery_types]
    
    data = []
    for unit_size in unit_sizes:
        for rt, min_col, max_col in zip(recovery_types, min_airflow_cols, max_airflow_cols):
            min_airflow = quarter_data[quarter_data['Unit size'] == unit_size][min_col].values[0]
            max_airflow = quarter_data[quarter_data['Unit size'] == unit_size][max_col].values[0]
            data.append([unit_size, rt, min_airflow, max_airflow])
    
    return pd.DataFrame(data, columns=['Unit size', 'Recovery type', 'Min airflow', 'Max airflow'])

# Streamlit app
st.title('AHU Airflow Comparison App')

# File upload
left_file = st.file_uploader('Upload left Excel file', type='xlsx')
right_file = st.file_uploader('Upload right Excel file', type='xlsx')

if left_file and right_file:
    left_df = pd.read_excel(left_file, sheet_name='data', engine='openpyxl')
    right_df = pd.read_excel(right_file, sheet_name='data', engine='openpyxl')
    
    # Quarter selection
    left_quarter = st.selectbox('Select quarter for left file', ['Q1', 'Q2', 'Q3', 'Q4'])
    right_quarter = st.selectbox('Select quarter for right file', ['Q1', 'Q2', 'Q3', 'Q4'])
    
    # Extract data for selected quarters
    left_data = extract_quarter_data(left_df, left_quarter)
    right_data = extract_quarter_data(right_df, right_quarter)
    
    # Plotting
    fig, axes = plt.subplots(1, 2, figsize=(15, 8))
    
    for ax, data, title in zip(axes, [left_data, right_data], ['Left File', 'Right File']):
        for recovery_type in data['Recovery type'].unique():
            subset = data[data['Recovery type'] == recovery_type]
            ax.barh(subset['Unit size'], subset['Max airflow'] - subset['Min airflow'], left=subset['Min airflow'], label=recovery_type)
        ax.set_xlabel('Airflow')
        ax.set_ylabel('Unit size')
        ax.set_title(title)
        ax.legend()
    
    st.pyplot(fig)
