import warnings
from soc_investigator.crew import SocInvestigator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# The exact same 5 scenarios you used for the RAG baseline
scenarios = [
    "A single user account (jsmith) has attempted to log in 45 times within 2 minutes from an external IP address (192.168.1.50). The attempts were followed by a successful login.",
    "Successful login for user amanda.doe from Singapore at 08:00 AM, followed by a successful login for amanda.doe from Moscow, Russia at 08:30 AM.",
    "Endpoint security flagged the mass encryption of 500+ PDF files in the Finance shared drive and the creation of a file named 'DECRYPT_MY_FILES.txt'.",
    "IT Admin account 'sysadmin_01' executed a bulk password reset script affecting 50 users.",
    "Intrusion Detection System flagged abnormal outbound traffic over port 4444 to an unknown IP address communicating with an encrypted payload."
]

def run_evaluation():
    print("🛡️ Starting Multi-Agent SOC Evaluation...\n")
    
    for i, alert in enumerate(scenarios, 1):
        print(f"\n{'='*30}")
        print(f"🚀 KICKING OFF SCENARIO {i}")
        print(f"ALERT: {alert}")
        print(f"{'='*30}\n")
        
        inputs = {'alert': alert}
        
        try:
            # Initialize and run the crew for this specific alert
            result = SocInvestigator().crew().kickoff(inputs=inputs)
            
            print(f"\n{'='*15} FINAL VERDICT FOR SCENARIO {i} {'='*15}")
            print(result)
            print(f"{'='*50}\n")
            
        except Exception as e:
            print(f"❌ Error running Scenario {i}: {e}")

if __name__ == "__main__":
    run_evaluation()