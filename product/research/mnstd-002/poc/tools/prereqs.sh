#!/usr/bin/env bash
# N1.3: fail fast, naming the missing prerequisite. Exit 2 on the first missing one.
# Declared host prerequisites: docker (daemon reachable), the pinned image present locally, python3 >= 3.14,
# git >= 2.32 (ruling R3: declared prerequisite), and the provisioned font cache (`make fonts`, ruling R1).
# Node 24 is allowed by N1.1/N2.3 but NOT used by this rig. Ruby must NOT be needed (N2.2).
# Authored by factory-poc (mnstd-002).
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
. "$HERE/tools/env.sh"
fail() { echo "PREREQUISITE MISSING: $1" >&2; exit 2; }
command -v docker >/dev/null 2>&1 || fail "docker (Docker CLI not on PATH)"
docker info >/dev/null 2>&1 || fail "docker daemon (not reachable: docker info failed)"
docker image inspect "$MN_IMAGE" >/dev/null 2>&1 || fail "container image $MN_IMAGE (pull it once: docker pull $MN_IMAGE)"
command -v python3 >/dev/null 2>&1 || fail "python3 (Python 3.14 required)"
python3 -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3, 14) else 1)' || fail "python3 >= 3.14 (found $(python3 --version 2>&1))"
command -v git >/dev/null 2>&1 || fail "git (host git >= 2.32 required, ruling R3)"
gv="$(git --version | awk '{print $3}')"
python3 -c "import sys; v=tuple(int(x) for x in '$gv'.split('.')[:2]); sys.exit(0 if v >= (2, 32) else 1)" || fail "git >= 2.32 (found $gv)"
[ -f "$FONT_CACHE/.provisioned" ] || fail "font cache at $FONT_CACHE (run the one-time networked step: make fonts)"
echo "prereqs: ok (docker, image by digest, python3 $(python3 -c 'import platform;print(platform.python_version())'), git $gv, fonts at $FONT_CACHE)"
