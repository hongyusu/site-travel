'use client';

import Link from 'next/link';
import { Briefcase, MapPin, Clock, Heart, Users, Zap } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

export default function CareersPage() {
  const { getTranslation } = useLanguage();
  
  const openings = [
    {
      title: getTranslation('careers.job_senior_fullstack'),
      department: getTranslation('careers.job_engineering'),
      location: getTranslation('careers.job_remote'),
      type: getTranslation('careers.job_fulltime'),
    },
    {
      title: getTranslation('careers.job_product_manager'),
      department: getTranslation('careers.job_product'),
      location: 'San Francisco, CA',
      type: getTranslation('careers.job_fulltime'),
    },
    {
      title: getTranslation('careers.job_customer_success_manager'),
      department: getTranslation('careers.job_customer_success'),
      location: 'New York, NY',
      type: getTranslation('careers.job_fulltime'),
    },
    {
      title: getTranslation('careers.job_marketing_manager'),
      department: getTranslation('careers.job_marketing'),
      location: getTranslation('careers.job_remote'),
      type: getTranslation('careers.job_fulltime'),
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">{getTranslation('careers.title')}</h1>
          <p className="text-xl text-white/90 max-w-3xl">
            {getTranslation('careers.hero_subtitle')}
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12">
        {/* Why Work With Us */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">{getTranslation('careers.why_work_title')}</h2>

          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <Heart className="w-12 h-12 text-primary mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">{getTranslation('careers.passion_travel')}</h3>
              <p className="text-gray-600">
                {getTranslation('careers.passion_travel_desc')}
              </p>
            </div>

            <div className="text-center">
              <Users className="w-12 h-12 text-primary mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">{getTranslation('careers.collaborative_culture')}</h3>
              <p className="text-gray-600">
                {getTranslation('careers.collaborative_culture_desc')}
              </p>
            </div>

            <div className="text-center">
              <Zap className="w-12 h-12 text-primary mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">{getTranslation('careers.growth_opportunities')}</h3>
              <p className="text-gray-600">
                {getTranslation('careers.growth_opportunities_desc')}
              </p>
            </div>
          </div>
        </div>

        {/* Benefits */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">{getTranslation('careers.benefits_title')}</h2>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <ul className="space-y-3">
                <li className="flex items-start">
                  <span className="text-primary mr-2">✓</span>
                  <span className="text-gray-700">{getTranslation('careers.benefit_salary')}</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary mr-2">✓</span>
                  <span className="text-gray-700">{getTranslation('careers.benefit_insurance')}</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary mr-2">✓</span>
                  <span className="text-gray-700">{getTranslation('careers.benefit_flexible')}</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary mr-2">✓</span>
                  <span className="text-gray-700">{getTranslation('careers.benefit_pto')}</span>
                </li>
              </ul>
            </div>
            <div>
              <ul className="space-y-3">
                <li className="flex items-start">
                  <span className="text-primary mr-2">✓</span>
                  <span className="text-gray-700">{getTranslation('careers.benefit_travel')}</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary mr-2">✓</span>
                  <span className="text-gray-700">{getTranslation('careers.benefit_development')}</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary mr-2">✓</span>
                  <span className="text-gray-700">{getTranslation('careers.benefit_401k')}</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary mr-2">✓</span>
                  <span className="text-gray-700">{getTranslation('careers.benefit_parental')}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Open Positions */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">{getTranslation('careers.open_positions')}</h2>

          {openings.length > 0 ? (
            <div className="space-y-4">
              {openings.map((job, index) => (
                <div
                  key={index}
                  className="border border-gray-200 rounded-lg p-6 hover:border-primary transition-colors"
                >
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                    <div className="mb-4 md:mb-0">
                      <h3 className="text-xl font-bold text-gray-900 mb-2">{job.title}</h3>
                      <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                        <span className="flex items-center">
                          <Briefcase className="w-4 h-4 mr-1" />
                          {job.department}
                        </span>
                        <span className="flex items-center">
                          <MapPin className="w-4 h-4 mr-1" />
                          {job.location}
                        </span>
                        <span className="flex items-center">
                          <Clock className="w-4 h-4 mr-1" />
                          {job.type}
                        </span>
                      </div>
                    </div>
                    <button className="btn-primary whitespace-nowrap">
                      {getTranslation('careers.apply_now')}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600 text-center py-8">
              {getTranslation('careers.no_openings')}
            </p>
          )}
        </div>

        {/* CTA */}
        <div className="bg-primary rounded-lg shadow-lg p-8 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">{getTranslation('careers.cta_title')}</h2>
          <p className="text-xl mb-6">
            {getTranslation('careers.cta_subtitle')}
          </p>
          <a href="mailto:careers@findtravelmate.com" className="btn-secondary inline-block">
            {getTranslation('careers.get_in_touch')}
          </a>
        </div>
      </div>
    </div>
  );
}
