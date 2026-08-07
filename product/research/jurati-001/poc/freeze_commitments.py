#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
paths=[BASE/"SCOPE.md",BASE/"SPEC-v0.1-dev.md",BASE/"EXAMPLES-v0.1-dev.md",BASE/"findings-W4.md",
 BASE/"task/FREEZE-CANDIDATE.md",BASE/"task/semantic-prompt-v1.txt",BASE/"task/semantic-policy-v1.json",
 BASE/"poc/jurati.py",BASE/"poc/test_jurati.py",BASE/"poc/verify_freeze.py",BASE/"poc/run_semantic.py",
 BASE/"poc/run_mechanical_arm.py",BASE/"poc/generate_corpus.py",BASE/"poc/import_custody_handoff.py",
 BASE/"poc/capture_environment.py",BASE/"corpus-generated/SHA256SUMS",BASE/"corpus-generated/manifest.jsonl",
 BASE/"corpus-generated/splits.json",BASE/"corpus-generated/restricted-map-commitment.json",
 BASE/"corpus-generated/reference-labels-nonholdout.jsonl",BASE/"artifacts/effective-envelope.json",
 BASE/"corpus-generated/evidence-exclusion-summary.json",BASE/"artifacts/non-inspection-attestations.json",
 BASE/"artifacts/arm-a-summary.json",BASE/"artifacts/RESULTS.md",BASE/"reports/gate-corpus-freeze.md"]
rows={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
record={"schema":"jurati-freeze-commitment-v1","files":rows,"aggregate_sha256":hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(",",":")).encode()).hexdigest()}
(BASE/"artifacts/freeze-commitments.json").write_text(json.dumps(record,sort_keys=True,indent=2)+"\n"); print(json.dumps({"files":len(rows),"aggregate_sha256":record["aggregate_sha256"]},sort_keys=True))
