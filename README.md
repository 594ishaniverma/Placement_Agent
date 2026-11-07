# Placement Agent

A LangGraph placement-notice workflow with a read-only MCP SQLite tool server,
human approval, guardrails, shadow-mode execution, and evaluation.

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
python data/seed_students.py
python app.py --post 01
```

Copy `.env.example` to `.env` and add API keys for Anthropic/LangSmith. The CLI
also works without an API key using deterministic extraction and notice drafting.

## Workflow

```text
Job post -> extract rules -> ambiguity check -> eligible student query
         -> draft notice -> human approval -> approved/rejected result
```

The [architecture diagram](docs/architecture.png) is available as an SVG-compatible
placeholder for local documentation. MCP queries are allowlisted and row-limited.
Student IDs are validated before a notice is approved, and private fields are
excluded from drafts.

## Synthetic data

`data/students.db` is generated from Faker data by `data/seed_students.py`.
The database is synthetic and contains no real student records.

## Commands

```powershell
python mcp_server/server.py
python shadow/run_shadow.py
python eval/run_eval.py
python -m pytest tests
```