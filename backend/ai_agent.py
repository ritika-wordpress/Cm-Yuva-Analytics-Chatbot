import os
import re
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.chains import LLMChain

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase

from database import engine

# ---------------------------------------------------
# LOAD ENV
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

db = SQLDatabase(engine)

print("TABLES:", db.get_usable_table_names())

# ---------------------------------------------------
# LLM
# ---------------------------------------------------

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b",
    temperature=0
)

# ---------------------------------------------------
# STEP 1: SQL GENERATION PROMPT
# ---------------------------------------------------

sql_prompt = PromptTemplate(
    input_variables=["input", "table_info"],
    template="""
You are a SQL expert for SQLite.

Database Schema:
{table_info}

Question:
{input}

RULES:
- Output ONLY valid SQLite SQL
- NO markdown
- NO ** or backticks
- NO explanations
"""
)

sql_chain = LLMChain(llm=llm, prompt=sql_prompt)

# ---------------------------------------------------
# CLEAN SQL
# ---------------------------------------------------

def clean_sql(sql):
    sql = re.sub(r"```sql|```|\*\*", "", sql)
    return sql.strip()

# ---------------------------------------------------
# STEP 2: INSIGHT GENERATION PROMPT
# ---------------------------------------------------

insight_prompt = PromptTemplate(
    input_variables=["question", "data"],
    template="""
You are a business data analyst.

Question:
{question}

SQL Result Data:
{data}

TASK:
- Give ONLY insights
- No SQL
- No formatting
- Explain trends clearly
"""
)

insight_chain = LLMChain(llm=llm, prompt=insight_prompt)

# ---------------------------------------------------
# EXECUTE SQL
# ---------------------------------------------------

def run_sql(query):
    return db.run(query)

# ---------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------

def ask_ai(question):

    try:
        # 1. Generate SQL
        sql = sql_chain.run({
            "input": question,
            "table_info": db.get_table_info()
        })

        sql = clean_sql(sql)

        # 2. Execute SQL safely
        data = run_sql(sql)

        # 3. Generate insights
        result = insight_chain.run({
            "question": question,
            "data": data
        })

        return result

    except Exception as e:
        return f"AI Error: {str(e)}"