#!/usr/bin/env python3
"""GitHub push script - token gets patched in"""
import urllib.request, json, os, subprocess

TOKEN = "github...m3Q"

# Check auth
req = urllib.request.Request("https://api.github.com/repos/fishtea/aiweb")
req.add_header("Authorization", f"Bearer {TOKEN}")
req.add_header("Accept", "application/vnd.github+json")
try:
    resp = urllib.request.urlopen(req)
    repo = json.loads(resp.read())
    print(f"✅ 仓库存在, push权限: {repo.get('permissions',{}).get('push', False)}")
    if repo.get('permissions',{}).get('push'):
        home = os.path.expanduser("~")
        with open(f"{home}/.git-credentials", "w") as f:
            f.write(f"https://fishtea:{TOKEN}@github.com\n")
        os.chmod(f"{home}/.git-credentials", 0o600)
        subprocess.run(["git", "config", "--global", "credential.helper", "store"], cwd="/Users/fishtea/aiweb")
        r = subprocess.run(["git", "push", "-u", "origin", "master"], cwd="/Users/fishtea/aiweb", capture_output=True, text=True, timeout=30)
        print(f"stdout: {r.stdout[-200:]}")
        print(f"stderr: {r.stderr[-200:]}")
        print(f"exit: {r.returncode}")
        print("✅ 推送成功!" if r.returncode == 0 else "❌ 推送失败")
except urllib.error.HTTPError as e:
    body = json.loads(e.read())
    print(f"❌ HTTP {e.code}: {body.get('message', '')}")
