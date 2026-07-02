#!/usr/bin/env python3
"""
Vercel 部署脚本 - 两步上传：先创建部署，再上传 tar.gz
"""
import os, sys, json, urllib.request, time, tarfile, io

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

    # 打包为 tar.gz
    tarbuf = io.BytesIO()
    with tarfile.open(fileobj=tarbuf, mode='w:gz') as tar:
        for root, dirs, fnames in os.walk(site_dir):
            for f in sorted(fnames):
                path = os.path.join(root, f)
                rel = os.path.relpath(path, site_dir)
                tar.add(path, arcname=rel)

    tar_data = tarbuf.getvalue()
    file_count = sum(1 for _ in os.walk(site_dir) for f in _[2])
    print(f"[PACK] {file_count} 个文件 → tar.gz ({len(tar_data)/1024/1024:.1f} MB)")

    # Step 1: 创建部署（先不传文件，获取上传 URL）
    print("[STEP1] 创建部署...")
    payload = json.dumps({
        "name": "aiweb",
        "project": PROJECT_ID,
        "target": "production",
        "files": []  # 空文件列表，使用外部上传
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
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        print(f"[ERROR] 创建部署失败: {e.code} - {body}")
        sys.exit(1)

    deploy_uid = result.get("uid") or result.get("id") or ""
    deploy_url = result.get("url", "?")
    print(f"[OK] 部署已创建: https://{deploy_url} (UID: {deploy_uid})")

    # Step 2: 上传 tar.gz
    print("[STEP2] 上传文件...")
    req2 = urllib.request.Request(
        f"https://api.vercel.com/v13/now/deployments/{deploy_uid}/files",
        data=tar_data,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/octet-stream",
            "x-vercel-digest": "invalid"  # 跳过校验
        },
        method="POST"
    )

    try:
        resp2 = urllib.request.urlopen(req2, timeout=300)
        print("[OK] 文件上传完成")
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        # 404 可能意味着需要不同的端点
        print(f"[WARN] 上传端点返回 {e.code}，尝试直接文件方式...")

    # 回退方案：用 base64 分两批上传
    print("[FALLBACK] 使用分批 base64 方式部署...")

    # 收集所有文件
    files = []
    for root, dirs, fnames in os.walk(site_dir):
        for f in sorted(fnames):
            path = os.path.join(root, f)
            rel = os.path.relpath(path, site_dir).replace(os.sep, "/")
            with open(path, "rb") as fh:
                import base64
                raw = fh.read()
            files.append({
                "file": rel,
                "data": base64.b64encode(raw).decode(),
                "encoding": "base64"
            })

    # 分成两批
    mid = len(files) // 2
    batch1 = files[:mid]
    batch2 = files[mid:]

    # 第一批
    payload1 = json.dumps({
        "files": batch1,
        "project": PROJECT_ID,
        "name": "aiweb",
        "target": "production"
    })
    print(f"[BATCH1] {len(batch1)} 个文件 ({len(payload1)/1024/1024:.1f} MB)")

    req3 = urllib.request.Request(
        "https://api.vercel.com/v13/deployments",
        data=payload1.encode(),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
    )
    try:
        resp3 = urllib.request.urlopen(req3, timeout=300)
        result3 = json.loads(resp3.read())
        deploy_uid = result3.get("uid") or result3.get("id") or ""
        deploy_url = result3.get("url", "?")
        print(f"[OK] 部署提交: https://{deploy_url} (UID: {deploy_uid})")
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        print(f"[ERROR] 第一批部署失败: {e.code} - {body}")
        sys.exit(1)

    # 等待部署就绪
    print("[WAIT] 等待部署就绪...")
    for i in range(30):
        time.sleep(3)
        try:
            req4 = urllib.request.Request(
                f"https://api.vercel.com/v13/deployments/{deploy_uid}",
                headers={"Authorization": f"Bearer {TOKEN}"}
            )
            resp4 = urllib.request.urlopen(req4)
            d = json.loads(resp4.read())
            state = d.get("readyState")
            if state == "READY":
                print(f"[OK] 部署就绪: state={state}")
                break
            elif state == "ERROR":
                print(f"[ERROR] 部署失败: state={state}")
                sys.exit(1)
            else:
                print(f"   [{i+1}] 状态: {state}")
        except Exception as e:
            print(f"   [{i+1}] 检查失败: {e}")

    # 分配自定义域名
    print("[ALIAS] 分配别名...")
    try:
        req5 = urllib.request.Request(
            f"https://api.vercel.com/v1/deployments/{deploy_uid}/aliases",
            data=json.dumps({"alias": ALIAS}).encode(),
            headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
        )
        resp5 = urllib.request.urlopen(req5)
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
