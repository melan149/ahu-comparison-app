
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to extract data for a specific quarter
def extract_quarter_data(df, quarter):
    # Transpose the DataFrame
    df = df.T
    
    # Use the second column as row labels
    df.columns = df.iloc[1]
    df = df.drop([0, 1])
    
    # Extract data for the specified quarter
    quarter_data = df[df.index == quarter]
    
    # Extract unit sizes and airflow data
    unit_sizes = quarter_data['Unit size'].unique()
    recovery_types = [col for col in quarter_data.columns if 'Recovery type' in col]
    
    data = []
    for unit_size in unit_sizes:
        for recovery_type in recovery_types:
            min_airflow_col = f'Minimum airflow_{recovery_type}'
            max_airflow_col = f'Maximum airflow_{recovery_type}'
            if min_airflow_col in quarter_data.columns and max_airflow_col in quarter_data.columns:
                min_airflow = quarter_data[min_airflow_col].values[0]
                max_airflow = quarter_data[max_airflow_col].values[0]
                data.append([unit_size, recovery_type, min_airflow, max_airflow])
    
    return pd.DataFrame(data, columns=['Unit size', 'Recovery type', 'Min airflow', 'Max airflow'])

# Streamlit app
st.title('AHU Airflow Comparison')

# File upload
left_file = st.file_uploader('Upload left AHU file', type='xlsx', key='left')
right_file = st.file_uploader('Upload right AHU file', type='xlsx', key='right')

if left_file and right_file:
    # Load the Excel files
    left_df = pd.read_excel(left_file, sheet_name='data', engine='openpyxl')
    right_df = pd.read_excel(right_file, sheet_name='data', engine='openpyxl')
    
    # Quarter selection
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    left_quarter = st.selectbox('Select quarter for left AHU', quarters, key='left_quarter')
    right_quarter = st.selectbox('Select quarter for right AHU', quarters, key='right_quarter')
    
    # Extract data for the selected quarters
    left_data = extract_quarter_data(left_df, left_quarter)
    right_data = extract_quarter_data(right_df, right_quarter)
    
    # Plotting
    fig, axes = plt.subplots(1, 2, figsize=(15, 10), sharey=True)
    
    for ax, data, title in zip(axes, [left_data, right_data], ['Left AHU', 'Right AHU']):
        for recovery_type in data['Recovery type'].unique():
            subset = data[data['Recovery type'] == recovery_type]
            ax.barh(subset['Unit size'], subset['Max airflow'] - subset['Min airflow'], left=subset['Min airflow'], label=recovery_type)
        ax.set_title(title)
        ax.set_xlabel('Airflow')
        ax.set_ylabel('Unit size')
        ax.legend()
    
    st.pyplot(fig)
