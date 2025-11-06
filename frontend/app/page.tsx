'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import SearchBar from '@/components/search/SearchBar';
import DestinationCard from '@/components/destinations/DestinationCard';
import CategoryCard from '@/components/categories/CategoryCard';
import ActivityCard from '@/components/activities/ActivityCard';
import { Activity, Category, Destination } from '@/types';
import { apiClient } from '@/lib/api';
import { ArrowRight, Shield, Clock, Award, Calendar, User } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';
import Link from 'next/link';

export default function HomePage() {
  const [featuredDestinations, setFeaturedDestinations] = useState<Destination[]>([]);
  const [popularActivities, setPopularActivities] = useState<Activity[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const { getTranslation } = useLanguage();

  // Featured blog posts (static data from blog page)
  const featuredBlogPosts = [
    {
      title: '10 Hidden Gems in Rome You Must Visit',
      excerpt: 'Discover the lesser-known attractions that make Rome truly magical...',
      date: 'January 20, 2024',
      author: 'Sarah Mitchell',
      category: 'Destination Guides',
      image: 'https://picsum.photos/seed/blog-rome/800/500',
    },
    {
      title: 'How to Plan the Perfect Family Vacation',
      excerpt: 'Essential tips for creating unforgettable memories with your loved ones...',
      date: 'January 15, 2024',
      author: 'David Chen',
      category: 'Travel Tips',
      image: 'https://picsum.photos/seed/blog-family/800/500',
    },
    {
      title: 'Best Time to Visit European Capitals',
      excerpt: 'Your comprehensive guide to seasonal travel across Europe...',
      date: 'January 10, 2024',
      author: 'Emma Rodriguez',
      category: 'Travel Planning',
      image: 'https://picsum.photos/seed/blog-europe/800/500',
    },
  ];

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
      console.error('Full error details:', error.response || error);
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
            {getTranslation('homepage.hero.title')}
          </h1>
          <p className="text-xl md:text-2xl text-white mb-8 drop-shadow-md">
            {getTranslation('homepage.hero.subtitle')}
          </p>
          <div className="max-w-3xl mx-auto">
            <SearchBar
              placeholder={getTranslation('homepage.search.placeholder')}
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
              <h3 className="font-semibold text-lg mb-2">{getTranslation('homepage.trust.millions.title')}</h3>
              <p className="text-gray-600">{getTranslation('homepage.trust.millions.desc')}</p>
            </div>
            <div className="text-center">
              <Clock className="w-12 h-12 text-primary mx-auto mb-3" />
              <h3 className="font-semibold text-lg mb-2">{getTranslation('homepage.trust.cancellation.title')}</h3>
              <p className="text-gray-600">{getTranslation('homepage.trust.cancellation.desc')}</p>
            </div>
            <div className="text-center">
              <Award className="w-12 h-12 text-primary mx-auto mb-3" />
              <h3 className="font-semibold text-lg mb-2">{getTranslation('homepage.trust.guarantee.title')}</h3>
              <p className="text-gray-600">{getTranslation('homepage.trust.guarantee.desc')}</p>
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
                {getTranslation('homepage.destinations.title')}
              </h2>
              <p className="text-gray-600">
                {getTranslation('homepage.destinations.subtitle')}
              </p>
            </div>
            <a href="/destinations" className="text-primary hover:text-primary-600 flex items-center font-medium">
              {getTranslation('button.view_more')}
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
              {getTranslation('homepage.categories.title')}
            </h2>
            <p className="text-gray-600">
              {getTranslation('homepage.categories.subtitle')}
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
                {getTranslation('homepage.activities.title')}
              </h2>
              <p className="text-gray-600">
                {getTranslation('homepage.activities.subtitle')}
              </p>
            </div>
            <a href="/search?bestseller=true" className="text-primary hover:text-primary-600 flex items-center font-medium">
              {getTranslation('button.view_more')}
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

      {/* Travel Stories */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                {getTranslation('blog.homepage.title')}
              </h2>
              <p className="text-gray-600">
                {getTranslation('blog.homepage.subtitle')}
              </p>
            </div>
            <Link href="/blog" className="text-primary hover:text-primary-600 flex items-center font-medium">
              {getTranslation('blog.homepage.read_blog')}
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {featuredBlogPosts.map((post, index) => (
              <div key={index} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
                <div className="relative h-48">
                  <Image
                    src={post.image}
                    alt={post.title}
                    fill
                    className="object-cover"
                  />
                </div>
                <div className="p-6">
                  <span className="text-primary text-sm font-semibold">{post.category}</span>
                  <h3 className="text-xl font-bold text-gray-900 mt-2 mb-3 line-clamp-2">{post.title}</h3>
                  <p className="text-gray-600 mb-4 line-clamp-2">{post.excerpt}</p>
                  <div className="flex items-center text-sm text-gray-500 mb-3">
                    <Calendar className="w-4 h-4 mr-1" />
                    <span className="mr-4">{post.date}</span>
                    <User className="w-4 h-4 mr-1" />
                    <span>{post.author}</span>
                  </div>
                  <Link href="/blog" className="text-primary hover:text-primary-600 font-medium flex items-center">
                    {getTranslation('blog.read_more')} <ArrowRight className="w-4 h-4 ml-1" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            {getTranslation('homepage.vendor.title')}
          </h2>
          <p className="text-xl text-white mb-8 max-w-2xl mx-auto">
            {getTranslation('homepage.vendor.subtitle')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/vendor/register" className="btn-secondary">
              {getTranslation('homepage.vendor.list_activity')}
            </a>
            <a href="/vendor/login" className="bg-white/10 hover:bg-white/20 text-white font-medium py-3 px-6 rounded-full transition-colors">
              {getTranslation('homepage.vendor.login')}
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
