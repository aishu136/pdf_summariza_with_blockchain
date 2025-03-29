from fastapi import FastAPI, UploadFile, File
import pdfplumber
from model import summarize_text
from blockchain import store_summary_on_blockchain

app = FastAPI()

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...), store_on_blockchain: bool = False):
    try:
        with pdfplumber.open(file.file) as pdf:
            text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        
        if not text:
            return {"error": "No text extracted from PDF."}

        summary = summarize_text(text)

        if store_on_blockchain:
            tx_hash = store_summary_on_blockchain(summary)
            return {"summary": summary, "tx_hash": tx_hash}

        return {"summary": summary}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

