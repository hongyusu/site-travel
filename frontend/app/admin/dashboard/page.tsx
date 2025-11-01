'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Users, Activity, Calendar, DollarSign, TrendingUp, AlertCircle } from 'lucide-react';
import { apiClient } from '@/lib/api';

export default function AdminDashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalActivities: 0,
    totalBookings: 0,
    totalRevenue: 0,
    pendingActivities: 0,
    activeVendors: 0,
  });
  const [recentActivities, setRecentActivities] = useState<any[]>([]);
  const [recentUsers, setRecentUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/admin/login?return=/admin/dashboard');
        return;
      }

      const profileResponse = await apiClient.auth.getProfile();

      if (profileResponse.data.role !== 'admin') {
        router.push('/');
        return;
      }

      setUser(profileResponse.data);

      // Fetch admin stats from new API
      const statsResponse = await apiClient.admin.getStats();
      const statsData = statsResponse.data.data;

      setStats({
        totalUsers: statsData.users.total,
        totalActivities: statsData.activities.total,
        totalBookings: statsData.bookings.total,
        totalRevenue: statsData.revenue.total,
        pendingActivities: statsData.activities.inactive,
        activeVendors: statsData.users.vendors,
      });

      // Fetch recent activities
      const activitiesResponse = await apiClient.admin.listActivities({ per_page: 10 });
      setRecentActivities(activitiesResponse.data.data || []);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      router.push('/admin/login?return=/admin/dashboard');
    } finally {
      setLoading(false);
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

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="container mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
              <p className="text-gray-600 mt-1">Platform Overview & Management</p>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Activities</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stats.totalActivities}</p>
                <p className="text-sm text-gray-500 mt-1">
                  {stats.pendingActivities} pending approval
                </p>
              </div>
              <div className="w-12 h-12 bg-primary-50 rounded-full flex items-center justify-center">
                <Activity className="w-6 h-6 text-primary" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Bookings</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stats.totalBookings}</p>
                <p className="text-sm text-success mt-1">All time bookings</p>
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
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  ${stats.totalRevenue.toFixed(2)}
                </p>
                <p className="text-sm text-success mt-1">Platform revenue</p>
              </div>
              <div className="w-12 h-12 bg-yellow-50 rounded-full flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Active Vendors</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stats.activeVendors}</p>
                <p className="text-sm text-gray-500 mt-1">Registered vendors</p>
              </div>
              <div className="w-12 h-12 bg-green-50 rounded-full flex items-center justify-center">
                <Users className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Platform Growth</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">+12.5%</p>
                <p className="text-sm text-success mt-1">vs last month</p>
              </div>
              <div className="w-12 h-12 bg-purple-50 rounded-full flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Pending Approvals</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stats.pendingActivities}</p>
                <p className="text-sm text-yellow-600 mt-1">Require attention</p>
              </div>
              <div className="w-12 h-12 bg-orange-50 rounded-full flex items-center justify-center">
                <AlertCircle className="w-6 h-6 text-orange-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activities */}
        <div className="bg-white rounded-lg shadow overflow-hidden mb-8">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Recent Activities</h2>
          </div>

          {recentActivities.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-gray-600">No activities found.</p>
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
                      Vendor
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Category
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Price
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Rating
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {recentActivities.map(activity => (
                    <tr key={activity.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 text-sm font-medium text-gray-900">
                        {activity.title}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {activity.vendor_name || 'N/A'}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {activity.categories && activity.categories.length > 0
                          ? activity.categories.join(', ')
                          : 'N/A'}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        ${activity.price_adult}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          activity.is_active
                            ? 'bg-success-light text-success'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {activity.is_active ? 'Active' : 'Pending'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {activity.average_rating ? activity.average_rating.toFixed(1) : 'N/A'} ({activity.review_count || 0})
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Link href="/admin/users" className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">User Management</h3>
            <p className="text-gray-600 mb-4">Manage users and admin accounts</p>
            <button className="btn-primary w-full">Manage Users</button>
          </Link>

          <Link href="/admin/vendors" className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Vendor Management</h3>
            <p className="text-gray-600 mb-4">Verify and manage vendor accounts</p>
            <button className="btn-primary w-full">Manage Vendors</button>
          </Link>

          <Link href="/admin/activities" className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Activity Moderation</h3>
            <p className="text-gray-600 mb-4">Review and moderate activities</p>
            <button className="btn-primary w-full">Review Activities</button>
          </Link>

          <Link href="/admin/bookings" className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Bookings Management</h3>
            <p className="text-gray-600 mb-4">View and manage all bookings</p>
            <button className="btn-primary w-full">View Bookings</button>
          </Link>

          <Link href="/admin/reviews" className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Reviews Moderation</h3>
            <p className="text-gray-600 mb-4">Moderate customer reviews</p>
            <button className="btn-primary w-full">Moderate Reviews</button>
          </Link>
        </div>
      </div>
    </div>
  );
}
