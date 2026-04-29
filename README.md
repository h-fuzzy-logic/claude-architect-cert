# Claude Architect Certification + AI Safety Research

A dual-purpose repo, studying for the **Claude Certified Architect** [exam](https://claudecertifications.com/claude-certified-architect/study-guide) while combining AI safety research topics from the **ARENA curriculum** (Alignment Research
Engineer Accelerator) [GitHub repo](https://github.com/callummcdougall/ARENA_3.0). 

---

## Reason for repo

Most cert prep is abstract or simply memorization. I really wanted to the learn the Claude Architect topics and use them in code. There is some overlap between the exam domains and the ARENA repo. Where ARENA has no cert equivalent (and vice versa), standalone exercises fill the gap. 

In my daily use of AI coding assistants, AI chatbots, and LLM APIs, I regularly see responses that I'd like to understand: 
* Why was the word "dead" included in the generated README.md?
* Why does changing the pronoun from he to she generate such different advice?
* Why do I have to prompt: Try again. Don't use the hypothesis framework. Use pytest. 
---

## The Claude Certified Architect Exam

The exam covers five domains, weighted by importance:

| Domain | Topic | Weight |
|--------|-------|--------|
| D1 | Agentic Architecture & Orchestration | ~25% |
| D2 | Tool Design & MCP Integration | ~20% |
| D3 | Claude Code Configuration & Workflows | ~20% |
| D4 | Prompt Engineering & Structured Output | ~20% |
| D5 | Context Management & Reliability | ~15% |

Each domain has its own top-level directory (`d1_agentic/`, `d2_tools/`, etc.) containing
both ARENA research projects and cert-specific exercises.

---

## The ARENA Curriculum

[ARENA](https://learn.arena.education) is a structured AI safety curriculum covering:

- **Chapter 0** — Fundamentals (PyTorch, backprop, CNNs)
- **Chapter 1** — Transformer Interpretability (probes, SAEs, circuit analysis)
- **Chapter 2** — Reinforcement Learning (DQN, PPO, RLHF)
- **Chapter 3** — LLM Evaluations (threat models, dataset generation, agents)
- **Chapter 4** — Alignment Science (misalignment, reasoning models, investigator agents)

---

## How the Domains Map to ARENA

Some cert domains map directly to ARENA chapters. Others have no ARENA equivalent and are covered by standalone exercises.  See [mapping summary](/docs/domain-map.md).


---

## Repo Structure

```
project-root/
├── d1_agentic/          # Domain 1 — Agentic Architecture & Orchestration
│   ├── arena/           # Safety evaluator, red-team pipeline
│   └── cert/            # Hook enforcement, escalation patterns
├── d2_tools/            # Domain 2 — Tool Design & MCP Integration
│   ├── arena/           # Interpretability MCP server
│   └── cert/            # Structured error responses, MCP config
├── d3_claude_code/      # Domain 3 — Claude Code Configuration & Workflows
│   └── cert/            # Slash commands, CI pipeline
├── d4_prompts/          # Domain 4 — Prompt Engineering & Structured Output
│   ├── arena/           # Eval dataset generator, behavior extraction
│   └── cert/            # Session isolation patterns
├── d5_context/          # Domain 5 — Context Management & Reliability
│   ├── arena/           # Long-horizon interpretability assistant
│   └── cert/            # Escalation triggers, accuracy tracker
├── shared/              # Utilities used across 3+ domains
│   ├── api/             # Anthropic client, model constants, retry logic
│   ├── logging/         # Loguru setup, result serialization
│   ├── schemas/         # Pydantic models, reusable JSON schemas
│   └── testing/         # Pytest fixtures, API mock helpers
├── data/
│   ├── raw/             # Never modified — original outputs and datasets
│   ├── processed/       # Cleaned versions; transformation documented in README
│   └── results/         # Timestamped experiment outputs
├── tests/               # Unit tests mirroring domain structure
│   └── integration/     # API-calling tests; require INTEGRATION=1
└── notebooks/           # Exploratory only — production code lives in domain dirs
```

---

