import streamlit as st

SNOWFLAKE_ACCOUNT = st.secrets["SNOWFLAKE_ACCOUNT"]
SNOWFLAKE_USER = st.secrets["SNOWFLAKE_USER"]
SNOWFLAKE_PASSWORD = st.secrets["SNOWFLAKE_PASSWORD"]
SNOWFLAKE_DATABASE = st.secrets["SNOWFLAKE_DATABASE"]
SNOWFLAKE_SCHEMA = st.secrets["SNOWFLAKE_SCHEMA"]
SNOWFLAKE_WAREHOUSE = st.secrets["SNOWFLAKE_WAREHOUSE"]

LLM_MODEL = "mistral-large2" 

TRULENS_API_KEY = st.secrets["TRULENS_API_KEY"]
TRULENS_PROJECT_NAME = "RAGAssistant" 