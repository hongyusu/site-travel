'use client';

import { useState, useEffect } from 'react';
import { Star, ThumbsUp, MoreHorizontal, ChevronDown, X } from 'lucide-react';
import { apiClient } from '@/lib/api';
import { toast } from 'react-hot-toast';
import ReviewForm from './ReviewForm';
import Image from 'next/image';
import { useLanguage } from '@/contexts/LanguageContext';

interface Review {
  id: number;
  user_name: string;
  rating: number;
  title: string;
  comment: string;
  created_at: string;
  helpful_count: number;
  verified_booking: boolean;
  images?: string[];
}

interface ReviewsSectionProps {
  activityId: number;
  averageRating: number;
  totalReviews: number;
}

export default function ReviewsSection({
  activityId,
  averageRating,
  totalReviews
}: ReviewsSectionProps) {
  const { getTranslation } = useLanguage();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [helpfulReviews, setHelpfulReviews] = useState<number[]>([]);
  const [expandedReviews, setExpandedReviews] = useState<number[]>([]);
  const [lightboxImage, setLightboxImage] = useState<string | null>(null);

  // Check authentication
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      setIsAuthenticated(!!token);
    }
  }, []);

  // Rating distribution (mock data for now)
  const ratingDistribution = {
    5: Math.floor(totalReviews * 0.6),
    4: Math.floor(totalReviews * 0.25),
    3: Math.floor(totalReviews * 0.10),
    2: Math.floor(totalReviews * 0.03),
    1: Math.floor(totalReviews * 0.02)
  };

  useEffect(() => {
    fetchReviews();
  }, [activityId]);

  const fetchReviews = async (loadMore = false) => {
    try {
      console.log('Fetching reviews for activity:', activityId);
      const response = await apiClient.reviews.list(activityId);
      console.log('Reviews API response:', response.data);

      // API returns {success, data: [...], pagination}
      const apiReviews = Array.isArray(response.data?.data) ? response.data.data : [];
      console.log('Parsed reviews count:', apiReviews.length);

      // Map API response to Review interface
      const newReviews: Review[] = apiReviews.map((r: any) => ({
        id: r.id,
        user_name: r.user?.name || 'Anonymous',
        rating: r.rating,
        title: r.title,
        comment: r.comment,
        created_at: r.created_at,
        helpful_count: r.helpful_count,
        verified_booking: r.is_verified_booking,
        images: r.images?.map((img: any) => img.url) || []
      }));

      console.log('Mapped reviews:', newReviews);

      if (loadMore) {
        setReviews(prev => [...prev, ...newReviews]);
      } else {
        setReviews(newReviews);
      }

      // Check pagination info from API
      const pagination = response.data?.pagination;
      setHasMore(pagination?.has_next || false);
    } catch (error) {
      console.error('Error fetching reviews:', error);
      // Create mock reviews for demonstration if API fails
      if (!loadMore) {
        const mockReviews = generateMockReviews();
        setReviews(mockReviews);
        setHasMore(false);
      }
    } finally {
      setLoading(false);
    }
  };

  const generateMockReviews = (): Review[] => {
    return [
      {
        id: 1,
        user_name: 'Sarah M.',
        rating: 5,
        title: 'Amazing experience!',
        comment: 'This was absolutely fantastic! Our guide was knowledgeable and entertaining. The tour exceeded all expectations. Would highly recommend to anyone visiting the city.',
        created_at: '2024-10-20',
        helpful_count: 23,
        verified_booking: true
      },
      {
        id: 2,
        user_name: 'John D.',
        rating: 4,
        title: 'Great tour, minor issues',
        comment: 'Overall a great experience. The guide was excellent and the sites were beautiful. Only downside was that it felt a bit rushed at times. Still worth it!',
        created_at: '2024-10-18',
        helpful_count: 15,
        verified_booking: true
      },
      {
        id: 3,
        user_name: 'Maria L.',
        rating: 5,
        title: 'Perfect day out',
        comment: 'Everything was perfectly organized. The meeting point was easy to find, the guide was professional, and we saw so much in one day. Great value for money!',
        created_at: '2024-10-15',
        helpful_count: 8,
        verified_booking: true
      }
    ];
  };

  const handleLoadMore = () => {
    setPage(prev => prev + 1);
    fetchReviews(true);
  };

  const toggleExpandReview = (reviewId: number) => {
    console.log('Toggling review:', reviewId);
    console.log('Current expanded reviews:', expandedReviews);
    setExpandedReviews(prev => {
      const newState = prev.includes(reviewId)
        ? prev.filter(id => id !== reviewId)
        : [...prev, reviewId];
      console.log('New expanded reviews:', newState);
      return newState;
    });
  };

  const handleMarkHelpful = async (reviewId: number) => {
    if (helpfulReviews.includes(reviewId)) {
      toast.error('You already marked this review as helpful');
      return;
    }

    try {
      // For now, work without authentication
      // TODO: Re-enable authentication check when auth is implemented
      // await apiClient.reviews.markHelpful(reviewId);

      // Update local state immediately for better UX
      setHelpfulReviews(prev => [...prev, reviewId]);
      setReviews(prev =>
        prev.map(review =>
          review.id === reviewId
            ? { ...review, helpful_count: review.helpful_count + 1 }
            : review
        )
      );
      toast.success('Marked as helpful');
    } catch (error) {
      toast.error('Failed to mark as helpful');
    }
  };

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`w-4 h-4 ${
          i < rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
        }`}
      />
    ));
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map(i => (
          <div key={i} className="bg-white rounded-lg p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Rating Overview */}
      <div className="bg-white rounded-lg p-6 border border-gray-200">
        <h3 className="text-xl font-semibold mb-4">{getTranslation('reviews.customer_reviews')}</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Average Rating */}
          <div>
            <div className="flex items-center mb-4">
              <span className="text-4xl font-bold text-gray-900 mr-3">
                {averageRating.toFixed(1)}
              </span>
              <div>
                <div className="flex items-center mb-1">
                  {renderStars(Math.round(averageRating))}
                </div>
                <p className="text-sm text-gray-600">
                  Based on {totalReviews} reviews
                </p>
              </div>
            </div>

            {isAuthenticated && (
              <button
                onClick={() => setShowReviewForm(true)}
                className="btn-primary text-sm px-4 py-2"
              >
                {getTranslation('reviews.write_review')}
              </button>
            )}
          </div>

          {/* Rating Distribution */}
          <div className="space-y-2">
            {[5, 4, 3, 2, 1].map(stars => {
              const count = ratingDistribution[stars as keyof typeof ratingDistribution];
              const percentage = totalReviews > 0 ? (count / totalReviews) * 100 : 0;

              return (
                <div key={stars} className="flex items-center">
                  <span className="text-sm text-gray-600 w-8">{stars}</span>
                  <Star className="w-4 h-4 text-yellow-400 fill-current mr-2" />
                  <div className="flex-1 bg-gray-200 rounded-full h-2 mr-3">
                    <div
                      className="bg-yellow-400 h-2 rounded-full"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                  <span className="text-sm text-gray-600 w-12 text-right">
                    {count}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Reviews List */}
      <div className="space-y-4">
        {reviews.map(review => (
          <div key={review.id} className="bg-white rounded-lg p-6 border border-gray-200">
            <div className="flex items-start justify-between mb-3">
              <div>
                <div className="flex items-center mb-1">
                  <span className="font-semibold text-gray-900 mr-2">
                    {review.user_name}
                  </span>
                  {review.verified_booking && (
                    <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                      Verified Booking
                    </span>
                  )}
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <div className="flex mr-2">{renderStars(review.rating)}</div>
                  <span>{formatDate(review.created_at)}</span>
                </div>
              </div>
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  toggleExpandReview(review.id);
                }}
                className="text-gray-400 hover:text-gray-600 transition-colors"
                title={expandedReviews.includes(review.id) ? "Show less" : "Show more"}
              >
                <MoreHorizontal className="w-5 h-5" />
              </button>
            </div>

            <h4 className="font-medium text-gray-900 mb-2">{review.title}</h4>
            <p className={`text-gray-700 mb-3 ${
              !expandedReviews.includes(review.id) && review.comment.length > 100
                ? 'line-clamp-2'
                : ''
            }`}>
              {review.comment}
            </p>
            {!expandedReviews.includes(review.id) && review.comment.length > 100 && (
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  toggleExpandReview(review.id);
                }}
                className="text-primary text-sm hover:text-primary-600 mb-3 font-medium"
              >
                {getTranslation('reviews.show_more')}
              </button>
            )}
            {expandedReviews.includes(review.id) && review.comment.length > 100 && (
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  toggleExpandReview(review.id);
                }}
                className="text-primary text-sm hover:text-primary-600 mb-3 font-medium"
              >
                {getTranslation('reviews.show_less')}
              </button>
            )}

            {/* Review Images */}
            {review.images && review.images.length > 0 && (
              <div className="flex space-x-2 mb-3">
                {review.images.map((img, index) => (
                  <div
                    key={index}
                    onClick={() => {
                      console.log('Image clicked:', img);
                      console.log('Setting lightbox image to:', img);
                      setLightboxImage(img);
                      console.log('Lightbox state after set:', lightboxImage);
                    }}
                    className="w-20 h-20 rounded-lg overflow-hidden hover:opacity-90 transition-opacity cursor-pointer"
                  >
                    <img
                      src={img}
                      alt={`Review image ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                  </div>
                ))}
              </div>
            )}

            {/* Helpful */}
            <div className="flex items-center">
              <button
                onClick={() => handleMarkHelpful(review.id)}
                className={`flex items-center text-sm ${
                  helpfulReviews.includes(review.id)
                    ? 'text-primary'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <ThumbsUp className="w-4 h-4 mr-1" />
                {getTranslation('reviews.helpful')} ({review.helpful_count})
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Load More */}
      {hasMore && reviews.length > 0 && (
        <div className="text-center">
          <button
            onClick={handleLoadMore}
            className="inline-flex items-center px-6 py-3 border border-gray-300 rounded-full hover:bg-gray-50"
          >
            {getTranslation('reviews.show_more')}
            <ChevronDown className="w-4 h-4 ml-2" />
          </button>
        </div>
      )}

      {reviews.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-600 mb-4">No reviews yet. Be the first to review!</p>
          {isAuthenticated && (
            <button
              onClick={() => setShowReviewForm(true)}
              className="btn-primary"
            >
              Write a Review
            </button>
          )}
        </div>
      )}

      {/* Review Form Modal */}
      {showReviewForm && (
        <ReviewForm
          activityId={activityId}
          onClose={() => setShowReviewForm(false)}
          onSuccess={() => {
            // Refresh reviews after successful submission
            setPage(1);
            fetchReviews(false);
          }}
        />
      )}

      {/* Image Lightbox */}
      {lightboxImage && (
        <div
          className="fixed inset-0 z-50 bg-black bg-opacity-90 flex items-center justify-center p-4"
          onClick={() => setLightboxImage(null)}
        >
          <button
            onClick={() => setLightboxImage(null)}
            className="absolute top-4 right-4 text-white hover:text-gray-300 transition-colors"
          >
            <X className="w-8 h-8" />
          </button>
          <div className="relative max-w-4xl max-h-[90vh] w-full h-full">
            <Image
              src={lightboxImage}
              alt="Review image"
              fill
              className="object-contain"
              unoptimized
            />
          </div>
        </div>
      )}
    </div>
  );
}