# query_knowledge_base.py
import os
from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# Connect to Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME", "de-knowledge-base")
pinecone_index = pc.Index(index_name)

# Configure LlamaIndex settings
Settings.embed_model = OpenAIEmbedding(
    model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
    api_key=os.getenv("OPENAI_API_KEY")
)
Settings.llm = OpenAI(
    model=os.getenv("CHAT_MODEL", "gpt-4o-mini"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create vector store and query engine
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
index = VectorStoreIndex.from_vector_store(vector_store)
qa = index.as_query_engine(similarity_top_k=5)

print("✅ Ready to chat with your Data Engineering Knowledge Base!")
print("Type your question (or Ctrl+C to quit).\n")

while True:
    try:
        q = input("Q: ")
        if not q.strip():
            continue
        a = qa.query(q)
        print(f"\nA: {a.response}\n")
    except (EOFError, KeyboardInterrupt):
        print("\n👋 Exiting.")
        break
