#!/usr/bin/env python3
"""shd-007 W3/W4 -- a minimal agentic loop over BOTH serving protocols.

Deliberately minimal and route-symmetric: the same task, tools and step budget
run over Ollama's OpenAI-compatible /v1/chat/completions and its native
Anthropic /v1/messages. Anything that differs between the two runs is a
property of the protocol contract, not of the model or the task.

Finding #16 predicts the contract breaks here. The point is to record WHERE --
so every step is journalled with its raw response and a typed failure, not a
bare pass/fail.
"""
import argparse, json, pathlib, shutil, subprocess, sys, time, urllib.error, urllib.request

HOST = "http://100.122.119.72:11434"
FIXTURE = pathlib.Path("/workspaces/arch-research/product/research/shd-007/task/fixture")
VERIFY = pathlib.Path("/workspaces/arch-research/product/research/shd-007/task/verify.sh")

TASK = """The test suite in tests/ is the specification and is CORRECT. It currently fails.
Fix the code under roster/ until `python -m pytest` passes.

Rules:
- Do NOT edit anything under tests/.
- The docstrings in roster/ describe the intended behaviour. Where the code and its
  own docstring disagree, the docstring is right.
- Work by reading files, editing them, and re-running the tests until they pass.
- When all tests pass, say DONE and stop.
"""

