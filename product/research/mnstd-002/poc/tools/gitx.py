"""Deterministic local git for the PR simulation (C4) and the edit path (C5, N3.2).

* identity, dates and config are fixed: GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_NOSYSTEM=1, fixed author/
  committer and a monotonic synthetic clock (never the wall clock), so every SHA is reproducible.
* GIT_CEILING_DIRECTORIES stops discovery above the run dir, so a command can never reach the outer repo.
* protocol.allow=never + a refusing pre-push hook (guards against accidents only; the evidence for C4.5/N6 is the
  remote inspection plus the command trace — findings-W3 §5).
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from common import die

BASE_EPOCH = 1790812800  # 2026-10-01T00:00:00Z


class Git:
    def __init__(self, repo: Path):
        self.repo = Path(repo)
        self.tick = 0
        self.env = dict(os.environ)
        self.env.update({
            "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CEILING_DIRECTORIES": str(self.repo.parent),
            "GIT_TERMINAL_PROMPT": "0", "LC_ALL": "C", "TZ": "UTC",
        })

    def __call__(self, *args, check=True, who=("Secretariat", "secretariat@example.invalid"), input=None) -> str:
        env = dict(self.env)
        when = f"{BASE_EPOCH + 60 * self.tick} +0000"
        env.update({"GIT_AUTHOR_NAME": who[0], "GIT_AUTHOR_EMAIL": who[1], "GIT_AUTHOR_DATE": when,
                    "GIT_COMMITTER_NAME": who[0], "GIT_COMMITTER_EMAIL": who[1], "GIT_COMMITTER_DATE": when})
        p = subprocess.run(["git", "-C", str(self.repo), *args], text=True, capture_output=True, env=env, input=input)
        if check and p.returncode != 0:
            die(f"git {' '.join(args)} failed ({p.returncode}): {p.stderr.strip()}")
        return p.stdout

    def ok(self, *args) -> bool:
        p = subprocess.run(["git", "-C", str(self.repo), *args], text=True, capture_output=True, env=self.env)
        return p.returncode == 0

    def commit(self, message: str, who=("Secretariat", "secretariat@example.invalid")) -> str:
        self.tick += 1
        self("add", "-A")
        self("-c", "commit.gpgsign=false", "commit", "-q", "-m", message, who=who)
        return self("rev-parse", "HEAD").strip()

    def merge(self, branch: str, message: str) -> str:
        self.tick += 1
        self("-c", "commit.gpgsign=false", "merge", "-q", "--no-ff", "-m", message, branch)
        return self("rev-parse", "HEAD").strip()

    def init(self):
        self.repo.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.repo)], check=True, env=self.env,
                       capture_output=True)
        for k, v in (("protocol.allow", "never"), ("core.autocrlf", "false"), ("commit.gpgsign", "false"),
                     ("user.useConfigOnly", "true")):
            self("config", k, v)
        hook = self.repo / ".git" / "hooks" / "pre-push"
        hook.write_text("#!/bin/sh\necho 'mnstd-002: push is forbidden (N6)' >&2\nexit 1\n")
        hook.chmod(0o755)


def apply_edits(worktree: Path, edits: list[dict], cid: str) -> list[str]:
    """Literal find/replace; each `find` must occur exactly once at apply time (findings-W2 §3 rank 1)."""
    touched = []
    for ed in edits:
        f = Path(worktree) / ed["file"]
        s = f.read_text(encoding="utf-8")
        n = s.count(ed["find"])
        if n != 1:
            die(f"{cid}: edit find occurs {n} times in {ed['file']} (must be exactly 1): {ed['find']!r}")
        f.write_text(s.replace(ed["find"], ed["replace"], 1), encoding="utf-8")
        touched.append(ed["file"])
    return sorted(set(touched))


def apply_edits_text(text: str, edits: list[dict], file: str) -> str | None:
    for ed in edits:
        if ed["file"] != file:
            continue
        if text.count(ed["find"]) != 1:
            return None
        text = text.replace(ed["find"], ed["replace"], 1)
    return text


def trailers(git: Git, rev: str, key: str) -> list[str]:
    out = git("log", "-1", f"--format=%(trailers:key={key},valueonly,separator=%x2C)", rev).strip()
    return [x.strip() for x in out.split(",") if x.strip()]
