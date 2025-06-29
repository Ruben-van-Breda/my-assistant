from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from pandasai.middlewares.streamlit import StreamlitMiddleware
import matplotlib as mpl
import threading

import webbrowser
import shutil

def read_api_key():
    """
    Reads the OpenAI API key from a secrets file.
    """
    api_key_path = "./secrets.txt"  # Adjust the path as needed
    if not os.path.exists(api_key_path):
        raise FileNotFoundError(f"❌ API key file not found at {api_key_path}.")
    
    with open(api_key_path, "r") as f:
        api_key = f.read().strip()
    
    if not api_key:
        raise ValueError("❌ API key is empty.")
    
    return api_key


load_dotenv()
# Read api key from secrets file

API_KEY = read_api_key()
git_path = "https://github.com/Ruben-van-Breda/PandaDataAnalyser/tree/main"
git_path = "/app/pandadataanalyser/"
git_path = "./"

mpl.rcParams['xtick.major.pad'] = 8

st.set_page_config(page_title="Data Analyser", page_icon="🦌", layout="wide")
st.title("Data Analyiser")

st.cache(allow_output_mutation=True, persist=False)
def load_file():
    uploaded_file = st.file_uploader("Upload a file", type=['csv', 'xlsx'])


    return uploaded_file

def save_file():
    pass

def load_files():
    pass

uploaded_file = load_file()
response = ""

# textDir = st.text_input("Enter a directory")
# if st.button("view", "view"):
#     for l in os.listdir(path=textDir):
#         st.write(l)

def chat_with_data(df, prompt):
    llm = OpenAI(api_token=API_KEY)
    # 
    pandas_ai = PandasAI(llm, middlewares=[StreamlitMiddleware()], save_charts=True,
                         save_charts_path=f"{git_path}/picknpay", enforce_privacy=True)
    response = pandas_ai.run(df, prompt=prompt)
    return response



if uploaded_file is not None:
    st.write(uploaded_file)
    # check file extension
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.write(df)

    prompt = st.text_area("Enter you query")

    if st.button("Ask"):
        if prompt:
            st.write("Processing query")
            response = chat_with_data(df, prompt)
            
            print(response)
            st.write(response)
        else:
            st.warning("Please enter a query")
else:
    st.warning("Please upload a file")

# show side bar of the page
st.sidebar.title("Charts")

# show a list of files in directory 
st.sidebar.subheader("Files")
curr_dir = os.getcwd()


# check if there are files in directory
if os.path.exists(f"{git_path}") and os.listdir(f"{git_path}"):

    if st.sidebar.button("Delete All", key="deleteAll"):
        # current directory
        curr_dir = os.getcwd()
        # delete all files in directory
        try:
            # shutil.rmtree(f"{git_path}/")
            pass
            # for i in os.listdir("./picknpay/exports/charts/"):
            #     os.remove(f"{curr_dir}/picknpay/exports/charts/{i}")
            # st.sidebar.write("All files deleted")
        except Exception as e:
            st.sidebar.write("No files found", e)
            pass

try:
    for i in os.listdir(f"{git_path}"):
        st.sidebar.write(i)

        for chart in os.listdir(f"{git_path}"):
            # create a container
            if st.sidebar.button("Delete", i+'delete'):
                # current directory
                curr_dir = os.getcwd()
                os.remove(f"{git_path}/exports/charts/{i}")
                st.sidebar.write("File deleted")
            # load image data
            image = open(f"{git_path}/exports/charts/{i}/{chart}", 'rb').read()
            st.sidebar.download_button(label="Download", key=i+'download' ,data=image, file_name=chart)

            if st.sidebar.button("Open", i+chart):
                # download file
                curr_dir = os.getcwd()
                webbrowser.open_new_tab(f"{git_path}/exports/charts/{i}/{chart}")
                
                
except Exception as e:
    st.sidebar.write("No files found")
                # webbrowser.open_new_tab(f"./picknpay/exports/charts/{i}/{chart}")


