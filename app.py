
import streamlit as st
import pandas as pd

# Function to load and process the Excel file
def load_data(file):
    df = pd.read_excel(file, sheet_name='data', engine='openpyxl')
    df = df.set_index(df.columns[0]).transpose()
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    return df

# Function to extract relevant data for a given quarter
def extract_quarter_data(df, quarter):
    quarter_data = df.loc[quarter]
    unit_sizes = quarter_data['Unit size'].split(',')
    recovery_types = quarter_data[['Recovery type1', 'Recovery type2']].values.flatten()
    min_airflows = quarter_data[['Minimum airflow_recovery type1', 'Minimum airflow_recovery type2']].values.flatten()
    max_airflows = quarter_data[['Maximum airflow_recovery type1', 'Maximum airflow_recovery type2']].values.flatten()
    
    data = {
        'Unit size': unit_sizes,
        'Recovery type': recovery_types,
        'Min airflow': min_airflows,
        'Max airflow': max_airflows
    }
    
    return pd.DataFrame(data)

# Streamlit app
st.title('AHU Airflow Range Comparison')

# File upload
left_file = st.file_uploader('Upload left AHU Excel file', type='xlsx')
right_file = st.file_uploader('Upload right AHU Excel file', type='xlsx')

if left_file and right_file:
    left_df = load_data(left_file)
    right_df = load_data(right_file)
    
    # Quarter selection
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    left_quarter = st.selectbox('Select quarter for left file', quarters)
    right_quarter = st.selectbox('Select quarter for right file', quarters)
    
    left_data = extract_quarter_data(left_df, left_quarter)
    right_data = extract_quarter_data(right_df, right_quarter)
    
    # Display side-by-side bar charts
    st.subheader('Left File Airflow Range')
    st.bar_chart(left_data.set_index('Unit size')[['Min airflow', 'Max airflow']])
    
    st.subheader('Right File Airflow Range')
    st.bar_chart(right_data.set_index('Unit size')[['Min airflow', 'Max airflow']])
