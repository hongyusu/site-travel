'use client';

import { useEffect, useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { CheckCircle, ArrowLeft, Calendar, Users, MapPin, Clock } from 'lucide-react';
import { apiClient } from '@/lib/api';
import { formatPrice } from '@/lib/utils';
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
  const bookingRef = searchParams.get('ref');

  const [booking, setBooking] = useState<Booking | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!bookingRef) {
      setError('No booking reference provided');
      setLoading(false);
      return;
    }

    const fetchBooking = async () => {
      try {
        const response = await apiClient.bookings.getByRef(bookingRef);
        setBooking(response.data);
      } catch (err) {
        console.error('Error fetching booking:', err);
        setError('Failed to load booking details');
      } finally {
        setLoading(false);
      }
    };

    fetchBooking();
  }, [bookingRef]);

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
          <p className="mt-4 text-gray-600">Loading your booking...</p>
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
            {error || 'Booking not found'}
          </h2>
          <Link href="/" className="text-primary hover:underline">
            Return to homepage
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4">
        {/* Success Header */}
        <div className="bg-white rounded-lg shadow-sm p-8 mb-6 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
            <CheckCircle className="w-10 h-10 text-green-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Booking Confirmed!
          </h1>
          <p className="text-gray-600 mb-4">
            Your booking reference is <span className="font-semibold text-primary">{booking.booking_ref}</span>
          </p>
          <p className="text-sm text-gray-500">
            A confirmation email has been sent to {booking.customer_email}
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Activity Details */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Activity Details</h2>
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
                      {booking.adults} {booking.adults === 1 ? 'Adult' : 'Adults'}
                      {booking.children > 0 && `, ${booking.children} ${booking.children === 1 ? 'Child' : 'Children'}`}
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
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Order Status</h2>
              <OrderTimeline
                bookingStatus={booking.status}
                createdAt={booking.created_at}
                confirmedAt={booking.confirmed_at}
                vendorApprovedAt={booking.vendor_approved_at}
                vendorRejectedAt={booking.vendor_rejected_at}
                cancelledAt={booking.cancelled_at}
                completedAt={booking.completed_at}
                bookingDate={booking.booking_date}
                rejectionReason={booking.rejection_reason}
              />
            </div>

            {/* Special Requirements */}
            {booking.special_requirements && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-3">Special Requirements</h2>
                <p className="text-gray-700">{booking.special_requirements}</p>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Booking Summary */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="font-semibold text-gray-900 mb-4">Booking Summary</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Status</span>
                  <OrderStatusBadge status={booking.status} />
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Reference</span>
                  <span className="font-medium">{booking.booking_ref}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Participants</span>
                  <span className="font-medium">{booking.total_participants}</span>
                </div>
                <div className="border-t pt-3 mt-3">
                  <div className="flex justify-between text-lg font-semibold">
                    <span>Total</span>
                    <span>{formatPrice(booking.total_price)}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Contact Information */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="font-semibold text-gray-900 mb-4">Contact Information</h3>
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
                View All Orders
              </Link>
              <Link
                href="/"
                className="btn-secondary w-full text-center flex items-center justify-center"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Continue Shopping
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function OrderConfirmationPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    }>
      <OrderConfirmationContent />
    </Suspense>
  );
}
