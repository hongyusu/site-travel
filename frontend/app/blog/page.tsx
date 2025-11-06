'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Calendar, User, ArrowRight } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

export default function BlogPage() {
  const { getTranslation } = useLanguage();
  
  const posts = [
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
    {
      title: 'Sustainable Travel: Making a Difference',
      excerpt: 'How to explore the world while minimizing your environmental impact...',
      date: 'January 5, 2024',
      author: 'Michael Green',
      category: 'Sustainable Travel',
      image: 'https://picsum.photos/seed/blog-sustainable/800/500',
    },
  ];

  const categories = [
    getTranslation('blog.all_posts'),
    getTranslation('blog.category.destination_guides'),
    getTranslation('blog.category.travel_tips'),
    getTranslation('blog.category.travel_planning'),
    getTranslation('blog.category.sustainable_travel'),
    getTranslation('blog.category.food_culture'),
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">{getTranslation('blog.title')}</h1>
          <p className="text-xl text-white/90 max-w-3xl">
            {getTranslation('blog.subtitle')}
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12">
        {/* Categories */}
        <div className="bg-white rounded-lg shadow p-4 mb-8">
          <div className="flex flex-wrap gap-3">
            {categories.map((category, index) => (
              <button
                key={index}
                className={`px-4 py-2 rounded-full transition-colors ${
                  index === 0
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Featured Post */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden mb-12">
          <div className="grid md:grid-cols-2 gap-0">
            <div className="relative h-64 md:h-auto">
              <Image
                src={posts[0].image}
                alt={posts[0].title}
                fill
                className="object-cover"
              />
            </div>
            <div className="p-8 flex flex-col justify-center">
              <span className="text-primary text-sm font-semibold mb-2">
                {posts[0].category}
              </span>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">{posts[0].title}</h2>
              <p className="text-gray-700 mb-4">{posts[0].excerpt}</p>
              <div className="flex items-center text-sm text-gray-500 mb-4">
                <Calendar className="w-4 h-4 mr-1" />
                <span className="mr-4">{posts[0].date}</span>
                <User className="w-4 h-4 mr-1" />
                <span>{posts[0].author}</span>
              </div>
              <Link href="#" className="text-primary hover:text-primary-600 font-medium flex items-center">
                {getTranslation('blog.read_more')} <ArrowRight className="w-4 h-4 ml-1" />
              </Link>
            </div>
          </div>
        </div>

        {/* Blog Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {posts.slice(1).map((post, index) => (
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
                <h3 className="text-xl font-bold text-gray-900 mt-2 mb-3">{post.title}</h3>
                <p className="text-gray-600 mb-4">{post.excerpt}</p>
                <div className="flex items-center text-sm text-gray-500 mb-3">
                  <Calendar className="w-4 h-4 mr-1" />
                  <span>{post.date}</span>
                </div>
                <Link href="#" className="text-primary hover:text-primary-600 font-medium flex items-center">
                  {getTranslation('blog.read_more')} <ArrowRight className="w-4 h-4 ml-1" />
                </Link>
              </div>
            </div>
          ))}
        </div>

        {/* Newsletter */}
        <div className="bg-primary rounded-lg shadow-lg p-8 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">{getTranslation('blog.newsletter.title')}</h2>
          <p className="text-xl mb-6">
            {getTranslation('blog.newsletter.subtitle')}
          </p>
          <form className="max-w-md mx-auto flex gap-3">
            <input
              type="email"
              placeholder={getTranslation('blog.newsletter.placeholder')}
              className="flex-1 px-4 py-3 rounded-lg text-gray-900"
            />
            <button type="submit" className="btn-secondary whitespace-nowrap">
              {getTranslation('blog.newsletter.subscribe')}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
