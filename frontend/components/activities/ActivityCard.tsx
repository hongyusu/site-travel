'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { Star, Clock, Users, MapPin, Check, Heart } from 'lucide-react';
import { Activity } from '@/types';
import { formatPrice, formatDuration, getImageUrl } from '@/lib/utils';
import { apiClient } from '@/lib/api';

interface ActivityCardProps {
  activity: Activity;
}

export default function ActivityCard({ activity }: ActivityCardProps) {
  const [inWishlist, setInWishlist] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is authenticated
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    setIsAuthenticated(!!token);

    // Check if activity is in wishlist
    if (token) {
      checkWishlistStatus();
    }
  }, [activity.id]);

  const checkWishlistStatus = async () => {
    try {
      const response = await apiClient.wishlist.check(activity.id);
      setInWishlist(response.data.data.in_wishlist);
    } catch (error) {
      // Silently fail - user might not be authenticated
    }
  };

  const toggleWishlist = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    if (!isAuthenticated) {
      window.location.href = '/login?return=' + encodeURIComponent(window.location.pathname);
      return;
    }

    setIsLoading(true);
    try {
      if (inWishlist) {
        await apiClient.wishlist.remove(activity.id);
        setInWishlist(false);
      } else {
        await apiClient.wishlist.add(activity.id);
        setInWishlist(true);
      }
    } catch (error) {
      console.error('Failed to toggle wishlist:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="activity-card group relative">
      <Link href={`/activities/${activity.slug}`}>
        {/* Image */}
        <div className="relative h-48 overflow-hidden">
          <Image
            src={getImageUrl(activity.primary_image?.url)}
            alt={activity.title}
            fill
            className="object-cover group-hover:scale-110 transition-transform duration-300"
          />
          {activity.is_bestseller && (
            <div className="absolute top-2 left-2">
              <span className="badge badge-primary">Bestseller</span>
            </div>
          )}
          {activity.is_skip_the_line && (
            <div className="absolute top-2 right-2">
              <span className="badge bg-purple-100 text-purple-800">Skip the line</span>
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-4">
          {/* Destination */}
          {activity.destinations && activity.destinations.length > 0 && (
            <div className="flex items-center text-gray-500 text-sm mb-1">
              <MapPin className="w-3 h-3 mr-1" />
              <span>{activity.destinations[0].name}</span>
            </div>
          )}

          {/* Title */}
          <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-primary transition-colors">
            {activity.title}
          </h3>

          {/* Rating */}
          {activity.average_rating > 0 && (
            <div className="flex items-center mb-2">
              <div className="flex items-center">
                <Star className="w-4 h-4 text-yellow-400 fill-current" />
                <span className="ml-1 text-sm font-medium">{activity.average_rating}</span>
              </div>
              <span className="ml-1 text-sm text-gray-500">
                ({activity.total_reviews} reviews)
              </span>
            </div>
          )}

          {/* Info */}
          <div className="flex items-center text-sm text-gray-600 mb-3 space-x-4">
            {activity.duration_minutes && (
              <div className="flex items-center">
                <Clock className="w-4 h-4 mr-1" />
                <span>{formatDuration(activity.duration_minutes)}</span>
              </div>
            )}
            {activity.max_group_size && (
              <div className="flex items-center">
                <Users className="w-4 h-4 mr-1" />
                <span>Max {activity.max_group_size}</span>
              </div>
            )}
          </div>

          {/* Features */}
          <div className="space-y-1 mb-3">
            {activity.free_cancellation_hours > 0 && (
              <div className="flex items-center text-success text-sm">
                <Check className="w-4 h-4 mr-1" />
                <span>Free cancellation</span>
              </div>
            )}
            {activity.instant_confirmation && (
              <div className="flex items-center text-success text-sm">
                <Check className="w-4 h-4 mr-1" />
                <span>Instant confirmation</span>
              </div>
            )}
          </div>

          {/* Price */}
          <div className="flex items-baseline justify-between mt-auto">
            <div>
              <span className="text-sm text-gray-500">From</span>
              <p className="text-xl font-bold text-gray-900">
                {formatPrice(activity.price_adult)}
              </p>
              <span className="text-sm text-gray-500">per person</span>
            </div>
          </div>
        </div>
      </Link>

      {/* Wishlist Button */}
      <button
        onClick={toggleWishlist}
        disabled={isLoading}
        className="absolute top-3 right-3 p-2 bg-white rounded-full shadow-md hover:shadow-lg transition-all z-10"
        title={inWishlist ? 'Remove from wishlist' : 'Add to wishlist'}
      >
        <Heart
          className={`w-5 h-5 transition-colors ${
            inWishlist ? 'fill-red-500 text-red-500' : 'text-gray-600'
          } ${isLoading ? 'opacity-50' : ''}`}
        />
      </button>
    </div>
  );
}