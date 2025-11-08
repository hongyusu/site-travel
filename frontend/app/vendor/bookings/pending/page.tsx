'use client';

import { useEffect, useState } from 'react';
import { Calendar, Users, Mail, Phone, CheckCircle, XCircle, Clock } from 'lucide-react';
import { apiClient } from '@/lib/api';
import { useLocation } from '@/contexts/LocationContext';
import OrderStatusBadge from '@/components/orders/OrderStatusBadge';
import RejectBookingModal from '@/components/vendor/RejectBookingModal';
import { toast } from 'react-hot-toast';
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
  status: string;
  customer_name: string;
  customer_email: string;
  customer_phone: string | null;
  special_requirements: string | null;
  created_at: string;
}

export default function VendorPendingBookingsPage() {
  const { formatPrice } = useLocation();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [rejectModal, setRejectModal] = useState<{ bookingId: number; bookingRef: string; activityTitle: string } | null>(null);

  useEffect(() => {
    fetchPendingBookings();
  }, []);

  const fetchPendingBookings = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/bookings/vendor/bookings', {
        params: {
          status: 'pending_vendor_approval',
          per_page: 100
        }
      });
      const bookingsData = response.data?.data || [];
      setBookings(bookingsData);
    } catch (error) {
      console.error('Error fetching pending bookings:', error);
      toast.error('Failed to load pending bookings');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (bookingId: number) => {
    try {
      await apiClient.patch(`/bookings/vendor/${bookingId}/approve`);
      toast.success('Booking approved successfully');
      fetchPendingBookings();
    } catch (error) {
      console.error('Error approving booking:', error);
      toast.error('Failed to approve booking');
    }
  };

  const handleReject = async (bookingId: number, reason: string) => {
    try {
      await apiClient.patch(`/bookings/vendor/${bookingId}/reject`, null, {
        params: { rejection_reason: reason }
      });
      toast.success('Booking rejected');
      setRejectModal(null);
      fetchPendingBookings();
    } catch (error) {
      console.error('Error rejecting booking:', error);
      toast.error('Failed to reject booking');
    }
  };

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
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading pending bookings...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Pending Bookings</h1>
          <p className="text-gray-600">
            Review and approve bookings awaiting your confirmation
          </p>
        </div>

        {/* Stats */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center gap-3">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 rounded-full">
              <Clock className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{bookings.length}</div>
              <div className="text-sm text-gray-600">Bookings awaiting approval</div>
            </div>
          </div>
        </div>

        {/* Bookings List */}
        {bookings.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <div className="text-gray-400 text-5xl mb-4">✓</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">All caught up!</h3>
            <p className="text-gray-600">You don't have any pending bookings at the moment.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {bookings.map((booking) => (
              <div
                key={booking.id}
                className="bg-white rounded-lg shadow-sm p-6"
              >
                <div className="flex gap-6">
                  {/* Activity Image */}
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

                  {/* Booking Details */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1 min-w-0 pr-4">
                        <h3 className="text-lg font-semibold text-gray-900 mb-1">
                          {booking.activity.title}
                        </h3>
                        <div className="text-sm text-gray-600 mb-2">
                          Ref: {booking.booking_ref}
                        </div>
                        <OrderStatusBadge status={booking.status as any} />
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-gray-900">
                          {formatPrice(booking.total_price)}
                        </div>
                      </div>
                    </div>

                    {/* Date and Participants */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 text-sm">
                      <div className="flex items-center text-gray-600">
                        <Calendar className="w-4 h-4 mr-2 flex-shrink-0" />
                        <div>
                          <div className="font-medium">{formatDate(booking.booking_date)}</div>
                          {booking.booking_time && (
                            <div className="text-xs">{formatTime(booking.booking_time)}</div>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center text-gray-600">
                        <Users className="w-4 h-4 mr-2 flex-shrink-0" />
                        {booking.adults} {booking.adults === 1 ? 'Adult' : 'Adults'}
                        {booking.children > 0 && `, ${booking.children} ${booking.children === 1 ? 'Child' : 'Children'}`}
                      </div>
                    </div>

                    {/* Customer Information */}
                    <div className="bg-gray-50 rounded-lg p-4 mb-4">
                      <h4 className="font-semibold text-gray-900 mb-3">Customer Information</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                        <div>
                          <div className="text-gray-600 mb-1">Name</div>
                          <div className="font-medium text-gray-900">{booking.customer_name}</div>
                        </div>
                        <div>
                          <div className="text-gray-600 mb-1 flex items-center">
                            <Mail className="w-3 h-3 mr-1" />
                            Email
                          </div>
                          <div className="font-medium text-gray-900">{booking.customer_email}</div>
                        </div>
                        {booking.customer_phone && (
                          <div>
                            <div className="text-gray-600 mb-1 flex items-center">
                              <Phone className="w-3 h-3 mr-1" />
                              Phone
                            </div>
                            <div className="font-medium text-gray-900">{booking.customer_phone}</div>
                          </div>
                        )}
                      </div>

                      {booking.special_requirements && (
                        <div className="mt-3 pt-3 border-t border-gray-200">
                          <div className="text-gray-600 mb-1">Special Requirements</div>
                          <div className="text-gray-900">{booking.special_requirements}</div>
                        </div>
                      )}
                    </div>

                    {/* Actions */}
                    <div className="flex gap-3">
                      <button
                        onClick={() => handleApprove(booking.id)}
                        className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center gap-2"
                      >
                        <CheckCircle className="w-4 h-4" />
                        Approve Booking
                      </button>
                      <button
                        onClick={() => setRejectModal({
                          bookingId: booking.id,
                          bookingRef: booking.booking_ref,
                          activityTitle: booking.activity.title
                        })}
                        className="flex-1 px-4 py-2 border border-red-300 text-red-700 rounded-lg hover:bg-red-50 transition-colors flex items-center justify-center gap-2"
                      >
                        <XCircle className="w-4 h-4" />
                        Reject Booking
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Reject Modal */}
        {rejectModal && (
          <RejectBookingModal
            bookingRef={rejectModal.bookingRef}
            activityTitle={rejectModal.activityTitle}
            onClose={() => setRejectModal(null)}
            onConfirm={(reason) => handleReject(rejectModal.bookingId, reason)}
          />
        )}
      </div>
    </div>
  );
}
