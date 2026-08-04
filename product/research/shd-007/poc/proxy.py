#!/usr/bin/env python3
"""Transparent logging proxy in front of Ollama, to capture exactly what a
harness puts on the wire. Records request + response bodies per call."""
import http.server, json, pathlib, socketserver, sys, urllib.request, urllib.error

UPSTREAM = "http://100.122.119.72:11434"
LOG = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "proxy.jsonl")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8899
n = 0


class H(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _do(self, method):
        global n
        n += 1
        ln = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(ln) if ln else b""
        rec = {"i": n, "method": method, "path": self.path,
               "req_headers": {k: v for k, v in self.headers.items()
                               if k.lower() not in ("authorization", "x-api-key")}}
        try:
            rec["req"] = json.loads(body)
        except Exception:
            rec["req_raw"] = body[:2000].decode("utf-8", "replace")

        req = urllib.request.Request(UPSTREAM + self.path, data=body or None, method=method)
        for k, v in self.headers.items():
            if k.lower() not in ("host", "content-length", "accept-encoding"):
                req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=1200) as r:
                out, status = r.read(), r.status
                hdrs = dict(r.headers)
        except urllib.error.HTTPError as e:
            out, status, hdrs = e.read(), e.code, dict(e.headers)
        except Exception as e:
            rec["upstream_error"] = repr(e)
            with LOG.open("a") as f:
                f.write(json.dumps(rec) + "\n")
            self.send_response(502); self.end_headers(); return

        rec["status"] = status
        try:
            rec["resp"] = json.loads(out)
        except Exception:
            rec["resp_raw"] = out[:6000].decode("utf-8", "replace")
        with LOG.open("a") as f:
            f.write(json.dumps(rec) + "\n")

        self.send_response(status)
        for k, v in hdrs.items():
            if k.lower() in ("content-type",):
                self.send_header(k, v)
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def do_POST(self): self._do("POST")
    def do_GET(self): self._do("GET")
    def log_message(self, *a): pass


class S(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


print(f"proxy on :{PORT} -> {UPSTREAM}, logging {LOG}", flush=True)
S(("127.0.0.1", PORT), H).serve_forever()
