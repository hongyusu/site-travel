import { MetadataRoute } from 'next'

const BASE = 'https://travel.finuo.fi'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        // Keep private / transactional / personalized pages out of the index.
        disallow: [
          '/admin',
          '/vendor',
          '/checkout',
          '/cart',
          '/order-confirmation',
          '/orders',
          '/my-account',
          '/wishlist',
          '/login',
          '/register',
          '/api/',
        ],
      },
    ],
    sitemap: `${BASE}/sitemap.xml`,
    host: BASE,
  }
}
