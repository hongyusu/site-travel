'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Building2, CheckCircle, XCircle, ArrowLeft, Package } from 'lucide-react';
import { apiClient } from '@/lib/api';

export default function AdminVendorsPage() {
  const router = useRouter();
  const [vendors, setVendors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchVendors();
  }, [page]);

  const fetchVendors = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/admin/login?return=/admin/vendors');
        return;
      }

      const response = await apiClient.admin.listVendors({
        page,
        per_page: 20
      });

      setVendors(response.data.data);
      setTotalPages(response.data.pagination.total_pages);
    } catch (error: any) {
      console.error('Error fetching vendors:', error);
      if (error.response?.status === 403 || error.response?.status === 401) {
        router.push('/admin/login?return=/admin/vendors');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleToggleVerification = async (vendorId: number) => {
    try {
      const response = await apiClient.admin.toggleVendorVerification(vendorId);
      setVendors(vendors.map(v =>
        v.id === vendorId ? { ...v, is_verified: response.data.data.is_verified } : v
      ));
    } catch (error) {
      console.error('Error toggling vendor verification:', error);
      alert('Failed to toggle vendor verification');
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
                <h1 className="text-3xl font-bold text-gray-900">Vendor Management</h1>
                <p className="text-gray-600 mt-1">Manage and verify vendors</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Vendors Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900 flex items-center">
                <Building2 className="w-6 h-6 mr-2" />
                Vendors ({vendors.length})
              </h2>
            </div>
          </div>

          {vendors.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-gray-600">No vendors found.</p>
            </div>
          ) : (
            <>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Vendor
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Activities
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Bookings
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Joined
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {vendors.map(vendor => (
                      <tr key={vendor.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4">
                          <div>
                            <div className="text-sm font-medium text-gray-900">{vendor.company_name}</div>
                            <div className="text-sm text-gray-500">{vendor.email}</div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-sm text-gray-900">
                            <Package className="w-4 h-4 inline mr-1" />
                            {vendor.activity_count} ({vendor.active_activity_count} active)
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-sm text-gray-900">{vendor.total_bookings}</div>
                        </td>
                        <td className="px-6 py-4">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            vendor.is_verified
                              ? 'bg-success-light text-success'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {vendor.is_verified ? 'Verified' : 'Unverified'}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {new Date(vendor.created_at).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4 text-right text-sm font-medium">
                          <button
                            onClick={() => handleToggleVerification(vendor.id)}
                            className={`inline-flex items-center ${
                              vendor.is_verified
                                ? 'text-red-600 hover:text-red-900'
                                : 'text-green-600 hover:text-green-900'
                            }`}
                            title={vendor.is_verified ? 'Unverify' : 'Verify'}
                          >
                            {vendor.is_verified ? (
                              <>
                                <XCircle className="w-5 h-5 mr-1" />
                                Unverify
                              </>
                            ) : (
                              <>
                                <CheckCircle className="w-5 h-5 mr-1" />
                                Verify
                              </>
                            )}
                          </button>
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
