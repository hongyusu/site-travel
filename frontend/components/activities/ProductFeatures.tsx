"use client";

import { ProductFeatures as ProductFeaturesData } from "@/types";
import { useLanguage } from "@/contexts/LanguageContext";

export default function ProductFeatures({ data }: { data?: ProductFeaturesData | null }) {
  const { language } = useLanguage();
  const lang = language as string;
  if (!data || (!(data.bullets && data.bullets.length) && !(data.images && data.images.length))) return null;
  const pick = (en?: string, zh?: string) => (lang === "zh" ? zh || en : en || zh) || "";

  return (
    <div className="bg-paper rounded-lg shadow-sm p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4">{lang === "zh" ? "产品特色" : "Product highlights"}</h2>

      {data.bullets && data.bullets.length > 0 && (
        <ul className="space-y-2 mb-5">
          {data.bullets.map((b, i) => (
            <li key={i} className="flex gap-2 items-baseline">
              <span className="text-primary font-semibold whitespace-nowrap">{pick(b.tag_en, b.tag_zh)}</span>
              <span className="text-gray-700">{pick(b.text_en, b.text_zh)}</span>
            </li>
          ))}
        </ul>
      )}

      {data.images && data.images.length > 0 && (
        // Sliced infographic: stack seamlessly, full width.
        <div className="overflow-hidden rounded-lg">
          {data.images.map((src, i) => (
            // eslint-disable-next-line @next/next/no-img-element
            <img key={i} src={src} alt="" loading="lazy" className="w-full block align-top" />
          ))}
        </div>
      )}
    </div>
  );
}
