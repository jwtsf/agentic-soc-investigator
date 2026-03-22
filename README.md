# SocInvestigator Crew

This is an autonomous multi-agent SOC investigator that triages incoming threat alerts built using crewAI. It uses Retrieval-Augmented Generation (RAG) architecture to investigate security alerts against historical case studies and displays the analysis on a dashboard.  

## 🛠️ Installation & Setup

Follow these steps to set up and run the multi-agent SOC investigator on your local machine.

### Prerequisites
- Python >= 3.10
- [Git](https://git-scm.com/)
- A [Groq API Key](https://console.groq.com/) (Free)

### 1. Clone the Repository
```bash
git clone [https://github.com/jwtsf/agentic-soc-investigator.git](https://github.com/jwtsf/agentic-soc-investigator.git)
cd agentic-soc-investigator
```

### 2. Install dependencies

```bash
pip install crewai crewai[tools] streamlit chromadb litellm python-dotenv
```

### 3. Update environment variables

```bash
MODEL=groq/llama-3.3-70b-versatile
GROQ_API_KEY=your_actual_api_key_here
```

### 4. Run the application

```bash
streamlit run app.py
```

The final threat report will be available on the dashboard:
<img width="961" height="512" alt="image" src="https://github.com/user-attachments/assets/3b8b0f75-f3b1-490c-bc34-7fa233e2025c" />

Further decisions can be made post-report:
<img width="961" height="494" alt="image" src="https://github.com/user-attachments/assets/1b57d1d0-9d99-45b3-a6d5-63bc97bdedaf" />




## Architecture Comparison: Baseline RAG vs. Multi-Agent System

This repository includes two different triage scripts to demonstrate the value and necessity of Agentic AI in a cybersecurity context.

### 1. The Baseline: `rag_baseline.py`
This script represents a standard **Retrieval-Augmented Generation (RAG)** approach. 
* **Mechanism:** It operates on a linear, single-shot prompt (`Retrieve Context → Prompt LLM → Output`).
* **Limitation:** It acts as a "black box" and struggles with edge cases. During testing, if the vector database lacked relevant historical playbooks, the standard RAG model suffered from hallucinations, fabricating fake IP addresses and vulnerabilities (e.g., CVE-2024-3400) to satisfy the prompt.

### 2. The Solution: `evaluate_agents.py` (CrewAI)
This script utilizes a **Multi-Agent Architecture** to simulate a rigorous SOC review process.
* **Mechanism:** It employs a **ReAct (Reasoning and Acting)** loop. An **L1 Investigator Agent** autonomously uses tools to query the database, drafts a report, and passes it to a **Senior Critic Agent**. 
* **The Agentic Edge:** The Critic Agent acts as an adversarial verification layer. It audits the L1 Analyst's logic, assigns a quantitative **Confidence Score (0-100)**, and mandates a **Human-in-the-Loop (HITL)** escalation if the evidence is insufficient. This explicitly prevents hallucinations and ensures the system safely handles zero-day or missing-context scenarios.

### Feature Comparison

| Feature | `rag_baseline.py` (Standard RAG) | `evaluate_agents.py` (Multi-Agent) |
| :--- | :--- | :--- |
| **Execution** | Single-shot prompt | Iterative Thought → Action → Observation loop |
| **Data Retrieval** | Hardcoded vector search | Autonomous Tool Use (`SOC Playbook Search`) |
| **Verification** | None (Blind output) | Adversarial Critic Agent review |
| **Edge Case Handling** | High hallucination risk | Fails safely (Assigns low confidence, outputs ESCALATE) |
| **Accountability** | Black Box | Full reasoning transparency via terminal logs |


## Understanding Your Crew

The soc_investigator Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.



