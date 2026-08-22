# Ruflo — Claude Code Configuration

## Rules

- Do what has been asked; nothing more, nothing less
- NEVER create files unless absolutely necessary — prefer editing existing files
- NEVER create documentation files unless explicitly requested
- NEVER save working files or tests to root — use `/src`, `/tests`, `/docs`, `/config`, `/scripts`
- ALWAYS read a file before editing it
- NEVER commit secrets, credentials, or .env files
- NEVER add a `Co-Authored-By` trailer to user commits unless this project's `.claude/settings.json` has `attribution.commit` set (#2078). The Claude Code Bash tool may suggest one in its default commit-message template — ignore it. `Co-Authored-By` is semantic authorship attribution under git/GitHub convention; the tool is the facilitator, not a co-author.
- Keep files under 500 lines
- Validate input at system boundaries

## Shopify mutation rules

**`userErrors: []` does not prove a mutation succeeded.**

Every mutation requires an authoritative read-back and an expected-state
comparison before it may be classified as successful. An empty error list means
the request was accepted, not that anything was written.

Confirmed on this store by two separate APIs:

- `themeFilesUpsert` reports success as an empty list whether or not the file
  landed — verify with `checksumMd5` against the local source.
- `productOptionsReorder` returns `userErrors: []`, echoes a well-formed
  payload, and performs no write at all — `updatedAt` never moves.

The read-back must check the field that actually carries the change, plus the
resource's `updatedAt`. A write bumps that timestamp; if it has not moved,
nothing happened regardless of what the payload said.

Two more that follow from the same class of failure:

- **A mutation payload can echo stale state.** Query the resource again rather
  than trusting the object the mutation returned.
- **Two no-ops are the stop signal.** If the officially documented operation
  does not take effect, report it blocked and name the smallest human action.
  Do not reach for a strategy that rebuilds what it was meant to adjust —
  recreating variants, options or products to fix an ordering or display
  problem risks the identity of everything downstream.

### The mutation sequence

Every Shopify mutation runs this sequence. It is one sequence, not one per
resource type; steps 11 and 12 are the only additions.

**Before**

1. Authoritative current-state read — from Shopify, this session, not from a
   prompt, a prior report, or a document in this repo.
2. Target identity verification — the GID you are about to write to is the GID
   you read back, checked field by field, not matched by name or by position.
3. Role / status verification — theme `role`, product `status`.
4. Concurrency snapshot — capture the fields the write must not disturb, so
   collateral damage is detectable afterwards.
5. Smallest mutation that achieves the goal.

**After**

6. Independent fresh read, issued after the mutation returned.
7. Exact comparison on the intended field.
8. Comparison on unrelated state that must not have moved.
9. `updatedAt` check wherever the resource carries one.
10. Only then classify the mutation as successful.

**Theme mutations add:**

11. Re-verify the target theme's `role` immediately before the write. Role can
    change between your first read and your write — that is exactly what
    happened on 2026-08-21.

**Product mutations add:**

12. Re-verify the product's `status` immediately before the write.

---

## Shopify production-state rule

**Theme role must never be inferred from a theme ID or a theme name.**

Before any theme mutation:

1. Query current theme roles from Shopify.
2. Identify `MAIN` dynamically, from the returned `role` field.
3. Identify the intended non-production target dynamically, the same way.
4. Compare live state against the assumptions in the task prompt.
5. **If they disagree, live Shopify state wins.**
6. Stop before writing until the target is confirmed safe.

Never conclude a theme is `MAIN` or `UNPUBLISHED` from any of these:

- a numeric theme ID
- a theme name
- a prior session's report
- the task prompt
- a branch name
- a directory name
- a document in this repository, including `docs/HIVOLT-CURRENT-STATE.md`

**Theme IDs survive role changes. Theme names go stale. Only the current
`role` field returned by Shopify is authoritative.**

This store has already produced both failure modes:

| Theme | Name says | Role actually is |
|---|---|---|
| `158653808872` | "HIVOLT v7 — **DRAFT**: PDP data layer (do not publish)" | **`MAIN`** — live since 2026-08-21 |
| `158482727144` | "HIVOLT v35 — **LIVE** (returns copy fixed)" | `UNPUBLISHED` |

Two themes, both named the opposite of what they are. A session that trusted
either name would have written to the wrong one.

### MAIN theme write rule

A write to whichever theme currently holds role `MAIN` requires **explicit task
authorization for production modification.**

If the task says "draft only" and the intended theme is currently `MAIN`:

**STOP.**

- Do not reinterpret the authorization.
- Do not silently redirect the write to a different theme.
- Do not publish or unpublish any theme as a workaround.

Report the conflict and name the smallest human action. A refused write that
names the conflict is a successful outcome.

### Preflight

`site/check-hivolt-theme-target.py` adjudicates a target against a theme list.
It does not fetch — fetching is connector-only, see below — but it applies the
rules above deterministically and exits non-zero on a violation:

