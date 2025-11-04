"use client";

import { ActivityAddOn } from "@/types";
import { Plus, Minus, AlertCircle } from "lucide-react";
import { useState } from "react";
import { useLanguage } from "@/contexts/LanguageContext";

interface AddOnsSelectorProps {
  addOns: ActivityAddOn[];
  selectedAddOns?: { id: number; quantity: number }[];
  onAddOnsChange?: (addOns: { id: number; quantity: number }[]) => void;
}

export default function AddOnsSelector({
  addOns,
  selectedAddOns = [],
  onAddOnsChange,
}: AddOnsSelectorProps) {
  const { getTranslation } = useLanguage();
  const [selections, setSelections] = useState<Map<number, number>>(
    new Map(selectedAddOns.map(a => [a.id, a.quantity]))
  );

  if (!addOns || addOns.length === 0) return null;

  const handleQuantityChange = (addOnId: number, change: number) => {
    const newSelections = new Map(selections);
    const current = newSelections.get(addOnId) || 0;
    const newQuantity = Math.max(0, current + change);

    if (newQuantity === 0) {
      newSelections.delete(addOnId);
    } else {
      newSelections.set(addOnId, newQuantity);
    }

    setSelections(newSelections);
    onAddOnsChange?.(
      Array.from(newSelections.entries()).map(([id, quantity]) => ({ id, quantity }))
    );
  };

  const optionalAddOns = addOns.filter(a => a.is_optional);
  const requiredAddOns = addOns.filter(a => !a.is_optional);

  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold mb-3">{getTranslation('addons.add_ons')}</h3>

      {/* Required Add-ons */}
      {requiredAddOns.length > 0 && (
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-3">
            <AlertCircle className="w-5 h-5 text-orange-600" />
            <h4 className="text-sm font-semibold text-orange-600 uppercase">
              {getTranslation('addons.required')}
            </h4>
          </div>
          <div className="space-y-3">
            {requiredAddOns.map((addOn) => (
              <div
                key={addOn.id}
                className="p-4 bg-orange-50 border border-orange-200 rounded-lg"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h5 className="font-semibold text-gray-900">{addOn.name}</h5>
                    {addOn.description && (
                      <p className="text-sm text-gray-600 mt-1">
                        {addOn.description}
                      </p>
                    )}
                  </div>
                  <div className="text-right ml-4">
                    <div className="font-bold text-gray-900">
                      ${addOn.price}
                    </div>
                    <div className="text-xs text-orange-600 font-medium mt-1">
                      {getTranslation('addons.required').toUpperCase()}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Optional Add-ons */}
      {optionalAddOns.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-gray-600 uppercase mb-3">
            {getTranslation('addons.optional_extras')}
          </h4>
          <div className="space-y-3">
            {optionalAddOns.map((addOn) => {
              const quantity = selections.get(addOn.id) || 0;
              const isSelected = quantity > 0;

              return (
                <div
                  key={addOn.id}
                  className={`
                    p-4 rounded-lg border-2 transition-all
                    ${isSelected ? "border-blue-600 bg-blue-50" : "border-gray-200 bg-white"}
                  `}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h5 className="font-semibold text-gray-900">
                        {addOn.name}
                      </h5>
                      {addOn.description && (
                        <p className="text-sm text-gray-600 mt-1">
                          {addOn.description}
                        </p>
                      )}
                    </div>
                    <div className="text-right ml-4">
                      <div className="font-bold text-gray-900">
                        ${addOn.price}
                      </div>
                      {quantity > 0 && (
                        <div className="text-xs text-blue-600 font-medium mt-1">
                          {getTranslation('addons.total')}: ${(addOn.price * quantity).toFixed(2)}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Quantity selector */}
                  <div className="mt-3 flex items-center gap-3">
                    <button
                      onClick={() => handleQuantityChange(addOn.id, -1)}
                      disabled={quantity === 0}
                      className="w-8 h-8 rounded-full border-2 border-gray-300 flex items-center justify-center hover:border-blue-600 hover:bg-blue-50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                    >
                      <Minus className="w-4 h-4" />
                    </button>

                    <div className="w-12 text-center">
                      <span className="text-lg font-semibold">
                        {quantity}
                      </span>
                    </div>

                    <button
                      onClick={() => handleQuantityChange(addOn.id, 1)}
                      className="w-8 h-8 rounded-full border-2 border-blue-600 bg-blue-600 text-white flex items-center justify-center hover:bg-blue-700 transition-colors"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
