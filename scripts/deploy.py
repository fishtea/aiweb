#!/usr/bin/env python3
"""
Vercel 部署脚本 - 将 VitePress 静态产物部署到 Vercel
供 cron job 调用，无依赖（只用了 Python 标准库）
"""
import os, sys, json, base64, urllib.request, time

TOKEN = "vcp_6KidUE1T9ECwrPNYPAoX2WO7cacGW0b8DF2SugUGloKNDp7pjt4OPkc5"
PROJECT_ID = "prj_NDWaVIdrgb5aOQdyKUW8XZxC2sk2"
SITE_DIR = os.path.join("docs", ".vitepress", "dist")
ALIAS = "aiweb-lemon.vercel.app"

def deploy():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    site_dir = os.path.join(project_root, SITE_DIR)

    if not os.path.isdir(site_dir):
        print(f"[ERROR] {SITE_DIR}/ 目录不存在，请先运行 npm run build")
        sys.exit(1)

    # 收集所有文件
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

    total_size = len(json.dumps({"files": files}))
    print(f"[UPLOAD] 上传 {len(files)} 个文件 ({total_size/1024/1024:.1f} MB)...")

    # 创建部署
    payload = json.dumps({
        "files": files,
        "project": PROJECT_ID,
        "name": "aiweb",
        "target": "production"
    }).encode()

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
        deploy_url = result.get("url", "?")
        deploy_uid = result.get("uid") or result.get("id") or ""
        print(f"[OK] 部署提交: https://{deploy_url}")
        print(f"   UID: {deploy_uid}")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] 部署失败: {e.code} - {e.read().decode()[:300]}")
        sys.exit(1)

    # 等待部署就绪
    print("[WAIT] 等待部署就绪...")
    for i in range(30):
        time.sleep(3)
        try:
            req2 = urllib.request.Request(
                "https://api.vercel.com/v6/deployments?limit=1",
                headers={"Authorization": f"Bearer {TOKEN}"}
            )
            resp2 = urllib.request.urlopen(req2)
            data = json.loads(resp2.read())
            d = data["deployments"][0]
            state = d.get("readyState")
            uid2 = d.get("uid") or d.get("id") or ""
            if uid2 != deploy_uid:
                print(f"   [{i+1}] 状态: {state} (等待中...)")
                continue
            if state == "READY":
                print(f"[OK] 部署就绪: state={state}")
                break
            elif state == "ERROR":
                print(f"[ERROR] 部署失败: state={state}")
                print(f"   错误: {d.get('errorCode')}")
                sys.exit(1)
            else:
                print(f"   [{i+1}] 状态: {state}")
        except Exception as e:
            print(f"   [{i+1}] 检查失败: {e}")
    else:
        print("[WARN] 超时，部署可能尚未完成")
        # 不退出，继续尝试分配别名

    # 分配自定义域名
    print("[ALIAS] 分配别名...")
    try:
        req3 = urllib.request.Request(
            f"https://api.vercel.com/v1/deployments/{deploy_uid}/aliases",
            data=json.dumps({"alias": ALIAS}).encode(),
            headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
        )
        resp3 = urllib.request.urlopen(req3)
        print(f"[OK] 别名分配成功: https://{ALIAS}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "already" in body or "409" in body:
            print(f"[OK] 别名已存在: https://{ALIAS}")
        else:
            print(f"[WARN] 别名分配: {e.code} - {body[:200]}")

    print(f"\n网站: https://{ALIAS}")

if __name__ == "__main__":
    deploy()
