# Cycle-level split freeze candidate

Splits were assigned before language or prompt work. All episodes from a cycle inherit its partition.

| Domain | Development (50%) | Calibration (25%) | Sealed holdout (25%) |
|---|---|---|---|
| SDLC (16 cycles) | `vnc-047`, `col-023`, `crt-025`, `bugfix-444`, `vnc-044`, `col-024`, `crt-030`, `bugfix-458` | `vnc-046`, `col-022`, `bugfix-381`, `crt-029` | `vnc-045`, `col-020`, `crt-018`, `bugfix-230` |
| Garage (8 cycles) | `shd-007`, `wfh-002`, `wfh-005`, `smart-edge-002` | `shd-005`, `wfh-004` | `wfh-001`, `shd-004` |

The allocation is exactly 8/4/4 SDLC cycles and 4/2/2 garage cycles. `vnc-045` contributes three holdout
episodes, the maximum allowed per cycle; every other selected cycle contributes one or two.

## Hash policy

No final split hash is asserted while AR items remain open. At approval,
canonical JSON uses UTF-8, LF, sorted object keys, and episode rows sorted by `episode_id`; `sha256sum`
produces separate hashes for manifest, labels, packets, and split assignment. Any change motivated by a
holdout failure creates a new language version and untouched holdout; the old hashes remain immutable.
