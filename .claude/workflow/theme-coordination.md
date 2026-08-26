# Protocol: theme-coordination

Persistent portfolio governance for **one research theme**. The `theme-coordinator` reconstructs the
theme's live state, selects bounded work, delegates each run to a `research-leader`, communicates
decisions and surprises to the human, and reconciles results into the next frontier. It does not execute
the delegated run itself.

This protocol is platform-neutral. Claude and Codex map spawn/wait/interrupt mechanics through their
execution adapters; authority, gates, role boundaries, and outputs are identical.

## Inputs

- Theme slug and its definition + `Coordinator authority` block in `product/factory/themes.md`.
- Live graph state, open Issues, git state, and cycle telemetry derived via `factory-onboard`.
- Human direction, including any standing priorities, spend ceiling, or stop/redirection.

## 1. Reconstruct

Run `factory-onboard`. Reconcile the theme's three surfaces before selecting new work:

- open/in-flight Issues and their human gates;
- cycle phase and method stamp;
- git artifacts and their `Status:` marker;
- graph frontier, promoted-but-unrun proof goals, and untriaged shortlist.

An existing inconsistency or governed backlog is work before a new launch. Do not widen the mouth while
the neck/proving grounds are invisibly stalled.

## 2. Select and scope

Choose the cheapest next question that materially reduces a declared uncertainty. Produce a proposed
run packet:

- protocol and run type;
- exact theme/frontier target and question;
- confidence required and proof bar;
- in/out boundary;
- coverage rule and expected outputs;
- budget, concurrency slot, and autonomous follow-on depth consumed;
- authority classification: `autonomous` or `human-required`, with the rule that decided it.

Inside the declared authority envelope, the coordinator may approve and launch the packet. Otherwise it
presents the packet to the human and waits.

## 3. Launch by delegation

Spawn a fresh `research-leader` with:

- its complete role contract: `.claude/agents/factory/research-leader.md`;
- the applicable canonical protocol path;
- the run packet and artifact paths;
- the requirement to open all three surfaces at INIT;
- explicit gates and return conditions, including immediate surprise escalation;
- the instruction to remain alive until all nested specialist work returns.

The theme coordinator makes no `context_cycle` call, opens no run Issue itself, and performs no run
content. Those actions belong to the leader and specialists after launch.

## 4. Supervise

The leader returns at phase boundaries, human gates, budget/concurrency exceptions, surprises, and CLOSE.
The coordinator checks:

- work remains within the approved question and envelope;
- all three surfaces agree on the phase;
- nested work has actually completed rather than been orphaned;
- no graph write escaped the curator and no proof escaped the firewall;
- new findings have not triggered a surprise duty.

It may order reconciliation, retry a failed mechanical action, or replace a failed leader with the same
approved packet. It may not reinterpret the scope, do specialist work, or answer a human gate.

## 5. Surprise and stop protocol

Classify premise-changing evidence immediately:

- `inform-continue`: report now; reversible continuation remains inside authority.
- `inform-hold`: stop new launches, instruct affected leaders to preserve and park safely, then present
  the decision to the human.

Human STOP overrides every delegated permission. Record what stopped, what completed, which grades did
not move, and the smallest safe resume point. A held run is not a failed run.

## 6. Reconcile and continue

At run close:

1. receive the leader's paths, verdict, gates, graph IDs, telemetry, and retrospective result;
2. translate the outcome into a short plain-English human update;
3. update the theme frontier/config only through the appropriate reviewed method change;
4. decide `park | follow-up | proof | human decision` under the authority matrix;
5. increment autonomous follow-on depth for a chained launch; stop at the configured maximum.

The coordinator may supervise several runs up to `max_concurrent_runs`, but each run has its own leader,
Issue, cycle, directory, budget, and gates.

## Human communication rules

Escalate a decision, not a document dump. State what changed, why it matters, what is active/held, the
real choices, recommendation, cost/risk, and the default if the human does not intervene. Provide evidence
paths as drill-down links.

Mandatory human moments are defined by the role authority boundary and theme config, not by platform UI.

## Output

A continuously reconciled theme frontier; bounded delegated runs; prompt surprise reports; human rulings
on strategic/expensive/irreversible/firewall matters; and a durable stop/resume point for interrupted work.

