# Claude Architect Cert × ARENA — Domain Map

Cert domains first. ARENA sections mapped where overlap exists. Standalone projects fill the gaps.

---

## D1 — Agentic Architecture & Orchestration (~25%) · Strong ARENA overlap

| Cert topic to master | ARENA section | Project that covers both |
|---|---|---|
| Agentic loops: stop_reason checks, no arbitrary iteration caps | **3.4 LLM Agents** — ARENA's "glorified for-loop" framing maps 1:1 | **Multi-agent safety evaluator** — Coordinator + probe/classify/aggregate subagents. Exercises stop_reason loops, session isolation, error propagation. |
| Multi-agent orchestration: hub-and-spoke, context isolation, error propagation | **4.5 Investigator Agents** — Petri's auditor/judge IS coordinator/subagent | **Petri-style red-teaming pipeline (Claude SDK)** — Direct port of ARENA 4.5 to Claude Agent SDK. Coordinator + auditor + judge subagents. |
| Hooks for deterministic enforcement; escalation on task complexity not sentiment | No ARENA equivalent — cert-specific production pattern | **Hook-based policy enforcement layer** — Pre/post hooks that enforce safety rules programmatically, not via prompting. |

---

## D2 — Tool Design & MCP Integration (~20%) · Partial ARENA overlap

| Cert topic to master | ARENA section | Project that covers both |
|---|---|---|
| Tool description best practices; 4–5 tools per agent max | **3.4 LLM Agents** — ARENA teaches function calling with Inspect | **Interpretability ops as MCP server** — Wrap TransformerLens/SAE ops as MCP tools. Forces rigorous tool descriptions and schema design. |
| Structured error responses: isError, errorCategory, isRetryable, context | No ARENA equivalent — cert-specific production pattern | **Structured error response wrapper** — Consistent error layer for any MCP server. Key exam anti-pattern: generic error messages. |
| MCP server config, Claude's built-in tools, tool distribution across agents | No ARENA equivalent — cert-specific tooling knowledge | **Research MCP server + Claude Desktop setup** — End-to-end MCP config exercise. Covers tool distribution, built-in tools, `.mcp.json` pattern. |

---

## D3 — Claude Code Configuration & Workflows (~20%) · No ARENA overlap — build to learn

| Cert topic to master | ARENA section | Project |
|---|---|---|
| CLAUDE.md hierarchy: project vs user vs local; /init and iterative refinement | No overlap — Claude Code-specific; do as setup | **ARENA repo CLAUDE.md hierarchy** — Build the CLAUDE.md system for your repo. Covers project/user/local scoping and path-specific rules. |
| Custom slash commands and skills; plan mode vs direct execution | No overlap — Claude Code-specific; dev workflow | **Research slash commands: /run-interp-experiment etc.** — Build real slash commands for ARENA workflow. Exercises skills, plan mode, iterative refinement. |
| CI/CD integration: -p flag, --output-format json, separate reviewer session | No overlap — cert-specific; pure engineering | **Automated experiment code review pipeline** — GitHub Actions + Claude Code -p flag. Separate reviewer session is the key anti-pattern to avoid. |

---

## D4 — Prompt Engineering & Structured Output (~20%) · Strong ARENA overlap

| Cert topic to master | ARENA section | Project that covers both |
|---|---|---|
| Few-shot prompting; explicit criteria; tool_use for structured output | **3.2 Dataset Generation** — Near 1:1, same techniques, different SDK | **Alignment eval dataset generator** — ARENA 3.2 ported to Claude SDK. Few-shot prompting + tool_use schema + validation-retry loop. |
| JSON schema design for tool_use; validation-retry loops; field-level confidence | **3.1 Intro to Evals** — Threat model specs → schema design | **Behavior extraction schema + retry loop** — Design and implement the JSON schema + retry loop pattern the cert exam tests directly. |
| Multi-pass review strategies; separate sessions for generator vs reviewer | **4.2 Science of Misalignment** — Black-box investigation = multi-pass review | **Generator / reviewer session isolation** — Core cert anti-pattern in practice. Separate sessions, explicit scoring criteria, no context leakage. |

---

## D5 — Context Management & Reliability (~15%) · Partial ARENA overlap

| Cert topic to master | ARENA section | Project that covers both |
|---|---|---|
| Progressive summarization risks; context positioning; information provenance | **4.1 Emergent Misalignment** — Long investigations stress context management | **Long-horizon interpretability assistant** — Stress-tests context management. Activation data fills context fast — real constraint that forces good D5 patterns. |
| Escalation patterns; human review triggers; context degradation detection | **4.2 Science of Misalignment** — Knowing when to stop trusting synthesis | **Programmatic escalation trigger system** — Covers the cert's key D5 anti-pattern: escalating on sentiment vs structured criteria. |
| Accuracy per document type; masking failures in aggregate metrics | No ARENA equivalent — cert-specific reliability engineering | **Per-category accuracy tracker** — Targets the cert anti-pattern of aggregate-only metrics hiding subcategory failures. |

---

*Claude Certified Architect × ARENA Curriculum — study reference*
