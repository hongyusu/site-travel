"use client";

import { Activity, ActivityDetailResponse } from "@/types";
import {
  Shield,
  Smartphone,
  DollarSign,
  CheckCircle,
  Clock,
  Baby,
  Dog,
  Gift,
  CreditCard,
  AlertTriangle,
  Video,
  Cloud,
  ShieldAlert,
} from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

interface ActivityBadgesProps {
  activity: Activity | ActivityDetailResponse;
}

export default function ActivityBadges({ activity }: ActivityBadgesProps) {
  const { getTranslation } = useLanguage();
  const badges = [];

  // Trust & Verification Badges
  if (activity.is_verified_activity) {
    badges.push({
      icon: CheckCircle,
      label: getTranslation('features.verified_activity'),
      color: "text-green-600",
      bgColor: "bg-green-50",
      borderColor: "border-green-200",
    });
  }

  if (activity.has_best_price_guarantee) {
    badges.push({
      icon: DollarSign,
      label: getTranslation('features.best_price_guarantee'),
      color: "text-blue-600",
      bgColor: "bg-blue-50",
      borderColor: "border-blue-200",
    });
  }

  // Convenience Badges
  if (activity.has_mobile_ticket) {
    badges.push({
      icon: Smartphone,
      label: getTranslation('features.mobile_ticket'),
      color: "text-purple-600",
      bgColor: "bg-purple-50",
      borderColor: "border-purple-200",
    });
  }

  if (activity.is_likely_to_sell_out) {
    badges.push({
      icon: AlertTriangle,
      label: getTranslation('features.likely_to_sell_out'),
      color: "text-orange-600",
      bgColor: "bg-orange-50",
      borderColor: "border-orange-200",
    });
  }

  if (activity.response_time_hours && activity.response_time_hours <= 24) {
    badges.push({
      icon: Clock,
      label: `${activity.response_time_hours}h ${getTranslation('features.response_time')}`,
      color: "text-teal-600",
      bgColor: "bg-teal-50",
      borderColor: "border-teal-200",
    });
  }

  // Accessibility Badges
  if (activity.is_wheelchair_accessible) {
    badges.push({
      icon: CheckCircle,
      label: getTranslation('features.wheelchair_accessible'),
      color: "text-indigo-600",
      bgColor: "bg-indigo-50",
      borderColor: "border-indigo-200",
    });
  }

  if (activity.is_stroller_accessible) {
    badges.push({
      icon: Baby,
      label: getTranslation('features.stroller_accessible'),
      color: "text-pink-600",
      bgColor: "bg-pink-50",
      borderColor: "border-pink-200",
    });
  }

  if (activity.allows_service_animals) {
    badges.push({
      icon: Dog,
      label: getTranslation('features.service_animals_allowed'),
      color: "text-amber-600",
      bgColor: "bg-amber-50",
      borderColor: "border-amber-200",
    });
  }

  if (activity.has_infant_seats) {
    badges.push({
      icon: Baby,
      label: getTranslation('features.infant_seats_available'),
      color: "text-rose-600",
      bgColor: "bg-rose-50",
      borderColor: "border-rose-200",
    });
  }

  // Payment & Booking Options
  if (activity.is_giftable) {
    badges.push({
      icon: Gift,
      label: getTranslation('features.gift_option_available'),
      color: "text-red-600",
      bgColor: "bg-red-50",
      borderColor: "border-red-200",
    });
  }

  if (activity.allows_reserve_now_pay_later) {
    badges.push({
      icon: CreditCard,
      label: getTranslation('features.reserve_now_pay_later'),
      color: "text-cyan-600",
      bgColor: "bg-cyan-50",
      borderColor: "border-cyan-200",
    });
  }

  // Safety & Requirements
  if (activity.has_covid_measures) {
    badges.push({
      icon: ShieldAlert,
      label: getTranslation('features.covid_measures'),
      color: "text-emerald-600",
      bgColor: "bg-emerald-50",
      borderColor: "border-emerald-200",
    });
  }

  if (activity.weather_dependent) {
    badges.push({
      icon: Cloud,
      label: getTranslation('features.weather_dependent'),
      color: "text-sky-600",
      bgColor: "bg-sky-50",
      borderColor: "border-sky-200",
    });
  }

  if (activity.video_url) {
    badges.push({
      icon: Video,
      label: getTranslation('features.video_preview_available'),
      color: "text-violet-600",
      bgColor: "bg-violet-50",
      borderColor: "border-violet-200",
    });
  }

  if (!badges.length) return null;

  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold mb-3">{getTranslation('features.title')}</h3>
      <div className="flex flex-wrap gap-2">
        {badges.map((badge, index) => {
          const Icon = badge.icon;
          return (
            <div
              key={index}
              className={`
                flex items-center gap-2 px-3 py-2 rounded-lg border
                ${badge.bgColor} ${badge.borderColor}
              `}
            >
              <Icon className={`w-4 h-4 ${badge.color}`} />
              <span className={`text-sm font-medium ${badge.color}`}>
                {badge.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