```
# paste the themes read-back into a file, then:
python3 site/check-hivolt-theme-target.py --themes state.json --report
python3 site/check-hivolt-theme-target.py --themes state.json \
        --target <gid> --expect-role UNPUBLISHED
python3 site/check-hivolt-theme-target.py --self-test
```

Exit 1 is a refusal. Do not work around it. Passing the live theme's gid with
`--expect-role UNPUBLISHED` — the assumption every session held before
2026-08-21 — prints the conflict and exits 1, which is the whole point.

**No standalone script in this repo can query Shopify.** There are no Shopify
credentials in the environment, no script contains an Admin API call, and
egress to `f36zps-yd.myshopify.com` is denied at CONNECT by network policy.
Shopify is reachable only through the MCP connector, which is available to the
Claude session and not to a subprocess. Fetch with the connector; adjudicate
with the script.

Current known state lives in `docs/HIVOLT-CURRENT-STATE.md`. **That file is a
convenience, not an authority** — it is written by a past session and can be as
stale as any prompt. Re-query before writing.

## Ruflo Capability Brain & Implementation Loop

Ruflo is the coordination ledger and policy decision point. Claude Code is the
executor: after a Ruflo coordination call, continue implementing the task.

When it is registered, call
`guidance_brain({ mode: "recommend", task: "..." })` before complex Ruflo
work. Use its live registry instead of guessing tool names. Treat
`registered`, `configured`, `reachable`, `healthy`, and `authorized`
as separate facts. If the brain is unavailable, continue with the compatible
`guidance_recommend` tool, CLI discovery, and repository instructions.

Follow the returned loop:

1. Recall memory and ADR constraints.
2. Inspect source, runtime, dependencies, policy, and health.
3. Route to the smallest capable topology, agents, skills, and tools.
4. Plan acceptance criteria, safety envelope, ownership, and validation.
5. Execute in isolated scopes; the coding agent performs the work.
6. Test focused, regression, and failure paths.
7. Validate types, security, policy, compatibility, and artifacts.
8. Benchmark a source-bound candidate against a source-bound baseline.
9. Optimize measured bottlenecks without weakening safety.
10. Bind claims and evidence to exact source/build receipts.
11. Reconcile concurrent handoffs and disclose limitations.
12. Publish only through a separately authorized release gate.

### Concurrency and authority

- Never allow two writers in one worktree; give each writing agent an isolated
  worktree and explicit file ownership.
- Read-only research may run concurrently and report findings to the owner.
- Only the integration owner edits shared manifests and lockfiles or reconciles
  overlapping changes.
- A child may drop capabilities but cannot add tools, network, secrets, spend,
  concurrency, namespaces, or delegation depth.
- A lease or claim coordinates ownership; it does not authorize a side effect.
- Darwin, Flywheel, MetaHarness, memory, and neural systems may propose or
  evaluate candidates but cannot self-promote or expand their SafetyEnvelope.
- Bind tests, benchmarks, policy decisions, and release evidence to an exact
  commit or immutable dirty-worktree snapshot.

## Agent Comms (SendMessage-First Coordination)

Named agents coordinate via `SendMessage`, not polling or shared state.

```
Lead (you) ←→ architect ←→ developer ←→ tester ←→ reviewer
              (named agents message each other directly)
```

### Spawning a Coordinated Team

```javascript
// ALL agents in ONE message, each knows WHO to message next
Agent({ prompt: "Research the codebase. SendMessage findings to 'architect'.",
  subagent_type: "researcher", name: "researcher", run_in_background: true })
Agent({ prompt: "Wait for 'researcher'. Design solution. SendMessage to 'coder'.",
  subagent_type: "system-architect", name: "architect", run_in_background: true })
Agent({ prompt: "Wait for 'architect'. Implement it. SendMessage to 'tester'.",
  subagent_type: "coder", name: "coder", run_in_background: true })
Agent({ prompt: "Wait for 'coder'. Write tests. SendMessage results to 'reviewer'.",
  subagent_type: "tester", name: "tester", run_in_background: true })
Agent({ prompt: "Wait for 'tester'. Review code quality and security.",
  subagent_type: "reviewer", name: "reviewer", run_in_background: true })

// Kick off the pipeline
SendMessage({ to: "researcher", summary: "Start", message: "[task context]" })
```

### Patterns

| Pattern | Flow | Use When |
|---------|------|----------|
| **Pipeline** | A → B → C → D | Sequential dependencies (feature dev) |
| **Fan-out** | Lead → A, B, C → Lead | Independent parallel work (research) |
| **Supervisor** | Lead ↔ workers | Ongoing coordination (complex refactor) |

### Rules

- ALWAYS name agents — `name: "role"` makes them addressable
- ALWAYS include comms instructions in prompts — who to message, what to send
- Spawn ALL agents in ONE message with `run_in_background: true`
- After spawning, continue independent local work; wait only when a dependency
  genuinely blocks progress
