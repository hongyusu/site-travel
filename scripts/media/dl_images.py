#!/usr/bin/env python3
"""Download every external image URL (from /tmp/img_urls.txt) to public/media/stock/.

Writes a manifest /tmp/img_manifest.json mapping each original URL to its new
root-relative path /media/stock/<sha1>.<ext>. Run on the deploy server (host),
where frontend/public/media/stock/ lives.
"""
import os, hashlib, json, urllib.request, ssl
from concurrent.futures import ThreadPoolExecutor

URLS = [l.strip() for l in open("/tmp/img_urls.txt") if l.strip()]
DEST = "/opt/sites/site-travel/frontend/public/media/stock"
os.makedirs(DEST, exist_ok=True)
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
EXT = {"image/jpeg": ".jpg", "image/jpg": ".jpg", "image/png": ".png",
       "image/webp": ".webp", "image/gif": ".gif"}


def fetch(url):
    h = hashlib.sha1(url.encode()).hexdigest()[:16]
    err = None
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=40, context=ctx) as r:
                ct = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                ext = EXT.get(ct, ".jpg")
                data = r.read()
            if len(data) < 100:
                raise ValueError("tiny response")
            fn = h + ext
            with open(os.path.join(DEST, fn), "wb") as f:
                f.write(data)
            return url, "/media/stock/" + fn, None
        except Exception as e:
            err = str(e)
    return url, None, err


def main():
    manifest, fails, done = {}, [], 0
    with ThreadPoolExecutor(max_workers=12) as ex:
        for url, path, err in ex.map(fetch, URLS):
            done += 1
            if path:
                manifest[url] = path
            else:
                fails.append((url, err))
            if done % 100 == 0:
                print(f"  {done}/{len(URLS)}", flush=True)
    json.dump(manifest, open("/tmp/img_manifest.json", "w"))
    print(f"DONE: {len(manifest)} ok, {len(fails)} failed")
    for u, e in fails[:10]:
        print("  FAIL", e, u)


if __name__ == "__main__":
    main()
