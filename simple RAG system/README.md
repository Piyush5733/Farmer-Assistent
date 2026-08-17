# 🌿 OrganicAI – AI-Powered Organic Farming Assistant

> **Ask anything about organic farming. Get expert answers — instantly.**
>
> OrganicAI is a production-ready **Retrieval-Augmented Generation (RAG)** application
> that answers farmers' questions by searching trusted organic farming books and
> combining them with state-of-the-art AI language models.

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3%2B-1C3C3C?logo=chainlink)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B?logo=streamlit)](https://streamlit.io)
[![FAISS](https://img.shields.io/badge/FAISS-1.8%2B-00599C)](https://faiss.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## ✨ Features

| Feature | Details |
|---|---|
| 📄 **Document RAG** | Retrieves answers from your own PDF library (organic farming books) |
| 🌍 **Bilingual** | Responds in **English** or **Hindi** — toggle in the UI |
| 📚 **Source Citations** | Shows exact book name + page number for every answer |
| 💡 **Follow-up Questions** | Suggests 3 related questions after each answer |
| 🤖 **Multi-LLM** | Supports **Google Gemini** and **OpenAI** — switch via `.env` |
| 🧠 **Local Embeddings** | HuggingFace MiniLM embeddings run on CPU — **no API cost** |
| ⚡ **Fast Search** | FAISS vector index for sub-second similarity retrieval |
| 🔄 **Persistent Index** | Build once, query forever — rebuild with one click |
| 💬 **Chat Memory** | Maintains conversation context across turns |
| 🏷️ **Knowledge Flagging** | Clearly marks when answers use general AI knowledge |

---

## 🏗️ Architecture

```
User Question
     │
     ▼
┌─────────────────────────────────────────┐
│         Streamlit UI  (app.py)           │
│  Chat bubbles │ Source panel │ Follow-ups│
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│         OrganicAIChatbot                 │
│         (src/chatbot.py)                 │
│                                          │
│  1. Condense question (with history)     │
│  2. Retrieve k=5 document chunks         │
│  3. Format context + prompt              │
│  4. Call LLM → parse response            │
└───┬───────────────────┬─────────────────┘
    │                   │
    ▼                   ▼
FAISS Vectorstore    LLM (Gemini / OpenAI)
(vectorstore/)       src/prompts.py
    ▲
    │ embed
HuggingFace MiniLM (local)
    ▲
    │ load + split
PDFs in Docs/
(src/ingest.py)
```

---

## 📁 Project Structure

```
OrganicAI/
├── Docs/                          ← Put your organic farming PDFs here
│   ├── ES-2020-118971.pdf
│   └── ORGANIC FARMING - ...pdf
│
├── src/
│   ├── __init__.py
│   ├── ingest.py                  ← PDF loading, chunking, FAISS indexing
│   ├── retriever.py               ← FAISS vector store loader + retriever
│   ├── chatbot.py                 ← RAG chain, LLM integration, response parsing
│   ├── prompts.py                 ← System prompt, chat template, condense prompt
│   ├── utils.py                   ← Logger, source formatter, language helpers
│   └── tests/
│       ├── test_ingest.py         ← Unit tests for ingestion pipeline
│       └── test_chatbot.py        ← Unit tests for RAG chain (mocked LLM)
│
├── vectorstore/                   ← Auto-generated FAISS index (gitignored)
├── app.py                         ← Streamlit chat UI
├── main.py                        ← CLI entrypoint
├── rebuild_db.py                  ← Standalone vector store rebuild script
├── requirements.txt               ← Python dependencies
├── pyproject.toml                 ← Project metadata + tool config
├── .env.example                   ← Environment variable template
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone / open the project

```bash
cd "d:\Projects\Langchain_RAG\simple RAG system"
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

```bash
copy .env.example .env      # Windows
# or: cp .env.example .env  # macOS / Linux
```

Edit `.env` and set your key:

```dotenv
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_actual_key_here
```

> **Get a free Gemini key** → https://aistudio.google.com/app/apikey

### 5. Add your PDFs

Place any organic farming PDF books inside the `Docs/` folder.
The project already includes two books to get you started.

### 6. Build the knowledge base

```bash
python main.py --ingest
```

This reads all PDFs, creates embeddings, and saves the FAISS index.
**Run this once** — or whenever you add new PDFs.

### 7. Launch OrganicAI

```bash
python main.py
# or directly:
streamlit run app.py
```

Open your browser at **http://localhost:8501** 🎉

---

## 🔄 Vector Database Management (`rebuild_db.py`)

The `rebuild_db.py` script provides a dedicated utility to process all source PDF documents in `Docs/`, generate vector embeddings, and rebuild the persistent FAISS vector store index in `vectorstore/`.

### Command Line Usage

```bash
# Rebuild the FAISS vector database from PDFs in Docs/
python rebuild_db.py

# Force rebuild over existing index files
python rebuild_db.py --force

# Rebuild using a custom docs folder or vectorstore target directory
python rebuild_db.py --docs-dir ./my_pdfs --vectorstore-dir ./my_vectorstore
```

### Core Functions Breakdown

| Function | Module | Description |
|---|---|---|
| `rebuild_database(docs_dir, vectorstore_dir, force)` | `rebuild_db.py` | Top-level function orchestrating the complete ingestion & vector index creation pipeline. |
| `load_documents(docs_dir)` | `src/ingest.py` | Loads all PDF files using `PyPDFLoader`, extracting page text and tagging metadata (`filename`, 0-indexed `page`). |
| `split_documents(documents, chunk_size, chunk_overlap)` | `src/ingest.py` | Splits loaded documents into overlapping chunks (`1000` chars chunk size, `200` chars overlap) using `RecursiveCharacterTextSplitter`. |
| `build_vectorstore(chunks, embedding_model)` | `src/ingest.py` | Generates 384-dimensional dense vectors using `sentence-transformers/all-MiniLM-L6-v2` and constructs the FAISS index. |
| `save_vectorstore(vectorstore, output_dir)` | `src/ingest.py` | Persists index data (`index.faiss` and `index.pkl`) to disk in the `vectorstore/` directory. |

---

## 🔧 Configuration

All settings are controlled through your `.env` file:

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `gemini` | LLM to use: `gemini` or `openai` |
| `GOOGLE_API_KEY` | — | Your Google AI Studio API key |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Gemini model name |
| `OPENAI_API_KEY` | — | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model name |
| `RETRIEVER_K` | `5` | Number of document chunks retrieved per query |
| `CHUNK_SIZE` | `1000` | Characters per document chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between consecutive chunks |
| `DOCS_DIR` | `Docs` | Folder containing PDF files |
| `VECTORSTORE_DIR` | `vectorstore` | Folder where FAISS index is saved |
| `LOG_LEVEL` | `INFO` | Logging verbosity: DEBUG / INFO / WARNING |

---

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest src/tests/ -v

# Run only ingestion tests
python -m pytest src/tests/test_ingest.py -v

# Run only chatbot tests (no API key needed — uses mocks)
python -m pytest src/tests/test_chatbot.py -v
```

---

## 💬 Example Questions

**English:**
- *"How do I start composting at home?"*
- *"What are natural ways to control aphids on tomatoes?"*
- *"How can I improve clay soil for growing vegetables?"*
- *"What is crop rotation and why is it important?"*
- *"How do I make liquid fertiliser from banana peels?"*

**Hindi:**
*(Select Hindi in the sidebar first)*
- *"जैविक खेती में कीट नियंत्रण कैसे करें?"*
- *"मिट्टी की उर्वरता कैसे बढ़ाएं?"*
- *"कम्पोस्ट खाद कैसे बनाएं?"*

---

## 🔌 Extending OrganicAI

The project is designed to be easy to extend:

### 🎤 Voice Input
Integrate [`streamlit-webrtc`](https://github.com/whitphx/streamlit-webrtc) for browser microphone access, then pipe audio through OpenAI Whisper for transcription. Feed the transcript to `chatbot.ask()`.

### 🌦️ Weather Integration
Add a weather tool using the [Open-Meteo API](https://open-meteo.com/) (free, no key needed). Create `src/tools/weather.py` and wrap it as a LangChain `Tool` for the chatbot.

### 🔬 Plant Disease Detection
Add an image upload widget in `app.py`. Use a fine-tuned ResNet / EfficientNet model from HuggingFace Hub (`src/tools/disease_detector.py`) to classify crop diseases from photos.

### 🗄️ Additional Document Types
Replace `PyPDFLoader` in `src/ingest.py` with LangChain's `DirectoryLoader` and add `.docx`, `.txt`, or `.csv` loaders.

### 📊 Analytics Dashboard
Add a `pages/analytics.py` Streamlit page that visualises query frequency, popular topics, and source coverage using Plotly.

---

## 🛠️ CLI Reference

```
python main.py [OPTIONS]

Options:
  --ingest          Build/rebuild the FAISS knowledge base from PDFs
  --force           Force rebuild even if index already exists
  --docs-dir PATH   Override the docs directory
  --help            Show this help message

Examples:
  python main.py                    # Launch the web UI
  python main.py --ingest           # Build knowledge base (skip if exists)
  python main.py --ingest --force   # Always rebuild the knowledge base
  python main.py --ingest --docs-dir ./my_books   # Custom docs folder
```

---

## 📦 Key Dependencies

| Package | Version | Purpose |
|---|---|---|
| `langchain` | ≥ 0.3 | RAG framework & LCEL chains |
| `langchain-community` | ≥ 0.3 | FAISS integration, PyPDFLoader |
| `langchain-google-genai` | ≥ 2.0 | Gemini LLM wrapper |
| `langchain-openai` | ≥ 0.2 | OpenAI LLM wrapper |
| `langchain-huggingface` | ≥ 0.1 | HuggingFace embeddings |
| `faiss-cpu` | ≥ 1.8 | Vector similarity search |
| `sentence-transformers` | ≥ 3.0 | Local embedding model |
| `streamlit` | ≥ 1.38 | Web UI framework |
| `pypdf` | ≥ 4.0 | PDF parsing |
| `loguru` | ≥ 0.7 | Structured logging |
| `python-dotenv` | ≥ 1.0 | Environment variable management |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built with ❤️ for farmers worldwide — OrganicAI v1.0*
