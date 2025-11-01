"use client";

import { ActivityPricingTier } from "@/types";
import { Check, Crown, Star, Sparkles } from "lucide-react";
import { useState } from "react";

interface PricingTiersSelectorProps {
  pricingTiers: ActivityPricingTier[];
  selectedTierId?: number;
  onTierSelect?: (tierId: number) => void;
}

export default function PricingTiersSelector({
  pricingTiers,
  selectedTierId,
  onTierSelect,
}: PricingTiersSelectorProps) {
  const [selected, setSelected] = useState<number | undefined>(selectedTierId);

  if (!pricingTiers || pricingTiers.length === 0) return null;

  const handleSelect = (tierId: number) => {
    setSelected(tierId);
    onTierSelect?.(tierId);
  };

  const getIcon = (tierName: string) => {
    const name = tierName.toLowerCase();
    if (name.includes("vip") || name.includes("premium")) return Crown;
    if (name.includes("deluxe") || name.includes("luxury")) return Sparkles;
    return Star;
  };

  const getColorClasses = (tierName: string, isSelected: boolean) => {
    const name = tierName.toLowerCase();
    if (name.includes("vip") || name.includes("luxury")) {
      return {
        border: isSelected ? "border-purple-600" : "border-purple-200 hover:border-purple-400",
        bg: isSelected ? "bg-purple-50" : "bg-white",
        icon: "text-purple-600",
        badge: "bg-purple-600",
      };
    }
    if (name.includes("premium") || name.includes("deluxe")) {
      return {
        border: isSelected ? "border-amber-600" : "border-amber-200 hover:border-amber-400",
        bg: isSelected ? "bg-amber-50" : "bg-white",
        icon: "text-amber-600",
        badge: "bg-amber-600",
      };
    }
    return {
      border: isSelected ? "border-blue-600" : "border-gray-200 hover:border-blue-300",
      bg: isSelected ? "bg-blue-50" : "bg-white",
      icon: "text-blue-600",
      badge: "bg-blue-600",
    };
  };

  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold mb-3">Select Ticket Type</h3>
      <div className="space-y-4">
        {pricingTiers.map((tier) => {
          const isSelected = selected === tier.id;
          const Icon = getIcon(tier.tier_name);
          const colors = getColorClasses(tier.tier_name, isSelected);

          return (
            <button
              key={tier.id}
              onClick={() => tier.is_active && handleSelect(tier.id)}
              disabled={!tier.is_active}
              className={`
                relative p-5 rounded-lg border-2 transition-all text-left
                ${colors.border} ${colors.bg}
                ${!tier.is_active && "opacity-50 cursor-not-allowed"}
              `}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Icon className={`w-5 h-5 ${colors.icon}`} />
                  <h4 className="font-bold text-lg">{tier.tier_name}</h4>
                </div>
                {isSelected && (
                  <div className={`w-6 h-6 ${colors.badge} rounded-full flex items-center justify-center`}>
                    <Check className="w-4 h-4 text-white" />
                  </div>
                )}
              </div>

              {tier.tier_description && (
                <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                  {tier.tier_description}
                </p>
              )}

              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-bold text-gray-900">
                  ${tier.price_adult}
                </span>
                <span className="text-sm text-gray-500">per adult</span>
              </div>

              {tier.price_child && (
                <div className="mt-1 text-sm text-gray-600">
                  ${tier.price_child} per child
                </div>
              )}

              {!tier.is_active && (
                <div className="absolute inset-0 bg-gray-500 bg-opacity-10 rounded-lg flex items-center justify-center">
                  <span className="bg-red-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                    Unavailable
                  </span>
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
