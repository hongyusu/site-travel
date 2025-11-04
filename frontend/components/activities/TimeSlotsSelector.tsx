"use client";

import { ActivityTimeSlot } from "@/types";
import { Clock } from "lucide-react";
import { useState } from "react";
import { useLanguage } from "@/contexts/LanguageContext";

interface TimeSlotsSelectorProps {
  timeSlots: ActivityTimeSlot[];
  selectedSlotId?: number;
  onSlotSelect?: (slotId: number) => void;
}

export default function TimeSlotsSelector({
  timeSlots,
  selectedSlotId,
  onSlotSelect,
}: TimeSlotsSelectorProps) {
  const { getTranslation } = useLanguage();
  const [selected, setSelected] = useState<number | undefined>(selectedSlotId);

  if (!timeSlots || timeSlots.length === 0) return null;

  const handleSelect = (slotId: number) => {
    setSelected(slotId);
    onSlotSelect?.(slotId);
  };

  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold mb-3">{getTranslation('timeslots.select_time')}</h3>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {timeSlots.map((slot) => {
          const isSelected = selected === slot.id;
          const priceAdjustment = slot.price_adjustment;
          const hasAdjustment = priceAdjustment !== 0;

          return (
            <button
              key={slot.id}
              onClick={() => slot.is_available && handleSelect(slot.id)}
              disabled={!slot.is_available}
              className={`
                relative p-4 rounded-lg border-2 transition-all
                ${
                  isSelected
                    ? "border-blue-600 bg-blue-50"
                    : slot.is_available
                    ? "border-gray-200 hover:border-blue-300 bg-white"
                    : "border-gray-100 bg-gray-50 cursor-not-allowed"
                }
              `}
            >
              <div className="flex flex-col items-center">
                <Clock className={`w-5 h-5 mb-2 ${
                  slot.is_available ? "text-gray-700" : "text-gray-400"
                }`} />
                <div className={`font-semibold ${
                  slot.is_available ? "text-gray-900" : "text-gray-400"
                }`}>
                  {slot.slot_time}
                </div>
                {slot.slot_label && (
                  <div className="text-xs text-gray-500 mt-1">
                    {slot.slot_label}
                  </div>
                )}
                {hasAdjustment && slot.is_available && (
                  <div className={`text-xs mt-1 ${
                    priceAdjustment > 0 ? "text-orange-600" : "text-green-600"
                  }`}>
                    {priceAdjustment > 0 ? "+" : ""}${Math.abs(priceAdjustment)}
                  </div>
                )}
                {!slot.is_available && (
                  <div className="text-xs text-red-500 mt-1">{getTranslation('timeslots.sold_out')}</div>
                )}
              </div>

              {isSelected && (
                <div className="absolute top-2 right-2">
                  <div className="w-5 h-5 bg-blue-600 rounded-full flex items-center justify-center">
                    <svg
                      className="w-3 h-3 text-white"
                      fill="none"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path d="M5 13l4 4L19 7"></path>
                    </svg>
                  </div>
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
