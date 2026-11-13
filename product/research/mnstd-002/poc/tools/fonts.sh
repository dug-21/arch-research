#!/usr/bin/env bash
# One-time, NETWORKED font provisioning (SCOPE Extension ruling R1).
# This is NOT part of the gated `make demo`. It populates a host-side cache OUTSIDE the repo;
# the gated demo then mounts that cache and runs every compile with --network none.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
. "$HERE/tools/env.sh"
command -v docker >/dev/null || { echo "fonts: prerequisite missing: docker" >&2; exit 2; }
docker image inspect "$MN_IMAGE" >/dev/null 2>&1 || { echo "fonts: prerequisite missing: image $MN_IMAGE (run: docker pull $MN_IMAGE)" >&2; exit 2; }
mkdir -p "$FONT_CACHE/fontist" "$FONT_CACHE/metanorma" "$FONT_CACHE/warm"
cp "$HERE/fonts/warm.adoc" "$FONT_CACHE/warm/warm.adoc"
echo "fonts: provisioning into $FONT_CACHE (network ON for this step only)"
docker run --rm \
  -v "$FONT_CACHE/fontist":/config -v "$FONT_CACHE/metanorma":/root/.metanorma \
  -v "$FONT_CACHE/warm":/metanorma -w /metanorma "$MN_IMAGE" \
  sh -c 'metanorma compile -t iso --agree-to-terms warm.adoc; rc=$?; chown -R '"$(id -u):$(id -g)"' /metanorma /config /root/.metanorma; exit $rc'
test -s "$FONT_CACHE/warm/warm.pdf" || { echo "fonts: FAILED - warm.pdf not produced" >&2; exit 1; }
touch "$FONT_CACHE/.provisioned"
du -sh "$FONT_CACHE"
