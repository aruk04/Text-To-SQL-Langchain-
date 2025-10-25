# text2sql-streamlit-app/README.md

# Text-to-SQL Streamlit App

This project is a Streamlit application that allows users to generate SQL queries based on natural language questions. It leverages the Langchain framework and the RAGAS evaluation metrics to provide accurate and helpful SQL query generation.

## Project Structure

```
text2sql-streamlit-app
├── app.py                # Entry point for the Streamlit application
├── src                   # Source files for the application
│   ├── frontend.py       # Streamlit components for the user interface
│   ├── llm_chain.py      # Logic for interacting with the language model
│   ├── sql_runner.py      # Functions to execute SQL queries
│   ├── db.py             # Database connection and query execution
│   ├── ragas_eval.py      # Evaluation logic using RAGAS framework
│   └── utils.py          # Utility functions for the application
├── notebooks
│   └── langchain.ipynb   # Jupyter notebook with implementation details
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables
├── .gitignore            # Files to ignore in Git
├── tests                 # Unit tests for the application
│   └── test_app.py       # Tests for the Streamlit application
└── README.md             # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd text2sql-streamlit-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables in the `.env` file. Make sure to include any necessary API keys and database credentials.

## Usage

To run the Streamlit application, execute the following command:
```
streamlit run app.py
```

Open your web browser and navigate to `http://localhost:8501` to access the application.

## Features

- Input natural language questions to generate SQL queries.
- Evaluate the generated queries using RAGAS metrics.
- Display results from the database based on the generated SQL queries.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.