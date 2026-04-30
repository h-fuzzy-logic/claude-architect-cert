
# Domain 1: Agentic Architecture & Orchestration
Design and implement agentic systems using Claude's Agent SDK. Covers agentic loops, multi-agent orchestration, hooks, workflows, session management, and task decomposition patterns for production-grade AI applications. Details in the [exam guide](https://claudecertifications.com/claude-certified-architect/domains/agentic-architecture).

## In This Domain

### Agentic Loops & Core API
Multi-agent safety evaulator built with [Claude command](../.claude/commands/d1-safety-evaluator.md).
#### Learnings
In the [safety evaluator](/d1_agentic/arena/safety_evaluator/run.py), these are the three key pieces of the architecture: 
1. Coordinator (run_coordinator, line 163) — loops over active safety dimensions (harm, honesty, helpfulness, instruction_following) and dispatches one subagent per dimension. It never evaluates text itself.      
2. Subagents (evaluate_dimension, line 103) — each gets a fresh anthropic.Anthropic() client (line 115), which is the critical rule: subagents must never share sessions with the coordinator. Each evaluates exactly one dimension.                                                      
3. Structured output via tool_use (line 45) — instead of parsing free text, the subagent is forced to call submit_verdict with a typed schema. The loop terminates on stop_reason == "end_turn" or "tool_use" — never a string match on response content.  

The cert concepts demonstrated:                                             
1. stop_reason controls the loop (line 137–155), not iteration caps
2. Fresh client per subagent (no shared sessions)                            
3. VERDICT_TOOL schema has description + required fields (per agents.md rules)  
4. _empty_verdict always includes isError, errorCategory, isRetryable, context

### Multi-Agent Orchestration
#### Learnings

### Hooks & Programmatic Enforcement
#### Learnings


### Session Management & Workflows
#### Learnings






