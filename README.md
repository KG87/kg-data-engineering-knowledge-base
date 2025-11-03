# KG: Data Engineering Knowledge Base

An AI-powered retrieval-augmented generation (RAG) system built by **Kenroy Green (KG)**.

This application lets you:

- Ask data-engineering questions in natural language
- Retrieve relevant context from a curated knowledge base
- Get answers grounded in your own documents
- Upload new documents and extend the knowledge base over time

The focus is practical, production-grade data engineering:
Azure Data Factory, dbt, data modeling (Kimball + Medallion), SQL optimisation, and insurance analytics.

---

## Tech Stack

- **Python 3.12+**
- **Gradio** – web UI (chat + upload)
- **LlamaIndex** – RAG orchestration and document handling
- **Pinecone** – vector database for semantic search
- **OpenAI API** – embeddings + language model
- **dotenv** – environment variable management

---

## Repository Structure

```
kg-data-engineering-knowledge-base/
│
├── app.py                    # Main Gradio app (KG-branded dark UI, chat + upload)
├── ingest_documents.py       # One-off / batch ingestion into Pinecone
├── query_knowledge_base.py   # Command-line querying for quick tests
│
├── documents/                # Example domain knowledge used by the RAG system
│   ├── azure_data_factory.txt
│   ├── data_modeling.txt
│   ├── dbt_best_practices.txt
│   ├── insurance_analytics.txt
│   └── sql_optimization.txt
│
├── requirements.txt          # Python dependencies
└── .gitignore                # venv, .env, caches, OS files, etc.
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/KG87/kg-data-engineering-knowledge-base.git
cd kg-data-engineering-knowledge-base
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
# .\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=de-knowledge-base

EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

> The `.env` file is already in `.gitignore` and should **not** be committed.

---

## Ingest Documents

Before chatting, you need to build the vector index in Pinecone.

This script:

- Reads all files in the `documents/` folder  
- Chunks them  
- Generates OpenAI embeddings  
- Stores them in a Pinecone index  

Run:

```bash
python ingest_documents.py
```

You should see logs indicating documents are loaded, embeddings created, and vectors upserted to Pinecone.

---

## Run the Application Locally

Start the Gradio app:

```bash
python app.py
```

Then open your browser at:

```
http://127.0.0.1:7860
```

You’ll see:

- A **dark, professional interface** branded as:  
  `KG: Data Engineering Knowledge Base`
- Tab 1: **“Chat with KG-AI”** – conversational interface backed by the RAG system  
- Tab 2: **“Upload Knowledge”** – upload `.txt`, `.md`, or `.pdf` files to extend the knowledge base

Uploaded files are:

1. Read from the temporary paths Gradio provides  
2. Parsed into documents  
3. Embedded with the same OpenAI embedding model  
4. Stored in the existing Pinecone index  

No restart is required after uploads – new content becomes searchable immediately.

---

## Deploying to Hugging Face Spaces

This project is ready to deploy as a **Gradio Space**.

### Steps

1. On Hugging Face, create a new Space  
   - SDK: **Gradio**  
   - Hardware: **CPU Basic**  
   - Visibility: **Public** (for portfolio/demo)

2. Either:
   - Connect it directly to this GitHub repo  
   **or**
   - Upload the project files manually (`app.py`, `requirements.txt`, `ingest_documents.py`, `documents/`, etc.)

3. In the Space settings, add the following **Secrets** / **Environment variables**:

   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
   - `PINECONE_INDEX_NAME` (e.g. `de-knowledge-base`)
   - `EMBEDDING_MODEL` (optional override)
   - `CHAT_MODEL` (optional override)

4. Commit / save.  
   Hugging Face will:
   - Install from `requirements.txt`
   - Run `app.py`
   - Expose the application at:

   ```text
   https://huggingface.co/spaces/<your-username>/kg-data-engineering-knowledge-base
   ```

(You can pre-run `ingest_documents.py` locally to populate Pinecone once, then the Space only needs `app.py`.)

---

## Roadmap / Ideas

- Add authentication for private knowledge bases
- Support additional file types (Excel, JSON, Parquet, database connectors)
- Add observability: request logging, latency metrics, retrieval stats
- Swap in alternative LLMs or embedding models if costs or latency change

---

## Author

**Kenroy Green (KG)**  
Data Engineer → AI Engineer

- GitHub: [@KG87](https://github.com/KG87)
- LinkedIn: [Kenroy Green](https://www.linkedin.com/in/kenroy-green-73b583ba/)

---

## License

This project is released under the **MIT License**.  
You are free to use, modify, and extend it, with attribution.
