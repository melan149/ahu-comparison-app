
import streamlit as st
import pandas as pd

# Load and process the Excel file
df = pd.read_excel('Data_2025.xlsx', header=None, engine='openpyxl')
df = df.transpose()

# Set the second row as header and drop the first two rows
df.columns = df.iloc[1]
df = df.drop([0, 1])

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Convert all data to string
df = df.astype(str)

# Sidebar filters
st.sidebar.header('Filters')
unit_name = st.sidebar.selectbox('Unit name', df['unit name'].unique())
region = st.sidebar.selectbox('Region', df['region'].unique())
year = st.sidebar.selectbox('Year', df['year'].unique())
quarter = st.sidebar.selectbox('Quarter', df['quarter'].unique())
unit_size = st.sidebar.selectbox('Unit size', df['unit size'].unique())
recovery_type = st.sidebar.selectbox('Recovery type', df['recovery type1'].unique())

# Filter the data
filtered_df = df[
    (df['unit name'] == unit_name) &
    (df['region'] == region) &
    (df['year'] == year) &
    (df['quarter'] == quarter) &
    (df['unit size'] == unit_size) &
    (df['recovery type1'] == recovery_type)
]

# Display results
st.write('### Filtered Data')
st.dataframe(filtered_df)
