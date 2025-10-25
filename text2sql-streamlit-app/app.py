import streamlit as st
from src.llm_chain import generate_sql_query
from src.sql_runner import execute_query
from src.db import get_schema

def main():
    st.title("Text to SQL Chatbot")
    
    # Display the database schema
    schema = get_schema()
    st.subheader("Database Schema")
    st.write(schema)

    # User input for the question
    user_question = st.text_input("Ask a question about the database:")

    if st.button("Generate SQL Query"):
        if user_question:
            # Generate SQL query using the LLM
            sql_query = generate_sql_query(user_question, schema)
            st.subheader("Generated SQL Query")
            st.code(sql_query)

            # Execute the SQL query
            if st.button("Execute SQL Query"):
                results = execute_query(sql_query)
                st.subheader("Query Results")
                st.write(results)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()