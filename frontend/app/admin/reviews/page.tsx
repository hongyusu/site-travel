'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { MessageSquare, Star, Trash2, ArrowLeft, CheckCircle } from 'lucide-react';
import { apiClient } from '@/lib/api';

export default function AdminReviewsPage() {
  const router = useRouter();
  const [reviews, setReviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchReviews();
  }, [page]);

  const fetchReviews = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/admin/login?return=/admin/reviews');
        return;
      }

      const response = await apiClient.admin.listReviews({
        page,
        per_page: 20
      });

      setReviews(response.data.data);
      setTotalPages(response.data.pagination.total_pages);
    } catch (error: any) {
      console.error('Error fetching reviews:', error);
      if (error.response?.status === 403 || error.response?.status === 401) {
        router.push('/admin/login?return=/admin/reviews');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (reviewId: number) => {
    if (!confirm('Are you sure you want to delete this review? This action cannot be undone.')) {
      return;
    }

    try {
      await apiClient.admin.deleteReview(reviewId);
      setReviews(reviews.filter(r => r.id !== reviewId));
    } catch (error) {
      console.error('Error deleting review:', error);
      alert('Failed to delete review');
    }
  };

  const renderStars = (rating: number) => {
    return (
      <div className="flex items-center">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`w-4 h-4 ${
              star <= rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
            }`}
          />
        ))}
      </div>
    );
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
                <h1 className="text-3xl font-bold text-gray-900">Reviews Moderation</h1>
                <p className="text-gray-600 mt-1">Moderate and manage customer reviews</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Reviews List */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900 flex items-center">
                <MessageSquare className="w-6 h-6 mr-2" />
                Reviews ({reviews.length})
              </h2>
            </div>
          </div>

          {reviews.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-gray-600">No reviews found.</p>
            </div>
          ) : (
            <>
              <div className="divide-y divide-gray-200">
                {reviews.map(review => (
                  <div key={review.id} className="p-6 hover:bg-gray-50">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        {/* Review Header */}
                        <div className="flex items-center space-x-3 mb-2">
                          {renderStars(review.rating)}
                          {review.is_verified_booking && (
                            <span className="inline-flex items-center px-2 py-1 text-xs font-medium bg-success-light text-success rounded">
                              <CheckCircle className="w-3 h-3 mr-1" />
                              Verified Booking
                            </span>
                          )}
                        </div>

                        {/* Review Title */}
                        {review.title && (
                          <h3 className="text-lg font-semibold text-gray-900 mb-2">
                            {review.title}
                          </h3>
                        )}

                        {/* Review Comment */}
                        <p className="text-gray-700 mb-3">{review.comment}</p>

                        {/* Review Meta */}
                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <span>
                            <strong>User:</strong> {review.user?.full_name} ({review.user?.email})
                          </span>
                          <span>
                            <strong>Activity:</strong> {review.activity?.title}
                          </span>
                          <span>
                            <strong>Helpful:</strong> {review.helpful_count} votes
                          </span>
                          <span>
                            {new Date(review.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>

                      {/* Delete Button */}
                      <button
                        onClick={() => handleDelete(review.id)}
                        className="ml-4 text-red-600 hover:text-red-900"
                        title="Delete review"
                      >
                        <Trash2 className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                ))}
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
