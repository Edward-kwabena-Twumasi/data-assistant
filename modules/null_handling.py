import streamlit as st
import pandas as pd
import pathlib as path

#What fields have  null values

def get_null_stats(data):
    
    #What is the percentage of these null values 
    null_fields = get_null_fields(data)[0]

    if len(null_fields) == 0:
        st.write("Dataset has no missing values")
        return

    null_fields_names = get_null_fields(data)[1]
    
    st.write(""" ###
        Missing values in dataset
    """)
    
    left_column, right_column = st.columns(2)

    with left_column:
        st.write(null_fields)
    
    for col in null_fields_names:
        null_fields[col] = null_fields[col]*100/len(data)

    null_fields = null_fields.rename("Missing Values %")

    with right_column:
        st.write(null_fields)
        st.write("n_null/n_rows % per column")
       
def get_null_fields(data):
    null_stats = data.isnull().sum()
    null_fields = null_stats[null_stats>0]

    null_fields = null_fields.rename("Missing Values")
    #What is the percentage of these null values 
    null_fields_names = null_fields.index

    return (null_fields,null_fields_names)

def suggest_cleaning_options():
        st.write("##### Possible actions to take")
        st.write("""
            1. Drop columns with missing values
            2. Inpute missing data
            """)