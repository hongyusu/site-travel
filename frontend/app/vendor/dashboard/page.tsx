'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Plus, Edit, Trash2, Eye, TrendingUp, Calendar, DollarSign, ToggleLeft, ToggleRight, List, CalendarDays } from 'lucide-react';
import { api, apiClient } from '@/lib/api';
import BookingCalendar from '@/components/vendor/BookingCalendar';
import BookingDetailsModal from '@/components/vendor/BookingDetailsModal';

export default function VendorDashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [activities, setActivities] = useState<any[]>([]);
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'list' | 'calendar'>('list');
  const [selectedBooking, setSelectedBooking] = useState<any>(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('access_token');
      console.log('Dashboard: Checking token...', token ? 'Token exists' : 'No token');

      if (!token) {
        console.log('Dashboard: No token, redirecting to login');
        router.push('/vendor/login?return=/vendor/dashboard');
        return;
      }

      console.log('Dashboard: Fetching profile, activities, and bookings...');
      const [profileResponse, activitiesResponse, bookingsResponse] = await Promise.all([
        apiClient.auth.getProfile(),
        apiClient.activities.search({ vendor_only: true }),
        api.get('/bookings/vendor/bookings'),
      ]);

      console.log('Dashboard: Profile response:', profileResponse.data);
      console.log('Dashboard: Activities count:', activitiesResponse.data?.data?.length || activitiesResponse.data?.length);

      if (profileResponse.data.role !== 'vendor') {
        console.log('Dashboard: User is not a vendor, redirecting home');
        router.push('/');
        return;
      }

      setUser(profileResponse.data);
      setActivities(activitiesResponse.data.data || activitiesResponse.data);
      setBookings(bookingsResponse.data.data || bookingsResponse.data);
      console.log('Dashboard: Successfully loaded all data');
    } catch (error: any) {
      console.error('Dashboard: Error fetching data:', error);
      console.error('Dashboard: Error details:', error.response?.data);
      router.push('/vendor/login?return=/vendor/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteActivity = async (id: number) => {
    if (!confirm('Are you sure you want to delete this activity?')) return;

    try {
      await apiClient.activities.delete(id);
      setActivities(activities.filter(a => a.id !== id));
    } catch (error) {
      console.error('Error deleting activity:', error);
      alert('Failed to delete activity');
    }
  };

  const handleToggleStatus = async (id: number) => {
    try {
      const response = await apiClient.activities.toggleStatus(id);
      console.log('Toggle response:', response.data);
      // Update the activity's is_active field
      setActivities(activities.map(a =>
        a.id === id ? { ...a, is_active: response.data.is_active } : a
      ));
    } catch (error) {
      console.error('Error toggling activity status:', error);
      alert('Failed to toggle activity status');
    }
  };

  const handleApproveBooking = async (bookingId: number) => {
    if (!confirm('Approve this booking?')) return;

    try {
      await api.post(`/bookings/vendor/${bookingId}/approve`);
      // Refresh bookings
      const response = await api.get('/bookings/vendor/bookings');
      setBookings(response.data.data || response.data);
    } catch (error) {
      console.error('Error approving booking:', error);
      alert('Failed to approve booking');
    }
  };

  const handleRejectBooking = async (bookingId: number) => {
    const reason = prompt('Please provide a reason for rejection:');
    if (!reason) return;

    try {
      await api.post(`/bookings/vendor/${bookingId}/reject`, { reason });
      // Refresh bookings
      const response = await api.get('/bookings/vendor/bookings');
      setBookings(response.data.data || response.data);
    } catch (error) {
      console.error('Error rejecting booking:', error);
      alert('Failed to reject booking');
    }
  };

  const handleCancelBooking = async (bookingId: number) => {
    const reason = prompt('Please provide a reason for cancellation:');
    if (!reason) return;

    try {
      await api.post(`/bookings/vendor/${bookingId}/cancel`, { reason });
      // Refresh bookings
      const response = await api.get('/bookings/vendor/bookings');
      setBookings(response.data.data || response.data);
    } catch (error) {
      console.error('Error cancelling booking:', error);
      alert('Failed to cancel booking');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto" />
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  const totalRevenue = bookings.reduce((sum, b) => sum + (Number(b.total_price) || 0), 0);
  const activeActivities = activities.filter(a => a.is_active).length;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="container mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Vendor Dashboard</h1>
              <p className="text-gray-600 mt-1">Welcome back, {user?.full_name}</p>
            </div>
            <Link
              href="/vendor/activities/new"
              className="btn-primary flex items-center shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 animate-pulse hover:animate-none"
            >
              <Plus className="w-5 h-5 mr-2" />
              Add Activity
            </Link>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Activities</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{activities.length}</p>
              </div>
              <div className="w-12 h-12 bg-primary-50 rounded-full flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-primary" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Active Activities</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{activeActivities}</p>
              </div>
              <div className="w-12 h-12 bg-success-50 rounded-full flex items-center justify-center">
                <Eye className="w-6 h-6 text-success" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Bookings</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{bookings.length}</p>
              </div>
              <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center">
                <Calendar className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Revenue</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">€{totalRevenue.toFixed(2)}</p>
              </div>
              <div className="w-12 h-12 bg-yellow-50 rounded-full flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Activities Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Your Activities</h2>
          </div>

          {activities.length === 0 ? (
            <div className="p-12 text-center">
              <div className="max-w-md mx-auto">
                <div className="w-24 h-24 mx-auto bg-primary-50 rounded-full flex items-center justify-center mb-4">
                  <Plus className="w-12 h-12 text-primary" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No Activities Yet</h3>
                <p className="text-gray-600 mb-6">Get started by creating your first activity. Share your experiences with travelers worldwide!</p>
                <Link
                  href="/vendor/activities/new"
                  className="btn-primary inline-flex items-center gap-2 text-lg px-8 py-4 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
                >
                  <Plus className="w-6 h-6" />
                  Create Your First Activity
                </Link>
              </div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Activity
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Category
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Price
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Rating
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {activities.map(activity => (
                    <tr key={activity.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4">
                        <div className="flex items-center">
                          <div className="text-sm font-medium text-gray-900">{activity.title}</div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-900">
                          {activity.categories?.[0]?.name || 'N/A'}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-900">${activity.price_adult}</div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-900">
                          {activity.average_rating?.toFixed(1) || 'N/A'} ({activity.review_count || 0})
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          activity.is_active
                            ? 'bg-success-light text-success'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {activity.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right text-sm font-medium">
                        <div className="flex justify-end space-x-2">
                          <Link
                            href={`/activities/${activity.slug}`}
                            className="text-blue-600 hover:text-blue-900"
                            title="View"
                          >
                            <Eye className="w-5 h-5" />
                          </Link>
                          <button
                            onClick={() => handleToggleStatus(activity.id)}
                            className={activity.is_active ? 'text-gray-600 hover:text-gray-900' : 'text-green-600 hover:text-green-900'}
                            title={activity.is_active ? 'Deactivate' : 'Activate'}
                          >
                            {activity.is_active ? <ToggleRight className="w-5 h-5" /> : <ToggleLeft className="w-5 h-5" />}
                          </button>
                          <Link
                            href={`/vendor/activities/${activity.id}/edit`}
                            className="text-primary hover:text-primary-600"
                            title="Edit"
                          >
                            <Edit className="w-5 h-5" />
                          </Link>
                          <button
                            onClick={() => handleDeleteActivity(activity.id)}
                            className="text-red-600 hover:text-red-900"
                            title="Delete"
                          >
                            <Trash2 className="w-5 h-5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Recent Bookings */}
        <div className="bg-white rounded-lg shadow overflow-hidden mt-8">
          <div className="p-6 border-b border-gray-200 flex justify-between items-center">
            <h2 className="text-xl font-bold text-gray-900">Recent Bookings</h2>
            <div className="flex gap-2">
              <button
                onClick={() => setViewMode('list')}
                className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
                  viewMode === 'list'
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <List className="w-4 h-4" />
                List
              </button>
              <button
                onClick={() => setViewMode('calendar')}
                className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
                  viewMode === 'calendar'
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <CalendarDays className="w-4 h-4" />
                Calendar
              </button>
            </div>
          </div>

          {bookings.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-gray-600">No bookings yet.</p>
            </div>
          ) : viewMode === 'calendar' ? (
            <div className="p-6">
              <BookingCalendar
                bookings={bookings}
                onBookingClick={(booking) => setSelectedBooking(booking)}
              />
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Booking Ref
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Activity
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Customer
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Amount
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {bookings.slice(0, 10).map(booking => (
                    <tr
                      key={booking.id}
                      className="hover:bg-gray-50 cursor-pointer"
                      onClick={() => setSelectedBooking(booking)}
                    >
                      <td className="px-6 py-4 text-sm font-medium text-gray-900">
                        {booking.booking_ref}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {booking.activity?.title || 'N/A'}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {booking.customer_name}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {new Date(booking.booking_date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        €{Number(booking.total_price || 0).toFixed(2)}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          booking.status === 'confirmed'
                            ? 'bg-success-light text-success'
                            : booking.status === 'pending'
                            ? 'bg-yellow-100 text-yellow-800'
                            : booking.status === 'completed'
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {booking.status}
                        </span>
                      </td>
                      <td className="px-6 py-4" onClick={(e) => e.stopPropagation()}>
                        {/* Pending - needs approval */}
                        {(booking.status === 'pending' || booking.status === 'pending_vendor_approval') && (
                          <div className="flex gap-2">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleApproveBooking(booking.id);
                              }}
                              className="text-sm text-green-600 hover:text-green-800 font-medium"
                            >
                              Approve
                            </button>
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleRejectBooking(booking.id);
                              }}
                              className="text-sm text-red-600 hover:text-red-800 font-medium"
                            >
                              Reject
                            </button>
                          </div>
                        )}

                        {/* Confirmed - can check in or cancel */}
                        {booking.status === 'confirmed' && (
                          <div className="flex gap-2">
                            <button
                              onClick={async (e) => {
                                e.stopPropagation();
                                if (confirm('Mark this booking as checked in?')) {
                                  try {
                                    await api.put(`/bookings/vendor/${booking.id}/checkin`);
                                    // Refresh bookings
                                    const response = await api.get('/bookings/vendor/bookings');
                                    setBookings(response.data.data || response.data);
                                  } catch (error) {
                                    console.error('Error checking in booking:', error);
                                    alert('Failed to check in booking');
                                  }
                                }
                              }}
                              className="text-sm text-primary hover:text-primary-600 font-medium"
                            >
                              Check In
                            </button>
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleCancelBooking(booking.id);
                              }}
                              className="text-sm text-gray-600 hover:text-gray-800 font-medium"
                            >
                              Cancel
                            </button>
                          </div>
                        )}

                        {/* Final states - no actions */}
                        {['completed', 'rejected', 'cancelled'].includes(booking.status) && (
                          <span className="text-sm text-gray-500">—</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Booking Details Modal */}
      {selectedBooking && (
        <BookingDetailsModal
          booking={selectedBooking}
          onClose={() => setSelectedBooking(null)}
        />
      )}
    </div>
  );
}
