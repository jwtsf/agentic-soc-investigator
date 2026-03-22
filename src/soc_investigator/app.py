import streamlit as st
from soc_investigator.crew import SocInvestigator
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="SOC Multi-Agent Triage",
    page_icon="🛡️",
    layout="wide"
)

# --- Header Section ---
st.title("🛡️ Autonomous SOC Alert Investigator")
st.markdown("""
This system uses a **Multi-Agent Architecture (Investigator & Critic)** connected to a **Persistent Vector Memory (ChromaDB)** to automatically triage security alerts, pulling from historical SOC playbooks to reduce alert fatigue.
""")
st.divider()

# --- Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🚨 Incoming Alert")
    # Pre-fill with one of your complex scenarios for an easy demo
    default_alert = "Successful login for user amanda.doe from Singapore at 08:00 AM, followed by a successful login for amanda.doe from Moscow, Russia at 08:30 AM."
    alert_data = st.text_area("Paste Security Alert Details:", value=default_alert, height=150)
    
    analyze_button = st.button("🔍 Run Agentic Triage", type="primary", use_container_width=True)

with col2:
    st.subheader("⚙️ System Status")
    status_placeholder = st.empty()
    status_placeholder.info("Awaiting alert input...")

st.divider()

# --- Execution Logic ---
if analyze_button and alert_data:
    status_placeholder.warning("Agents are coordinating... Check terminal for Reasoning Logs (Thought → Action → Observation).")
    
    # Progress bar for visual effect during the demo
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    
    with st.spinner("Executing Investigator and Critic Agents..."):
        try:
            inputs = {'alert': alert_data}
            
            # Kick off the multi-agent system
            result = SocInvestigator().crew().kickoff(inputs=inputs)
            
            status_placeholder.success("Analysis Complete!")
            
            # --- Results Section ---
            st.subheader("📄 Final Threat Intelligence Report")
            
            # Display the Markdown output from the Critic Agent
            report_container = st.container(border=True)
            report_container.markdown(str(result))
            
            # --- Human-in-the-Loop (HITL) Escalation UI ---
            st.divider()
            st.subheader("👤 Human-in-the-Loop Decision")
            
            # Simple logic to check if the Critic escalated the alert
            if "ESCALATE" in str(result).upper():
                st.error("⚠️ **CRITIC AGENT ESCALATION TRIGGERED:** The AI is not confident enough to resolve this automatically or the severity is too high.")
                
                hitl_col1, hitl_col2, hitl_col3 = st.columns(3)
                with hitl_col1:
                    if st.button("✅ Approve & Send to Tier 2 Support", use_container_width=True):
                        st.success("Alert escalated to human Tier 2 team.")
                with hitl_col2:
                    if st.button("🛑 Reject Escalation (Mark False Positive)", use_container_width=True):
                        st.info("Escalation rejected. Alert closed.")
                with hitl_col3:
                    if st.button("🔄 Force AI Re-investigation", use_container_width=True):
                        st.warning("Re-running investigation...")
            else:
                st.success("✅ **RESOLVED:** The AI has determined this alert can be safely closed based on historical playbooks.")
                if st.button("Archive Report"):
                    st.toast("Report archived to database.")

        except Exception as e:
            st.error(f"An error occurred during triage: {e}")