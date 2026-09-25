from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "MRNH/mbart-german-grammar-corrector"
device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)
model.eval()

app = FastAPI(title="German Grammar Corrector")

class CorrectionRequest(BaseModel):
    text: str

class CorrectionResponse(BaseModel):
    original: str
    corrected: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/correct", response_model=CorrectionResponse)
def correct(req: CorrectionRequest):
    inputs = tokenizer(req.text, return_tensors="pt").to(device)
    with torch.no_grad():
        generated = model.generate(**inputs, max_length=256)
    corrected_text = tokenizer.decode(generated[0], skip_special_tokens=True)
    return CorrectionResponse(original=req.text, corrected=corrected_text)
