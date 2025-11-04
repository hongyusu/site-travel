'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import ActivityCard from '@/components/activities/ActivityCard';
import { Activity, Destination } from '@/types';
import { apiClient } from '@/lib/api';
import { getImageUrl } from '@/lib/utils';
import { MapPin } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

export default function DestinationDetailPage() {
  const params = useParams();
  const slug = params.slug as string;
  const { getCountryName } = useLanguage();
  const [destination, setDestination] = useState<Destination | null>(null);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, [slug]);

  const fetchData = async () => {
    try {
      const [destResponse, activitiesResponse] = await Promise.all([
        apiClient.destinations.getBySlug(slug),
        apiClient.activities.search({ destination_slug: slug, per_page: 12 })
      ]);

      setDestination(destResponse.data);
      setActivities(activitiesResponse.data.data);
    } catch (error) {
      console.error('Error fetching destination:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="animate-pulse">
          <div className="h-96 bg-gray-200" />
          <div className="container mx-auto px-4 py-8">
            <div className="h-8 bg-gray-200 rounded w-1/3 mb-4" />
            <div className="h-4 bg-gray-200 rounded w-1/4 mb-8" />
            <div className="grid grid-cols-4 gap-6">
              {[1, 2, 3, 4].map(i => (
                <div key={i} className="h-64 bg-gray-200 rounded" />
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!destination) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Destination not found</h1>
          <a href="/destinations" className="btn-primary">Browse Destinations</a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="relative h-96 bg-black">
        {destination.image_url && (
          <Image
            src={getImageUrl(destination.image_url)}
            alt={destination.name}
            fill
            className="object-cover opacity-70"
            priority
          />
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 p-8">
          <div className="container mx-auto">
            <div className="flex items-center text-white mb-2">
              <MapPin className="w-5 h-5 mr-2" />
              {destination.country && <span>{getCountryName(destination.country)}</span>}
            </div>
            <h1 className="text-5xl font-bold text-white mb-4">{destination.name}</h1>
            {destination.is_featured && (
              <span className="inline-block bg-primary px-4 py-2 rounded-full text-white text-sm font-medium">
                Featured Destination
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-12">
        {/* Stats */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold text-primary mb-2">
                {activities.length}+
              </div>
              <div className="text-gray-600">Activities Available</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary mb-2">
                {activities.filter(a => a.is_bestseller).length}
              </div>
              <div className="text-gray-600">Bestsellers</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary mb-2">
                {activities.filter(a => a.free_cancellation_hours > 0).length}
              </div>
              <div className="text-gray-600">Free Cancellation</div>
            </div>
          </div>
        </div>

        {/* Activities */}
        <div>
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">
              Things to do in {destination.name}
            </h2>
            <a
              href={`/search?destination=${slug}`}
              className="text-primary hover:text-primary-600 font-medium"
            >
              View all activities →
            </a>
          </div>

          {activities.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-12 text-center">
              <p className="text-gray-600 mb-4">
                No activities available for this destination yet.
              </p>
              <a href="/search" className="btn-primary">
                Browse All Activities
              </a>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {activities.map(activity => (
                <ActivityCard key={activity.id} activity={activity} />
              ))}
            </div>
          )}
        </div>

        {/* Popular Categories */}
        {activities.length > 0 && (
          <div className="mt-16">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Popular Categories</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Array.from(new Set(activities.flatMap(a => a.categories.map(c => c.name))))
                .slice(0, 8)
                .map(categoryName => (
                  <a
                    key={categoryName}
                    href={`/search?destination=${slug}&category=${categoryName.toLowerCase().replace(/\s+/g, '-')}`}
                    className="bg-white rounded-lg shadow p-4 text-center hover:shadow-lg transition-shadow"
                  >
                    <div className="font-medium text-gray-900">{categoryName}</div>
                  </a>
                ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}