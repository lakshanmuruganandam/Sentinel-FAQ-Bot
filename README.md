<div align="center">
  <img src="https://img.shields.io/badge/Sentinel-FAQ_Bot-0f172a?style=for-the-badge&logo=scikitlearn" alt="Sentinel FAQ Bot Banner">
  <h1>Sentinel FAQ Bot ✦</h1>
  <p><b>Cognitive TF-IDF Intent Matching Chatbot</b></p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
  [![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)]()
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![Status](https://img.shields.io/badge/Status-Production_Ready-success.svg)]()
</div>

---

## 🚀 The Vision

Customer support systems are often plagued by rigid logic trees or overly expensive LLM APIs that hallucinate. **Sentinel FAQ Bot** strikes the perfect balance by leveraging localized, deterministic machine learning models to answer customer queries instantly.

By transforming text into high-dimensional semantic vectors using TF-IDF, it mathematically determines user intent, matching it securely and rapidly against an internal knowledge base without exposing data to external cloud providers.

---

## 🏆 Unmatched Performance: Competitive Analysis

Sentinel FAQ Bot provides the deterministic reliability of rule-based systems with the semantic flexibility of machine learning.

| Feature | Sentinel FAQ Bot (Ours) | OpenAI API (RAG) | Dialogflow | Regex/Rule-Based |
|---------|-------------------------|------------------|------------|------------------|
| **Hallucination Risk**| **0% (Deterministic)** | Medium-High | Low | 0% |
| **Data Sovereignty** | **100% On-Premise** | Stored in Cloud | Stored in Cloud | On-Premise |
| **Cost Per Query**| **$0.00** | $0.002 | $0.007 | $0.00 |
| **Semantic Matching** | **Yes (TF-IDF)** | Yes | Yes | No |

---

## 🧠 Core Architecture & System Flow

```mermaid
graph TD
    A["Client UI (Web)"] -->|"POST {user_id, question}"| B("FastAPI Semantic Gateway")
    B --> C{"NLTK Pre-Processing"}
    C -->|"Tokenize & Lemmatize"| D["Stop-word Removal"]
    D --> E["TF-IDF Vectorization"]
    E --> F["Cosine Similarity Matrix"]
    F --> G{"Max Score > Threshold (0.1)"}
    G -->|"Match Found"| H["Retrieve KB Answer"]
    G -->|"No Match"| I["Return Default Fallback"]
    H --> J["JSON Success Payload"]
    I --> J
    J --> A
```

### 1. Semantic Vectorization (TF-IDF)
Instead of exact keyword matching, Sentinel leverages Term Frequency-Inverse Document Frequency (TF-IDF) to convert queries into vectors. It down-weights common filler words and prioritizes unique nouns and verbs, effectively understanding the mathematical "shape" of a user's intent.

### 2. Scalable Knowledge Base
The bot maps semantic distances (using Cosine Similarity) against a scalable JSON knowledge base. This allows non-technical teams to add FAQs without retraining models or modifying code.

---

## 📂 Project Structure & Files

- `main.py`: The secure FastAPI gateway hosting the NLP pipeline.
- `faqs.json`: The external knowledge base defining all question-answer pairs.
- `index.html`: The VisionOS-inspired conversational UI with glowing chat bubbles.
- `requirements.txt`: Python dependencies.
- `run_eval.py`: Automated testing script checking intent matching accuracy and confidence scores.

---

## ⚙️ Installation & Usage

### Prerequisites
- Python 3.9+
- NLTK, Scikit-Learn, FastAPI

### Quick Start
```bash
# 1. Clone the repository
git clone https://github.com/lakshanmuruganandam/Sentinel-FAQ-Bot.git
cd Sentinel-FAQ-Bot

# 2. Install dependencies
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"

# 3. Boot the Cognitive Engine
python main.py
```
*The UI Dashboard will be available at `http://localhost:8002/`.*

---

## 🤝 Contributing
We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📜 License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---
<div align="center">
  <b>Intelligence without hallucination. Engineered by Lakshan Muruganandam.</b>
</div>
