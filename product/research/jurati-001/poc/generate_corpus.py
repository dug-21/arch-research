#!/usr/bin/env python3
"""Generate the integrity-addressed jurati-001 corpus without printing sealed identities."""
from __future__ import annotations
import hashlib, json, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
SCOPE=ROOT/"product/research/jurati-001"
OUT=SCOPE/"corpus-generated"
PIN={"sdlc":"7ac778dfe3aa352d475dddc7897384191419ddf8","garage":"5d4ccdd92cac1ee0b13fd3c7aaa207e9720059de"}

def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*a): return subprocess.check_output(["git","-C",str(ROOT),*a], text=True)
def parse(text):
    rows=[]
    for line in text.splitlines():
        cells=[x.strip().strip("`") for x in line.strip().strip("|").split("|")]
        if len(cells) in {8,9} and re.fullmatch(r"[AB]-[DCH]\d\d",cells[0]) and cells[1] in {"development","calibration","holdout"}:
            if len(cells)==8: cells.insert(7,"prescribed")
            rows.append(dict(zip(["episode_id","partition","cycle","decision_point","primary","reference_class","next_action","provenance","state"],cells)))
    return rows
def source_bytes(domain,path,sdlc_root):
    if domain=="sdlc": return (sdlc_root/path).read_bytes()
    return subprocess.check_output(["git","-C",str(ROOT),"show",f"{PIN['garage']}:{path}"])
def main():
    if len(sys.argv)!=2: raise SystemExit("usage: generate_corpus.py /pinned/unimatrix")
    sdlc=Path(sys.argv[1]); visible=parse((SCOPE/"corpus/manifest.md").read_text())
    OUT.mkdir(exist_ok=True); (OUT/"packets").mkdir(exist_ok=True)
    manifest=[]; public_labels=[]
    for row in visible:
        domain="sdlc" if row["episode_id"].startswith("A-") else "garage"
        if row["partition"]=="holdout":
            packet={"episode_id":row["episode_id"],"domain":domain,"partition":"holdout","custody_import_required":True}
        else:
            primary=row["primary"].strip("`")
            if not primary.startswith("product/"): raise SystemExit(f"unresolved primary for {row['episode_id']}")
            body=source_bytes(domain,primary,sdlc); file_sha=sha(body)
            packet={"episode_id":row["episode_id"],"domain":domain,"partition":row["partition"],"decision_point":row["decision_point"],
                    "repository_sha":PIN[domain],"evidence":[{"id":"primary","media_type":"text/markdown","sha256":file_sha}],
                    "judge_facing":{"question":row["decision_point"],"evidence":[{"id":"primary","sha256":file_sha}],"reference_withheld":True}}
        packet_bytes=(canon(packet)+"\n").encode(); (OUT/"packets"/f"{row['episode_id']}.json").write_bytes(packet_bytes)
        manifest.append({"episode_id":row["episode_id"],"domain":domain,"partition":row["partition"],"cycle":row["cycle"],"packet_sha256":sha(packet_bytes),"repository_sha":PIN[domain]})
        if row["partition"]!="holdout": public_labels.append({"episode_id":row["episode_id"],"reference_class":row["reference_class"],"next_action":row["next_action"],"provenance":row["provenance"],"state":row["state"]})
    (OUT/"manifest.jsonl").write_text("".join(canon(x)+"\n" for x in manifest))
    (OUT/"reference-labels-nonholdout.jsonl").write_text("".join(canon(x)+"\n" for x in public_labels))
    splits={p:sorted(x["episode_id"] for x in manifest if x["partition"]==p) for p in ["development","calibration","holdout"]}
    (OUT/"splits.json").write_text(canon(splits)+"\n")
    files=sorted(p for p in OUT.rglob("*") if p.is_file() and p.name!="SHA256SUMS")
    (OUT/"SHA256SUMS").write_text("".join(f"{sha(p.read_bytes())}  {p.relative_to(OUT)}\n" for p in files))
    print(canon({"episodes":len(manifest),"holdout_placeholders":sum(x["partition"]=="holdout" for x in manifest),"next":"run import_custody_handoff.py"}))
if __name__=="__main__": main()
