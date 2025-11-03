"""
Document Ingestion Script for RAG Knowledge Base
Loads documents from /documents folder into Pinecone vector database
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

def setup_pinecone():
    """Initialize Pinecone and create index if needed"""
    print("🔧 Setting up Pinecone...")
    
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME")
    
    # Check if index exists
    if index_name not in pc.list_indexes().names():
        print(f"📊 Creating new index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=1536,  # text-embedding-3-small dimension
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
            )
        )
        print(f"✅ Index '{index_name}' created successfully!")
    else:
        print(f"✅ Index '{index_name}' already exists")
    
    return pc.Index(index_name)

def configure_llama_index():
    """Configure LlamaIndex settings"""
    print("🔧 Configuring LlamaIndex...")
    
    # Set embedding model
    Settings.embed_model = OpenAIEmbedding(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Set LLM
    Settings.llm = OpenAI(
        model=os.getenv("CHAT_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Set chunk parameters
    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", 1000))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 200))
    
    print("✅ LlamaIndex configured")

def load_documents():
    """Load documents from the documents directory"""
    print("📚 Loading documents...")
    
    docs_path = Path("documents")
    
    if not docs_path.exists():
        raise FileNotFoundError(f"Documents directory not found: {docs_path}")
    
    # Load all text files
    documents = SimpleDirectoryReader(
        input_dir=str(docs_path),
        required_exts=[".txt"]
    ).load_data()
    
    print(f"✅ Loaded {len(documents)} documents")
    
    # Print document info
    for i, doc in enumerate(documents, 1):
        filename = Path(doc.metadata.get('file_name', 'unknown')).name
        char_count = len(doc.text)
        print(f"   {i}. {filename} ({char_count:,} characters)")
    
    return documents

def ingest_documents(documents, pinecone_index):
    """Ingest documents into Pinecone vector store"""
    print("\n🚀 Starting document ingestion...")
    
    # Create vector store
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    
    # Create storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Create index and ingest documents
    print("📊 Creating embeddings and storing in Pinecone...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )
    
    print("✅ Documents successfully ingested!")
    
    return index

def main():
    """Main ingestion workflow"""
    print("\n" + "="*60)
    print("🔥 DATA ENGINEERING KNOWLEDGE BASE - DOCUMENT INGESTION 🔥")
    print("="*60 + "\n")
    
    try:
        # Setup
        pinecone_index = setup_pinecone()
        configure_llama_index()
        
        # Load documents
        documents = load_documents()
        
        # Ingest
        index = ingest_documents(documents, pinecone_index)
        
        # Summary
        print("\n" + "="*60)
        print("✅ INGESTION COMPLETE!")
        print("="*60)
        print(f"📊 Total documents ingested: {len(documents)}")
        print(f"🗄️  Vector store: Pinecone ({os.getenv('PINECONE_INDEX_NAME')})")
        print(f"🤖 Embedding model: {os.getenv('EMBEDDING_MODEL')}")
        print("\n💡 Next step: Run query_knowledge_base.py to ask questions!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        raise

if __name__ == "__main__":
    main()
