import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("Starting SOC documentation ingestion...")

# 1. Initialize the ChromaDB client (this creates a folder called 'chroma_db' to store data permanently)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 2. Set up the Embedding Function (uses a free, fast local model)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# 3. Create a collection (think of this like a table in a database)
collection = chroma_client.get_or_create_collection(
    name="soc_playbooks", 
    embedding_function=embedding_func
)

# 4. Load the documents from the downloaded GitHub repo
# We look for all text and markdown files in the directory
loader = DirectoryLoader('./SOC_DOCUMENTATIONS', glob="**/*.md", loader_cls=TextLoader, use_multithreading=True, recursive=True)
documents = loader.load()
print(f"Loaded {len(documents)} files from the repository.")

# 5. Split the text into smaller chunks
# AI models read better in smaller paragraphs. This splits the docs into 1000-character chunks.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
print(f"Split documents into {len(chunks)} searchable chunks.")

# 6. Prepare data for ChromaDB
documents_list = [chunk.page_content for chunk in chunks]
metadatas_list = [chunk.metadata for chunk in chunks]
ids_list = [f"doc_{i}" for i in range(len(chunks))]

# 7. Insert into ChromaDB
collection.add(
    documents=documents_list,
    metadatas=metadatas_list,
    ids=ids_list
)

print("✅ Successfully ingested all SOC documentation into ChromaDB!")