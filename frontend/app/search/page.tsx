'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import ActivityCard from '@/components/activities/ActivityCard';
import FilterSidebar from '@/components/search/FilterSidebar';
import SearchBar from '@/components/search/SearchBar';
import { Activity, SearchParams, PaginatedResponse, Category, Destination, Provider } from '@/types';
import { apiClient } from '@/lib/api';
import { SlidersHorizontal } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

export default function SearchPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { getTranslation, language } = useLanguage();
  const [activities, setActivities] = useState<Activity[]>([]);
  const [pagination, setPagination] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [categories, setCategories] = useState<Category[]>([]);
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [providers, setProviders] = useState<Provider[]>([]);

  // Parse URL params to SearchParams
  const getFiltersFromURL = (): SearchParams => {
    const filters: SearchParams = {};

    if (searchParams.get('q')) filters.q = searchParams.get('q')!;
    if (searchParams.get('category')) filters.category_slug = searchParams.get('category')!;
    if (searchParams.get('category_slug')) filters.category_slug = searchParams.get('category_slug')!;
    if (searchParams.get('vendor_id')) filters.vendor_id = parseInt(searchParams.get('vendor_id')!);
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
    const availability = searchParams.get('is_available');
    if (availability === 'true') filters.is_available = true;
    else if (availability === 'false') filters.is_available = false;
    if (searchParams.get('sort_by')) filters.sort_by = searchParams.get('sort_by') as any;
    if (searchParams.get('page')) filters.page = parseInt(searchParams.get('page')!);

    return filters;
  };

  const [filters, setFilters] = useState<SearchParams>(getFiltersFromURL());

  useEffect(() => {
    // Keep the filters state in sync with the URL (the source of truth) on every
    // navigation, so load-more / sort / the sidebar never act on stale filters.
    setFilters(getFiltersFromURL());
    fetchData();
    fetchMetadata();
  }, [searchParams]);

  // Re-fetch data when language changes
  useEffect(() => {
    fetchMetadata();
  }, [language]);

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
      const [categoriesRes, destinationsRes, providersRes] = await Promise.all([
        apiClient.categories.list(),
        apiClient.destinations.list(),
        apiClient.providers.list()
      ]);
      setCategories(categoriesRes.data);
      setDestinations(destinationsRes.data);
      setProviders(providersRes.data);
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
    if (!pagination || !pagination.has_next || loadingMore) return;

    const nextPage = pagination.page + 1;
    // Read the active filters from the URL (same source as fetchData) so the
    // next page matches the currently displayed result set.
    const newFilters = { ...getFiltersFromURL(), page: nextPage };

    // NOTE: do NOT write the page back to the URL here. In Next 14.1+,
    // window.history.replaceState syncs with useSearchParams(), which would
    // retrigger the [searchParams] effect and reset the list to a single page
    // — defeating the append. Load-more is intentionally URL-less.
    setLoadingMore(true);
    try {
      const response = await apiClient.activities.search(newFilters);
      setActivities(prev => [...prev, ...response.data.data]);
      setPagination(response.data.pagination);
    } catch (error) {
      console.error('Error loading more activities:', error);
    } finally {
      setLoadingMore(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Search Bar */}
      <div className="bg-paper border-b">
        <div className="container mx-auto px-4 py-6">
          <SearchBar
            placeholder={getTranslation('search.placeholder')}
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
              {getTranslation('button.filter')}
            </button>
          </div>

          {/* Filters Sidebar */}
          <aside className={`lg:block lg:w-80 ${showFilters ? 'block' : 'hidden'}`}>
            <FilterSidebar
              filters={filters}
              onFilterChange={handleFilterChange}
              categories={categories}
              destinations={destinations}
              providers={providers}
            />
          </aside>

          {/* Results */}
          <main className="flex-1">
            {/* Results Header */}
            <div className="flex justify-between items-center mb-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  {filters.q ? `${getTranslation('search.title.search_results')} "${filters.q}"` : getTranslation('search.title.all_activities')}
                </h1>
                {pagination && (
                  <p className="text-gray-600 mt-1">
                    {pagination.total} {getTranslation('search.activities_found')}
                  </p>
                )}
              </div>

              {/* Sort Dropdown */}
              <select
                value={filters.sort_by || 'recommended'}
                onChange={(e) => handleSortChange(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="recommended">{getTranslation('search.sort.recommended')}</option>
                <option value="price_asc">{getTranslation('search.sort.price_low_high')}</option>
                <option value="price_desc">{getTranslation('search.sort.price_high_low')}</option>
                <option value="rating">{getTranslation('search.sort.highest_rated')}</option>
                <option value="duration">{getTranslation('search.sort.duration')}</option>
              </select>
            </div>

            {/* Loading State */}
            {loading && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[1, 2, 3, 4, 5, 6].map(i => (
                  <div key={i} className="bg-paper rounded-lg h-96 shadow animate-pulse" />
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
                      className="px-8 py-3 bg-primary text-ink font-medium rounded-full hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                    >
                      {loadingMore ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          {getTranslation('search.loading')}
                        </>
                      ) : (
                        `${getTranslation('search.load_more')} (${activities.length} of ${pagination.total})`
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
                  {getTranslation('search.no_results.title')}
                </h3>
                <p className="text-gray-600 mb-6">
                  {getTranslation('search.no_results.subtitle')}
                </p>
                <button
                  onClick={() => handleFilterChange({ q: filters.q })}
                  className="btn-primary"
                >
                  {getTranslation('search.clear_filters')}
                </button>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}