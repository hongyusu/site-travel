'use client';

import { useEffect, useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { CheckCircle, ArrowLeft, Calendar, Users, MapPin, Clock } from 'lucide-react';
import { apiClient } from '@/lib/api';
import { useLocation } from '@/contexts/LocationContext';
import { useLanguage } from '@/contexts/LanguageContext';
import OrderTimeline from '@/components/orders/OrderTimeline';
import OrderStatusBadge from '@/components/orders/OrderStatusBadge';
import Image from 'next/image';

interface Booking {
  id: number;
  booking_ref: string;
  activity: {
    id: number;
    title: string;
    slug: string;
    primary_image: string | null;
    duration_minutes: number;
  };
  booking_date: string;
  booking_time: string | null;
  adults: number;
  children: number;
  total_participants: number;
  total_price: number;
  currency: string;
  status: 'pending' | 'pending_vendor_approval' | 'confirmed' | 'rejected' | 'cancelled' | 'completed';
  customer_name: string;
  customer_email: string;
  customer_phone: string | null;
  special_requirements: string | null;
  created_at: string;
  confirmed_at: string | null;
  vendor_approved_at?: string | null;
  vendor_rejected_at?: string | null;
  cancelled_at?: string | null;
  completed_at?: string | null;
  rejection_reason?: string | null;
}

function OrderConfirmationContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { formatPrice } = useLocation();
  const { getTranslation } = useLanguage();
  const bookingRef = searchParams.get('ref');
  const sessionId = searchParams.get('session_id');

  const [booking, setBooking] = useState<Booking | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const run = async () => {
      try {
        let ref = bookingRef;

        // Returning from Stripe Checkout: confirm the payment (which creates
        // the bookings) and use the resulting reference.
        if (!ref && sessionId) {
          const conf = await apiClient.payments.confirm(sessionId);
          ref = conf.data?.first_ref || null;
        }

        if (!ref) {
          if (!cancelled) setError(getTranslation('oc.not_found'));
          return;
        }

        const response = await apiClient.bookings.getByRef(ref);
        if (!cancelled) setBooking(response.data);
      } catch (err) {
        console.error('Error loading confirmation:', err);
        if (!cancelled) setError(getTranslation('oc.not_found'));
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    run();
    return () => {
      cancelled = true;
    };
  }, [bookingRef, sessionId]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatTime = (timeString: string | null) => {
    if (!timeString) return null;
    const time = new Date(`2000-01-01T${timeString}`);
    return time.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">{getTranslation('oc.loading')}</p>
        </div>
      </div>
    );
  }

  if (error || !booking) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            {error || getTranslation('oc.not_found')}
          </h2>
          <Link href="/" className="text-primary hover:underline">
            {getTranslation('oc.return_home')}
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4">
        {/* Success Header */}
        <div className="bg-paper rounded-lg shadow-sm p-8 mb-6 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
            <CheckCircle className="w-10 h-10 text-green-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {getTranslation('oc.confirmed')}
          </h1>
          <p className="text-gray-600 mb-4">
            {getTranslation('oc.reference_is')} <span className="font-semibold text-primary">{booking.booking_ref}</span>
          </p>
          <p className="text-sm text-gray-500">
            {getTranslation('oc.email_sent')} {booking.customer_email}
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Activity Details */}
            <div className="bg-paper rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">{getTranslation('oc.activity_details')}</h2>
              <div className="flex gap-4">
                {booking.activity.primary_image && (
                  <div className="w-32 h-32 rounded-lg overflow-hidden flex-shrink-0">
                    <Image
                      src={booking.activity.primary_image}
                      alt={booking.activity.title}
                      width={128}
                      height={128}
                      className="w-full h-full object-cover"
                      unoptimized
                    />
                  </div>
                )}
                <div className="flex-1">
                  <h3 className="font-semibold text-lg text-gray-900 mb-2">
                    {booking.activity.title}
                  </h3>
                  <div className="space-y-2 text-sm text-gray-600">
                    <div className="flex items-center">
                      <Calendar className="w-4 h-4 mr-2" />
                      {formatDate(booking.booking_date)}
                      {booking.booking_time && ` at ${formatTime(booking.booking_time)}`}
                    </div>
                    <div className="flex items-center">
                      <Users className="w-4 h-4 mr-2" />
                      {booking.adults} {booking.adults === 1 ? getTranslation('common.adult') : getTranslation('common.adults')}
                      {booking.children > 0 && `, ${booking.children} ${booking.children === 1 ? getTranslation('common.child') : getTranslation('common.children')}`}
                    </div>
                    {booking.activity.duration_minutes && (
                      <div className="flex items-center">
                        <Clock className="w-4 h-4 mr-2" />
                        {Math.floor(booking.activity.duration_minutes / 60)}h {booking.activity.duration_minutes % 60}m
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Order Timeline */}
            <div className="bg-paper rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">{getTranslation('oc.order_status')}</h2>
              <OrderTimeline
                bookingStatus={booking.status}
                createdAt={booking.created_at}
                confirmedAt={booking.confirmed_at ?? undefined}
                vendorApprovedAt={booking.vendor_approved_at ?? undefined}
                vendorRejectedAt={booking.vendor_rejected_at ?? undefined}
                cancelledAt={booking.cancelled_at ?? undefined}
                completedAt={booking.completed_at ?? undefined}
                bookingDate={booking.booking_date}
                rejectionReason={booking.rejection_reason ?? undefined}
              />
            </div>

            {/* Special Requirements */}
            {booking.special_requirements && (
              <div className="bg-paper rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-3">{getTranslation('oc.special_requirements')}</h2>
                <p className="text-gray-700">{booking.special_requirements}</p>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Booking Summary */}
            <div className="bg-paper rounded-lg shadow-sm p-6">
              <h3 className="font-semibold text-gray-900 mb-4">{getTranslation('oc.booking_summary')}</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">{getTranslation('oc.status')}</span>
                  <OrderStatusBadge status={booking.status} />
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">{getTranslation('oc.reference')}</span>
                  <span className="font-medium">{booking.booking_ref}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">{getTranslation('oc.participants')}</span>
                  <span className="font-medium">{booking.total_participants}</span>
                </div>
                <div className="border-t pt-3 mt-3">
                  <div className="flex justify-between text-lg font-semibold">
                    <span>{getTranslation('oc.total')}</span>
                    <span>{formatPrice(booking.total_price)}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Contact Information */}
            <div className="bg-paper rounded-lg shadow-sm p-6">
              <h3 className="font-semibold text-gray-900 mb-4">{getTranslation('oc.contact_info')}</h3>
              <div className="space-y-2 text-sm text-gray-600">
                <div>
                  <div className="font-medium text-gray-900">{booking.customer_name}</div>
                  <div>{booking.customer_email}</div>
                  {booking.customer_phone && <div>{booking.customer_phone}</div>}
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="space-y-3">
              <Link
                href="/orders"
                className="btn-primary w-full text-center block"
              >
                {getTranslation('oc.view_all_orders')}
              </Link>
              <Link
                href="/"
                className="btn-secondary w-full text-center flex items-center justify-center"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                {getTranslation('oc.continue_shopping')}
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function OrderConfirmationPage() {
  const { getTranslation } = useLanguage();
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">{getTranslation('oc.loading_short')}</p>
        </div>
      </div>
    }>
      <OrderConfirmationContent />
    </Suspense>
  );
}
