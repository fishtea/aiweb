#!/usr/bin/env python3
"""GitHub Actions: Build and deploy to Vercel."""
import os, json, base64, urllib.request, urllib.error, sys

def deploy():
    token = os.environ["VERCEL_TOKEN"]
    project_id = os.environ.get("VERCEL_PROJECT_ID", "prj_zHZb5irlWL16XXIOd6EEenYmMOt8")
    site_dir = "docs/.vitepress/dist"

    files = []
    for root, dirs, fnames in os.walk(site_dir):
        for f in sorted(fnames):
            path = os.path.join(root, f)
            rel = os.path.relpath(path, site_dir).replace(os.sep, "/")
            with open(path, "rb") as fh:
                raw = fh.read()
            files.append({
                "file": rel,
                "data": base64.b64encode(raw).decode(),
                "encoding": "base64"
            })

    payload = json.dumps({
        "files": files,
        "project": project_id,
        "name": "aiweb",
        "target": "production"
    }).encode()

    req = urllib.request.Request(
        "https://api.vercel.com/v13/deployments",
        data=payload,
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
    )

    try:
        resp = urllib.request.urlopen(req, timeout=300)
        result = json.loads(resp.read())
        url = result.get("url", "?")
        print(f"✅ Deployed: https://{url}")
        print(f"Aliases: {result.get('alias', [])}")
    except urllib.error.HTTPError as e:
        print(f"❌ Failed: {e.code} - {e.read().decode()[:300]}")
        sys.exit(1)

if __name__ == "__main__":
    deploy()
