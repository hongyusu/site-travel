'use client';

import Link from 'next/link';
import { Users, Globe, Award, Heart } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

export default function AboutPage() {
  const { getTranslation } = useLanguage();
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">{getTranslation('about.title')}</h1>
          <p className="text-xl text-white/90 max-w-3xl">
            {getTranslation('about.hero_subtitle')}
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-12">
        {/* Mission Section */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">{getTranslation('about.mission_title')}</h2>
          <p className="text-lg text-gray-700 mb-4">
            {getTranslation('about.mission_p1')}
          </p>
          <p className="text-lg text-gray-700">
            {getTranslation('about.mission_p2')}
          </p>
        </div>

        {/* Values */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <Users className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">{getTranslation('about.value_community')}</h3>
            <p className="text-gray-600">
              {getTranslation('about.value_community_desc')}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6 text-center">
            <Globe className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">{getTranslation('about.value_global')}</h3>
            <p className="text-gray-600">
              {getTranslation('about.value_global_desc')}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6 text-center">
            <Award className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">{getTranslation('about.value_quality')}</h3>
            <p className="text-gray-600">
              {getTranslation('about.value_quality_desc')}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6 text-center">
            <Heart className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">{getTranslation('about.value_passion')}</h3>
            <p className="text-gray-600">
              {getTranslation('about.value_passion_desc')}
            </p>
          </div>
        </div>

        {/* Story */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">{getTranslation('about.story_title')}</h2>
          <p className="text-lg text-gray-700 mb-4">
            {getTranslation('about.story_p1')}
          </p>
          <p className="text-lg text-gray-700 mb-4">
            {getTranslation('about.story_p2')}
          </p>
        </div>

        {/* Stats */}
        <div className="grid md:grid-cols-4 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-4xl font-bold text-primary mb-2">150K+</div>
            <div className="text-gray-600">{getTranslation('about.stat_activities')}</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-4xl font-bold text-primary mb-2">500+</div>
            <div className="text-gray-600">{getTranslation('about.stat_destinations')}</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-4xl font-bold text-primary mb-2">10M+</div>
            <div className="text-gray-600">{getTranslation('about.stat_travelers')}</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-4xl font-bold text-primary mb-2">5K+</div>
            <div className="text-gray-600">{getTranslation('about.stat_vendors')}</div>
          </div>
        </div>

        {/* CTA */}
        <div className="bg-primary rounded-lg shadow-lg p-8 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">{getTranslation('about.cta_title')}</h2>
          <p className="text-xl mb-6">{getTranslation('about.cta_subtitle')}</p>
          <Link href="/" className="btn-secondary inline-block">
            {getTranslation('about.cta_button')}
          </Link>
        </div>
      </div>
    </div>
  );
}
