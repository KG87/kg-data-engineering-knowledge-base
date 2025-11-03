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

## 🚀 Live Demo

👉 **Try it now:** [https://huggingface.co/spaces/kg307/kg-data-engineering-knowledge-base](https://huggingface.co/spaces/kg307/kg-data-engineering-knowledge-base)

---

## Tech Stack

- **Python 3.10+**
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
├── .env                      # Environment variables (not committed)
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

You'll see:

- A **dark, professional interface** branded as:  
  `KG: Data Engineering Knowledge Base`
- Tab 1: **"Chat with KG-AI"** – conversational interface backed by the RAG system  
- Tab 2: **"Upload Knowledge"** – upload `.txt`, `.md`, or `.pdf` files to extend the knowledge base

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

**Note:** Run `ingest_documents.py` locally BEFORE deploying to populate your Pinecone index with the base documents. The Hugging Face Space will then use the existing index, and users can add more documents via the Upload tab.

---

## Features

### ✨ Core Capabilities

- **Conversational AI Interface**: Natural language Q&A about data engineering topics
- **Semantic Search**: Vector-based retrieval using Pinecone for accurate context matching
- **Dynamic Knowledge Base**: Upload PDFs, markdown, or text files to expand the knowledge instantly
- **Real-time Processing**: Uploaded documents are embedded and indexed immediately
- **Production-Ready**: Deployed on Hugging Face Spaces with proper error handling

### 📚 Pre-loaded Knowledge Domains

- **Azure Data Factory**: Pipeline architecture, integration patterns, performance optimization
- **dbt Best Practices**: Medallion architecture, testing strategies, CI/CD workflows
- **Data Modeling**: Kimball dimensional modeling, slowly changing dimensions, fact tables
- **SQL Optimization**: Query tuning, indexing strategies, execution plan analysis
- **Insurance Analytics**: Loss ratios, claims processing, underwriting metrics

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Gradio Web UI                          │
│                  (Chat + Upload Tabs)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    LlamaIndex Layer                         │
│            (RAG Orchestration + Query Engine)               │
└────────────┬───────────────────────────┬────────────────────┘
             │                           │
             ▼                           ▼
    ┌────────────────┐         ┌────────────────────┐
    │ Pinecone Index │         │   OpenAI API       │
    │ (Vector Store) │         │ (Embeddings + LLM) │
    └────────────────┘         └────────────────────┘
```

---

## Technical Implementation Details

### Document Processing Pipeline

1. **Ingestion**: Documents are read from `documents/` folder or uploaded via UI
2. **Chunking**: Text is split into manageable chunks (1000 chars with 200 char overlap)
3. **Embedding**: OpenAI's `text-embedding-3-small` model generates 1536-dimensional vectors
4. **Storage**: Vectors are stored in Pinecone serverless index with metadata
5. **Retrieval**: User queries are embedded and matched against stored vectors using cosine similarity
6. **Generation**: Retrieved context is passed to GPT-4o-mini for response generation

### Key Dependencies

- `llama-index-core>=0.14.7` - Core RAG orchestration
- `llama-index-vector-stores-pinecone` - Pinecone integration
- `llama-index-embeddings-openai` - OpenAI embeddings
- `llama-index-llms-openai` - OpenAI LLM integration
- `gradio>=5.0` - Web UI framework
- `pinecone-client>=6.0` - Pinecone Python SDK
- `python-dotenv` - Environment variable management

---

## Use Cases

This RAG system is ideal for:

- **Personal Knowledge Management**: Build your own searchable knowledge base from PDFs, notes, documentation
- **Team Onboarding**: Create a company-specific Q&A system for new hires
- **Technical Documentation**: Make your technical docs conversational and searchable
- **Research Assistant**: Upload research papers and query them in natural language
- **Learning Aid**: Create study materials that can answer questions about specific topics

---

## Roadmap / Future Enhancements

- [ ] Add source citation in responses (show which document answered)
- [ ] Implement conversation history and chat sessions
- [ ] Add document management UI (view, delete uploaded docs)
- [ ] Support additional file formats (Excel, JSON, Parquet)
- [ ] Add authentication for private knowledge bases
- [ ] Build analytics dashboard (query logs, popular topics)
- [ ] Implement batch document processing
- [ ] Add document summarization feature
- [ ] Support for multiple knowledge base indices
- [ ] Integration with external data sources (databases, APIs)

---

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'llama_index.vector_stores'`  
**Solution**: Install the Pinecone vector store module:
```bash
pip install llama-index-vector-stores-pinecone
```

**Issue**: Pinecone index not found  
**Solution**: Run `ingest_documents.py` first to create and populate the index.

**Issue**: OpenAI API rate limits  
**Solution**: Check your OpenAI usage dashboard and upgrade your plan if needed.

**Issue**: File upload fails  
**Solution**: Ensure uploaded files are in supported formats (.txt, .md, .pdf) and under 10MB.

---

## Performance Considerations

- **Embedding Generation**: ~0.5-1 second per document chunk
- **Vector Search**: ~100-200ms query latency (Pinecone serverless)
- **LLM Response**: ~2-5 seconds depending on context length
- **Total Response Time**: Typically 3-7 seconds end-to-end

### Optimization Tips

- Use smaller chunk sizes for faster indexing
- Reduce chunk overlap to decrease total chunks
- Consider GPT-3.5-turbo for faster (but lower quality) responses
- Enable Pinecone caching for repeated queries
- Batch document uploads when possible

---

## Security Notes

- API keys are stored in `.env` (never committed to git)
- Hugging Face Spaces uses Secrets for secure key storage
- All API communication uses HTTPS
- No user data is stored permanently (stateless design)
- Uploaded documents are processed in memory and indexed in your private Pinecone index

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Author

**Kenroy Green (KG)**  
Data Engineer → AI Engineer Transition

- GitHub: [@KG87](https://github.com/KG87)
- LinkedIn: [Kenroy Green](https://www.linkedin.com/in/kenroy-green-73b583ba/)
- Live Demo: [Hugging Face Space](https://huggingface.co/spaces/kg307/kg-data-engineering-knowledge-base)

---

## Acknowledgments

- **LlamaIndex** - For the excellent RAG orchestration framework
- **Pinecone** - For scalable vector database infrastructure
- **OpenAI** - For powerful embedding and language models
- **Gradio** - For the intuitive web UI framework
- **Hugging Face** - For free hosting and deployment platform

---

## License

This project is released under the **MIT License**.  
You are free to use, modify, and extend it, with attribution.

---

## Project Stats

- **Lines of Code**: ~500
- **Documents**: 5 knowledge domains
- **Vector Dimensions**: 1536
- **Model**: GPT-4o-mini
- **Deployment**: Hugging Face Spaces
- **Status**: ✅ Production-ready

---

**Built with ❤️ by Kenroy Green | Data Engineering → AI Engineering**
