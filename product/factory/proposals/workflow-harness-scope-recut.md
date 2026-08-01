# Proposed re-cut: `theme:workflow-harness` — solo developer first, enterprise by seam

**Status:** proposal · **Author:** owner-directed, drafted at the wfh-005 gate, 2026-08-01
**Standing:** **NOT a wfh-005 verdict.** wfh-005 is advisory and forbidden from reshaping its own theme
(the failure that closed wfh-002). This document is the owner's direction, written down so it can be
ruled on — it does not amend `themes.md` and does not settle Option C, the substrate question, or H7.
**Evidence base:** `product/research/wfh-005/reports/triage.md` + `triage-amendment-1.md`.

---

## The object

Not a harness. **A bound** — an authority envelope for an LLM agent — plus the small compiler that emits
it into a plane the agent holds no credential for.

## The user, singular

**A solo developer with no infrastructure to run.** No Kubernetes, no service mesh, no daemon, no
orchestrator. They want their data and their agents bounded, and they will not stand up a control plane
to get it. That user is currently unserved: every shipping instance of real enforcement charges an
infrastructure toll — GitHub Actions, Kubernetes + Istio + eBPF, or a hypervisor.

## The staging rule

**Architect the hard parts for enterprise. Build only the personal OSS tool.** Enterprise lives in its own
repos as a second codebase — not a tier, not a config flag. The move between them must be an extension,
never a rebuild, and what makes that true is getting a small number of **security seams** structurally
right on day one.

### The seams that must be right now

| Seam | Why it is a seam | What OSS must do so enterprise is not a rebuild |
|---|---|---|
| **Principal identity** | Enterprise needs per-tenant, per-agent identity; OSS needs one developer | The envelope names a principal explicitly, never implies "the current user." A uid today, a workload identity later, same field |
| **Credential minting** | The whole guarantee reduces to *who holds the token* | The agent never receives a long-lived credential. Something else mints, scoped and short-lived — a local broker now, a real broker later |
| **Isolation boundary** | This is where multi-tenancy is either possible or impossible | The boundary is named and enforced by the kernel, not by the harness's own code. Second uid now; namespace, pod or tenant later |
| **Attestation / audit record** | Enterprise audit is not a bigger log, it is a different trust root | Every bound decision and refusal is recorded with its inputs and its authority. External trust root from the start — the run's evidence includes a live counter-example where the verifying key sits inside the signed document |
| **The plane interface** | The one thing that must be pluggable | The compiler emits *through* an interface. Adding an enforcement plane is a new emitter, not a change to the envelope |

## What we build

**Two things, and they are what survived four surfaces of attack.**

1. **Bounds derived from demand observed during execution.** Every shipping system derives authority from a
   declaration written before the run — a manifest, a CRD, an objective string, frontmatter. An agent's
   demand set is discovered while it works. Derive from observation instead. The nearest prior art
   (AWS IAM Access Analyzer, `audit2rbac`) does this for programs, never for agents.
2. **Monotone, with approval to widen.** Narrow freely and unilaterally; widen only through an approval
   whose issuer is not the principal. Both halves ship separately in the wild; nothing composes them.

**Plus the small piece that makes it honest:** a **per-tier guarantee statement**. The developer must be
told what their configuration actually enforces and what degrades to advice. Shipping a bound without that
label is the "instrumented tendency wearing a guarantee" failure this run kept finding.

## What we rebuild rather than adopt

`@claude-flow/security`'s envelope algebra is genuinely good and genuinely small underneath — subset checks
on a handful of lists, `≤` on a handful of numbers, a delegation-depth decrement, one thrown error. The
adoption surface around it is not: 106 registered environment escape hatches, a 540MB repo, a release train
moving several times a day, bus factor 1, and a policy engine that is **inert by default**. The parts
nearest our two build legs are stubs by their own admission — the delegation propagator's header says it
has no call sites.

**Read it, then build it small.** This is the Unimatrix-over-`agentdb` move, and it is the right one here.

## What we emit into, and never build

The enforcement planes. These are not library-sized and rebuilding any of them is footprint, not economy.

- **Solo tier, today:** a second uid (kernel-enforced, free, already installed) · the harness's own
  pre-tool hook, evaluated by a process the agent does not control · a local egress proxy as the next rung.
- **Enterprise tier, later, in the second codebase:** Envoy sidecar + eBPF (Cisco's CASA, Apache-2.0), or
  a CI platform's derived job identity.

**The solo tier is the one we build against.** One real target keeps the compiler honest; two hypothetical
ones do not.

## Scope boundary

This serves **protocol-authored, repeated work** — the regime where a derived bound amortizes, evidenced
by 354 executions against 31 protocol revisions in `dug-21/unimatrix`. It does not serve interactive,
progressively-refined sessions. State that in the lens rather than discovering it later.

## Dropped

The novelty claim (prior art on all three legs) · the workflow canvas · harness-as-runtime · count-based
inference minimality · rebuilding an enforcement plane of any kind.

## Open, and not settled here

- **The unclaimed asset.** The loudest measured failure in the field is agents reporting success they did
  not achieve. No capability bound touches it; artifact-backed proof does. This operation already runs that
  as its firewall and it appears nowhere in the eight concerns.
- **Tension with premise H8, flagged not resolved.** `themes.md` currently states JURATI is built
  "multi-tenant SaaS from the start (not a single-user tool retrofitted later)," and makes multi-tenancy
  the trigger that pulls the Anchor-B verifier forward to foundational-now. **OSS-first-with-seams is not
  the same claim.** Whether H8 is revised, scoped to the second codebase, or held as written is an owner
  decision, and this proposal does not make it.
