'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import SearchBar from '@/components/search/SearchBar';
import DestinationCard from '@/components/destinations/DestinationCard';
import CategoryCard from '@/components/categories/CategoryCard';
import ActivityCard from '@/components/activities/ActivityCard';
import { Activity, Category, Destination } from '@/types';
import { apiClient } from '@/lib/api';
import { ArrowRight, Shield, Clock, Award } from 'lucide-react';

export default function HomePage() {
  const [featuredDestinations, setFeaturedDestinations] = useState<Destination[]>([]);
  const [popularActivities, setPopularActivities] = useState<Activity[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHomePageData();
  }, []);

  const fetchHomePageData = async () => {
    try {
      const [destinationsRes, activitiesRes, categoriesRes] = await Promise.all([
        apiClient.destinations.getFeatured(),
        apiClient.activities.search({ bestseller: true, per_page: 8 }),
        apiClient.categories.list()
      ]);

      setFeaturedDestinations(destinationsRes.data.slice(0, 6));
      setPopularActivities(activitiesRes.data.data);
      setCategories(categoriesRes.data.slice(0, 8));
    } catch (error) {
      console.error('Error fetching homepage data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-[600px] flex items-center justify-center bg-gradient-to-br from-primary to-orange-600">
        <Image
          src="https://picsum.photos/seed/hero-travel-partner/1920/600"
          alt="Meet your travel partner"
          fill
          className="object-cover opacity-50"
          priority
        />
        <div className="absolute inset-0 bg-gradient-to-br from-primary/60 to-orange-600/60"></div>
        <div className="relative z-10 container mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4 drop-shadow-lg">
            Meet Your Perfect Travel Partner
          </h1>
          <p className="text-xl md:text-2xl text-white mb-8 drop-shadow-md">
            Connect with local experts and discover authentic experiences
          </p>
          <div className="max-w-3xl mx-auto">
            <SearchBar
              placeholder="Where would you like to explore?"
              showDatePicker={true}
              autoFocus={true}
            />
          </div>
        </div>
      </section>

      {/* Trust Indicators */}
      <section className="bg-gray-50 py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <Shield className="w-12 h-12 text-primary mx-auto mb-3" />
              <h3 className="font-semibold text-lg mb-2">Trusted by millions</h3>
              <p className="text-gray-600">Over 150,000 activities worldwide</p>
            </div>
            <div className="text-center">
              <Clock className="w-12 h-12 text-primary mx-auto mb-3" />
              <h3 className="font-semibold text-lg mb-2">Free cancellation</h3>
              <p className="text-gray-600">Most activities offer free cancellation</p>
            </div>
            <div className="text-center">
              <Award className="w-12 h-12 text-primary mx-auto mb-3" />
              <h3 className="font-semibold text-lg mb-2">Best price guarantee</h3>
              <p className="text-gray-600">Find it cheaper? We'll refund the difference</p>
            </div>
          </div>
        </div>
      </section>

      {/* Popular Destinations */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Popular destinations
              </h2>
              <p className="text-gray-600">
                Explore our most popular travel destinations
              </p>
            </div>
            <a href="/destinations" className="text-primary hover:text-primary-600 flex items-center font-medium">
              See all destinations
              <ArrowRight className="w-4 h-4 ml-1" />
            </a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {loading ? (
              <>
                {[1, 2, 3, 4, 5, 6].map(i => (
                  <div key={i} className="h-64 bg-gray-200 rounded-lg animate-pulse" />
                ))}
              </>
            ) : (
              featuredDestinations.map((destination, index) => (
                <DestinationCard
                  key={destination.id}
                  destination={destination}
                  variant={index === 0 ? 'large' : 'default'}
                />
              ))
            )}
          </div>
        </div>
      </section>

      {/* Browse by Category */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Browse by category
            </h2>
            <p className="text-gray-600">
              Find the perfect activity for your interests
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-4 gap-4">
            {loading ? (
              <>
                {[1, 2, 3, 4, 5, 6, 7, 8].map(i => (
                  <div key={i} className="bg-white rounded-lg h-32 animate-pulse" />
                ))}
              </>
            ) : (
              categories.map(category => (
                <CategoryCard key={category.id} category={category} />
              ))
            )}
          </div>
        </div>
      </section>

      {/* Popular Activities */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Bestselling activities
              </h2>
              <p className="text-gray-600">
                Our most popular tours and activities
              </p>
            </div>
            <a href="/search?bestseller=true" className="text-primary hover:text-primary-600 flex items-center font-medium">
              See all activities
              <ArrowRight className="w-4 h-4 ml-1" />
            </a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {loading ? (
              <>
                {[1, 2, 3, 4, 5, 6, 7, 8].map(i => (
                  <div key={i} className="bg-white rounded-lg h-96 shadow animate-pulse" />
                ))}
              </>
            ) : (
              popularActivities.map(activity => (
                <ActivityCard key={activity.id} activity={activity} />
              ))
            )}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Become a vendor
          </h2>
          <p className="text-xl text-white mb-8 max-w-2xl mx-auto">
            Join thousands of activity providers and reach millions of travelers worldwide
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/vendor/register" className="btn-secondary">
              List your activity
            </a>
            <a href="/vendor/login" className="bg-white/10 hover:bg-white/20 text-white font-medium py-3 px-6 rounded-full transition-colors">
              Vendor login
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
