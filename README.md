# ⚡ Residuum_Modulus: CPS Security Agent

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Pro-Vertex_AI-4285F4?logo=google&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB_Atlas-Data_Layer-47A248?logo=mongodb&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Orchestration-FF9900)

A Cyber-Physical System (CPS) Security Agent built for the **Google Cloud Rapid Agent Hackathon (MongoDB Track)**. 

This autonomous agent utilizes **Gemini 2.5 Pro** and **LangGraph** orchestration to detect and mitigate False Data Injection Attacks (FDIA) across networked microgrids. By integrating a Physics-Informed Generative Adversarial Network (PI-GAN) framework with historical telemetry stored in **MongoDB Atlas**, the agent identifies anomalous data manifolds and autonomously formulates grid-resilience strategies.

---

## 🏗️ Architecture

* **The Brain (LLM):** Google Vertex AI (`gemini-2.5-pro`) reasoning engine.
* **Orchestration:** `LangGraph` (`create_react_agent`) for structured tool calling and Chain-of-Thought execution.
* **Data Layer:** `MongoDB Atlas` serves as the centralized telemetry hub, queried dynamically via PyMongo.
* **Detection Engine:** Simulated PI-GAN logic designed to cross-reference real-time load/PV data against learned physical manifolds to detect data spoofing.

---

## 🚀 Features

* **Real-time Telemetry Retrieval:** Dynamically queries MongoDB collections for active microgrid states (Residential, Commercial, Industrial).
* **Physics-Informed Anomaly Detection:** Flags critical mismatches between Industrial Load ($1800\text{ kW}$) and PV Output ($850\text{ kW}$) using deterministic confidence thresholds.
* **Autonomous Mitigation:** Automatically generates incident response plans, including node isolation, load-shedding protocols, and grid rerouting to maintain overall stability.

---

## 🛠️ Installation & Setup

This project is optimized for deployment within **Google Cloud Shell**.

**1. Clone the Repository**
```bash
git clone [https://github.com/your-username/cps-security-agent.git](https://github.com/your-username/cps-security-agent.git)
cd cps-security-agent