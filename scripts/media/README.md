# Media self-hosting scripts

These scripts migrate site-travel image storage from external hosts (picsum.photos /
unsplash) to **self-hosted local files** served from `frontend/public/media/`, and point
the 8 China tours at the real photos from site-finuo.

Image URLs in the DB become root-relative `/media/...` paths. `frontend/lib/utils.ts`
`getImageUrl()` passes root-relative paths through unchanged; Next.js `<Image>` reads them
from `public/media/` on disk. Nothing depends on an external image host anymore.

Layout under `frontend/public/media/`:
- `china/`  — real curated tour photos copied from `site-finuo/public/images/anhui/`
- `stock/`  — every previously-external image, downloaded once, named `<sha1(url)>.<ext>`

## Re-running (on the deploy server)

1. `dl_images.py` — reads `/tmp/img_urls.txt` (distinct external URLs from the DB),
   downloads each into `frontend/public/media/stock/`, writes `/tmp/img_manifest.json`
   (`{old_url: "/media/stock/<hash>.<ext>"}`).
2. `build_china_map.py` — globs `frontend/public/media/china/` and emits
   `/tmp/china_images.json` (per-tour ordered galleries + per-destination hero).
3. `migrate_images.py` — run inside the backend container; applies the manifest to every
   image column, then overrides the 8 China activities/destinations/timelines with the
   real photos. Needs `/app/img_manifest.json` + `/app/china_images.json` copied in.

Note: 6 vendor `logo_url`s point at fabricated unsplash URLs that 404 at the source and
therefore could not be downloaded; they were left unchanged.
