'use client';

import { useEffect, useState } from 'react';
import DestinationCard from '@/components/destinations/DestinationCard';
import { Destination } from '@/types';
import { apiClient } from '@/lib/api';
import { Search } from 'lucide-react';

export default function DestinationsPage() {
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [filteredDestinations, setFilteredDestinations] = useState<Destination[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchDestinations();
  }, []);

  useEffect(() => {
    if (searchQuery) {
      const filtered = destinations.filter(dest =>
        dest.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        dest.country?.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredDestinations(filtered);
    } else {
      setFilteredDestinations(destinations);
    }
  }, [searchQuery, destinations]);

  const fetchDestinations = async () => {
    try {
      const response = await apiClient.destinations.list();
      setDestinations(response.data);
      setFilteredDestinations(response.data);
    } catch (error) {
      console.error('Error fetching destinations:', error);
    } finally {
      setLoading(false);
    }
  };

  const groupedDestinations = filteredDestinations.reduce((acc, dest) => {
    const country = dest.country || 'Other';
    if (!acc[country]) {
      acc[country] = [];
    }
    acc[country].push(dest);
    return acc;
  }, {} as Record<string, Destination[]>);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-4">Explore Destinations</h1>
          <p className="text-xl mb-8">
            Discover amazing activities in cities around the world
          </p>

          {/* Search */}
          <div className="max-w-2xl">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search destinations..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-12 pr-4 py-3 rounded-full text-gray-900 focus:outline-none focus:ring-2 focus:ring-white"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-12">
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map(i => (
              <div key={i} className="h-64 bg-gray-200 rounded-lg animate-pulse" />
            ))}
          </div>
        ) : filteredDestinations.length === 0 ? (
          <div className="text-center py-12">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No destinations found
            </h3>
            <p className="text-gray-600">
              Try adjusting your search query
            </p>
          </div>
        ) : (
          <div className="space-y-12">
            {Object.entries(groupedDestinations).map(([country, dests]) => (
              <div key={country}>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">{country}</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {dests.map((dest, index) => (
                    <DestinationCard
                      key={dest.id}
                      destination={dest}
                      variant={index === 0 && dests.length >= 3 ? 'large' : 'default'}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Featured Destinations */}
        {!loading && !searchQuery && destinations.filter(d => d.is_featured).length > 0 && (
          <div className="mt-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-8">Featured Destinations</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {destinations.filter(d => d.is_featured).map(dest => (
                <DestinationCard key={dest.id} destination={dest} variant="large" />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}