TOOLS = [
    {"name": "list_files", "description": "List all source files in the project.",
     "schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "read_file", "description": "Read a file's full contents.",
     "schema": {"type": "object",
                "properties": {"path": {"type": "string", "description": "Path relative to project root, e.g. roster/parser.py"}},
                "required": ["path"]}},
    {"name": "write_file", "description": "Overwrite a file with new contents. Provide the COMPLETE file.",
     "schema": {"type": "object",
                "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                "required": ["path", "content"]}},
    {"name": "run_tests", "description": "Run the pytest suite and return its output.",
     "schema": {"type": "object", "properties": {}, "required": []}},
]


# ---------- tool execution ----------
def execute(work: pathlib.Path, name: str, args: dict) -> str:
    if name == "list_files":
        return "\n".join(sorted(
            str(p.relative_to(work)) for p in work.rglob("*.py")
            if "__pycache__" not in str(p)))
    if name == "read_file":
        p = (work / args["path"]).resolve()
        if not str(p).startswith(str(work.resolve())):
            return "ERROR: path escapes project root"
        if not p.exists():
            return f"ERROR: no such file: {args['path']}"
        return p.read_text()
    if name == "write_file":
        rel = args["path"]
        p = (work / rel).resolve()
        if not str(p).startswith(str(work.resolve())):
            return "ERROR: path escapes project root"
        if rel.startswith("tests/") or "/tests/" in rel:
            return "ERROR: editing tests/ is forbidden by the task"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(args["content"])
        return f"wrote {rel} ({len(args['content'])} bytes)"
    if name == "run_tests":
        r = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=work,
                           capture_output=True, text=True, timeout=120)
        return (r.stdout + r.stderr)[-3000:]
    return f"ERROR: unknown tool {name}"


# ---------- route adapters ----------
def post(path, payload, timeout=1200):
    req = urllib.request.Request(HOST + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


class OpenAIRoute:
    name = "openai:/v1/chat/completions"

    def init(self):
        return [{"role": "system", "content": "You are a coding agent. Use the provided tools."},
                {"role": "user", "content": TASK}]

    def request(self, msgs, model):
        return post("/v1/chat/completions", {
            "model": model, "messages": msgs, "temperature": 0,
            "tools": [{"type": "function",
                       "function": {"name": t["name"], "description": t["description"],
                                    "parameters": t["schema"]}} for t in TOOLS]})

    def parse(self, resp):
        """-> (assistant_msg, [(id,name,args_or_None,raw_args)], text, finish)"""
        m = resp["choices"][0]["message"]
        calls = []
        for tc in (m.get("tool_calls") or []):
            raw = tc["function"].get("arguments", "")
            try:
                args = json.loads(raw) if isinstance(raw, str) else raw
            except Exception:
                args = None
            calls.append((tc.get("id") or f"call_{len(calls)}", tc["function"]["name"], args, raw))
        return m, calls, m.get("content") or "", resp["choices"][0].get("finish_reason")

    def append_results(self, msgs, assistant_msg, results):
        msgs.append(assistant_msg)
        for cid, out in results:
            msgs.append({"role": "tool", "tool_call_id": cid, "content": out})


class AnthropicRoute:
    name = "anthropic:/v1/messages"

    def init(self):
        return [{"role": "user", "content": TASK}]

    def request(self, msgs, model):
        return post("/v1/messages", {
            "model": model, "max_tokens": 2048, "temperature": 0,
            "system": "You are a coding agent. Use the provided tools.",
            "messages": msgs,
            "tools": [{"name": t["name"], "description": t["description"],
                       "input_schema": t["schema"]} for t in TOOLS]})

    def parse(self, resp):
        calls, text = [], ""
        for b in resp.get("content", []):
            if b.get("type") == "text":
                text += b.get("text", "")
            elif b.get("type") == "tool_use":
                calls.append((b["id"], b["name"], b.get("input"), json.dumps(b.get("input"))))
        return {"role": "assistant", "content": resp.get("content", [])}, calls, text, resp.get("stop_reason")

    def append_results(self, msgs, assistant_msg, results):
        msgs.append(assistant_msg)
        msgs.append({"role": "user",
                     "content": [{"type": "tool_result", "tool_use_id": cid, "content": out}
                                 for cid, out in results]})


# ---------- the loop ----------
def run(route, model, work, max_steps, journal_path):
    msgs = route.init()
    journal, taxonomy = [], []
    t_start = time.perf_counter()
    calls_made = 0
    for step in range(1, max_steps + 1):
        rec = {"step": step, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        try:
            t0 = time.perf_counter()
            resp = route.request(msgs, model)
            rec["latency_s"] = round(time.perf_counter() - t0, 2)
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:800]
            rec.update(failure="http_error", http_status=e.code, body=body)
            journal.append(rec); taxonomy.append(f"http_error:{e.code}"); break
        except Exception as e:
            rec.update(failure="transport_error", error=repr(e))
            journal.append(rec); taxonomy.append("transport_error"); break

        try:
            amsg, calls, text, finish = route.parse(resp)
        except Exception as e:
            rec.update(failure="unparseable_response", error=repr(e), raw=str(resp)[:1500])
            journal.append(rec); taxonomy.append("unparseable_response"); break

        rec.update(finish_reason=finish, text=text[:400],
                   usage=resp.get("usage") or resp.get("usage", {}),
                   n_tool_calls=len(calls))

        if not calls:
            rec["failure"] = None if "DONE" in text.upper() else "no_tool_call"
            if "DONE" not in text.upper():
                taxonomy.append("no_tool_call")
            journal.append(rec)
            if "DONE" in text.upper():
                break
            # nudge once, then give up
            msgs.append(amsg if isinstance(amsg, dict) else {"role": "assistant", "content": text})
            msgs.append({"role": "user", "content": "Continue using the tools until pytest passes."})
            continue

        results, step_calls = [], []
        for cid, name, args, raw in calls:
            calls_made += 1
            if args is None:
                taxonomy.append("malformed_tool_args")
                step_calls.append({"name": name, "ok": False, "why": "malformed_json_args",
                                   "raw_args": raw[:400]})
                results.append((cid, "ERROR: your tool arguments were not valid JSON. Retry."))
                continue
            if name not in {t["name"] for t in TOOLS}:
                taxonomy.append("unknown_tool")
                step_calls.append({"name": name, "ok": False, "why": "unknown_tool"})
                results.append((cid, f"ERROR: unknown tool {name}"))
                continue
            try:
                out = execute(work, name, args)
                ok, why = True, None
            except Exception as e:
                out, ok, why = f"ERROR: {e!r}", False, "tool_raised"
                taxonomy.append("tool_raised")
            step_calls.append({"name": name, "ok": ok, "why": why,
                               "args": {k: (v[:120] if isinstance(v, str) else v)
                                        for k, v in (args or {}).items()},
                               "result_head": out[:200]})
            results.append((cid, out))

        rec["calls"] = step_calls
        journal.append(rec)
        route.append_results(msgs, amsg, results)
        pathlib.Path(journal_path).write_text(json.dumps(journal, indent=2))

        if any(c["name"] == "run_tests" and c["ok"] for c in step_calls) and \
           any("8 passed" in (c.get("result_head") or "") for c in step_calls):
            break

    wall = round(time.perf_counter() - t_start, 1)
    pathlib.Path(journal_path).write_text(json.dumps(journal, indent=2))
    return {"route": route.name, "model": model, "steps": len(journal),
            "tool_calls": calls_made, "wall_s": wall,
            "taxonomy": sorted(set(taxonomy)), "taxonomy_counts":
            {t: taxonomy.count(t) for t in sorted(set(taxonomy))}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--route", choices=["openai", "anthropic"], required=True)
    ap.add_argument("--model", default="qwen3-coder:30b")
    ap.add_argument("--max-steps", type=int, default=30)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--journal", required=True)
    a = ap.parse_args()

    work = pathlib.Path(a.workdir)
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(FIXTURE, work)

    route = OpenAIRoute() if a.route == "openai" else AnthropicRoute()
    summary = run(route, a.model, work, a.max_steps, a.journal)

    v = subprocess.run(["bash", str(VERIFY), str(work)], capture_output=True, text=True)
    summary["verify_exit"] = v.returncode
    summary["verify_out"] = (v.stdout + v.stderr).strip()[-600:]
    summary["passed"] = v.returncode == 0
    d = subprocess.run(["git", "diff", "--no-index", "--stat", str(FIXTURE), str(work)],
                       capture_output=True, text=True)
    summary["diffstat"] = d.stdout.strip()[-900:]
    print(json.dumps(summary, indent=2))
    pathlib.Path(a.journal.replace(".json", "-summary.json")).write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
