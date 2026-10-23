"""White-box (known-f) classical estimator on the Forrelation tasks: results/forr_knownf.json.
Same tuned readout (readout_best) as the quantum stream and the black-box estimators; all seeds present in
results/baselines.json; Q in FORR_Q. Does not modify map.jsonl or baselines.json."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qrcfit.tasks import all_tasks
from qrcfit.baselines import readout_best, forr_classical_stream, FORR_Q
ROOT = os.path.join(os.path.dirname(__file__), "..", "results")
base = json.load(open(os.path.join(ROOT, "baselines.json")))
OUT = os.path.join(ROOT, "forr_knownf.json")
out = json.load(open(OUT)) if os.path.exists(OUT) else {}
tasks = sorted({k.split("|")[0] for k in base if k.startswith("forr_")})
for tn in tasks:
    seeds = sorted(int(k.split("|")[1]) for k in base if k.startswith(tn + "|"))
    for s in seeds:
        key = f"{tn}|{s}"
        if key in out:
            continue
        task = all_tasks(s)[tn]; rec = {}
        for Q in FORR_Q:
            nm, name = readout_best(forr_classical_stream(task, "knownf", Q, s), task, s)
            rec[f"forr_knownf:{Q}"] = dict(nmse=nm, F=int(name.split(":")[1].split(",")[0].strip("()")) if name else 0, family="forr_knownf", size=Q, readout=name)
            print(f"{key} Q={Q} nmse={nm:.4g} ({name})", flush=True)
        out[key] = rec
        json.dump(out, open(OUT, "w"), indent=1)  # checkpoint per (task, seed)
print("DONE")
