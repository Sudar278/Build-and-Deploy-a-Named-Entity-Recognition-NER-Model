import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Load trained model and tokenizer
MODEL_DIR = "./bert-ner-trained"  # Update with your trained model directory
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForTokenClassification.from_pretrained(MODEL_DIR)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Basic API key authentication
API_KEY = os.getenv("API_KEY")

def verify_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

# Request model
class TextRequest(BaseModel):
    text: str

# Prediction endpoint
@app.post("/predict", dependencies=[Depends(verify_api_key)])
def predict(request: TextRequest) -> Dict[str, List[Dict]]:
    text = request.text
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    entities = ner_pipeline(text)
    return {"entities": entities}

# Run the FastAPI app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
