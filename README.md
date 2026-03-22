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

### 5. Evaluateing agents 

```bash
python evaluate_agents.py
```


## Understanding Your Crew

The soc_investigator Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.



