import streamlit as st
import requests

def main():
    st.title("Text-to-SQL Chatbot")

    # User input for the question
    user_question = st.text_input("Enter your question:")

    if st.button("Submit"):
        if user_question:
            # Call the backend API to get the SQL query
            response = requests.post("http://localhost:8000/generate_sql", json={"question": user_question})

            if response.status_code == 200:
                sql_query = response.json().get("sql_query")
                st.success(f"Generated SQL Query: {sql_query}")
                
                # Execute the SQL query and display results
                execute_query = st.button("Execute Query")
                if execute_query:
                    result_response = requests.post("http://localhost:8000/execute_sql", json={"query": sql_query})
                    if result_response.status_code == 200:
                        results = result_response.json().get("results")
                        st.write("Query Results:")
                        st.write(results)
                    else:
                        st.error("Error executing the SQL query.")
            else:
                st.error("Error generating SQL query.")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()