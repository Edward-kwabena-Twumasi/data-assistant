import streamlit as st
import pandas as pd

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
