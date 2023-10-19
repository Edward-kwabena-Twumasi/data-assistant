import streamlit as st
import pandas as pd
import pathlib as path


# read in excel or csv file
def validate_file(source):
    if path.Path(source).is_file():
        if path.Path(source).suffix in [".csv",".xlsx"]:
            print("file is valid")
            return True
        else:
            print("unaccepted file format")
            print(path.Path(source).suffix)
            return False
    else:
        print("file is invalid")
        return False
 
    
# read input 
def read_input(source):
    is_valid = validate_file(source)
    if is_valid:
        if path.Path(source).suffix == ".csv":
            data = pd.read_csv(source)
            return (data,source)

        elif path.Path(source).suffix == ".xlsx":
            data = pd.read_excel(source)
            return (data,source)
    return (None,source)

# summariise data
def describe_data(data):
    if len(data) > 0:
        """ ###
        Shape of dataset 
        """
        #Get shape of data
        shape = data.shape

        st.write(" ###### Dataset has {} rows and {} columns".format(shape[0],shape[1])) 
       
        # Take a peep at the data
        """ ### Explore your data
        View first 5 rows
        """

        st.write(data.head())

        """ ###
        Columns in dataset
        """
        #Get columns
        st.write(data.columns)

        """ ###
        Datatypes in dataset 
        """
        #Get data types
        st.write(data.dtypes)
        
        numerical_dtypes = ['int64', 'float64']  

        if all(dt in numerical_dtypes for dt in data.dtypes):
            st.write("Dataset contains only numerical data types")
            """ ###
           Summary  
             """
            st.write(data.describe())
        else:
            st.write(""" #### Dataset contains non-numerical data types""")

            """ ###
            Summary of numerical fields
            """
            #Descriptive summary
            st.write(data.describe())

            """ ###
            Summary of categorical fields
            """
            #Descriptive summary
            st.write(data.select_dtypes(exclude=['int64','float64']).describe())

