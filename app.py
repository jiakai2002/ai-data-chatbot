import streamlit as st
import pandas as pd
import tempfile
import os
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="CSV Chatbot", layout="centered", initial_sidebar_state="collapsed")
st.title("🤖 Ask your CSV")

# Initialize session state
if 'csv_files' not in st.session_state:
    st.session_state.csv_files = {}  # {filename: (dataframe, temp_path)}
if 'query_history' not in st.session_state:
    st.session_state.query_history = []  # [(query, response)]

# Sidebar for query history
with st.sidebar:
    st.title("Query History")

    if (st.session_state.query_history == []):
        st.info("No queries yet.")
    
    if st.button("Clear History"):
        st.session_state.query_history = []
        st.experimental_rerun()
    
    for i, (query, response) in enumerate(st.session_state.query_history):
        with st.expander(f"Q: {query[:50]}{'...' if len(query) > 50 else ''}"):
            st.text(f"Query: {query}")
            st.text(f"Response: {response}")
    

uploaded_files = st.file_uploader("Upload your CSV files", type=["csv"], accept_multiple_files=True)

# Store uploaded files in session state
for uploaded_file in uploaded_files:
    if uploaded_file.name not in st.session_state.csv_files:
        df = pd.read_csv(uploaded_file)
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        df.to_csv(temp_file.name, index=False)
        st.session_state.csv_files[uploaded_file.name] = (df, temp_file.name)

# Show preview
if st.session_state.csv_files:
    # Choose which file to preview
    if len(st.session_state.csv_files) > 0:
        selected_file = st.selectbox("Select file to preview:", options=list(st.session_state.csv_files.keys()))
        
        # Preview selected file
        df, _ = st.session_state.csv_files[selected_file]
        rows_to_show = st.slider("Rows to display", min_value=5, max_value=50, value=5)
        st.dataframe(df.head(rows_to_show))
    
    # Query section
    query = st.text_area("Enter your question:")
    
    if st.button("Submit"):
        if query:
            with st.spinner("Thinking..."):
                try:
                    # Create CSV agent 
                    file_paths = [path for _, path in st.session_state.csv_files.values()]
                    agent = create_csv_agent(
                        ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
                        file_paths,
                        verbose=True,
                        allow_dangerous_code=True
                    )
                    
                    # Get response
                    response = agent.run(query)
                    st.success("Answer")
                    st.write(response)
                    
                    # Add to history
                    st.session_state.query_history.append((query, response))
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a question.")
else:
    st.info("👆 Please upload one or more CSV files to get started!")

def cleanup():
    for _, path in st.session_state.csv_files.values():
        try:
            os.unlink(path)
        except:
            pass

import atexit
atexit.register(cleanup)