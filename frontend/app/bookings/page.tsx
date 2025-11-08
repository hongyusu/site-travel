'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { Calendar, MapPin, Users, Clock, CheckCircle, XCircle, Star } from 'lucide-react';
import { Booking } from '@/types';
import { apiClient } from '@/lib/api';
import { getImageUrl } from '@/lib/utils';
import { useLocation } from '@/contexts/LocationContext';
import ReviewForm from '@/components/reviews/ReviewForm';
import { useLanguage } from '@/contexts/LanguageContext';

export default function BookingsPage() {
  const { getTranslation } = useLanguage();
  const { formatPrice } = useLocation();
  const searchParams = useSearchParams();
  const success = searchParams.get('success');
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [reviewBooking, setReviewBooking] = useState<Booking | null>(null);

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        // Guest checkout - show success message
        setLoading(false);
        return;
      }

      const response = await apiClient.bookings.list();
      setBookings(response.data.data);
    } catch (error) {
      console.error('Error fetching bookings:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed':
        return 'bg-success-light text-success';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      case 'completed':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'confirmed':
        return getTranslation('bookings.status_confirmed');
      case 'pending':
        return getTranslation('bookings.status_pending');
      case 'cancelled':
        return getTranslation('bookings.status_cancelled');
      case 'completed':
        return getTranslation('bookings.status_completed');
      default:
        return status.charAt(0).toUpperCase() + status.slice(1);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8" />
            {[1, 2, 3].map(i => (
              <div key={i} className="h-48 bg-gray-200 rounded" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Show success message for guest checkout
  if (success && bookings.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md text-center">
          <CheckCircle className="w-16 h-16 text-success mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            {getTranslation('bookings.booking_confirmed')}
          </h1>
          <p className="text-gray-600 mb-6">
            {getTranslation('bookings.confirmation_email_sent')}
          </p>
          <div className="space-y-3">
            <Link href="/search" className="btn-primary w-full block">
              {getTranslation('bookings.book_more_activities')}
            </Link>
            <Link href="/" className="block text-primary hover:text-primary-600">
              {getTranslation('bookings.return_to_homepage')}
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        {success && (
          <div className="bg-success-light border border-success text-success px-6 py-4 rounded-lg mb-8 flex items-center">
            <CheckCircle className="w-6 h-6 mr-3 flex-shrink-0" />
            <p>{getTranslation('bookings.confirmation_success')}</p>
          </div>
        )}

        <h1 className="text-3xl font-bold text-gray-900 mb-8">{getTranslation('bookings.title')}</h1>

        {bookings.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <Calendar className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              {getTranslation('bookings.no_bookings_yet')}
            </h2>
            <p className="text-gray-600 mb-6">
              {getTranslation('bookings.start_exploring')}
            </p>
            <Link href="/search" className="btn-primary">
              {getTranslation('bookings.browse_activities')}
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {bookings.map((booking) => (
              <div key={booking.id} className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(booking.status)}`}>
                        {getStatusText(booking.status)}
                      </span>
                      <p className="text-sm text-gray-500 mt-2">
                        {getTranslation('bookings.booking_reference')}: {booking.booking_ref}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-gray-900">
                        {formatPrice(booking.total_price)}
                      </div>
                      <div className="text-sm text-gray-500">{booking.currency}</div>
                    </div>
                  </div>

                  <div className="flex gap-6">
                    {/* Activity Image */}
                    <div className="relative w-48 h-32 flex-shrink-0 rounded-lg overflow-hidden">
                      <Image
                        src={getImageUrl(booking.activity.primary_image)}
                        alt={booking.activity.title}
                        fill
                        className="object-cover"
                      />
                    </div>

                    {/* Details */}
                    <div className="flex-1">
                      <Link
                        href={`/activities/${booking.activity.slug}`}
                        className="text-xl font-semibold text-gray-900 hover:text-primary mb-3 block"
                      >
                        {booking.activity.title}
                      </Link>

                      <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                        <div className="flex items-center">
                          <Calendar className="w-4 h-4 mr-2 text-gray-400" />
                          {new Date(booking.booking_date).toLocaleDateString('en-US', {
                            weekday: 'long',
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                          })}
                        </div>

                        {booking.booking_time && (
                          <div className="flex items-center">
                            <Clock className="w-4 h-4 mr-2 text-gray-400" />
                            {booking.booking_time}
                          </div>
                        )}

                        <div className="flex items-center">
                          <Users className="w-4 h-4 mr-2 text-gray-400" />
                          {booking.adults} {booking.adults > 1 ? getTranslation('bookings.adults') : getTranslation('bookings.adult')}
                          {booking.children > 0 && `, ${booking.children} ${booking.children > 1 ? getTranslation('bookings.children') : getTranslation('bookings.child')}`}
                        </div>

                        {booking.activity.duration_minutes && (
                          <div className="flex items-center">
                            <Clock className="w-4 h-4 mr-2 text-gray-400" />
                            {getTranslation('bookings.duration')}: {Math.floor(booking.activity.duration_minutes / 60)}h {booking.activity.duration_minutes % 60}m
                          </div>
                        )}
                      </div>

                      {booking.special_requirements && (
                        <div className="mt-3 p-3 bg-gray-50 rounded text-sm">
                          <strong className="text-gray-700">{getTranslation('bookings.special_requirements')}:</strong>
                          <p className="text-gray-600 mt-1">{booking.special_requirements}</p>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="mt-6 pt-6 border-t flex gap-3">
                    {booking.status === 'confirmed' && (
                      <>
                        <Link
                          href={`/order-confirmation?ref=${booking.booking_ref}`}
                          className="btn-secondary flex-1"
                        >
                          {getTranslation('bookings.view_details')}
                        </Link>
                        <button className="btn-secondary text-red-600 hover:bg-red-50">
                          {getTranslation('bookings.cancel_booking')}
                        </button>
                      </>
                    )}
                    {booking.status === 'completed' && (
                      <button
                        onClick={() => setReviewBooking(booking)}
                        className="btn-primary flex items-center justify-center"
                      >
                        <Star className="w-4 h-4 mr-2" />
                        {getTranslation('bookings.leave_review')}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Review Form Modal */}
        {reviewBooking && (
          <ReviewForm
            activityId={reviewBooking.activity.id}
            bookingId={reviewBooking.id}
            onClose={() => setReviewBooking(null)}
            onSuccess={() => {
              setReviewBooking(null);
              // Optionally refresh bookings to update any review status
              fetchBookings();
            }}
          />
        )}
      </div>
    </div>
  );
}