"""Cross-build function equivalence matcher.

Usage:
    python match_functions.py A.fnprints.json B.fnprints.json [--min 0.55] [--top 5] [--json]

Triangulates function identity between two fingerprint databases using
several independent signals, none trusted alone:

  sig_eq     masked IDA signature equality          weight 0.35
  ngram      mnemonic 3-gram Jaccard similarity     weight 0.30
  refs       referenced constants/strings/4CC Jaccard  weight 0.25
  degree     call out-degree closeness              weight 0.10

Generalizes to any two Gamebryo-era builds: GOG exe <-> Steam dump,
runtime DLL <-> editor DLL, FO3 <-> FNV cousins.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pe_utils import emit

WEIGHTS = {"sig": 0.35, "ngram": 0.30, "refs": 0.25, "degree": 0.10}


def load_db(p: Path) -> dict:
    db = json.loads(p.read_text(encoding="utf-8"))
    if "functions" not in db:
        raise SystemExit(f"error: {p} is not a fingerprint database (run fingerprint_functions.py --all)")
    return db


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def refset(fn: dict) -> set:
    return set(fn.get("imm_const_rvas", [])) | set(fn.get("string_ref_rvas", [])) | set(fn.get("record_4cc_refs", []))


def match(db_a: dict, db_b: dict, min_score: float, top: int) -> dict:
    fns_a = db_a["functions"]
    fns_b = db_b["functions"]

    sig_index: dict[str, list[int]] = {}
    ngram_index: dict[str, list[int]] = {}
    for j, fb in enumerate(fns_b):
        sig_index.setdefault(fb["masked_sig"], []).append(j)
        for g in fb.get("ngram3", []):
            ngram_index.setdefault(g, []).append(j)

    def degree_sim(a: int, b: int) -> float:
        d = abs(a - b)
        m = max(a, b, 1)
        return max(0.0, 1.0 - d / m)

    matches = []
    for i, fa in enumerate(fns_a):
        grams_a = set(fa.get("ngram3", []))
        cand: dict[int, float] = {}
        for g in grams_a:
            for j in ngram_index.get(g, []):
                cand[j] = cand.get(j, 0.0) + 1.0
        exact = sig_index.get(fa["masked_sig"], [])
        for j in exact:
            cand[j] = cand.get(j, 0.0) + 1000.0  # guarantee inclusion
        if not cand:
            continue

        refs_a = refset(fa)
        scored = []
        for j in cand:
            fb = fns_b[j]
            sig_eq = 1.0 if fb["masked_sig"] == fa["masked_sig"] else 0.0
            ngram = jaccard(grams_a, set(fb.get("ngram3", [])))
            refs = jaccard(refs_a, refset(fb))
            deg = degree_sim(fa.get("out_degree", 0), fb.get("out_degree", 0))
            score = (WEIGHTS["sig"] * sig_eq + WEIGHTS["ngram"] * ngram
                     + WEIGHTS["refs"] * refs + WEIGHTS["degree"] * deg)
            if score >= min_score:
                scored.append((score, sig_eq, ngram, refs, deg, j))

        scored.sort(reverse=True)
        for score, sig_eq, ngram, refs, deg, j in scored[:top]:
            matches.append({
                "a": fns_a[i]["rva"], "b": fns_b[j]["rva"],
                "score": round(score, 3),
                "components": {"sig_eq": sig_eq, "ngram": round(ngram, 3),
                               "refs": round(refs, 3), "degree": round(deg, 3)},
                "a_size": fns_a[i]["size"], "b_size": fns_b[j]["size"],
            })

    matches.sort(key=lambda m: -m["score"])
    return {
        "a": db_a["build_id"],
        "b": db_b["build_id"],
        "functions_a": db_a["function_count"],
        "functions_b": db_b["function_count"],
        "matches_over_threshold": len(matches),
        "matches": matches,
    }


def human(data: dict) -> None:
    print(f"{data['a']}  <->  {data['b']}")
    print(f"functions: {data['functions_a']} vs {data['functions_b']}   matches: {data['matches_over_threshold']}")
    for m in data["matches"][:40]:
        c = m["components"]
        print(f"  {m['a']} <=> {m['b']}  score={m['score']:.3f}  "
              f"(sig={c['sig_eq']:.0f} ngram={c['ngram']:.2f} refs={c['refs']:.2f} deg={c['degree']:.2f})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("db_a", help="fingerprint database A")
    ap.add_argument("db_b", help="fingerprint database B")
    ap.add_argument("--min", type=float, default=0.55)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    data = match(load_db(Path(args.db_a)), load_db(Path(args.db_b)), args.min, args.top)
    emit(data, args.json, human)


if __name__ == "__main__":
    main()
