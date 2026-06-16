#!/usr/bin/env python3
"""Build per-tour China image galleries from the real files in public/media/china/.

Emits /tmp/china_images.json:
  {"activities": {<slug>: [/media/china/... ordered, hero first]},
   "destinations": {<dest_slug>: /media/china/...hero}}
Handles mixed .jpeg/.png extensions by globbing actual files.
"""
import os, json, re, glob

D = "/opt/sites/site-travel/frontend/public/media/china"


def files(prefix):
    fs = []
    for p in glob.glob(os.path.join(D, f"{prefix}-*")):
        b = os.path.basename(p)
        m = re.match(rf"{prefix}-(\d+)\.", b)
        if m:
            fs.append((int(m.group(1)), "/media/china/" + b))
    return [p for _, p in sorted(fs)]


def order(prefix, hero_n):
    allf = files(prefix)
    hero = next((p for p in allf if re.search(rf"{prefix}-{hero_n}\.", p)), allf[0])
    return [hero] + [p for p in allf if p != hero]


china = {
    "china-huangshan-yellow-mountain-3-day": order("huangshan", 3),
    "china-huizhou-ancient-villages-3-day":  order("huizhou", 6),
    "china-mount-qiyun-3-day":               order("qiyun", 3),
    "china-southern-anhui-jingxian-3-day":   order("anhui", 2),
    "china-suzhou-classical-gardens-3-day":  order("suzhou", 4),
    "china-hangzhou-west-lake-3-day":        order("hangzhou", 9),
    "china-shanghai-city-3-day":             order("shanghai", 18),
}
sz, hz = files("suzhou"), files("hangzhou")
hero = next(p for p in hz if "hangzhou-5." in p)
china["china-suzhou-hangzhou-3-day"] = [hero] + [p for p in (sz + hz) if p != hero]

dest = {
    "anhui": order("huangshan", 3)[0],
    "suzhou": order("suzhou", 4)[0],
    "shanghai": order("shanghai", 18)[0],
    "hangzhou": order("hangzhou", 9)[0],
}
json.dump({"activities": china, "destinations": dest},
          open("/tmp/china_images.json", "w"), indent=2)
for k, v in china.items():
    print(f"{k}: {len(v)} imgs, hero={v[0]}")
print("dests:", dest)
