import streamlit as st
import data_utils
import llm_utils
import trulens_utils
import config

st.title("Graph RAG Assistant")

search_table = st.text_input("Enter Snowflake table name with text", value="TEXT_DOCUMENTS")
user_query = st.text_area("Enter your question:", value="What is snowflake?")
db_connection = data_utils.get_snowflake_connection()


if st.button("Get Answer"):
    if search_table and user_query:
        with st.spinner("Searching and generating..."):
            try:
                tru_chain = trulens_utils.setup_trulens(app_id="Snowflake_RAG_App", search_table=search_table, db_connection=db_connection)
                response = tru_chain.app(user_query) # We are calling the app via the TruChain object
                st.write("Answer:", response)
            except Exception as e:
              st.error(f"An error occured: {e}")
    else:
        st.warning("Please provide the Table Name and a Query.")