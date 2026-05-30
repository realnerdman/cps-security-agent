import os
import json
from langchain_google_vertexai import ChatVertexAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

# ==========================================
# 1. Tool Definitions
# ==========================================

@tool
def query_historical_load(microgrid_id: str, timestamp: str) -> str:
    """Fetches historical load and PV data from the MongoDB MCP Server."""
    # Placeholder for actual MongoDB MCP integration logic
    # Mapping: Microgrid1=Residential, Microgrid2=Commercial, Microgrid3=Industrial
    return f"Retrieved data for {microgrid_id} at {timestamp} from MongoDB."

@tool
def detect_adversarial_fault(microgrid_id: str, load_data: float, pv_output: float) -> str:
    """
    Triggers Vertex AI PI-GAN model to check for False Data Injection Attacks (FDIA).
    Returns confidence score of data integrity violation.
    """
    # Simulated PI-GAN inference
    confidence = 0.92 if microgrid_id == "Microgrid3" else 0.15 
    return json.dumps({
        "microgrid": microgrid_id,
        "attack_confidence": confidence,
        "manifold_deviation": "High" if confidence > 0.85 else "Normal"
    })

tools = [query_historical_load, detect_adversarial_fault]

# ==========================================
# 2. The Brain: Gemini 1.5 Pro & System Logic
# ==========================================

llm = ChatVertexAI(
    model_name="gemini-1.5-pro-preview-0409", 
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
2. Analyze: State your reasoning explicitly. Example: "I am comparing the current PV output against the PI-GAN predicted manifold for potential spoofing."
3. Detect: Use 'detect_adversarial_fault' to analyze the data.
4. Mitigate: If attack_confidence > 0.85, you MUST output a mitigation plan (e.g., isolating the compromised node, re-routing load to unaffected microgrids).
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_instruction),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# ==========================================
# 3. Agent Execution
# ==========================================

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    # Test the Agent
    test_mission = "Analyze Microgrid3 for potential adversarial anomalies at 14:00 hours."
    print(f"Executing Mission: {test_mission}\n")
    response = agent_executor.invoke({"input": test_mission})
    print("\nFinal Output:", response['output'])