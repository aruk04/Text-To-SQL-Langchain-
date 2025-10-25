def format_sql_query(query):
    return query.strip()

def process_user_input(user_input):
    return user_input.strip()

def validate_query(query):
    if not query:
        raise ValueError("The SQL query cannot be empty.")
    # Additional validation logic can be added here

def extract_query_from_response(response):
    import re
    match = re.search(r"```sql\s*(.*?)\s*```", response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def log_error(error_message):
    import logging
    logging.error(error_message)