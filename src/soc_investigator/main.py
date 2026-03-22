#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

# Updated to match the class name in your crew.py
from soc_investigator.crew import SocInvestigator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Define a mock alert here so it is easily reusable across all testing functions
MOCK_ALERT = "A single user account (jsmith) has attempted to log in 45 times within 2 minutes from an external IP address (192.168.1.50). The attempts were followed by a successful login."


def run():
    """
    Run the crew.
    """
    inputs = {
        'alert': MOCK_ALERT
    }

    try:
        SocInvestigator().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'alert': MOCK_ALERT
    }
    
    try:
        SocInvestigator().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SocInvestigator().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'alert': MOCK_ALERT
    }

    try:
        SocInvestigator().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "alert": MOCK_ALERT
    }

    try:
        result = SocInvestigator().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")