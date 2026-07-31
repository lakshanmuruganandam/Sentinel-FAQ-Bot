import os
import json
import time
import re
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn

app = FastAPI(title="Sentinel FAQ AI | Neural Knowledge Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FAQ_FILE = "faqs.json"
FAQS = []
vectorizer = None
tfidf_matrix = None

STOP_WORDS = {
    'what', 'is', 'the', 'and', 'a', 'an', 'in', 'on', 'of', 'for', 'to', 
    'how', 'do', 'i', 'my', 'are', 'your', 'with', 'does', 'can', 'this', 'it'
}

def preprocess_text(text: str) -> str:
    """Clean, tokenize, and normalize input text without external ZIP dependencies."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    filtered = [w for w in tokens if w not in STOP_WORDS]
    return " ".join(filtered) if filtered else text

def build_faq_index():
    global FAQS, vectorizer, tfidf_matrix
    if not os.path.exists(FAQ_FILE):
        return
    with open(FAQ_FILE, "r", encoding="utf-8") as f:
        FAQS = json.load(f)
    
    questions = [preprocess_text(faq["question"]) for faq in FAQS]
    vectorizer = TfidfVectorizer().fit(questions)
    tfidf_matrix = vectorizer.transform(questions)
    print(f"[Knowledge Engine] Indexed {len(FAQS)} FAQs successfully.")

build_faq_index()

class ChatRequest(BaseModel):
    question: str

class AddFAQRequest(BaseModel):
    category: str
    question: str
    answer: str

@app.get("/api/faqs")
async def get_all_faqs():
    return {"faqs": FAQS, "total": len(FAQS)}

@app.post("/api/chat")
async def chat_faq(req: ChatRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    start_time = time.time()
    clean_q = preprocess_text(req.question)
    
    user_vec = vectorizer.transform([clean_q])
    similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    
    best_idx = int(similarities.argmax())
    best_score = float(similarities[best_idx])
    
    execution_time_ms = round((time.time() - start_time) * 1000, 2)
    
    SIMILARITY_THRESHOLD = 0.15
    
    if best_score >= SIMILARITY_THRESHOLD:
        matched_faq = FAQS[best_idx]
        
        top_indices = similarities.argsort()[-3:][::-1]
        suggestions = [FAQS[i]["question"] for i in top_indices if i != best_idx]
        
        return {
            "status": "success",
            "matched": True,
            "question": req.question,
            "answer": matched_faq["answer"],
            "matched_question": matched_faq["question"],
            "category": matched_faq["category"],
            "confidence": round(best_score * 100, 1),
            "suggestions": suggestions[:2],
            "metrics": {
                "execution_ms": f"{execution_time_ms}ms"
            }
        }
    else:
        suggestions = [faq["question"] for faq in FAQS[:3]]
        return {
            "status": "success",
            "matched": False,
            "question": req.question,
            "answer": "I'm sorry, I couldn't find a high-confidence match for your question in our knowledge base. Please check our suggested topics below or contact support@sentinel.ai.",
            "confidence": round(best_score * 100, 1),
            "suggestions": suggestions,
            "metrics": {
                "execution_ms": f"{execution_time_ms}ms"
            }
        }

@app.post("/api/faqs/add")
async def add_faq(req: AddFAQRequest):
    global FAQS
    new_faq = {
        "id": len(FAQS) + 1,
        "category": req.category,
        "question": req.question,
        "answer": req.answer
    }
    FAQS.append(new_faq)
    with open(FAQ_FILE, "w", encoding="utf-8") as f:
        json.dump(FAQS, f, indent=2)
    
    build_faq_index()
    return {"status": "success", "message": "New FAQ added and neural matrix re-indexed.", "faq": new_faq}

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
