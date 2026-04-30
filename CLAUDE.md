# Claude Architect Cert + AI Safety Research — Claude Code Instructions

## Project overview
Dual-purpose repo: studying for the Claude Certified Architect exam (5 domains)
while building real AI safety research projects drawing from the ARENA curriculum.
Primary language: Python 3.11+.
ML stack (ARENA projects): PyTorch, TransformerLens, nnsight.
Agent stack: claude-agent-sdk, anthropic.

## Directory layout
project-root/
├── d1_agentic/                  # Domain 1: Agentic Architecture & Orchestration (~25%)
│   ├── arena/                   # ARENA ch3.4 (LLM Agents), ch4.5 (Investigator Agents)
│   │   ├── safety_evaluator/    # Multi-agent safety evaluator (coordinator + subagents)
│   │   └── red_team_pipeline/   # Petri-style multi-turn red-teaming (Claude Agent SDK)
│   └── cert/                    # Cert-only D1 exercises (no ARENA equivalent)
│       └── hook_enforcement/    # Programmatic hooks + escalation patterns
│
├── d2_tools/                    # Domain 2: Tool Design & MCP Integration (~20%)
│   ├── arena/                   # ARENA ch1.2, ch1.3 (TransformerLens as MCP tools)
│   │   └── interp_mcp_server/   # Interpretability ops exposed as MCP server
│   └── cert/                    # Cert-only D2 exercises
│       ├── error_responses/     # Structured error response patterns
│       └── mcp_config/          # MCP server config + Claude Desktop wiring
│
├── d3_claude_code/              # Domain 3: Claude Code Configuration & Workflows (~20%)
│   ├── arena/                   # No ARENA equivalent — this folder intentionally thin
│   └── cert/                    # All D3 work lives here
│       ├── slash_commands/      # Custom slash commands for research workflows
│       └── ci_pipeline/         # Claude Code -p flag + automated review pipeline
│
├── d4_prompts/                  # Domain 4: Prompt Engineering & Structured Output (~20%)
│   ├── arena/                   # ARENA ch3.1 (threat models), ch3.2 (dataset gen)
│   │   ├── eval_dataset_gen/    # Alignment eval dataset generator
│   │   └── behavior_extraction/ # Behavior extraction schema + retry loop
│   └── cert/                    # Cert-only D4 exercises
│       └── session_isolation/   # Generator vs reviewer session separation
│
├── d5_context/                  # Domain 5: Context Management & Reliability (~15%)
│   ├── arena/                   # ARENA ch4.1, ch4.2 (misalignment case studies)
│   │   └── interp_assistant/    # Long-horizon interpretability research assistant
│   └── cert/                    # Cert-only D5 exercises
│       ├── escalation_triggers/ # Programmatic escalation trigger system
│       └── accuracy_tracker/    # Per-category accuracy tracker (anti-masking)
│
├── shared/                      # Shared utilities used by 3+ domains
│   ├── api/                     # Anthropic client wrappers, retry logic, model constants
│   ├── logging/                 # Loguru setup, result serialization helpers
│   ├── schemas/                 # Reusable Pydantic models + JSON schemas
│   └── testing/                 # Shared pytest fixtures, API mock helpers
│
├── data/
│   ├── raw/                     # Never modify — original model outputs and datasets
│   ├── processed/               # Cleaned/transformed; document transformation in README
│   └── results/                 # Experiment outputs — always timestamp filenames
│
├── tests/                       # Mirrors src structure; unit tests only
│   └── integration/             # API-calling tests; require INTEGRATION=1 env var
│
├── notebooks/                   # Exploratory only — production code lives in domain dirs
└── .claude/
└── rules/                   # Scoped rules applied per domain (see below)

## Environment setup
- Python env: `uv venv && source .venv/bin/activate`
- Install deps: `uv pip install -r requirements.txt`
- Set path: `export PYTHONPATH=/workspaces/claude-architect-cert` (add to ~/.bashrc to persist)
- Run tests: `pytest tests/ -v`
- Integration tests: `INTEGRATION=1 pytest tests/integration/ -v`
- Lint: `ruff check . && ruff format .`

## Coding conventions
- Type hints required on all public functions
- Docstrings required on all classes and public functions (Google style)
- Never hardcode API keys — load from `.env` via `python-dotenv`
- Use `loguru` for all logging — never `print()`. Set level via `LOG_LEVEL` env var
- Every runnable module needs a `main()` and `if __name__ == "__main__"` guard
- All Anthropic API calls must accept a `model: str` param with a sensible default

## Shared utilities usage rules
- If a utility is used by 3+ domain projects → it belongs in `shared/`
- If a utility is used by 1–2 projects → keep it local to that domain
- Never import from a domain directory into another domain directory
- `shared/api/` is the only place Anthropic client instances should be created

## Model constants (use these everywhere, never hardcode model strings)
```python
# shared/api/models.py — use these imports throughout the repo
DEFAULT_MODEL   = "claude-sonnet-4-6"   # balanced default for most tasks
EVAL_MODEL      = "claude-haiku-4-5"    # high-volume generation and classification
JUDGMENT_MODEL  = "claude-opus-4-6"     # complex reasoning and quality judgment
```

## Agent/API patterns (for all d1_agentic/ and d2_tools/ work)
- Always check `stop_reason` to control agentic loops — never use arbitrary iteration caps
- Max 4–5 tools per agent — use separate agents for separate concerns
- Subagents must never share sessions with their coordinator — always fresh sessions
- Structured outputs: always use `tool_use` with a typed JSON schema, not free-text parsing
- Error responses must always include: `isError`, `errorCategory`, `isRetryable`, `context`
- Programmatic hooks for policy enforcement — never rely on prompt-based rules for critical checks

## Experiment conventions (for arena/ subfolders)
- Each experiment directory needs: `README.md`, `config.py`, `run.py`
- `config.py` uses dataclasses for all hyperparameters — no magic numbers in run scripts
- Save all results to `data/results/<domain>_<experiment>_<YYYYMMDD_HHMMSS>.json`
- Log model name, timestamp, and git commit hash with every result
- Document which cert domain(s) the experiment covers in the README

## cert/ subfolder conventions
- Each cert exercise needs: `README.md` explaining the cert concept being demonstrated,
  and a `notes.md` flagging anti-patterns and exam gotchas
- Write at least one test per pattern demonstrated — the test IS the proof of understanding

## Git workflow
- Branch naming: `d<N>/<short-description>` e.g. `d1/safety-evaluator`
- Commit format: `[d<N>] short description` e.g. `[d1] add coordinator stop_reason loop`
- Never commit: API keys, model weights, large files (>10MB), `.env`
- `.gitignore` must include: `.env`, `*.pt`, `*.safetensors`, `data/raw/*`, `__pycache__`

## Testing
- Unit tests in `tests/` mirror the domain directory structure
- Mock all API calls in unit tests using `pytest-mock`
- Integration tests in `tests/integration/` — require `INTEGRATION=1` env var
- Minimum one test per public utility in `shared/`

## Notes for Claude Code
- Always use `/plan` before any task that touches multiple files or creates new modules
- When adding dependencies, update `requirements.txt` and explain why in your message
- If a file already exists, ask before overwriting
- When I say "start a new experiment", scaffold the full directory (README, config, run.py)
- When I say "this is a cert exercise", also create the `notes.md` anti-patterns file
- Prefer extending `shared/` utilities over duplicating logic in domain folders