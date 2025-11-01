'use client';

import Link from 'next/link';
import { Category } from '@/types';

interface CategoryCardProps {
  category: Category;
  count?: number;
}

const categoryIcons: Record<string, string> = {
  'tours': '🚶‍♂️',
  'museums': '🏛️',
  'day-trips': '🚌',
  'water-sports': '🏄‍♂️',
  'outdoor': '⛰️',
  'food-drink': '🍷',
  'cruises': '🚢',
  'transport': '🚕',
  'shows': '🎭',
  'adventure': '🎯',
  'cultural': '🎨',
  'nature-wildlife': '🦁'
};

export default function CategoryCard({ category, count }: CategoryCardProps) {
  const icon = categoryIcons[category.slug] || category.icon || '📍';

  return (
    <Link href={`/search?category=${category.slug}`}>
      <div className="category-card bg-white rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer text-center group">
        <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">
          {icon}
        </div>
        <h3 className="font-medium text-gray-900 mb-1">{category.name}</h3>
        {count !== undefined && (
          <p className="text-sm text-gray-500">{count} activities</p>
        )}
      </div>
    </Link>
  );
}