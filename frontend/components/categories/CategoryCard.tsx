'use client';

import Link from 'next/link';
import { Category } from '@/types';
import { 
  MapPin, 
  Building, 
  Bus, 
  Waves, 
  Mountain, 
  Wine, 
  Ship, 
  Car, 
  Theater, 
  Target, 
  Palette, 
  Trees,
  Camera,
  Moon,
  BookOpen,
  Users,
  Heart,
  Flower2,
  Dumbbell,
  ShoppingBag,
  Footprints,
  Anchor
} from 'lucide-react';

interface CategoryCardProps {
  category: Category;
  count?: number;
}

// Professional icon mapping using Lucide React icons
const categoryIcons: Record<string, React.ComponentType<any>> = {
  'tours-sightseeing': MapPin,
  'museums-attractions': Building,
  'day-trips-excursions': Bus,
  'water-sports': Waves,
  'outdoor-adventures': Mountain,
  'food-drink': Wine,
  'cruises-boat-tours': Ship,
  'transfers-ground-transport': Car,
  'shows-performances': Theater,
  'adventure-nature': Target,
  'arts-culture': Palette,
  'nature-wildlife': Trees,
  'tours': MapPin,
  'museums': Building,
  'day-trips': Bus,
  'water-sports': Waves,
  'outdoor': Mountain,
  'food-drink': Wine,
  'cruises': Ship,
  'transport': Car,
  'shows': Theater,
  'adventure': Target,
  'cultural': Palette,
  'nature-wildlife': Trees,
  'photography': Camera,
  'nightlife-entertainment': Moon,
  'workshops-classes': BookOpen,
  'family-friendly': Users,
  'romantic': Heart,
  'wellness-spa': Flower2,
  'sports-fitness': Dumbbell,
  'shopping': ShoppingBag,
  'hiking-walking': Footprints,
  'cruises-boat-tours': Anchor
};

export default function CategoryCard({ category, count }: CategoryCardProps) {
  const IconComponent = categoryIcons[category.slug] || MapPin;

  return (
    <Link href={`/search?category=${category.slug}`}>
      <div className="category-card bg-white rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer text-center group">
        <div className="text-primary mb-3 flex justify-center group-hover:scale-110 transition-transform">
          <IconComponent size={32} />
        </div>
        <h3 className="font-medium text-gray-900 mb-1">{category.name}</h3>
        {count !== undefined && (
          <p className="text-sm text-gray-500">{count} activities</p>
        )}
      </div>
    </Link>
  );
}