#!/usr/bin/env bash
# One-time, NETWORKED font provisioning (SCOPE Extension ruling R1).
# This is NOT part of the gated `make demo`. It populates a host-side cache OUTSIDE the repo;
# the gated demo then mounts that cache and runs every compile with --network none.
# Rework 1 (owner ruling 1): the provisioned set is PINNED by poc/fonts/MANIFEST.json (sha256 + size + font version
# per file, fontist formulas commit). A populated cache is not re-provisioned (set MNSTD_FONTS_REPROVISION=1 to
# force); the manifest is then verified and any mismatch FAILS. With no manifest yet, it is written (first pin).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
. "$HERE/tools/env.sh"
pin() {
  if [ -f "$HERE/fonts/MANIFEST.json" ] && [ "${MNSTD_FONTS_REPIN:-0}" != 1 ]; then
    python3 "$HERE/tools/fontpin.py" verify --cache "$FONT_CACHE" || { echo "fonts: FAILED - provisioned fonts do not match poc/fonts/MANIFEST.json" >&2; exit 1; }
  else
    python3 "$HERE/tools/fontpin.py" write --cache "$FONT_CACHE"
  fi
}
if [ -f "$FONT_CACHE/.provisioned" ] && [ "${MNSTD_FONTS_REPROVISION:-0}" != 1 ]; then
  echo "fonts: cache already provisioned at $FONT_CACHE (no network); verifying pin"
  pin
  exit 0
fi
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
pin
