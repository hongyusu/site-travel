import { MetadataRoute } from 'next'

// Generated at request time so it doesn't depend on the backend being up during
// the frontend image build, and always reflects the current catalogue.
export const dynamic = 'force-dynamic'

const BASE = 'https://travel.finuo.fi'
// Server-to-server (same as lib/api.ts SSR path); the public API is same-origin.
const API = 'http://backend:8000/api/v1'
const LANGS = ['en', 'zh', 'es', 'fr'] as const

// Build a sitemap entry that declares hreflang alternates for every language.
// x-default points at the bare URL; each language variant carries ?lang=xx,
// which the app honours (see LanguageProvider) so the URL renders that language.
function entry(
  path: string,
  priority: number,
  changeFrequency: MetadataRoute.Sitemap[number]['changeFrequency'] = 'weekly'
): MetadataRoute.Sitemap[number] {
  const url = `${BASE}${path}`
  const languages: Record<string, string> = { 'x-default': url }
  for (const l of LANGS) languages[l] = `${url}?lang=${l}`
  return { url, priority, changeFrequency, alternates: { languages } }
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const staticPaths: Array<[string, number]> = [
    ['/', 1.0],
    ['/destinations', 0.8],
    ['/search', 0.8],
    ['/blog', 0.6],
    ['/about', 0.5],
    ['/contact', 0.5],
    ['/help', 0.5],
    ['/careers', 0.4],
    ['/press', 0.4],
    ['/affiliate', 0.4],
    ['/privacy', 0.3],
    ['/terms', 0.3],
    ['/cookies', 0.3],
    ['/cancellation', 0.3],
  ]
  const entries: MetadataRoute.Sitemap = staticPaths.map(([p, prio]) => entry(p, prio))

  try {
    // Activity detail pages (paginate through the catalogue).
    for (let page = 1; page <= 5; page++) {
      const r = await fetch(`${API}/activities/search?per_page=100&page=${page}`, { cache: 'no-store' })
      if (!r.ok) break
      const d = await r.json()
      for (const a of d.data || []) {
        if (a?.slug) entries.push(entry(`/activities/${a.slug}`, 0.9))
      }
      if (!d?.pagination?.has_next) break
    }

    // Destination detail pages.
    const dr = await fetch(`${API}/activities/destinations`, { cache: 'no-store' })
    if (dr.ok) {
      const dests = await dr.json()
      for (const d of dests || []) {
        if (d?.slug) entries.push(entry(`/destination/${d.slug}`, 0.7))
      }
    }
  } catch {
    // If the API is unreachable, still return the static routes.
  }

  return entries
}
