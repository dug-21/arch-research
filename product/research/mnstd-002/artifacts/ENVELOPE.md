# mnstd-002 POC — effective envelope (configuration in force)

Captured by `factory-poc` at the start of every pipeline run (`tools/envelope.py` → `evidence/envelope.json`);
never inherited from an earlier reading. Values below are from invocation 2, run A (2026-11-13T18:10:23Z).
Invocation 1 (2026-11-13T17:59:58Z) captured the same values (`invocations/demo-1.json`).

## Measured by us

| Item | Value | How |
|---|---|---|
| Host arch | `x86_64` | `platform.machine()` |
| Host OS / kernel | Ubuntu 24.04.4 LTS (devcontainer) / `6.12.100+deb13-amd64` | `/etc/os-release`, `uname -r` |
| Docker | client 29.7.2-2 / server 29.7.2-2 (linux/amd64) | `docker version` |
| Image reference used by every container run | `metanorma/metanorma@sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da` | `tools/common.py`, `tools/env.sh`; every `docker run` line in `evidence/command-trace.log` |
| Image present locally, digest match | yes: RepoDigests `[metanorma/metanorma@sha256:836b7ab2…dff3da]`, Id `sha256:836b7ab2…dff3da`, Created `2026-11-13T02:30:54Z`, amd64 | `docker image inspect` |
| `metanorma --version` (inside the image, `--network none`) | Metanorma 2.5.24 · Metanorma::Cli 1.18.6 · Standoc 3.5.20 / IsoDoc 3.7.14 · Metanorma::Iso 3.5.14 · mn2pdf 2.74 · fontist 3.0.37 · canon 0.3.125 · metanorma-utils 2.0.12 | `evidence/envelope.json` (full list there) |
| Asciidoctor (in-image, used by `srcmap.rb`) | 2.0.26 per findings-W0 probe; **not re-captured by the rig** | attested from W0 |
| Host Python | 3.14.7 (stdlib only) | `sys.version` |
| Host Node | v24.20.0 (present, **not used**) | `node --version` |
| Host git | 2.55.0 | `git --version` |
| Host Ruby / gem | absent: `which ruby` exit 1, `which gem` exit 1 | `sh -c 'which ruby'` |
| Font cache | `/home/vscode/.cache/mnstd-002-fonts` · 873,405,539 bytes · 4,539 files · `.provisioned` marker present | walk of the directory at run start |
| Network for gated runs | every `docker run` carries `--network none` (12 per pipeline run); no git network verb, no curl/wget/gh/commenter, no docker pull/build in the trace (211 traced commands, invocation 2 run A) | `evidence/command-trace.log`, `checks.trace_scan` |
| Applied compile flags | `metanorma compile -t iso --agree-to-terms --no-install-fonts -x xml,html,pdf,rxl draft.adoc`, run as root in the container then `chown` to the host uid; `SOURCE_DATE_EPOCH=1794528000` | `tools/common.py::mn_compile`; `v1/compile.log` |
| Inner git config | `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `protocol.allow=never`, refusing pre-push hook, fixed author/committer, synthetic clock from 2026-10-01T00:00:00Z | `tools/gitx.py`; `evidence/repo-git-log.txt` |

## Attested, not measured

- The image's build provenance and contents beyond what `metanorma --version` and `docker image inspect` report
  (Docker Hub / Ribose). Every behavioural number in `RESULT.md` is conditional on this digest.
- Host hardware (CPU, RAM, disk): not captured. Nothing here is a performance claim; no timing is gated.
- Font *licensing/provenance* of the ~873 MB downloaded by `make fonts` (fontist formulas + Noto from GitHub):
  not inspected.

## Not measured

- Cross-day determinism (all four gated runs were on 2026-11-13, within ~25 minutes).
- A fresh clone on a second machine (N1.1 was exercised in this worktree only).
- Network isolation of the *host-side* Python steps at the syscall level: the evidence is the command trace
  (PATH-resolved docker/git, refusing shims for curl/wget/gh/commenter) plus a source check that no tool imports a
  network module; no strace / network namespace was used.

## Out-of-demo networked steps (ruling R1 — the validator rules N6.1 on its literal text)

1. `docker pull` of the pinned digest — **not performed by factory-poc**: the image was already present
   (pulled by the leader before this run).
2. `make fonts` — performed once by factory-poc on 2026-11-13 (networked compile of `poc/fonts/warm.adoc`).
   **Durable side effect: 873,405,539 bytes (≈833 MiB, 4,539 files) at `/home/vscode/.cache/mnstd-002-fonts`,
   outside the repo, never committed.** Gated compiles mount it read-write; its size and file count were identical at the start of run A and
   run B of invocation 2 (873,405,539 bytes / 4,539 files), i.e. no growth was observed.

## Other durable side effects on the host

- `product/research/mnstd-002/poc/build/` (gitignored, ≈7.8 MB) holds the last `make demo` (run-a, run-b);
  `make clean` removes it. No containers left (`--rm`), no images added, no network remotes created anywhere.
