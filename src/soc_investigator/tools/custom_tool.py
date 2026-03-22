from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import chromadb
from chromadb.utils import embedding_functions

class RAGSearchInput(BaseModel):
    query: str = Field(description="The exact search query to look up in the SOC database.")

class RAGSearchTool(BaseTool):
    name: str = "SOC Playbook Search"
    description: str = "Search the local vector database for historical SOC documentation, playbooks, and incident response guides."
    args_schema: type[BaseModel] = RAGSearchInput

    def _run(self, query: str) -> str:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        # Added type: ignore to bypass the strict type mismatch in ChromaDB's stubs
        collection = chroma_client.get_collection(
            name="soc_playbooks", 
            embedding_function=embedding_func # type: ignore
        )
        
        results = collection.query(query_texts=[query], n_results=3)
        
        # Safely check if documents exist to satisfy the linter
        if not results.get('documents') or not results['documents'][0]:
            return "No relevant past incidents or playbooks found."
        
        return "\n\n--- NEXT RESULT ---\n\n".join(results['documents'][0])