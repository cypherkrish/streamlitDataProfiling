import streamlit as st
import pandas as pd
import sys
import os
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

def get_filesize(file):
    size_in_bytes = sys.getsizeof(file)
    size_mb = size_in_bytes / (1024 * 1024)
    return size_mb

def validate_file(file):
    filename = file.name
    name, ext = os.path.splitext(filename)

    if ext in ('.csv', '.xlsx'):
        return ext
    else:
        return False



st.set_page_config(page_title='Data Profiler', 
                   layout='wide')

with st.sidebar:
    upload_file = st.file_uploader("Upload .csv, .xls files, not exceeding 10MB ")
    if upload_file is not None:
        st.write("Mode of the report: ")
        minimal = st.checkbox("Display minimal report")
        display_mode = st.radio("Display Mode", 
                                options=('Primary', 'Dark', 'Orange'))
        if display_mode == 'Dark':
            dark_mode = True
            orange_mode = False
        elif display_mode == 'Orange':
            dark_mode = False
            orange_mode = True
        else:
            dark_mode = False
            orange_mode = False


if upload_file is not None:
    ext = validate_file(upload_file)

    if ext:
        filesize = get_filesize(upload_file)
        if filesize <= 10:

            if ext == '.csv':
                df = pd.read_csv(upload_file)
            
            else:
                xl_file = pd.ExcelFile(upload_file)
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar.selectbox('Select the sheet:', sheet_tuple)
                df = xl_file.parse(sheet_name=sheet_name)

            with st.spinner('Generating Report'):
                pr = ProfileReport(df, minimal=minimal, 
                                dark_mode=dark_mode, 
                                orange_mode=orange_mode, )
            
            st_profile_report(pr)
        
        else:
            st.error(f'Maximum file size is 10 MB, but received {filesize} MB.') 
        
    else:
        st.error("Please upload either .csv or .xlsx file.")
    
else:
    st.title('Data Profiler')
    st.info('Upload your file in the left sidebar to generate data profiling')
