"""Refresh the unpublished Zenodo draft 23589290: replace the code archive (git archive of HEAD) and the
manuscript PDF, and update the metadata from submission.json (commit hash and file names). Never publishes."""
import json, os, subprocess, sys, datetime
sys.path.insert(0, "/Users/deeptell01/Documents/alterego/personal/zenodo_deposit/src")
from zenodo_deposit import ZenodoClient, build_payload, load_config

DEP = 23589290
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
os.chdir(ROOT)
commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
today = datetime.date.today().isoformat()
os.makedirs("dist", exist_ok=True)
zipname = f"dist/qrcfit-0.1.0-{commit[:7]}.zip"; pdfname = f"dist/qrcfit-manuscript-{today}.pdf"
subprocess.check_call(["git", "archive", "--format=zip", "--prefix=qrcfit-0.1.0/", "-o", zipname, "HEAD"])
subprocess.check_call(["cp", "paper/main.pdf", pdfname])

cfg = json.load(open("submission.json"))
import re
cfg["description"] = re.sub(r"Snapshot of commit [0-9a-f]+ of", f"Snapshot of commit {commit[:12]} of", cfg["description"])
cfg["description"] = re.sub(r"qrcfit-manuscript-\d{4}-\d{2}-\d{2}\.pdf", os.path.basename(pdfname), cfg["description"])
cfg["related_identifiers"] = [ri for ri in cfg["related_identifiers"] if "/tree/" not in ri["identifier"]] + \
    [{"identifier": f"https://github.com/deeptell-inc/qrcfit/tree/{commit}", "relation": "isIdenticalTo", "scheme": "url"}]
cfg["files"] = [zipname, pdfname]
json.dump(cfg, open("submission.json", "w"), indent=2, ensure_ascii=False)

client = ZenodoClient.for_env(sandbox=False, token=os.environ["ZENODO_TOKEN"])
dep = client.get_deposition(DEP)
assert dep.get("state") == "unsubmitted", f"draft state is {dep.get('state')}; refusing to touch a published record"
for f in dep.get("files", []):
    client.delete_file(DEP, f["id"]); print("removed", f["filename"])
for path in cfg["files"]:
    client.upload_file(dep["links"]["bucket"], path); print("uploaded", path)
client.update_metadata(DEP, build_payload(load_config("submission.json"))["metadata"])
dep = client.get_deposition(DEP)
print("state:", dep["state"], "| reserved DOI:", dep["metadata"].get("prereserve_doi", {}).get("doi"))
print("files:", [(f["filename"], f["filesize"]) for f in dep["files"]])
print("draft:", dep["links"].get("html"))
