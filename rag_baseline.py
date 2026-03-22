import os
import chromadb
from chromadb.utils import embedding_functions
from litellm import completion
from dotenv import load_dotenv

# Load your Groq API key from the .env file
load_dotenv()

def run_baseline_rag(alert_text):
    print(f"\n[BASELINE RAG] Analyzing Alert: {alert_text}...\n")
    
    # 1. Retrieve context from your SOC database
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = chroma_client.get_collection(name="soc_playbooks", embedding_function=embedding_func) # type: ignore
    
    results = collection.query(query_texts=[alert_text], n_results=3)
    
    if results.get('documents') and results['documents'][0]:
        context = "\n\n".join(results['documents'][0])
    else:
        context = "No relevant past incidents found."
        
    # 2. Generate a response in a single shot (No agents, no tool-use loop)
    prompt = f"""
    You are a SOC analyst. Review the following security alert.
    
    ALERT: {alert_text}
    
    HISTORICAL CONTEXT FROM PLAYBOOKS:
    {context}
    
    Based ONLY on the context provided, determine if this is a threat and write a brief conclusion.
    """
    
    # Call the Groq model you set up in your .env file
    model_name = os.getenv("MODEL", "groq/llama-3.3-70b-versatile")
    response = completion(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

alerts = {
    1 : "User jsmith attempted to log in 45 times in 2 minutes from IP 192.168.1.50, followed by a successful login.",
    2 : "Successful login for user amanda.doe from Singapore at 08:00 AM, followed by a successful login for amanda.doe from Moscow, Russia at 08:30 AM",
    3 : "Endpoint security flagged the mass encryption of 500+ PDF files in the Finance shared drive and the creation of a file named 'DECRYPT_MY_FILES.txt'.",
    4 : "IT Admin account 'sysadmin_01' executed a bulk password reset script affecting 50 users.",
    5 : "Intrusion Detection System flagged abnormal outbound traffic over port 4444 to an unknown IP address communicating with an encrypted payload."
}

# Test it with our mock alert
if __name__ == "__main__":
    print("Starting ...")
    for scenario in alerts:
        alert = alerts[scenario]
        print(f"================= Scenario {scenario} ============================")
        print(run_baseline_rag(alert))
    
    print("SOC Investigation Complete")