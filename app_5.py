
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Function to extract quarter-specific data
def extract_quarter_data(df, quarter):
    # Drop the first two rows and set the second row as header
    df.columns = df.iloc[1]
    df = df.drop([0, 1])
    
    # Transpose the DataFrame
    df = df.transpose()
    
    # Set the first column as header
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    
    # Filter data for the selected quarter
    quarter_data = df[df.iloc[:, 0] == quarter]
    
    # Extract relevant columns
    unit_sizes = quarter_data['Unit size'].unique()
    recovery_types = [col for col in quarter_data.columns if 'Recovery type' in col]
    min_airflows = [col for col in quarter_data.columns if 'Minimum airflow' in col]
    max_airflows = [col for col in quarter_data.columns if 'Maximum airflow' in col]
    
    # Create a structured DataFrame
    data = []
    for unit_size in unit_sizes:
        for recovery_type, min_airflow, max_airflow in zip(recovery_types, min_airflows, max_airflows):
            data.append({
                'Unit size': unit_size,
                'Recovery type': recovery_type,
                'Min airflow': quarter_data[min_airflow].values[0],
                'Max airflow': quarter_data[max_airflow].values[0]
            })
    
    return pd.DataFrame(data)

# Streamlit app
st.title('AHU Airflow Comparison')

# File upload
left_file = st.file_uploader('Upload the first Excel file', type='xlsx', key='left')
right_file = st.file_uploader('Upload the second Excel file', type='xlsx', key='right')

if left_file and right_file:
    left_df = pd.read_excel(left_file, sheet_name='data', engine='openpyxl')
    right_df = pd.read_excel(right_file, sheet_name='data', engine='openpyxl')
    
    # Quarter selection
    left_quarter = st.selectbox('Select Quarter for the first file', ['Q1', 'Q2', 'Q3', 'Q4'], key='left_quarter')
    right_quarter = st.selectbox('Select Quarter for the second file', ['Q1', 'Q2', 'Q3', 'Q4'], key='right_quarter')
    
    # Extract data for the selected quarters
    left_data = extract_quarter_data(left_df, left_quarter)
    right_data = extract_quarter_data(right_df, right_quarter)
    
    # Plotting
    fig, axes = plt.subplots(1, 2, figsize=(15, 10), sharey=True)
    
    for ax, data, title in zip(axes, [left_data, right_data], ['Left File', 'Right File']):
        for recovery_type in data['Recovery type'].unique():
            subset = data[data['Recovery type'] == recovery_type]
            ax.barh(subset['Unit size'], subset['Max airflow'], label=f'{recovery_type} Max', alpha=0.5)
            ax.barh(subset['Unit size'], subset['Min airflow'], label=f'{recovery_type} Min', alpha=0.5)
        ax.set_title(title)
        ax.set_xlabel('Airflow')
        ax.set_ylabel('Unit size')
        ax.legend()
    
    st.pyplot(fig)
