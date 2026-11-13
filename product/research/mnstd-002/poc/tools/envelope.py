"""Capture the EFFECTIVE envelope at run start (never inherited from a prior reading).
Measured here: host arch/OS, tool versions, image digest actually present, `metanorma --version` inside the pinned
image, font cache size/location, `which ruby`. Attested (not measurable by us): host hardware, Docker Hub's
build provenance of the image. Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import FONT_CACHE, MN_IMAGE, dump_json  # noqa: E402


def sh(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return {"cmd": " ".join(cmd), "exit": p.returncode, "out": (p.stdout + p.stderr).strip()}
    except FileNotFoundError as e:
        return {"cmd": " ".join(cmd), "exit": 127, "out": str(e)}


def du(path: Path):
    total = files = 0
    for root, _, fs in os.walk(path):
        for f in fs:
            try:
                total += os.lstat(os.path.join(root, f)).st_size
                files += 1
            except OSError:
                pass
    return total, files


def capture() -> dict:
    insp = sh(["docker", "image", "inspect", MN_IMAGE, "--format", "{{json .RepoDigests}} {{.Id}} {{.Created}} {{.Architecture}}"])
    digest = MN_IMAGE.split("@")[1]
    size, nfiles = du(FONT_CACHE)
    osr = {}
    if Path("/etc/os-release").exists():
        for l in Path("/etc/os-release").read_text().split("\n"):
            if "=" in l:
                k, v = l.split("=", 1)
                osr[k] = v.strip('"')
    return {
        "captured_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": {"arch": platform.machine(), "kernel": platform.release(), "os": osr.get("PRETTY_NAME", "")},
        "python": sys.version.split()[0],
        "node": sh(["node", "--version"])["out"],
        "git": sh(["git", "--version"])["out"],
        "docker": sh(["docker", "version", "--format", "client {{.Client.Version}} / server {{.Server.Version}} ({{.Server.Os}}/{{.Server.Arch}})"])["out"],
        "which_ruby": sh(["sh", "-c", "which ruby"]),
        "which_gem": sh(["sh", "-c", "which gem"]),
        "image_ref": MN_IMAGE,
        "image_inspect": insp["out"],
        "image_digest_ok": insp["exit"] == 0 and digest in insp["out"],
        "metanorma_version": sh(["docker", "run", "--rm", "--network", "none", MN_IMAGE, "metanorma", "--version"])["out"],
        "font_cache": {"path": str(FONT_CACHE), "bytes": size, "files": nfiles,
                       "provisioned_marker": (FONT_CACHE / ".provisioned").exists()},
    }


if __name__ == "__main__":
    e = capture()
    dump_json(e, Path(sys.argv[1]))
    print(json.dumps(e, indent=2))
