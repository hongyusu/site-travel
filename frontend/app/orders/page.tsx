'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Calendar, Users, ArrowRight, Filter } from 'lucide-react';
import { apiClient } from '@/lib/api';
import { formatPrice } from '@/lib/utils';
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
  created_at: string;
  confirmed_at: string | null;
}

export default function MyOrdersPage() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'upcoming' | 'past'>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  useEffect(() => {
    fetchBookings();
  }, [filter, statusFilter]);

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const params: any = {};

      if (filter === 'upcoming') {
        params.upcoming_only = true;
      } else if (filter === 'past') {
        params.past_only = true;
      }

      if (statusFilter !== 'all') {
        params.status = statusFilter;
      }

      const response = await apiClient.bookings.list();
      const bookingsData = response.data?.data || [];
      setBookings(bookingsData);
    } catch (error) {
      console.error('Error fetching bookings:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
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

  const filteredBookings = bookings.filter(booking => {
    if (filter === 'upcoming') {
      return new Date(booking.booking_date) >= new Date();
    } else if (filter === 'past') {
      return new Date(booking.booking_date) < new Date();
    }
    return true;
  }).filter(booking => {
    if (statusFilter === 'all') return true;
    return booking.status === statusFilter;
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading your orders...</p>
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">My Orders</h1>
          <p className="text-gray-600">View and manage all your bookings</p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
          <div className="flex items-center gap-4 flex-wrap">
            <div className="flex items-center gap-2">
              <Filter className="w-5 h-5 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">Filters:</span>
            </div>

            {/* Time Filter */}
            <div className="flex gap-2">
              <button
                onClick={() => setFilter('all')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  filter === 'all'
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setFilter('upcoming')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  filter === 'upcoming'
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Upcoming
              </button>
              <button
                onClick={() => setFilter('past')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  filter === 'past'
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Past
              </button>
            </div>

            {/* Status Filter */}
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg text-sm"
            >
              <option value="all">All Statuses</option>
              <option value="pending_vendor_approval">Awaiting Approval</option>
              <option value="confirmed">Confirmed</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
        </div>

        {/* Bookings List */}
        {filteredBookings.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <div className="text-gray-400 text-5xl mb-4">📭</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No bookings found</h3>
            <p className="text-gray-600 mb-6">
              {filter === 'upcoming'
                ? "You don't have any upcoming bookings"
                : filter === 'past'
                ? "You don't have any past bookings"
                : "You haven't made any bookings yet"}
            </p>
            <Link href="/" className="btn-primary inline-block">
              Browse Activities
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredBookings.map((booking) => (
              <Link
                key={booking.id}
                href={`/order-confirmation?ref=${booking.booking_ref}`}
                className="block bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
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
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1 min-w-0 pr-4">
                        <h3 className="text-lg font-semibold text-gray-900 mb-1 truncate">
                          {booking.activity.title}
                        </h3>
                        <div className="text-sm text-gray-600">
                          Ref: {booking.booking_ref}
                        </div>
                      </div>
                      <OrderStatusBadge status={booking.status} />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
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
                        <div>
                          {booking.adults} {booking.adults === 1 ? 'Adult' : 'Adults'}
                          {booking.children > 0 && `, ${booking.children} ${booking.children === 1 ? 'Child' : 'Children'}`}
                        </div>
                      </div>

                      <div className="flex items-center justify-between md:justify-start">
                        <div className="font-semibold text-gray-900">
                          {formatPrice(booking.total_price)}
                        </div>
                        <ArrowRight className="w-5 h-5 text-gray-400 ml-2" />
                      </div>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
