from dotenv import load_dotenv
load_dotenv()

import os
import json
import warnings
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_google_vertexai import ChatVertexAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage

# 🛑 Mute all LangChain deprecation warnings for a pristine terminal UI
warnings.filterwarnings("ignore")

# Load environment variables from .env vault
load_dotenv()

# ==========================================
# 1. MongoDB Configuration & Tool Definition
# ==========================================

MONGO_URI = os.getenv("MONGODB_URI")
if not MONGO_URI:
    raise ValueError("MONGODB_URI environment variable not set.")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["microgrid_network"] 
collection = db["historical_telemetry"]

@tool
def query_historical_load(microgrid_id: str, timestamp: str) -> str:
    """Fetches historical load and PV data from the MongoDB database."""
    print(f"\n[Tool Execution] Querying MongoDB for {microgrid_id}...")
    
    # Pull the absolute latest telemetry reading using _id to avoid string sorting traps
    record = collection.find_one(
        {"microgrid_id": microgrid_id},
        sort=[("_id", -1)] 
    )
    
    if record:
        return f"Retrieved data for {microgrid_id}: Load = {record.get('load_kw')}kW, PV Output = {record.get('pv_kw')}kW."
    else:
        return f"No live data found in MongoDB for {microgrid_id}."

@tool
def detect_adversarial_fault(microgrid_id: str, load_data: float, pv_output: float) -> str:
    """
    Triggers Vertex AI PI-GAN model to check for False Data Injection Attacks (FDIA).
    Returns confidence score of data integrity violation.
    """
    print(f"[Tool Execution] Running PI-GAN Anomaly Detection on {microgrid_id}...")
    
    # Simulated PI-GAN inference
    confidence = 0.92 if microgrid_id == "Microgrid3" else 0.15 
    return json.dumps({
        "microgrid": microgrid_id,
        "attack_confidence": confidence,
        "manifold_deviation": "High" if confidence > 0.85 else "Normal"
    })

tools = [query_historical_load, detect_adversarial_fault]

# ==========================================
# 2. The Brain: Gemini 2.5 Pro & System Logic
# ==========================================

llm = ChatVertexAI(
    model_name="gemini-2.5-pro", 
    temperature=0.2 
)

system_instruction = """
You are a highly advanced Cyber-Physical System (CPS) Security Agent. 
Your core architecture relies on Physics-Informed Generative Adversarial Networks (PI-GANs) to ensure microgrid cyber-resilience against False Data Injection Attacks (FDIA).

You monitor the following topology:
- Microgrid1: Residential (Load & PV)
- Microgrid2: Commercial (Load & PV)
- Microgrid3: Industrial (Load & PV)

Chain-of-Thought Reasoning Protocol:
1. Observe: When tasked, fetch data using 'query_historical_load'.
2. Analyze: State your reasoning explicitly based on the physics of the grid.
3. Detect: Use 'detect_adversarial_fault' to analyze the data.
4. Mitigate: If attack_confidence > 0.85, you MUST output a mitigation plan (e.g., isolating the compromised node, re-routing load).
"""

# ==========================================
# 3. Agent Execution
# ==========================================

# Standardized LangGraph initialization
agent_executor = create_react_agent(llm, tools)

if __name__ == "__main__":
    test_mission = "Fetch the live telemetry for Microgrid3. Analyze it for potential adversarial anomalies using the PI-GAN logic, and deploy a mitigation plan if an attack is detected."
    print(f"Executing Mission: {test_mission}\n")
    
    # Injecting the SystemMessage directly into the invoke call avoids version conflicts
    response = agent_executor.invoke({
        "messages": [
            SystemMessage(content=system_instruction),
            HumanMessage(content=test_mission)
        ]
    })
    
    print("\n==========================================")
    print("FINAL MITIGATION PLAN:")
    print("==========================================")
    
    # Safely extract text if LangGraph returns a list of blocks
    final_verdict = response["messages"][-1].content
    if isinstance(final_verdict, list):
        final_verdict = final_verdict[0].get('text', str(final_verdict))
        
    print(final_verdict)