#!/usr/bin/env python3
"""Deploy aiweb site to Vercel API."""
import sys, os, json, base64, urllib.request, urllib.error

TOKEN_FILE = "/tmp/vercel_token.txt"
SITE_DIR = os.path.expanduser("~/aiweb/docs/.vitepress/dist")
PROJECT_ID = "prj_zHZb5irlWL16XXIOd6EEenYmMOt8"

with open(TOKEN_FILE) as f:
    TOKEN = f.read().strip()

files = []
for root, dirs, fnames in os.walk(SITE_DIR):
    for f in sorted(fnames):
        path = os.path.join(root, f)
        rel = os.path.relpath(path, SITE_DIR)
        with open(path, "rb") as fh:
            raw = fh.read()
        files.append({"file": rel, "data": base64.b64encode(raw).decode()})

print(f"Files: {len(files)}, Total: {sum(len(f['data']) for f in files)/1024/1024:.1f} MB")

payload = json.dumps({
    "files": files,
    "project": PROJECT_ID,
    "name": "aiweb",
    "target": "production"
}).encode()

print(f"Payload: {len(payload)/1024/1024:.1f} MB")

req = urllib.request.Request(
    "https://api.vercel.com/v13/deployments",
    data=payload,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
)

try:
    resp = urllib.request.urlopen(req, timeout=300)
    result = json.loads(resp.read())
    url = result.get("url", "?")
    state = result.get("readyState", result.get("state", "?"))
    print(f"✅ Deployed! URL: https://{url}")
    print(f"State: {state}")
    with open("/tmp/vercel-result.json", "w") as f:
        json.dump(result, f, indent=2)
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"❌ HTTP {e.code}: {body[:500]}")
    sys.exit(1)
