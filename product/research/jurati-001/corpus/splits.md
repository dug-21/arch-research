# Cycle-level split freeze candidate v0.2

Splits were assigned before language or prompt work. All episodes from a cycle inherit its partition.

| Domain | Development (50%) | Calibration (25%) | Sealed holdout (25%) |
|---|---|---|---|
| SDLC (16 cycles) | `vnc-047`, `col-023`, `crt-025`, `bugfix-444`, `vnc-044`, `col-024`, `crt-030`, `bugfix-458` | `vnc-046`, `col-022`, `bugfix-381`, `crt-029` | `A-HC01`–`A-HC04` (opaque) |
| Garage (8 cycles) | `shd-007`, `wfh-002`, `wfh-005`, `smart-edge-002` | `shd-005`, `wfh-004` | `B-HC01`–`B-HC02` (opaque) |

The allocation is exactly 8/4/4 SDLC cycles and 4/2/2 garage cycles. The sealed mapping must prove that one
SDLC holdout cycle contributes three episodes and every other selected cycle contributes one or two. Main
does not contain the identity mapping.

## Hash policy

No final split hash is asserted before the sealed mapping exists and its invariants are mechanically checked. At approval,
canonical JSON uses UTF-8, LF, sorted object keys, and episode rows sorted by `episode_id`; `sha256sum`
produces separate hashes for manifest, labels, packets, and split assignment. Any change motivated by a
holdout failure creates a new language version and untouched holdout; the old hashes remain immutable.

The sealed mapping must include opaque cycle ID, repository SHA, real cycle identity, ordered opaque bundle
IDs, and partition. Its verifier rejects cross-partition identities, duplicate real cycles, more than three
episodes per cycle, wrong ratios, or any clear-text holdout identity/path in a main-visible output.
