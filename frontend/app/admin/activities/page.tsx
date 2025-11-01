'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Package, ToggleLeft, ToggleRight, Trash2, ArrowLeft } from 'lucide-react';
import { apiClient } from '@/lib/api';

export default function AdminActivitiesPage() {
  const router = useRouter();
  const [activities, setActivities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchActivities();
  }, [statusFilter, page]);

  const fetchActivities = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/admin/login?return=/admin/activities');
        return;
      }

      const response = await apiClient.admin.listActivities({
        status_filter: statusFilter || undefined,
        page,
        per_page: 20
      });

      setActivities(response.data.data);
      setTotalPages(response.data.pagination.total_pages);
    } catch (error: any) {
      console.error('Error fetching activities:', error);
      if (error.response?.status === 403 || error.response?.status === 401) {
        router.push('/admin/login?return=/admin/activities');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleToggleStatus = async (activityId: number) => {
    try {
      const response = await apiClient.admin.toggleActivityStatus(activityId);
      setActivities(activities.map(a =>
        a.id === activityId ? { ...a, is_active: response.data.data.is_active } : a
      ));
    } catch (error) {
      console.error('Error toggling activity status:', error);
      alert('Failed to toggle activity status');
    }
  };

  const handleDelete = async (activityId: number) => {
    if (!confirm('Are you sure you want to delete this activity? This action cannot be undone.')) {
      return;
    }

    try {
      await apiClient.admin.deleteActivity(activityId);
      setActivities(activities.filter(a => a.id !== activityId));
    } catch (error: any) {
      console.error('Error deleting activity:', error);
      if (error.response?.status === 400) {
        alert(error.response.data.detail || 'Cannot delete activity with existing bookings');
      } else {
        alert('Failed to delete activity');
      }
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
            <div className="flex items-center">
              <Link href="/admin/dashboard" className="mr-4">
                <ArrowLeft className="w-6 h-6 text-gray-600 hover:text-gray-900" />
              </Link>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Activity Moderation</h1>
                <p className="text-gray-600 mt-1">Manage and moderate activities</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex items-center space-x-4">
            <label className="text-sm font-medium text-gray-700">Filter by status:</label>
            <select
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value);
                setPage(1);
              }}
              className="px-4 py-2 border border-gray-300 rounded-lg"
            >
              <option value="">All Activities</option>
              <option value="active">Active Only</option>
              <option value="inactive">Inactive Only</option>
            </select>
          </div>
        </div>

        {/* Activities Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900 flex items-center">
                <Package className="w-6 h-6 mr-2" />
                Activities ({activities.length})
              </h2>
            </div>
          </div>

          {activities.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-gray-600">No activities found.</p>
            </div>
          ) : (
            <>
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
                        Price
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Rating
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Bookings
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
                          <div>
                            <div className="text-sm font-medium text-gray-900">{activity.title}</div>
                            <div className="text-sm text-gray-500">
                              {new Date(activity.created_at).toLocaleDateString()}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {activity.vendor_name}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          ${activity.price_adult}
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-sm text-gray-900">
                            {activity.average_rating.toFixed(1)} ({activity.total_reviews})
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {activity.total_bookings}
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
                        <td className="px-6 py-4 text-right">
                          <div className="flex justify-end space-x-2">
                            <button
                              onClick={() => handleToggleStatus(activity.id)}
                              className={activity.is_active ? 'text-gray-600 hover:text-gray-900' : 'text-green-600 hover:text-green-900'}
                              title={activity.is_active ? 'Deactivate' : 'Activate'}
                            >
                              {activity.is_active ? <ToggleRight className="w-5 h-5" /> : <ToggleLeft className="w-5 h-5" />}
                            </button>
                            <button
                              onClick={() => handleDelete(activity.id)}
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

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="bg-gray-50 px-6 py-3 flex items-center justify-between border-t border-gray-200">
                  <div className="text-sm text-gray-700">
                    Page {page} of {totalPages}
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => setPage(p => Math.max(1, p - 1))}
                      disabled={page === 1}
                      className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
                    >
                      Previous
                    </button>
                    <button
                      onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                      disabled={page === totalPages}
                      className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
                    >
                      Next
                    </button>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
