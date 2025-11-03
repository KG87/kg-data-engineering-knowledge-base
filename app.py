import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Settings,
    SimpleDirectoryReader,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone


# -------------------------------------------------------------------
# Environment + global config
# -------------------------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "de-knowledge-base")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")
if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE_API_KEY not set")

# Configure LlamaIndex settings
Settings.embed_model = OpenAIEmbedding(
    model=EMBEDDING_MODEL,
    api_key=OPENAI_API_KEY,
)
Settings.llm = OpenAI(
    model=CHAT_MODEL,
    api_key=OPENAI_API_KEY,
)
Settings.chunk_size = CHUNK_SIZE
Settings.chunk_overlap = CHUNK_OVERLAP


# -------------------------------------------------------------------
# Connect to Pinecone vector store
# -------------------------------------------------------------------

pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(PINECONE_INDEX_NAME)

vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
query_engine = index.as_query_engine(similarity_top_k=5)


# -------------------------------------------------------------------
# Core functions
# -------------------------------------------------------------------

def chat(message: str, history: list[list[str]]):
    """Handles chat interaction."""
    if not message:
        return "⚠️ Please type a question."
    response = query_engine.query(message)
    return str(response)


def ingest_files(files):
    """Handles file upload and ingestion into Pinecone."""
    if not files:
        return "⚠️ No file uploaded."

    if isinstance(files, str) or isinstance(files, Path):
        file_paths = [str(files)]
    else:
        file_paths = [str(f) for f in files if os.path.exists(f)]

    if not file_paths:
        return "⚠️ Could not find any valid files to ingest."

    documents = SimpleDirectoryReader(input_files=file_paths).load_data()

    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
    )

    return f"✅ Ingested {len(documents)} document(s) into the knowledge base."


# -------------------------------------------------------------------
# Gradio UI
# -------------------------------------------------------------------

def build_app():
    with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
        gr.Markdown(
            """
            <div style='text-align:center; margin-bottom: 1.5em;'>
                <h1 style='font-size: 2.2em; font-weight: 700;'>KG: Data Engineering Knowledge Base</h1>
                <p style='font-style: italic; color: #9ca3af;'>An AI system engineered by Kenroy Green</p>
            </div>
            """
        )

        with gr.Tab("Chat with KG-AI"):
            gr.ChatInterface(
                fn=chat,
                title="Converse with the Knowledge Engine",
            )

        with gr.Tab("Upload Knowledge"):
            gr.Markdown(
                "Upload new data engineering docs (txt, md, pdf). "
                "They'll be embedded and added to your Pinecone index."
            )
            file_input = gr.File(label="Upload files", file_count="multiple", type="filepath")
            ingest_button = gr.Button("Ingest into knowledge base")
            status_box = gr.Markdown()

            ingest_button.click(fn=ingest_files, inputs=file_input, outputs=status_box)

        gr.Markdown(
            """
            <hr>
            <p style='text-align:center; color: #6b7280; font-size: 0.9em;'>
                ⚡ Built by <strong>Kenroy Green</strong> · Data Engineer → AI Engineer Transition ·
                <em>Medu Designs / Green Analytics Ltd</em>
            </p>
            """
        )

    return demo


if __name__ == "__main__":
    demo = build_app()
    demo.launch(server_name="0.0.0.0", server_port=7860)
