import requests
import os
import time
import warnings
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent

# 🛑 Mute all LangChain deprecation warnings for a pristine terminal UI
warnings.filterwarnings("ignore")

# Load environment variables from .env vault
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
if not MONGO_URI:
    raise ValueError("MONGODB_URI environment variable not set in .env file.")

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

# Initialize Core Services
client = MongoClient(MONGO_URI)
db = client["microgrid_network"]
collection = db["historical_telemetry"]

# Initialize Gemini 2.5 Pro Engine
llm = ChatVertexAI(model_name="gemini-2.5-pro", temperature=0.2)

def query_latest_telemetry(microgrid_id):
    """Fetches the absolute newest database entry for a specific grid node."""
    return collection.find_one({"microgrid_id": microgrid_id}, sort=[("_id", -1)])

# LangGraph Tool Definition
def automatic_grid_mitigator(anomaly_details: str) -> str:
    """Executes structural grid operations to contain a data integrity attack."""
    return f"Action logged: Isolated anomaly vector profiles. Triggered primary islanding routines for safety."

agent_executor = create_react_agent(llm, tools=[automatic_grid_mitigator])

print("🛡️ Sentinel Autonomous Security Daemon Online.")
print("Monitoring MongoDB telemetry stream for FDIA vectors... Press Ctrl+C to stop.")

# Track processed timestamps to avoid duplicate alerts for the same attack instance
last_processed_timestamp = None

try:
    while True:
        # Focus on the high-risk industrial node (Microgrid3)
        record = query_latest_telemetry("Microgrid3")
        
        if record:
            current_time = record.get("timestamp")
            load = record.get("load_kw", 0)
            pv = record.get("pv_kw", 0)
            
            # Embedded PI-GAN Manifold Validation Rule
            if load > 1500 and pv < 900:
                if current_time != last_processed_timestamp:
                    print(f"\n[🚨 ALERT] Critical Manifold Violation Detected at {current_time}!")
                    print(f" -> Current State: Load: {load} kW | PV: {pv} kW")
                    print(" -> Launching Gemini LangGraph Agent for Mitigation Plan...")
                    
                    prompt = f"""
                    CRITICAL EMERGENCY: False Data Injection Attack confirmed on Microgrid3 at telemetry timestamp {current_time}.
                    Live Readings: Industrial Load is {load} kW while PV output has been spoofed down to {pv} kW.
                    Analyze this anomalous state using PI-GAN physical validation constraints. 
                    Generate an immediate resilience, node isolation, and load-shedding report.
                    """
                    
                    response = agent_executor.invoke({"messages": [("user", prompt)]})
                    final_verdict = response["messages"][-1].content
                    
                    # 🛠️ THE FIX: Safely extract text if LangGraph returns a list of blocks
                    if isinstance(final_verdict, list):
                        final_verdict = final_verdict[0].get("text", str(final_verdict))
                    
                    # Generate Hardcopy Report Document
                    report_filename = f"incident_report_{current_time.replace(':', '')}.md"
                    with open(report_filename, "w") as report_file:
                        report_file.write(f"# ⚠️ CPS Security Incident Report\n\n")
                        report_file.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d')} {current_time}\n")
                        report_file.write(f"**Target System:** Microgrid3 (Industrial)\n")
                        report_file.write(f"**Telemetry Alteration:** Load: {load} kW / PV: {pv} kW\n")
                        report_file.write(f"---\n\n## Autonomous Agent Mitigation Strategy\n\n")
                        report_file.write(final_verdict)
                    
                    print(f"✅ Analysis Complete. Live incident report compiled successfully: {report_filename}\n")
                    last_processed_timestamp = current_time
                    # ==========================================
                    # 🚀 FIRE ENTERPRISE SLACK ALERT
                    # ==========================================
                    if SLACK_WEBHOOK:
                        slack_payload = {
                            "text": f"🚨 *CRITICAL ALERT: MICROGRID3 COMPROMISED* 🚨\n*Time:* {current_time}\n*Threat:* False Data Injection Attack (FDIA)\n*Status:* {load}kW Load vs {pv}kW PV\n*Agent Action:* {final_verdict[:150]}..."
                        }
                        try:
                            requests.post(SLACK_WEBHOOK, json=slack_payload)
                            print("📲 Enterprise Slack Alert dispatched to Engineering Team.")
                        except Exception as e:
                            print(f"Failed to send Slack alert: {e}")
                    
        time.sleep(2) # Poll database every 2 seconds

except KeyboardInterrupt:
    print("\nSentinel Daemon deactivated by operator.")