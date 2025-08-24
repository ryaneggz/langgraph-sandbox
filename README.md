# LangGraph Starter

A LangGraph-based starter template for building **collections of AI agents**. This template provides a foundation for creating multi-agent systems with capabilities like LinkedIn lead collection, web search, and Airtable data integration.

---

## ✨ Features

- Collection of configurable AI agents using **DeepAgents** and **LangGraph**
- Agent entrypoints defined in `langgraph.json` for easy management
- Example: **LinkedIn Lead Collector** agent
- **Airtable** integration for structured data storage
- Built-in **web search** tools
- **VS Code** debugging configuration included
- **Docker**-ready for containerized development & deployment

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Docker** (optional, for containerized deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone <YOUR_REPO_URL> langgraph-starter
   cd langgraph-starter
   ```

2. **Install dependencies with uv (recommended)**

   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Start the development server**

   ```bash
   make dev
   ```

---

## 🗂️ Project Structure

```text
langgraph-starter/
├─ agents/
│  └─ linkedin_leads.py          # LinkedIn lead collection agent (example)
├─ tools/
│  ├─ __init__.py
│  ├─ airtable.py                # Airtable integration tools
│  └─ search.py                  # Web search tools
├─ .vscode/
│  └─ launch.json                # VS Code debug config
├─ docker-compose.yml            # Docker services
├─ langgraph.json                # LangGraph configuration
├─ Makefile                      # Dev commands
├─ pyproject.toml                # Python project configuration
└─ .env.example                  # Example environment variables
```

---

## 🧰 Commands

### Make targets

```bash
make dev      # Start development server
make debug    # Start with debugging enabled (port 5678)
make build    # Build and push Docker image
```

### Using the LangGraph CLI directly

```bash
langgraph dev                       # Start dev server
langgraph dev --debug-port 5678     # Start with debugging
langgraph build                     # Build the application
```

---

## 🧠 How It Works

### Agent Architecture

* **Modular Design** — Each agent is a separate module under `agents/`
* **LangGraph Integration** — Agents and entrypoints are declared in `langgraph.json`
* **Tooling** — Shared tools under `tools/` (e.g., Airtable, search) can be reused
* **State & Orchestration** — LangGraph coordinates agent state and message flow

### Included Example Agents

1. **LinkedIn Lead Collector** — Searches LinkedIn for potential leads (example logic)
2. **Note Taker** — Normalizes and organizes collected data
3. **Airtable Integration** — Persists structured results to Airtable

### Adding a New Agent

1. Create a new file under `agents/` (e.g., `my_agent.py`)
2. Register it in `langgraph.json` (entrypoints, graph configuration)
3. Wire up any shared tools you need from `tools/`

---

## ⚙️ Configuration

Key files:

* `langgraph.json` — Graphs and entrypoints
* `.env` — Environment variables and API keys
* `pyproject.toml` — Python dependencies and project metadata
* `.vscode/launch.json` — VS Code debugging configuration

> Tip: Ensure any secrets (API keys, tokens) are only in `.env` and **excluded** from version control.

---

## 🖥️ Recommended LangGraph UIs

* **[LangGraph Studio](https://smith.langchain.com/studio)** — Official Studio for visual graph editing & monitoring
* **[Agent Chat UI](https://agentchat.vercel.app)** — Clean chat interface for testing your agents

---

## 🛠️ Development & Debugging

* **`.vscode/launch.json`** is pre-configured for:

  * **Attach to LangGraph** — Debug a running server on port `5678`
  * **Debug Script** — Run and debug individual scripts

**Steps:**

1. Run:

   ```bash
   make debug
   ```
2. In VS Code, press **F5** and select **Attach to LangGraph**.

---

## 🐳 Docker (optional)

Build and run with Docker:

```bash
docker compose up --build
```

Mount local files (e.g., `/files`) via `docker-compose.yml` volumes for read/write access.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch:

   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit:

   ```bash
   git commit -m "Add amazing feature"
   ```
4. Push:

   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

---

## 📄 License

This project is licensed under the terms specified in the **LICENSE** file.

```