# mnstd-002 POC — ISO-style Metanorma authoring + commenting/review, end to end.
# Authored by factory-poc. Host prerequisites: Docker (+ the pinned image), Python 3.14, git >= 2.32.
#
#   make fonts   one-time, NETWORKED font provisioning into $(FONT_CACHE) (ruling R1; outside the repo)
#   make demo    the gated, network-free demo: two full runs from clean + self-tests + cross-run checks
#   make once    a single pipeline run into build/run-a (no cross-run checks)
#   make clean   remove build/ (never touches the font cache or ../artifacts)

SHELL := /bin/bash
POC := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
FONT_CACHE ?= $(or $(MNSTD_FONT_CACHE),$(HOME)/.cache/mnstd-002-fonts)
export MNSTD_FONT_CACHE := $(FONT_CACHE)
# Every docker/git call the rig makes is traced (N6, C4.5); curl/wget/gh/commenter are refused.
export PATH := $(POC)/bin:$(PATH)
BUILD := $(POC)/build
ARTIFACTS := $(abspath $(POC)/../artifacts)

.PHONY: demo once fonts prereqs clean freeze

prereqs:
	@bash $(POC)/tools/prereqs.sh

fonts:
	@bash $(POC)/tools/fonts.sh

demo: prereqs clean
	python3 $(POC)/tools/demo.py $(BUILD) $(ARTIFACTS)

once: prereqs clean
	mkdir -p $(BUILD)/run-a && : > $(BUILD)/run-a/command-trace.log
	MNSTD_TRACE=$(BUILD)/run-a/command-trace.log python3 $(POC)/tools/pipeline.py $(BUILD)/run-a

# Re-freeze the task (fixtures + expectations + v1 source). Only before a first gated run; commit the result.
freeze:
	python3 $(POC)/tools/frozen.py write

clean:
	rm -rf $(BUILD)
