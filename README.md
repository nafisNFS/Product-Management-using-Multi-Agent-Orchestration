# Product-Management-using-Multi-Agent-Orchestration
# 🚀 Multi-Agent MCP System with Inventory & Transportation

## 📌 Overview

This project implements a **Multi-Agent System using MCP (Model Context Protocol)** with:

- 🧠 **Supervisor Agent** (task orchestration)  
- 📦 **Inventory Agent** (product management)  
- ✈️ **Transportation Agent** (flight booking system)  

The system supports **agent-to-agent communication**, enabling complex cross-domain workflows such as:

> *“If low stock products exist, cancel flights on a specific date.”*

---

## 🏗️ Architecture


User
↓
Supervisor Agent
↓
Inventory Agent ↔ Transportation Agent
↓ ↓
Inventory MCP Transport MCP
↓ ↓
SQLite DB SQLite DB


---

## ✨ Features

- ✅ MCP-based modular architecture  
- ✅ True multi-agent system (Supervisor + domain agents)  
- ✅ Agent-to-agent (A2A) communication  
- ✅ SQLite database integration (persistent storage)  
- ✅ Cross-domain reasoning (inventory + transport)  
- ✅ Tool-based execution using MCP  

---

## 📁 Project Structure


multi_agent_mcp/
│
├── database/
│ ├── inventory_database.py
│ └── transport_database.py
│
├── mcp_servers/
│ ├── product_mcp.py
│ └── transport_mcp.py
│
├── agents/
│ ├── agent_registry.py
│ ├── inventory_agent.py
│ ├── transport_agent.py
│ └── setup_agents.py
│
├── supervisor/
│ └── supervisor.py
│
└── requirements.txt


---

## ⚙️ Installation

```bash
pip install -r requirements.txt
▶️ Running the System

Open 3 terminals:

1️⃣ Start Inventory MCP Server
python mcp_servers/product_mcp.py
2️⃣ Start Transport MCP Server
python mcp_servers/transport_mcp.py
3️⃣ Start Supervisor
python supervisor/supervisor.py

🧪 Example Queries
➤ Inventory Operations
add product rice category food price 50 quantity 2
➤ Flight Booking
book flight Rahim 2026-03-27 Dhaka Chittagong
➤ Cross-Agent Query
if low stock then cancel flight on 2026-03-27
🔄 How It Works
User sends query → Supervisor Agent
Supervisor delegates task → appropriate agent
Agents use MCP tools to interact with databases
Agents communicate with each other if needed
Final result is returned to the user
🧠 Agent Roles
🔹 Supervisor Agent
Orchestrates tasks
Routes queries to agents
🔹 Inventory Agent
Manages product database
Detects low stock conditions
🔹 Transportation Agent
Handles flight booking and cancellation
🔗 Agent-to-Agent Communication

Agents can directly communicate without always relying on the supervisor.

Example:

Inventory Agent detects low stock
Directly triggers Transportation Agent
Transportation Agent cancels flights

💾 Database Design
📦 Inventory Database (inventory.db)
Field	Type
id	Integer
name	String
category	String
price	Float
quantity	Integer

✈️ Transport Database (transport.db)
Field	Type
id	Integer
name	String
date	String
source	String
destination	String
status	String

⚠️ Current Limitations
Some agent-to-agent triggers are rule-based (e.g., low stock threshold)
Supervisor routing is keyword-based
No shared memory between agents

🚀 Future Improvements
🔥 Fully LLM-driven agent communication
🔥 Shared memory across agents
🔥 Event-driven architecture
🔥 Web/Flutter UI integration
🔥 Distributed system with message queues

📚 Technologies Used
Python
FastMCP
LangChain
Ollama (LLM)
SQLite
SQLAlchemy
