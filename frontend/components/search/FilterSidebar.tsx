'use client';

import { useState } from 'react';
import { SearchParams } from '@/types';
import { X } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

interface FilterSidebarProps {
  filters: SearchParams;
  onFilterChange: (filters: SearchParams) => void;
  categories?: Array<{ id: number; name: string; slug: string }>;
  destinations?: Array<{ id: number; name: string; slug: string }>;
}

export default function FilterSidebar({
  filters,
  onFilterChange,
  categories = [],
  destinations = []
}: FilterSidebarProps) {
  const [localFilters, setLocalFilters] = useState<SearchParams>(filters);
  const { getTranslation } = useLanguage();

  const handlePriceChange = (min: string, max: string) => {
    const updated = {
      ...localFilters,
      min_price: min ? parseFloat(min) : undefined,
      max_price: max ? parseFloat(max) : undefined
    };
    setLocalFilters(updated);
    onFilterChange(updated);
  };

  const handleDurationChange = (min: string, max: string) => {
    const updated = {
      ...localFilters,
      min_duration: min ? parseInt(min) : undefined,
      max_duration: max ? parseInt(max) : undefined
    };
    setLocalFilters(updated);
    onFilterChange(updated);
  };

  const handleRatingChange = (rating: number) => {
    const updated = { ...localFilters, min_rating: rating };
    setLocalFilters(updated);
    onFilterChange(updated);
  };

  const handleCheckboxChange = (key: keyof SearchParams, value: boolean) => {
    const updated = { ...localFilters, [key]: value || undefined };
    setLocalFilters(updated);
    onFilterChange(updated);
  };

  const handleCategoryChange = (slug: string) => {
    const updated = { ...localFilters, category_slug: slug || undefined };
    setLocalFilters(updated);
    onFilterChange(updated);
  };

  const handleDestinationChange = (slug: string) => {
    const updated = { ...localFilters, destination_slug: slug || undefined };
    setLocalFilters(updated);
    onFilterChange(updated);
  };

  const clearFilters = () => {
    const cleared: SearchParams = { q: localFilters.q };
    setLocalFilters(cleared);
    onFilterChange(cleared);
  };

  const hasActiveFilters = Object.keys(localFilters).length > (localFilters.q ? 1 : 0);

  return (
    <div className="bg-white rounded-lg shadow p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h3 className="font-semibold text-lg">{getTranslation('filter.title')}</h3>
        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="text-sm text-primary hover:text-primary-600 flex items-center min-h-[44px] p-2"
          >
            <X className="w-4 h-4 mr-1" />
            {getTranslation('filter.clear_all')}
          </button>
        )}
      </div>

      {/* Category Filter */}
      {categories.length > 0 && (
        <div className="border-t pt-4">
          <h4 className="font-medium mb-3">{getTranslation('filter.category')}</h4>
          <select
            value={localFilters.category_slug || ''}
            onChange={(e) => handleCategoryChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent min-h-[44px] text-base"
          >
            <option value="">{getTranslation('filter.all_categories')}</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.slug}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Destination Filter */}
      {destinations.length > 0 && (
        <div className="border-t pt-4">
          <h4 className="font-medium mb-3">{getTranslation('nav.destinations')}</h4>
          <select
            value={localFilters.destination_slug || ''}
            onChange={(e) => handleDestinationChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent min-h-[44px] text-base"
          >
            <option value="">{getTranslation('filter.all_destinations')}</option>
            {destinations.map((dest) => (
              <option key={dest.id} value={dest.slug}>
                {dest.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Price Range */}
      <div className="border-t pt-4">
        <h4 className="font-medium mb-3">{getTranslation('filter.price_range')}</h4>
        <div className="flex items-center space-x-2">
          <input
            type="number"
            placeholder={getTranslation('filter.price.min')}
            value={localFilters.min_price || ''}
            onChange={(e) => handlePriceChange(e.target.value, String(localFilters.max_price || ''))}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent min-h-[44px] text-base"
          />
          <span>-</span>
          <input
            type="number"
            placeholder={getTranslation('filter.price.max')}
            value={localFilters.max_price || ''}
            onChange={(e) => handlePriceChange(String(localFilters.min_price || ''), e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent min-h-[44px] text-base"
          />
        </div>
      </div>

      {/* Duration */}
      <div className="border-t pt-4">
        <h4 className="font-medium mb-3">{getTranslation('filter.duration_hours')}</h4>
        <div className="flex items-center space-x-2">
          <input
            type="number"
            placeholder={getTranslation('filter.price.min')}
            value={localFilters.min_duration ? localFilters.min_duration / 60 : ''}
            onChange={(e) => handleDurationChange(String(parseFloat(e.target.value || '0') * 60), String(localFilters.max_duration || ''))}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent min-h-[44px] text-base"
          />
          <span>-</span>
          <input
            type="number"
            placeholder={getTranslation('filter.price.max')}
            value={localFilters.max_duration ? localFilters.max_duration / 60 : ''}
            onChange={(e) => handleDurationChange(String(localFilters.min_duration || ''), String(parseFloat(e.target.value || '0') * 60))}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent min-h-[44px] text-base"
          />
        </div>
      </div>

      {/* Rating */}
      <div className="border-t pt-4">
        <h4 className="font-medium mb-3">{getTranslation('filter.min_rating')}</h4>
        <div className="space-y-2">
          {[4.5, 4.0, 3.5, 3.0].map((rating) => (
            <label key={rating} className="flex items-center cursor-pointer min-h-[44px] p-1">
              <input
                type="radio"
                name="rating"
                checked={localFilters.min_rating === rating}
                onChange={() => handleRatingChange(rating)}
                className="mr-2"
              />
              <span className="text-sm">
                {rating}+ ⭐
              </span>
            </label>
          ))}
          <label className="flex items-center cursor-pointer min-h-[44px] p-1">
            <input
              type="radio"
              name="rating"
              checked={!localFilters.min_rating}
              onChange={() => handleRatingChange(0)}
              className="mr-2"
            />
            <span className="text-sm">{getTranslation('filter.any_rating')}</span>
          </label>
        </div>
      </div>

      {/* Features */}
      <div className="border-t pt-4">
        <h4 className="font-medium mb-3">{getTranslation('filter.features')}</h4>
        <div className="space-y-2">
          <label className="flex items-center cursor-pointer min-h-[44px] p-1">
            <input
              type="checkbox"
              checked={localFilters.free_cancellation || false}
              onChange={(e) => handleCheckboxChange('free_cancellation', e.target.checked)}
              className="mr-2"
            />
            <span className="text-sm">{getTranslation('filter.free_cancellation')}</span>
          </label>
          <label className="flex items-center cursor-pointer min-h-[44px] p-1">
            <input
              type="checkbox"
              checked={localFilters.instant_confirmation || false}
              onChange={(e) => handleCheckboxChange('instant_confirmation', e.target.checked)}
              className="mr-2"
            />
            <span className="text-sm">{getTranslation('filter.instant_confirmation')}</span>
          </label>
          <label className="flex items-center cursor-pointer min-h-[44px] p-1">
            <input
              type="checkbox"
              checked={localFilters.skip_the_line || false}
              onChange={(e) => handleCheckboxChange('skip_the_line', e.target.checked)}
              className="mr-2"
            />
            <span className="text-sm">{getTranslation('filter.skip_the_line')}</span>
          </label>
          <label className="flex items-center cursor-pointer min-h-[44px] p-1">
            <input
              type="checkbox"
              checked={localFilters.bestseller || false}
              onChange={(e) => handleCheckboxChange('bestseller', e.target.checked)}
              className="mr-2"
            />
            <span className="text-sm">{getTranslation('filter.bestseller')}</span>
          </label>
        </div>
      </div>
    </div>
  );
}