- Do not poll repeatedly — agents message back or complete automatically
- Give every writing agent an isolated worktree and a non-overlapping file scope

## Swarm & Routing

### Config
- **Topology**: hierarchical-mesh (anti-drift)
- **Max Agents**: 15
- **Memory**: hybrid
- **HNSW**: Enabled
- **Neural**: Enabled

```bash
npx @claude-flow/cli@latest swarm init --topology hierarchical --max-agents 8 --strategy specialized
```

### Agent Routing

| Task | Agents | Topology |
|------|--------|----------|
| Bug Fix | researcher, coder, tester | hierarchical |
| Feature | architect, coder, tester, reviewer | hierarchical |
| Refactor | architect, coder, reviewer | hierarchical |
| Performance | perf-engineer, coder | hierarchical |
| Security | security-architect, auditor | hierarchical |

### When to Swarm
- **YES**: 3+ files, new features, cross-module refactoring, API changes, security, performance
- **NO**: single file edits, 1-2 line fixes, docs updates, config changes, questions

### 3-Tier Model Routing

| Tier | Handler | Use Cases |
|------|---------|-----------|
| 1 | Agent Booster (WASM) | Simple transforms — skip LLM, use Edit directly |
| 2 | Haiku | Simple tasks, low complexity |
| 3 | Sonnet/Opus | Architecture, security, complex reasoning |

## Memory & Learning

### Before Any Task
```bash
npx @claude-flow/cli@latest memory search --query "[task keywords]" --namespace patterns
npx @claude-flow/cli@latest hooks route --task "[task description]"
```

### After Success
```bash
npx @claude-flow/cli@latest memory store --namespace patterns --key "[name]" --value "[what worked]"
npx @claude-flow/cli@latest hooks post-task --task-id "[id]" --success true --store-results true
```

### MCP Tools (use `ToolSearch("keyword")` to discover)

| Category | Key Tools |
|----------|-----------|
| **Memory** | `memory_store`, `memory_search`, `memory_search_unified` |
| **Bridge** | `memory_import_claude`, `memory_bridge_status` |
| **Swarm** | `swarm_init`, `swarm_status`, `swarm_health` |
| **Agents** | `agent_spawn`, `agent_list`, `agent_status` |
| **Hooks** | `hooks_route`, `hooks_post-task`, `hooks_worker-dispatch` |
| **Security** | `aidefence_scan`, `aidefence_is_safe`, `aidefence_has_pii` |
| **Hive-Mind** | `hive-mind_init`, `hive-mind_consensus`, `hive-mind_spawn` |

### Background Workers

| Worker | When |
|--------|------|
| `audit` | After security changes |
| `optimize` | After performance work |
| `testgaps` | After adding features |
| `map` | Every 5+ file changes |
| `document` | After API changes |

```bash
npx @claude-flow/cli@latest hooks worker dispatch --trigger audit
```

## Agents

**Core**: `coder`, `reviewer`, `tester`, `planner`, `researcher`
**Architecture**: `system-architect`, `backend-dev`, `mobile-dev`
**Security**: `security-architect`, `security-auditor`
**Performance**: `performance-engineer`, `perf-analyzer`
**Coordination**: `hierarchical-coordinator`, `mesh-coordinator`, `adaptive-coordinator`
**GitHub**: `pr-manager`, `code-review-swarm`, `issue-tracker`, `release-manager`

Any string works as a custom agent type.

## Build & Test

- ALWAYS run tests after code changes
- ALWAYS verify build succeeds before committing

```bash
npm run build && npm test
```

## CLI Quick Reference

```bash
npx @claude-flow/cli@latest init --wizard           # Setup
npx @claude-flow/cli@latest swarm init --v3-mode     # Start swarm
npx @claude-flow/cli@latest memory search --query "" # Vector search
npx @claude-flow/cli@latest hooks route --task ""    # Route to agent
npx @claude-flow/cli@latest doctor --fix             # Diagnostics
npx @claude-flow/cli@latest security scan            # Security scan
npx @claude-flow/cli@latest performance benchmark    # Benchmarks
```

26 commands, 140+ subcommands. Use `--help` on any command for details.

## Setup

```bash
claude mcp add claude-flow -- npx -y ruflo@latest mcp start
npx ruflo@latest doctor --fix
```

> The background `daemon` is optional. It runs interval workers that each spawn
> a headless `claude` session, so it consumes tokens continuously. Start it only
> if you want those sweeps: `npx ruflo@latest daemon start` (self-stops after 12h
> by default; `--ttl 0` to disable, `daemon status --all` to audit running daemons).

**Agent tool** handles execution (agents, files, code, git). **MCP tools** handle coordination (swarm, memory, hooks). **CLI** is the same via Bash.
