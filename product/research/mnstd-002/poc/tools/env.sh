# Shared configuration (sourced by shell entry points).
# The image is pinned BY DIGEST (N2.1). Never reference it by tag.
MN_IMAGE="metanorma/metanorma@sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da"
# Font cache lives OUTSIDE the repo by default (ruling R1); never committed.
FONT_CACHE="${MNSTD_FONT_CACHE:-$HOME/.cache/mnstd-002-fonts}"
export MN_IMAGE FONT_CACHE
