'use client';

import Image from 'next/image';
import Link from 'next/link';
import { MapPin } from 'lucide-react';
import { Destination } from '@/types';
import { getImageUrl } from '@/lib/utils';

interface DestinationCardProps {
  destination: Destination;
  variant?: 'default' | 'large';
}

export default function DestinationCard({
  destination,
  variant = 'default'
}: DestinationCardProps) {
  const heightClass = variant === 'large' ? 'h-80' : 'h-64';

  return (
    <Link href={`/destination/${destination.slug}`}>
      <div className={`destination-card relative ${heightClass} rounded-lg overflow-hidden group cursor-pointer`}>
        <Image
          src={getImageUrl(destination.image_url)}
          alt={destination.name}
          fill
          className="object-cover group-hover:scale-110 transition-transform duration-500"
        />

        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />

        {/* Content */}
        <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
          <div className="flex items-center mb-2">
            <MapPin className="w-4 h-4 mr-1" />
            {destination.country && (
              <span className="text-sm">{destination.country}</span>
            )}
          </div>
          <h3 className="text-2xl font-bold mb-1">{destination.name}</h3>
          {destination.is_featured && (
            <span className="inline-block bg-primary px-2 py-1 rounded text-xs font-medium">
              Popular destination
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}