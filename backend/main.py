from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

import pandas as pd

from database import engine

from ai_agent import ask_ai

# ---------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------

app = FastAPI(title="CM YUVA AI Agent")

# ---------------------------------------------------
# UPLOAD API (FAST VERSION)
# ---------------------------------------------------

@app.post("/upload-data")

async def upload_data(

    certification: UploadFile = File(...),

    loan: UploadFile = File(...),

    fraud: UploadFile = File(...)
):

    try:

        # ---------------------------------------------------
        # READ CSV FILES
        # ---------------------------------------------------

        cert_df = pd.read_csv(certification.file)

        loan_df = pd.read_csv(loan.file)

        fraud_df = pd.read_csv(fraud.file)

        # ---------------------------------------------------
        # CLEAN COLUMN NAMES
        # ---------------------------------------------------

        cert_df.columns = (
            cert_df.columns
            .str.strip()
            .str.replace("\n", "")
        )

        loan_df.columns = (
            loan_df.columns
            .str.strip()
            .str.replace("\n", "")
        )

        fraud_df.columns = (
            fraud_df.columns
            .str.strip()
            .str.replace("\n", "")
            .str.replace("  ", " ")
        )

        # ---------------------------------------------------
        # SAVE TO DATABASE (VERY FAST)
        # ---------------------------------------------------

        cert_df.to_sql(

            "certification",

            engine,

            if_exists="replace",

            index=False,

        )

        loan_df.to_sql(

            "loan_application",

            engine,

            if_exists="replace",

            index=False,

        )

        fraud_df.to_sql(

            "fraud_record",

            engine,

            if_exists="replace",

            index=False,

        )

        return {
            "message": "CSV datasets uploaded successfully"
        }

    except Exception as e:

        return JSONResponse(

            status_code=500,

            content={
                "error": str(e)
            }
        )

# ---------------------------------------------------
# AI CHAT ENDPOINT
# ---------------------------------------------------

@app.post("/chat")

async def chat(query: dict):

    try:

        question = query.get("question")

        response = ask_ai(question)

        return {
            "response": response
        }

    except Exception as e:

        return JSONResponse(

            status_code=500,

            content={
                "error": str(e)
            }
        )