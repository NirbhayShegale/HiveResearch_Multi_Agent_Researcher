<p align="center">
</p>

<h1 align="center">🐝 HiveResearch — Multi-Agent Research System</h1>

<p align="center">
  <b>An autonomous AI research pipeline that decomposes complex questions, searches the web, synthesizes findings, drafts reports, and self-critiques — all orchestrated by a supervisor agent.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python 3.12"/>
  <img src="https://img.shields.io/badge/LangGraph-Orchestration-00A67E?logo=langchain&logoColor=white" alt="LangGraph"/>
  <img src="https://img.shields.io/badge/Groq-LLM_Inference-F55036?logo=groq&logoColor=white" alt="Groq"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/PostgreSQL-Checkpointing-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Tavily-Web_Search-000000" alt="Tavily"/>
</p>

<p align="center">
  <a href="https://hivemindreseacher.streamlit.app"><img src="https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge" alt="Live Demo"/></a>
  &nbsp;
  <a href="https://hiveresearch-multi-agent-researcher.onrender.com"><img src="https://img.shields.io/badge/⚡_API-Render-46E3B7?style=for-the-badge" alt="API on Render"/></a>
</p>

---

## 🌐 Live Demo

| | Link |
|:--|:-----|
| **🖥️ Web App** | [hivemindreseacher.streamlit.app](https://hivemindreseacher.streamlit.app) |
| **⚡ API** | [hiveresearch-multi-agent-researcher.onrender.com](https://hiveresearch-multi-agent-researcher.onrender.com) |

> **Try it now** — enter any research question in the Streamlit app and watch the agents work in real-time.

---

## 📌 Overview

**HiveResearch** is a production-grade, multi-agent AI system built on [LangGraph](https://github.com/langchain-ai/langgraph) that automates deep research. Instead of a single LLM call, it deploys a **hive of 5 specialized agents**, each with a distinct role, coordinated by a central Supervisor through a stateful directed graph.

> **Give it a question. Get back a well-researched, structured report — with citations.**

---

## 🏗️ System Architecture

```mermaid
graph TB
    User([🧑 User Query]) --> Supervisor

    subgraph "🐝 HiveResearch Agent Graph"
        Supervisor{"🎯 Supervisor<br/><i>Orchestrator</i>"}

        Supervisor -->|1| Planner["📋 Planner Agent<br/><i>Decomposes query into<br/>3-5 sub-tasks</i>"]
        Planner --> Supervisor

        Supervisor -->|2| Researcher["🔍 Researcher Agent<br/><i>Searches web per<br/>sub-task via Tavily</i>"]
        Researcher <-->|tool calls| TavilyTool[("🌐 Tavily<br/>Search API")]
        Researcher --> Supervisor

        Supervisor -->|3| Synthesizer["🧩 Synthesizer Agent<br/><i>Merges all research<br/>notes into outline</i>"]
        Synthesizer --> Supervisor

        Supervisor -->|4| Writer["✍️ Writer Agent<br/><i>Drafts structured<br/>final report</i>"]
        Writer --> Supervisor

        Supervisor -->|5| Critic["🔎 Critic Agent<br/><i>Reviews draft quality<br/>& factual accuracy</i>"]
        Critic -->|✅ Approved| Supervisor
        Critic -->|❌ Rejected| Supervisor
        Supervisor -->|revision| Writer
    end

    Supervisor -->|"✅ FINISH"| Output([📄 Final Report])

    style Supervisor fill:#FFA500,stroke:#333,stroke-width:2px,color:#fff
    style Planner fill:#4A90D9,stroke:#333,color:#fff
    style Researcher fill:#7B68EE,stroke:#333,color:#fff
    style Synthesizer fill:#2ECC71,stroke:#333,color:#fff
    style Writer fill:#E67E22,stroke:#333,color:#fff
    style Critic fill:#E74C3C,stroke:#333,color:#fff
    style TavilyTool fill:#34495E,stroke:#333,color:#fff
```

---

## 🤖 Agent Roles

| Agent | Responsibility | Input | Output |
|:---:|:---|:---|:---|
| **🎯 Supervisor** | Orchestrates the entire pipeline using deterministic routing logic based on current state | `AgentState` | Routing decision (`next_agent`) |
| **📋 Planner** | Decomposes the user's query into 3–5 independent, prioritized sub-tasks with search hints | User query | `sub_tasks[]` with aspect, priority, source type |
| **🔍 Researcher** | Picks the next sub-task, invokes Tavily search, and synthesizes findings into a research note | One sub-task | Research note (appended to `research[]`) |
| **🧩 Synthesizer** | Merges all research notes into a coherent, structured outline with key themes | All research notes | `synthesis` outline |
| **✍️ Writer** | Converts the synthesis into a polished, publication-ready report with sections & citations | Synthesis outline | `draft` report |
| **🔎 Critic** | Reviews the draft for accuracy, completeness, and quality; approves or rejects with feedback | Draft report | `critic_approval` (bool) + feedback |

---

## ⚡ Key Features

- **Autonomous Multi-Agent Pipeline** — Five specialized agents collaborate through a stateful LangGraph, with no human-in-the-loop required after the initial query.
- **Supervisor-Driven Orchestration** — Deterministic state-based routing eliminates LLM hallucination in control flow; the supervisor reads the graph state and always makes the correct next step.
- **Self-Correcting Feedback Loop** — The Critic agent can reject drafts and loop back to the Writer, ensuring output quality meets a threshold before completing.
- **Structured Output with Pydantic** — All inter-agent contracts use Pydantic models for validated, typed data exchange (e.g., `SubTask`, `SupervisorDecision`).
- **Live Web Research** — Tavily search integration enables real-time information retrieval with advanced depth and source diversity.
- **Persistent Checkpointing** — PostgreSQL-backed `langgraph.checkpoint.postgres` enables workflow recovery, replay, and state inspection.
- **Production-Ready API** — FastAPI backend with streaming SSE responses, integrated with LangSmith for full observability and tracing.
- **Interactive UI** — Streamlit frontend with real-time agent status updates as the pipeline progresses.
- **Docker-Ready** — Containerized with a multi-stage Dockerfile using `uv` for fast, reproducible dependency resolution.

---

## 🧱 Project Structure

```
HiveResearch_Multi_Agent_Researcher/
│
├── main.py                          # CLI entrypoint
├── pyproject.toml                   # Dependencies & project metadata (uv/pip)
├── Dockerfile                       # Production container
├── .env                             # API keys (GROQ_API_KEY, TAVILY_API_KEY, DB_URI)
│
├── src/
│   ├── Agents/
│   │   ├── PlannerAgent/            # Query → sub-tasks decomposition
│   │   ├── ResearcherAgent/         # Sub-task → web search → research note
│   │   ├── SynthesizeAgent/         # Research notes → structured outline
│   │   ├── WriterAgent/             # Outline → polished report
│   │   └── CriticAgent/            # Draft → approval / rejection + feedback
│   │
│   ├── Graph/
│   │   ├── state.py                 # AgentState (TypedDict) definition
│   │   ├── graph.py                 # LangGraph StateGraph assembly
│   │   └── router.py               # SupervisorDecision Pydantic model
│   │
│   ├── Orchestration/
│   │   ├── supervisor_agent.py      # Deterministic routing logic
│   │   └── Supervisor_prompt.py     # Supervisor system prompt
│   │
│   ├── Tools/
│   │   └── Tavily.py                # Tavily search tool wrapper
│   │
│   └── config/
│       └── config.py                # LLM factory (Groq model configs)
│
├── UI/
│   ├── Backend.py                   # FastAPI app with SSE streaming
│   └── streamlit_app.py            # Streamlit chat interface
│
└── Database/
    └── database.py                  # PostgreSQL checkpointer setup
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- **[uv](https://github.com/astral-sh/uv)** (recommended) or pip
- API keys for **[Groq](https://console.groq.com/)**, **[Tavily](https://tavily.com/)**, and optionally **PostgreSQL**

### 1. Clone the Repository

```bash
git clone https://github.com/NirbhayShegale/HiveResearch_Multi_Agent_Researcher.git
cd HiveResearch_Multi_Agent_Researcher
```

### 2. Install Dependencies

```bash
# Using uv (recommended — fast & reproducible)
uv sync

# Or using pip
pip install -e .
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
DB_URI=postgresql://user:password@host:5432/dbname   # optional, for checkpointing
LANGSMITH_API_KEY=your_langsmith_key                  # optional, for tracing
```

### 4. Run

**CLI mode:**
```bash
python main.py
```

**API + UI mode (local):**
```bash
# Terminal 1 — Start the FastAPI backend
uvicorn UI.Backend:app --host 0.0.0.0 --port 8000

# Terminal 2 — Start the Streamlit frontend
streamlit run UI/streamlit_app.py
```

> 💡 Or skip local setup entirely — use the **[live deployment](https://hivemindreseacher.streamlit.app)** instead.

**Docker:**
```bash
docker build -t hiveresearch .
docker run --env-file .env -p 8000:8000 hiveresearch
```

---

## 🔄 How It Works — Step by Step

```
User: "What are the environmental and economic trade-offs of EVs vs hydrogen trucks?"
```

| Step | Agent | What Happens |
|:----:|:-----:|:-------------|
| 1 | **Supervisor** | Inspects state → no sub-tasks exist → routes to **Planner** |
| 2 | **Planner** | Decomposes into 4 sub-tasks: environmental impact, economics, infrastructure, industry adoption |
| 3 | **Supervisor** | 4 sub-tasks in queue → routes to **Researcher** |
| 4 | **Researcher** | Searches "lifecycle carbon footprint electric vs hydrogen truck" via Tavily → writes research note |
| 5 | **Supervisor** | 3 sub-tasks remaining → routes to **Researcher** again |
| ... | **Researcher** | Repeats for each remaining sub-task |
| 8 | **Supervisor** | 0 sub-tasks, no synthesis → routes to **Synthesizer** |
| 9 | **Synthesizer** | Merges 4 research notes into a structured outline with themes |
| 10 | **Supervisor** | Synthesis exists, no draft → routes to **Writer** |
| 11 | **Writer** | Produces a polished, sectioned report with citations |
| 12 | **Supervisor** | Draft exists, not reviewed → routes to **Critic** |
| 13 | **Critic** | Reviews for accuracy & completeness → ✅ Approved |
| 14 | **Supervisor** | Approved → **FINISH** → Returns final report to user |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|:------|:-----------|:--------|
| **LLM Inference** | [Groq](https://groq.com/) (Llama 3.3 70B) | Ultra-fast inference for all agents |
| **Agent Framework** | [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful, cyclic agent graph with checkpointing |
| **Structured Output** | [Pydantic](https://docs.pydantic.dev/) | Typed contracts between agents |
| **Web Search** | [Tavily](https://tavily.com/) | Advanced web search with depth control |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com/) | Streaming SSE endpoint for the research pipeline |
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive research chat UI |
| **Checkpointing** | [PostgreSQL](https://www.postgresql.org/) + psycopg | Persistent workflow state & recovery |
| **Observability** | [LangSmith](https://smith.langchain.com/) | Full trace visualization & debugging |
| **Package Management** | [uv](https://github.com/astral-sh/uv) | Fast, deterministic dependency resolution |
| **Containerization** | [Docker](https://www.docker.com/) | Production-ready deployment |

---

## 📊 Design Decisions

| Decision | Rationale |
|:---------|:----------|
| **Deterministic routing over LLM-based routing** | The supervisor uses explicit state checks (`if sub_tasks is None → planner`) instead of asking the LLM to decide next steps. This eliminates routing hallucinations and makes the workflow 100% predictable. |
| **One sub-task per researcher invocation** | Processing sub-tasks sequentially ensures focused, high-quality research per topic and naturally fits LangGraph's graph traversal model. |
| **Critic → Writer feedback loop** | Adding a review cycle catches factual errors and missing coverage before the final output, mimicking real editorial workflows. |
| **PostgreSQL checkpointing** | Enables long-running research sessions to survive process restarts and allows replaying past workflows for debugging. |
| **Pydantic structured output** | Enforces schema compliance between agents at runtime — a malformed sub-task or routing decision will raise immediately rather than causing silent downstream failures. |

<p align="center">
  Built with ❤️ by <a href="https://github.com/NirbhayShegale">Nirbhay Shegale</a>
</p>
