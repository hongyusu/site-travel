"use client";

import { ActivityTimeline } from "@/types";
import { Clock } from "lucide-react";
import Image from "next/image";

interface TimelineSectionProps {
  timelines: ActivityTimeline[];
}

export default function TimelineSection({ timelines }: TimelineSectionProps) {
  if (!timelines || timelines.length === 0) return null;

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
      <h2 className="text-2xl font-bold mb-6">What to Expect</h2>

      <div className="space-y-6">
        {timelines.map((step, index) => (
          <div key={step.id} className="flex gap-4">
            {/* Step number indicator */}
            <div className="flex-shrink-0">
              <div className="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-semibold">
                {step.step_number}
              </div>
              {index < timelines.length - 1 && (
                <div className="w-0.5 h-full bg-gray-200 ml-5 mt-2" />
              )}
            </div>

            {/* Content */}
            <div className="flex-1 pb-8">
              <div className="flex items-start justify-between mb-2">
                <h3 className="text-lg font-semibold">{step.title}</h3>
                {step.duration_minutes && (
                  <div className="flex items-center text-sm text-gray-600 ml-4">
                    <Clock className="w-4 h-4 mr-1" />
                    {step.duration_minutes} min
                  </div>
                )}
              </div>

              {step.description && (
                <p className="text-gray-700 mb-3">{step.description}</p>
              )}

              {step.image_url && (
                <div className="relative h-48 w-full rounded-lg overflow-hidden">
                  <Image
                    src={step.image_url}
                    alt={step.title}
                    fill
                    className="object-cover"
                  />
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Total duration summary */}
      {timelines.some(t => t.duration_minutes) && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-center text-gray-700">
            <Clock className="w-5 h-5 mr-2" />
            <span className="font-medium">Total Duration: </span>
            <span className="ml-2">
              {timelines.reduce((sum, t) => sum + (t.duration_minutes || 0), 0)} minutes
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
