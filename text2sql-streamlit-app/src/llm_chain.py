import os
import re
from typing import Optional

from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# evaluation helpers (keep if you use ragas)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas import evaluate
from ragas.metrics import ContextPrecision, RubricsScore

# Require the Google GenAI client only (Gemini)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
    _CHAT_GOOGLE_AVAILABLE = True
except Exception:
    _CHAT_GOOGLE_AVAILABLE = False


class LLMChain:
    def __init__(self, db_uri: str = "", model_name: str = "gemini-2.0-flash", api_key: Optional[str] = None):
        """
        LLMChain that uses Google Gemini (langchain_google_genai).
        Set API_KEY and MODEL_NAME env vars or pass api_key/model_name directly.
        """
        if not _CHAT_GOOGLE_AVAILABLE:
            raise RuntimeError("langchain_google_genai not installed. Run: pip install langchain_google_genai")

        self.db = SQLDatabase.from_uri(db_uri) if db_uri else None
        self.model_name = model_name or "gemini-2.0-flash"
        self.api_key = api_key or os.environ.get("API_KEY")
        if not self.api_key:
            raise RuntimeError("API key not set. Set API_KEY environment variable with your Gemini key.")

        self.llm = ChatGoogleGenerativeAI(model=self.model_name, api_key=self.api_key)

        self.prompt_template = ChatPromptTemplate.from_template(
            """Based on the table schema below, write an SQL query that would answer the user's question:
Remember: Only provide the SQL query, don't include anything else. Provide the SQL query in a single line (no line breaks).
Table Schema: {schema}
Question: {question}
SQL Query:"""
        )

    def get_schema(self) -> Optional[str]:
        if not self.db:
            return None
        return self.db.get_table_info()

    def generate_sql_query(self, question: str) -> str:
        schema = self.get_schema() or ""
        prompt_text = self.prompt_template.invoke({"schema": schema, "question": question})
        raw = self.llm.invoke(prompt_text)
        return _clean_sql_from_response(raw)

    def execute_query(self, query: str):
        if not self.db:
            raise RuntimeError("No database configured for LLMChain.execute_query.")
        return self.db.run(query)

    def evaluate_response(self, user_input, response, reference):
        context_precision = ContextPrecision(llm=LangchainLLMWrapper(self.llm))
        rubrics_score = RubricsScore(
            name="helpfulness",
            rubrics=self.get_helpfulness_rubrics(),
            llm=LangchainLLMWrapper(self.llm),
        )
        ragas_metrics = [context_precision, rubrics_score]
        result = evaluate(
            metrics=ragas_metrics,
            dataset=self.create_evaluation_dataset(user_input, response, reference),
        )
        return result

    def get_helpfulness_rubrics(self):
        return {
            "score1_description": "Response is useless/irrelevant, contains inaccurate/deceptive/misleading information and/or contains harmful/offensive content.",
            "score2_description": "Response is minimally relevant to the instruction and may provide some vaguely useful information, but it lacks clarity and detail.",
            "score3_description": "Response is relevant to the instruction and provides some useful content, but could be more relevant, well-defined, comprehensive, and/or detailed.",
            "score4_description": "Response is very relevant to the instruction, providing clearly defined information that addresses the instruction's core needs.",
            "score5_description": "Response is useful and very comprehensive with well-defined key details to address the needs in the instruction."
        }

    def create_evaluation_dataset(self, user_input, response, reference):
        raise NotImplementedError("create_evaluation_dataset not implemented")


def _clean_sql_from_response(resp: Optional[str]) -> str:
    if resp is None:
        return ""
    if not isinstance(resp, str):
        resp = str(resp)
    m = re.search(r"```sql\s*(.*?)\s*```", resp, re.DOTALL | re.IGNORECASE)
    sql = m.group(1).strip() if m else resp.strip()
    return " ".join(sql.split())


def generate_sql_query(question: str, schema: Optional[str] = None) -> str:
    """
    Module-level helper that generates SQL using Google Gemini via langchain_google_genai.
    Uses API_KEY and MODEL_NAME environment variables if not provided explicitly.
    """
    if not question:
        return "-- No question provided."

    if not _CHAT_GOOGLE_AVAILABLE:
        return (
            "-- langchain_google_genai not installed. Install with: pip install langchain_google_genai\n"
            "SELECT * FROM your_table_name WHERE <conditions> LIMIT 100;"
        )

    api_key = os.environ.get("API_KEY")
    model_name = os.environ.get("MODEL_NAME", "gemini-2.0-flash")
    if not api_key:
        return "-- API_KEY environment variable not set. Set it to your Gemini 2.0 Flash key."

    template = """Based on the table schema below, write an SQL query that would answer the user's question:
Remember: Only provide the SQL query, don't include anything else. Provide the SQL query in a single line (no line breaks).
Table Schema: {schema}
Question: {question}
SQL Query:"""

    try:
        prompt = ChatPromptTemplate.from_template(template)
        prompt_text = prompt.invoke({"schema": schema or "", "question": question})
        llm = ChatGoogleGenerativeAI(model=model_name, api_key=api_key)
        raw = llm.invoke(prompt_text)
        return _clean_sql_from_response(raw)
    except Exception as e:
        return (
            f"-- Could not call Gemini LLM: {e}\n"
            "-- Ensure API_KEY is a valid Gemini key and langchain_google_genai is installed.\n"
            "SELECT * FROM your_table_name WHERE <conditions> LIMIT 100;"
        )


__all__ = ["LLMChain", "generate_sql_query"]