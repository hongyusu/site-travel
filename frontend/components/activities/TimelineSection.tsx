"use client";

import { ActivityTimeline, TimelineSubsection, TimelineAttraction } from "@/types";
import { useLanguage } from "@/contexts/LanguageContext";
import Image from "next/image";

interface TimelineSectionProps {
  timelines: ActivityTimeline[];
}

const pick = (lang: string, en?: string, zh?: string) =>
  (lang === "zh" ? zh || en : en || zh) || "";

function ImageRow({ images, alt }: { images: string[]; alt: string }) {
  if (!images || images.length === 0) return null;
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-3">
      {images.map((src, i) => (
        <div key={i} className="relative h-32 sm:h-36 rounded-lg overflow-hidden bg-gray-100">
          <Image src={src} alt={alt} fill className="object-cover" sizes="(max-width:640px) 50vw, 33vw" />
        </div>
      ))}
    </div>
  );
}

function Sub({ label, sub, lang }: { label: string; sub?: TimelineSubsection; lang: string }) {
  if (!sub) return null;
  const text = pick(lang, sub.text_en, sub.text_zh);
  if (!text && !(sub.images && sub.images.length)) return null;
  return (
    <div className="mb-5">
      <h4 className="text-sm font-semibold uppercase tracking-wide text-primary mb-2">{label}</h4>
      {text && <p className="text-gray-700 leading-relaxed whitespace-pre-line">{text}</p>}
      <ImageRow images={sub.images || []} alt={label} />
    </div>
  );
}

function Attractions({ items, lang }: { items?: TimelineAttraction[]; lang: string }) {
  if (!items || items.length === 0) return null;
  return (
    <div className="mb-2">
      <h4 className="text-sm font-semibold uppercase tracking-wide text-primary mb-3">
        {lang === "zh" ? "景点活动" : "Sights & activities"}
      </h4>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {items.map((a, i) => {
          const name = pick(lang, a.name_en, a.name_zh);
          const text = pick(lang, a.text_en, a.text_zh);
          return (
            <div key={i} className="border border-gray-200 rounded-lg overflow-hidden flex flex-col">
              {a.images && a.images[0] && (
                <div className="relative h-44 w-full bg-gray-100">
                  <Image src={a.images[0]} alt={name} fill className="object-cover" sizes="(max-width:640px) 100vw, 50vw" />
                </div>
              )}
              <div className="p-3">
                {name && <div className="font-semibold text-gray-900 mb-1">{name}</div>}
                {text && <p className="text-sm text-gray-600 leading-relaxed">{text}</p>}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function TimelineSection({ timelines }: TimelineSectionProps) {
  const { language } = useLanguage();
  const lang = language as string;
  if (!timelines || timelines.length === 0) return null;

  const labels = lang === "zh"
    ? { heading: "每日行程", day: "第", overview: "行程概述", accommodation: "住宿", highlights: "行程高亮" }
    : { heading: "Day-by-day itinerary", day: "Day", overview: "Itinerary overview", accommodation: "Accommodation", highlights: "Highlights" };

  return (
    <div className="bg-paper rounded-lg shadow-sm p-6 mb-6">
      <h2 className="text-2xl font-bold mb-6">{labels.heading}</h2>

      <div className="space-y-8">
        {timelines.map((step) => {
          const s = step.sections;
          return (
            <div key={step.id} className="border-b border-gray-100 pb-6 last:border-0 last:pb-0">
              {/* Day header */}
              <div className="flex items-center gap-3 mb-4">
                <span className="flex-shrink-0 inline-flex items-center justify-center min-w-[3rem] h-8 px-2 rounded-full bg-primary text-white text-sm font-semibold">
                  {lang === "zh" ? `第${step.step_number}天` : `${labels.day} ${step.step_number}`}
                </span>
                <h3 className="text-lg font-semibold text-gray-900">{step.title}</h3>
              </div>

              {s ? (
                <div className="pl-1">
                  <Sub label={labels.overview} sub={s.overview} lang={lang} />
                  <Sub label={labels.accommodation} sub={s.accommodation} lang={lang} />
                  <Sub label={labels.highlights} sub={s.highlights} lang={lang} />
                  <Attractions items={s.attractions} lang={lang} />
                </div>
              ) : (
                <div className="pl-1">
                  {step.description && <p className="text-gray-700 mb-3">{step.description}</p>}
                  {step.image_url && (
                    <div className="relative h-48 w-full rounded-lg overflow-hidden">
                      <Image src={step.image_url} alt={step.title} fill className="object-cover" />
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
