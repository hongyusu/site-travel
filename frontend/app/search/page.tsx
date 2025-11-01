'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import ActivityCard from '@/components/activities/ActivityCard';
import FilterSidebar from '@/components/search/FilterSidebar';
import SearchBar from '@/components/search/SearchBar';
import { Activity, SearchParams, PaginatedResponse, Category, Destination } from '@/types';
import { apiClient } from '@/lib/api';
import { SlidersHorizontal } from 'lucide-react';

export default function SearchPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [activities, setActivities] = useState<Activity[]>([]);
  const [pagination, setPagination] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [categories, setCategories] = useState<Category[]>([]);
  const [destinations, setDestinations] = useState<Destination[]>([]);

  // Parse URL params to SearchParams
  const getFiltersFromURL = (): SearchParams => {
    const filters: SearchParams = {};

    if (searchParams.get('q')) filters.q = searchParams.get('q')!;
    if (searchParams.get('category')) filters.category_slug = searchParams.get('category')!;
    if (searchParams.get('category_slug')) filters.category_slug = searchParams.get('category_slug')!;
    if (searchParams.get('destination')) filters.destination_slug = searchParams.get('destination')!;
    if (searchParams.get('destination_slug')) filters.destination_slug = searchParams.get('destination_slug')!;
    if (searchParams.get('min_price')) filters.min_price = parseFloat(searchParams.get('min_price')!);
    if (searchParams.get('max_price')) filters.max_price = parseFloat(searchParams.get('max_price')!);
    if (searchParams.get('min_duration')) filters.min_duration = parseInt(searchParams.get('min_duration')!);
    if (searchParams.get('max_duration')) filters.max_duration = parseInt(searchParams.get('max_duration')!);
    if (searchParams.get('min_rating')) filters.min_rating = parseFloat(searchParams.get('min_rating')!);
    if (searchParams.get('free_cancellation')) filters.free_cancellation = searchParams.get('free_cancellation') === 'true';
    if (searchParams.get('instant_confirmation')) filters.instant_confirmation = searchParams.get('instant_confirmation') === 'true';
    if (searchParams.get('skip_the_line')) filters.skip_the_line = searchParams.get('skip_the_line') === 'true';
    if (searchParams.get('bestseller')) filters.bestseller = searchParams.get('bestseller') === 'true';
    if (searchParams.get('sort_by')) filters.sort_by = searchParams.get('sort_by') as any;
    if (searchParams.get('page')) filters.page = parseInt(searchParams.get('page')!);

    return filters;
  };

  const [filters, setFilters] = useState<SearchParams>(getFiltersFromURL());

  useEffect(() => {
    fetchData();
    fetchMetadata();
  }, [searchParams]);

  const fetchData = async (append: boolean = false) => {
    if (!append) {
      setLoading(true);
    } else {
      setLoadingMore(true);
    }

    try {
      const filters = getFiltersFromURL();
      const response = await apiClient.activities.search(filters);

      if (append) {
        setActivities(prev => [...prev, ...response.data.data]);
      } else {
        setActivities(response.data.data);
      }
      setPagination(response.data.pagination);
    } catch (error) {
      console.error('Error fetching activities:', error);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };

  const fetchMetadata = async () => {
    try {
      const [categoriesRes, destinationsRes] = await Promise.all([
        apiClient.categories.list(),
        apiClient.destinations.list()
      ]);
      setCategories(categoriesRes.data);
      setDestinations(destinationsRes.data);
    } catch (error) {
      console.error('Error fetching metadata:', error);
    }
  };

  const updateURL = (newFilters: SearchParams) => {
    const params = new URLSearchParams();

    Object.entries(newFilters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.set(key, String(value));
      }
    });

    router.push(`/search?${params.toString()}`);
  };

  const handleFilterChange = (newFilters: SearchParams) => {
    setFilters(newFilters);
    updateURL(newFilters);
  };

  const handleSortChange = (sortBy: string) => {
    const newFilters = { ...filters, sort_by: sortBy as any };
    handleFilterChange(newFilters);
  };

  const handleLoadMore = async () => {
    if (pagination && pagination.has_next) {
      const nextPage = pagination.page + 1;
      const newFilters = { ...filters, page: nextPage };

      // Update URL without triggering full refetch
      const params = new URLSearchParams();
      Object.entries(newFilters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.set(key, String(value));
        }
      });

      // Fetch more data and append
      setLoadingMore(true);
      try {
        const response = await apiClient.activities.search(newFilters);
        setActivities(prev => [...prev, ...response.data.data]);
        setPagination(response.data.pagination);

        // Update URL without triggering useEffect
        window.history.replaceState({}, '', `/search?${params.toString()}`);
      } catch (error) {
        console.error('Error loading more activities:', error);
      } finally {
        setLoadingMore(false);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Search Bar */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-4 py-6">
          <SearchBar
            placeholder="Search for activities..."
            className="max-w-3xl mx-auto"
          />
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Mobile Filter Toggle */}
          <div className="lg:hidden">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="btn-secondary w-full flex items-center justify-center"
            >
              <SlidersHorizontal className="w-5 h-5 mr-2" />
              Filters
            </button>
          </div>

          {/* Filters Sidebar */}
          <aside className={`lg:block lg:w-80 ${showFilters ? 'block' : 'hidden'}`}>
            <FilterSidebar
              filters={filters}
              onFilterChange={handleFilterChange}
              categories={categories}
              destinations={destinations}
            />
          </aside>

          {/* Results */}
          <main className="flex-1">
            {/* Results Header */}
            <div className="flex justify-between items-center mb-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  {filters.q ? `Search results for "${filters.q}"` : 'All Activities'}
                </h1>
                {pagination && (
                  <p className="text-gray-600 mt-1">
                    {pagination.total} activities found
                  </p>
                )}
              </div>

              {/* Sort Dropdown */}
              <select
                value={filters.sort_by || 'recommended'}
                onChange={(e) => handleSortChange(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="recommended">Recommended</option>
                <option value="price_asc">Price: Low to High</option>
                <option value="price_desc">Price: High to Low</option>
                <option value="rating">Highest Rated</option>
                <option value="duration">Duration</option>
              </select>
            </div>

            {/* Loading State */}
            {loading && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[1, 2, 3, 4, 5, 6].map(i => (
                  <div key={i} className="bg-white rounded-lg h-96 shadow animate-pulse" />
                ))}
              </div>
            )}

            {/* Results Grid */}
            {!loading && activities.length > 0 && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {activities.map(activity => (
                    <ActivityCard key={activity.id} activity={activity} />
                  ))}
                </div>

                {/* Load More Button */}
                {pagination && pagination.has_next && (
                  <div className="mt-8 flex justify-center">
                    <button
                      onClick={handleLoadMore}
                      disabled={loadingMore}
                      className="px-8 py-3 bg-primary text-white font-medium rounded-full hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                    >
                      {loadingMore ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Loading...
                        </>
                      ) : (
                        `Load More (${activities.length} of ${pagination.total})`
                      )}
                    </button>
                  </div>
                )}
              </>
            )}

            {/* No Results */}
            {!loading && activities.length === 0 && (
              <div className="text-center py-12">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  No activities found
                </h3>
                <p className="text-gray-600 mb-6">
                  Try adjusting your filters or search terms
                </p>
                <button
                  onClick={() => handleFilterChange({ q: filters.q })}
                  className="btn-primary"
                >
                  Clear Filters
                </button>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}