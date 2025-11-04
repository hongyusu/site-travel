'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import { ActivityDetailResponse } from '@/types';
import BookingWidget from '@/components/booking/BookingWidget';
import ActivityCard from '@/components/activities/ActivityCard';
import ReviewsSection from '@/components/reviews/ReviewsSection';
import Breadcrumbs from '@/components/layout/Breadcrumbs';
import TimelineSection from '@/components/activities/TimelineSection';
import ActivityBadges from '@/components/activities/ActivityBadges';
import ActivityVideo from '@/components/activities/ActivityVideo';
import TranslationNotAvailable from '@/components/TranslationNotAvailable';
import { useLanguage } from '@/contexts/LanguageContext';
import {
  Star, Clock, Users, Globe, Check, X, MapPin,
  ChevronDown, ChevronUp, Shield, Award
} from 'lucide-react';

export default function ActivityDetailsPage() {
  const params = useParams();
  const slug = params.slug as string;
  const { language, getTranslation, getDestinationName, getCategoryName, getLanguageName } = useLanguage();
  const [activity, setActivity] = useState<ActivityDetailResponse | null>(null);
  const [similarActivities, setSimilarActivities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(0);
  const [expandedFAQs, setExpandedFAQs] = useState<number[]>([]);

  useEffect(() => {
    fetchActivity();
  }, [slug, language]);

  const fetchActivity = async () => {
    try {
      const response = await apiClient.activities.getBySlug(slug);
      setActivity(response.data);

      // Fetch similar activities
      if (response.data.id) {
        try {
          const similarResponse = await apiClient.activities.getSimilar(response.data.id);
          setSimilarActivities(similarResponse.data);
        } catch (error) {
          console.error('Error fetching similar activities:', error);
        }
      }
    } catch (error) {
      console.error('Error fetching activity:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleFAQ = (index: number) => {
    setExpandedFAQs(prev =>
      prev.includes(index)
        ? prev.filter(i => i !== index)
        : [...prev, index]
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="animate-pulse">
          <div className="h-96 bg-gray-200" />
          <div className="container mx-auto px-4 py-8">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-4">
                <div className="h-8 bg-gray-200 rounded w-3/4" />
                <div className="h-4 bg-gray-200 rounded w-1/2" />
                <div className="h-32 bg-gray-200 rounded" />
              </div>
              <div className="h-96 bg-gray-200 rounded" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!activity) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Activity not found</h2>
          <p className="text-gray-600 mb-6">The activity you're looking for doesn't exist.</p>
          <Link href="/search" className="btn-primary">
            Browse Activities
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Image Gallery */}
      <div className="bg-black">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 py-4">
            <div className="relative h-96 lg:h-[500px]">
              <Image
                src={activity.images[selectedImage]?.url || '/placeholder-activity.jpg'}
                alt={activity.title}
                fill
                className="object-cover rounded-lg"
                unoptimized
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              {activity.images.slice(0, 4).map((image, index) => (
                <div
                  key={image.id}
                  className={`relative h-40 lg:h-60 cursor-pointer rounded-lg overflow-hidden ${
                    selectedImage === index ? 'ring-4 ring-primary' : ''
                  }`}
                  onClick={() => setSelectedImage(index)}
                >
                  <Image
                    src={image.url}
                    alt={`${activity.title} - Image ${index + 1}`}
                    fill
                    className="object-cover hover:scale-110 transition-transform"
                    unoptimized
                  />
                  {index === 3 && activity.images.length > 4 && (
                    <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
                      <span className="text-white text-2xl font-bold">
                        +{activity.images.length - 4}
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Breadcrumbs */}
        <Breadcrumbs
          items={[
            { label: activity.destinations[0] ? getDestinationName(activity.destinations[0].slug, activity.destinations[0].name) : 'Activities', href: activity.destinations[0] ? `/search?destination=${activity.destinations[0].slug}` : '/search' },
            { label: activity.categories[0] ? getCategoryName(activity.categories[0].slug, activity.categories[0].name) : 'Category', href: activity.categories[0] ? `/search?category=${activity.categories[0].slug}` : undefined },
            { label: activity.title }
          ]}
        />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Title and Key Info */}
            <div>
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">
                    {activity.title}
                  </h1>
                  <div className="flex items-center space-x-4 text-sm mb-3">
                    {activity.destinations.map(dest => (
                      <Link
                        key={dest.id}
                        href={`/search?destination=${dest.slug}`}
                        className="text-primary hover:text-primary-600"
                      >
                        {getDestinationName(dest.slug, dest.name)}
                      </Link>
                    ))}
                  </div>

                  {/* Badges */}
                  <div className="flex flex-wrap gap-2">
                    {activity.is_bestseller && (
                      <span className="badge bg-orange-100 text-orange-800 font-semibold">
                        <Award className="w-3 h-3 mr-1" />
                        {getTranslation('badge.bestseller')}
                      </span>
                    )}
                    {activity.is_skip_the_line && (
                      <span className="badge bg-purple-100 text-purple-800">
                        {getTranslation('badge.skip_the_line')}
                      </span>
                    )}
                    {activity.free_cancellation_hours > 0 && (
                      <span className="badge bg-green-100 text-green-800">
                        <Check className="w-3 h-3 mr-1" />
                        {getTranslation('badge.free_cancellation')}
                      </span>
                    )}
                    {activity.instant_confirmation && (
                      <span className="badge bg-blue-100 text-blue-800">
                        <Shield className="w-3 h-3 mr-1" />
                        {getTranslation('badge.instant_confirmation')}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Ratings and Reviews */}
              <div className="flex items-center space-x-6 mb-4">
                <div className="flex items-center">
                  <Star className="w-5 h-5 text-yellow-400 fill-current" />
                  <span className="ml-1 font-semibold">{activity.average_rating}</span>
                  <span className="ml-1 text-gray-600">
                    ({activity.total_reviews} reviews)
                  </span>
                </div>
                <div className="text-gray-600">
                  {activity.total_bookings}+ {getTranslation('activity.booked')}
                </div>
              </div>

              {/* Quick Info */}
              <div className="flex flex-wrap gap-4">
                <div className="flex items-center text-gray-600">
                  <Clock className="w-4 h-4 mr-1" />
                  {Math.floor(activity.duration_minutes / 60)}h {activity.duration_minutes % 60}m
                </div>
                <div className="flex items-center text-gray-600">
                  <Users className="w-4 h-4 mr-1" />
                  {getTranslation('booking.max_people')} {activity.max_group_size} {getTranslation('booking.people')}
                </div>
                <div className="flex items-center text-gray-600">
                  <Globe className="w-4 h-4 mr-1" />
                  {activity.languages.map(lang => getLanguageName(lang)).join(', ')}
                </div>
              </div>
            </div>

            {/* Description */}
            <div className="prose max-w-none">
              <h3 className="text-xl font-semibold mb-4">{getTranslation('activity.overview')}</h3>
              {activity.description ? (
                <p className="text-gray-700 whitespace-pre-line">
                  {activity.description}
                </p>
              ) : (
                <TranslationNotAvailable fieldName={getTranslation('activity.overview')} />
              )}
            </div>

            {/* Activity Badges */}
            <ActivityBadges activity={activity} />

            {/* Video Preview */}
            {activity.video_url && (
              <ActivityVideo videoUrl={activity.video_url} title={activity.title} />
            )}

            {/* Timeline/What to Expect */}
            {activity.timelines && activity.timelines.length > 0 && (
              <TimelineSection timelines={activity.timelines} />
            )}

            {/* Highlights */}
            <div>
              <h3 className="text-xl font-semibold mb-4">{getTranslation('activity.highlights')}</h3>
              {activity.highlights && activity.highlights.length > 0 ? (
                <ul className="space-y-2">
                  {activity.highlights.map((highlight, index) => (
                    <li key={index} className="flex items-start">
                      <Check className="w-5 h-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700">{highlight.text}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <TranslationNotAvailable fieldName="Highlights" />
              )}
            </div>

            {/* What's Included / Not Included */}
            <div>
              <h3 className="text-xl font-semibold mb-4">{getTranslation('activity.included')}</h3>
              {activity.includes && activity.includes.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium text-green-700 mb-2">{getTranslation('activity.included')}</h4>
                    <ul className="space-y-2">
                      {activity.includes
                        .filter(item => item.is_included)
                        .map((item, index) => (
                          <li key={index} className="flex items-start">
                            <Check className="w-4 h-4 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                            <span className="text-gray-700 text-sm">{item.item}</span>
                          </li>
                        ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium text-red-700 mb-2">{getTranslation('activity.excluded')}</h4>
                    <ul className="space-y-2">
                      {activity.includes
                        .filter(item => !item.is_included)
                        .map((item, index) => (
                          <li key={index} className="flex items-start">
                            <X className="w-4 h-4 text-red-500 mr-2 flex-shrink-0 mt-0.5" />
                            <span className="text-gray-700 text-sm">{item.item}</span>
                          </li>
                        ))}
                    </ul>
                  </div>
                </div>
              ) : (
                <TranslationNotAvailable fieldName="What's included" />
              )}
            </div>

            {/* Additional Information */}
            {(activity.what_to_bring || activity.not_suitable_for || activity.dress_code || activity.covid_measures) && (
              <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
                <h3 className="text-xl font-semibold mb-4">{getTranslation('activity.important_info')}</h3>
                <div className="space-y-4">
                  {activity.what_to_bring && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">{getTranslation('activity.what_to_bring')}</h4>
                      <p className="text-gray-700 whitespace-pre-line">{activity.what_to_bring}</p>
                    </div>
                  )}
                  {activity.not_suitable_for && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">{getTranslation('activity.not_suitable_for')}</h4>
                      <p className="text-gray-700 whitespace-pre-line">{activity.not_suitable_for}</p>
                    </div>
                  )}
                  {activity.dress_code && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">{getTranslation('activity.dress_code')}</h4>
                      <p className="text-gray-700 whitespace-pre-line">{activity.dress_code}</p>
                    </div>
                  )}
                  {activity.covid_measures && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">{getTranslation('activity.covid_measures')}</h4>
                      <p className="text-gray-700 whitespace-pre-line">{activity.covid_measures}</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Meeting Point */}
            {activity.meeting_point && (
              <div>
                <h3 className="text-xl font-semibold mb-4">{getTranslation('activity.meeting_point')}</h3>
                <div className="bg-white rounded-lg p-4 border border-gray-200">
                  <div className="flex items-start mb-2">
                    <MapPin className="w-5 h-5 text-primary mr-2 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium text-gray-900">
                        {activity.meeting_point.address}
                      </p>
                      {activity.meeting_point.instructions && (
                        <p className="text-sm text-gray-600 mt-1">
                          {activity.meeting_point.instructions}
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Meeting Point Photos */}
                  {activity.meeting_point.photos && activity.meeting_point.photos.length > 0 && (
                    <div className="mt-4">
                      <h4 className="font-medium text-gray-900 mb-3">{getTranslation('activity.meeting_point_photos')}</h4>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                        {activity.meeting_point.photos.map((photo: any, index: number) => (
                          <div key={index} className="relative h-32 rounded-lg overflow-hidden border border-gray-200">
                            <Image
                              src={photo.url}
                              alt={photo.caption || `Meeting point photo ${index + 1}`}
                              fill
                              className="object-cover"
                              unoptimized
                            />
                            {photo.caption && (
                              <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-xs p-2">
                                {photo.caption}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Map */}
                  {activity.meeting_point.latitude && activity.meeting_point.longitude ? (
                    <div className="h-64 rounded-lg mt-3 overflow-hidden border border-gray-200">
                      <iframe
                        width="100%"
                        height="100%"
                        frameBorder="0"
                        scrolling="no"
                        src={`https://www.openstreetmap.org/export/embed.html?bbox=${activity.meeting_point.longitude-0.005},${activity.meeting_point.latitude-0.005},${activity.meeting_point.longitude+0.005},${activity.meeting_point.latitude+0.005}&layer=mapnik&marker=${activity.meeting_point.latitude},${activity.meeting_point.longitude}`}
                        style={{ border: 0 }}
                        title="Meeting point location"
                      />
                    </div>
                  ) : (
                    <div className="h-48 bg-gray-100 rounded-lg mt-3 flex items-center justify-center">
                      <span className="text-gray-500">{getTranslation('activity.map_not_available')}</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* FAQs */}
            <div>
              <h3 className="text-xl font-semibold mb-4">{getTranslation('activity.faqs')}</h3>
              {activity.faqs && activity.faqs.length > 0 ? (
                <div className="space-y-3">
                  {activity.faqs.map((faq, index) => (
                    <div key={index} className="bg-white rounded-lg border border-gray-200">
                      <button
                        onClick={() => toggleFAQ(index)}
                        className="w-full px-4 py-3 text-left flex items-center justify-between hover:bg-gray-50"
                      >
                        <span className="font-medium text-gray-900">
                          {faq.question}
                        </span>
                        {expandedFAQs.includes(index) ? (
                          <ChevronUp className="w-5 h-5 text-gray-500" />
                        ) : (
                          <ChevronDown className="w-5 h-5 text-gray-500" />
                        )}
                      </button>
                      {expandedFAQs.includes(index) && (
                        <div className="px-4 pb-3">
                          <p className="text-gray-700">{faq.answer}</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <TranslationNotAvailable fieldName="FAQs" />
              )}
            </div>

            {/* Vendor Info */}
            <div className="bg-white rounded-lg p-6 border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold">{getTranslation('activity.provider')}</h3>
                {activity.vendor.is_verified && (
                  <div className="flex items-center text-green-600">
                    <Shield className="w-4 h-4 mr-1" />
                    <span className="text-sm">{getTranslation('activity.verified')}</span>
                  </div>
                )}
              </div>
              <p className="font-medium text-gray-900">{activity.vendor.company_name}</p>
            </div>

            {/* Reviews Section */}
            <div className="mt-8">
              <ReviewsSection
                activityId={activity.id}
                averageRating={activity.average_rating}
                totalReviews={activity.total_reviews}
              />
            </div>
          </div>

          {/* Sidebar - Booking Widget */}
          <div className="lg:col-span-1">
            <div className="sticky top-4">
              <BookingWidget activity={activity} />
            </div>
          </div>
        </div>

        {/* Similar Activities */}
        {similarActivities.length > 0 && (
          <div className="mt-16">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              {getTranslation('activity.similar')}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {similarActivities.slice(0, 4).map(activity => (
                <ActivityCard key={activity.id} activity={activity} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}