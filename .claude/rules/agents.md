---
paths:
  - "d1_agentic/**/*.py"
  - "d2_tools/**/*.py"
---

# Agent and tool code rules

- Every agent module must define its system prompt as a module-level constant
- Agentic loops must terminate on stop_reason == "end_turn" — no string parsing of responses
- All tool schemas must include description, required fields, and example values in descriptions
- Use programmatic hooks for policy enforcement — never prompt-based rules for critical checks
- Subagents must never share sessions with the coordinator
- Document intended tool count per agent in the module docstring (max 5)
- Import the Anthropic client only from shared/api/ — never instantiate it directly in agent code