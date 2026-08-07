#!/usr/bin/env python3
"""Jurati v0.1 prototype: fail-closed contract validation and deterministic replay."""
from __future__ import annotations
import hashlib, json, re, sys, time
from pathlib import Path

RESULTS = {"demonstrated", "contradicted", "not_demonstrated", "insufficient_evidence"}
VERDICTS = {"pass", "pass_with_advisory", "fail", "not_demonstrated", "insufficient_evidence"}
FORBIDDEN_JUDGE_FIELDS = {"verdict", "action", "target", "authority", "question", "evidence", "contract"}

class ContractError(ValueError): pass

def canonical(value): return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def digest(value): return hashlib.sha256(canonical(value).encode()).hexdigest()

def validate_contract(c):
    required = {"contract_id", "question", "evidence", "clauses", "transitions"}
    missing = required - c.keys()
    if missing: raise ContractError(f"missing fields: {sorted(missing)}")
    if set(c["transitions"]) != VERDICTS: raise ContractError("transitions must be total and exact")
    evidence_ids = [x["id"] for x in c["evidence"]]
    clause_ids = [x["id"] for x in c["clauses"]]
    if len(evidence_ids) != len(set(evidence_ids)) or len(clause_ids) != len(set(clause_ids)):
        raise ContractError("duplicate identity")
    for ev in c["evidence"]:
        if not re.fullmatch(r"[0-9a-f]{64}", ev.get("sha256", "")): raise ContractError("bad evidence digest")
    for cl in c["clauses"]:
        if cl.get("evaluator") not in {"mechanical", "semantic", "human_reserved"}: raise ContractError("bad evaluator")
        if cl.get("criticality") not in {"blocking", "advisory"}: raise ContractError("bad criticality")
        if not set(cl.get("evidence_ids", [])) <= set(evidence_ids): raise ContractError("undeclared evidence")
    for verdict, action in c["transitions"].items():
        if not isinstance(action, dict) or not {"id", "kind", "target", "authority"} <= action.keys():
            raise ContractError(f"malformed transition {verdict}")
        if action["kind"] == "advance" and verdict not in {"pass", "pass_with_advisory"}:
            raise ContractError("non-pass advancement")
    return c

def validate_evidence(c, base):
    for ev in c["evidence"]:
        p = (base / ev["path"]).resolve()
        if base.resolve() not in p.parents: raise ContractError("evidence path escapes base")
        if not p.is_file(): raise ContractError(f"missing evidence {ev['id']}")
        if hashlib.sha256(p.read_bytes()).hexdigest() != ev["sha256"]: raise ContractError(f"tampered evidence {ev['id']}")

def validate_judge_response(clause, response):
    extra = set(response) - {"clause_id", "result", "rationale", "evidence_refs", "policy"}
    if extra & FORBIDDEN_JUDGE_FIELDS or extra: raise ContractError(f"judge widened response: {sorted(extra)}")
    if response.get("clause_id") != clause["id"] or response.get("result") not in RESULTS: raise ContractError("invalid judge result")
    if not set(response.get("evidence_refs", [])) <= set(clause.get("evidence_ids", [])): raise ContractError("judge cited undeclared evidence")
    return response["result"]

def reduce_verdict(c, results):
    if set(results) != {x["id"] for x in c["clauses"]}: raise ContractError("incomplete clause vector")
    blocking = [results[x["id"]] for x in c["clauses"] if x["criticality"] == "blocking"]
    advisory = [results[x["id"]] for x in c["clauses"] if x["criticality"] == "advisory"]
    if "contradicted" in blocking: return "fail"
    if "insufficient_evidence" in blocking: return "insufficient_evidence"
    if "not_demonstrated" in blocking: return "not_demonstrated"
    return "pass" if all(x == "demonstrated" for x in advisory) else "pass_with_advisory"

def replay(contract, results, log_path):
    validate_contract(contract)
    verdict = reduce_verdict(contract, results)
    record = {"seq": sum(1 for _ in open(log_path)) if Path(log_path).exists() else 0,
              "time_ns": time.time_ns(), "contract_hash": digest(contract), "results": results,
              "verdict": verdict, "action": contract["transitions"][verdict]}
    with open(log_path, "a", encoding="utf-8") as out:
        out.write(canonical(record) + "\n")
        out.flush()
    return record

def main():
    if len(sys.argv) != 4: raise SystemExit("usage: jurati.py CONTRACT RESULTS APPEND_LOG")
    c=json.loads(Path(sys.argv[1]).read_text()); r=json.loads(Path(sys.argv[2]).read_text())
    print(canonical(replay(c, r, sys.argv[3])))
if __name__ == "__main__": main()
