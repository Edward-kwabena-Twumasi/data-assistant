
import streamlit as st
import pandas as pd
import pathlib as path
import os
import time

st.title("Data scientist assistant")

st.write("""
          ##### Assist with data preparation / model building"""
         )
def upload_file(file):
    try:

        with st.spinner("Processing the file..."):
            # Read the content of the uploaded file
            file_content = file.read()

        # Now, you can use the file_content or save it to a specific location
        # For example, save it to a temporary directory
        temp_dir = "datasets"  # Replace with your desired temporary directory
        os.makedirs(temp_dir, exist_ok=True)

        # Save the uploaded file to the temporary directory
        file_path = os.path.join(temp_dir, file.name)
        with open(file_path, "wb") as temp_file:
            temp_file.write(file_content)

        wait_time = 2  # seconds
        while not os.path.exists(file_path) or os.path.getsize(file_path) != len(file_content):
            time.sleep(wait_time)
    except:
       st.write("Exception occured reading file contents")

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
        
def clean_data(data):

    null_fields = get_null_fields(data)[0]

    if len(null_fields) > 0:

        suggest_cleaning_options()

        action = st.radio(
        'Preferred action',
        ("Impute missing","Drop columns"))
        st.write(f"Action . {action} ")

        cleaned_data = take_action(action,data,get_null_fields(data)[1])

        st.write(cleaned_data)



def impute_missing(data):
    from sklearn.impute import SimpleImputer
    object_cols = data.select_dtypes(exclude = ['int64','float64']).columns
    
    data_to_impute = data
    columns = data.columns
    if len(object_cols) > 0:
      data_to_impute =  encode_categorical(data,object_cols)
      columns = data_to_impute.columns
        
    # Imputation
    my_imputer = SimpleImputer()
    imputed_X_train = pd.DataFrame(my_imputer.fit_transform(data_to_impute))

    # Imputation removed column names; put them back
    imputed_X_train.columns = columns
    return imputed_X_train
    

def encode_categorical(data,object_cols):

    from sklearn.preprocessing import OneHotEncoder

    # Apply one-hot encoder to each column with categorical data
    OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(data[object_cols]))

    # One-hot encoding removed index; put it back
    OH_cols_train.index = data.index

    # Remove categorical columns (will replace with one-hot encoding)
    num_X_train = data.drop(object_cols, axis=1)

    # Add one-hot encoded columns to numerical features
    OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)

    # Ensure all columns have string type
    OH_X_train.columns = OH_X_train.columns.astype(str)

    return OH_X_train

def take_action(decision,data,columns=[]):
    
    if decision == "Drop columns": 
       cleaned = data.drop(columns,axis=1)
       st.write("Dropped columns {} from dataset".format(columns))
       return cleaned
    
    elif decision == "Impute missing":
       cleaned = impute_missing(data)
       return cleaned

def plot_data(data):
     st.write("Plotting columns {}".format(data.columns[1]))
     st.line_chart(data[data.columns[1]])



#read input

file = st.file_uploader("pick a file")

if file:
    upload_file(file)

    file_path = os.path.join("datasets",file.name)
    input = read_input(file_path)

    if input[0] is None:
        st.write("Provided file ' {} ' in ivalid".format(input[1]))
    else:
        st.write("Loaded dataset {}".format(file_path))
        data = input[0]
       
        describe_data(data)

        get_null_stats(data)

        clean_data(data)


        

       
