import axios from 'axios';

// Different URLs for server-side (container) vs client-side (browser)
const API_BASE_URL = typeof window !== 'undefined' 
  ? 'http://localhost:8000/api/v1'  // Client-side: browser to host
  : 'http://backend:8000/api/v1';  // Server-side: container to container

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Generate or get session ID
const getSessionId = () => {
  if (typeof window === 'undefined') return null;

  let sessionId = localStorage.getItem('session_id');
  if (!sessionId) {
    sessionId = `sess_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('session_id', sessionId);
  }
  return sessionId;
};

// Add auth token, session ID, and language to requests
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    const sessionId = getSessionId();
    if (sessionId) {
      config.headers['X-Session-ID'] = sessionId;
    }

    // Add language parameter to requests
    const language = localStorage.getItem('preferredLanguage') || 'en';
    // Add language param to GET requests for content endpoints
    if (config.method === 'get' && (
      config.url?.includes('/activities') ||
      config.url?.includes('/destinations') ||
      config.url?.includes('/categories')
    )) {
      config.params = {
        ...config.params,
        language,
      };
    }
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) throw new Error('No refresh token');

        const response = await api.post('/auth/refresh', {
          refresh_token: refreshToken,
        });

        const { access_token, refresh_token } = response.data;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// API endpoints
export const endpoints = {
  // Auth
  login: '/auth/login',
  register: '/auth/register',
  registerVendor: '/auth/register-vendor',
  me: '/auth/me',
  refresh: '/auth/refresh',

  // Activities
  activities: '/activities',
  searchActivities: '/activities/search',
  categories: '/activities/categories',
  destinations: '/activities/destinations',
  activityDetail: (id: number) => `/activities/${id}`,
  activityBySlug: (slug: string) => `/activities/slug/${slug}`,
  similarActivities: (id: number) => `/activities/${id}/similar`,

  // Bookings
  bookings: '/bookings',
  myBookings: '/bookings/my',
  bookingDetail: (ref: string) => `/bookings/${ref}`,
  cancelBooking: (ref: string) => `/bookings/${ref}/cancel`,
  availability: (activityId: number) => `/bookings/${activityId}/availability`,

  // Cart
  cart: '/cart',
  addToCart: '/cart/add',
  updateCartItem: (id: number) => `/cart/${id}`,
  removeFromCart: (id: number) => `/cart/${id}`,
  clearCart: '/cart',
  cartTotal: '/cart/total',

  // Reviews
  reviews: '/reviews',
  activityReviews: (activityId: number) => `/reviews/activity/${activityId}`,
  myReviews: '/reviews/my',
  markHelpful: (id: number) => `/reviews/${id}/helpful`,

  // Wishlist
  wishlist: '/wishlist',
  addToWishlist: (activityId: number) => `/wishlist/${activityId}`,
  removeFromWishlist: (activityId: number) => `/wishlist/${activityId}`,
  checkInWishlist: (activityId: number) => `/wishlist/check/${activityId}`,
};

// API Client with convenient methods
export const apiClient = {
  auth: {
    login: (email: string, password: string) =>
      api.post(endpoints.login, { email, password }),
    register: (data: any) =>
      api.post(endpoints.register, data),
    registerVendor: (data: any) =>
      api.post(endpoints.registerVendor, data),
    getProfile: () =>
      api.get(endpoints.me),
    updateProfile: (data: any) =>
      api.put(endpoints.me, data),
    getStatistics: () =>
      api.get('/auth/me/statistics'),
  },

  activities: {
    search: (params?: any) =>
      api.get(endpoints.searchActivities, { params }),
    getById: (id: number) =>
      api.get(endpoints.activityDetail(id)),
    getBySlug: (slug: string) =>
      api.get(endpoints.activityBySlug(slug)),
    getSimilar: (id: number) =>
      api.get(endpoints.similarActivities(id)),
    create: (data: any) =>
      api.post('/activities', data),
    update: (id: number, data: any) =>
      api.put(`/activities/${id}`, data),
    delete: (id: number) =>
      api.delete(`/activities/${id}`),
    toggleStatus: (id: number) =>
      api.patch(`/activities/${id}/toggle-status`),
  },

  categories: {
    list: () =>
      api.get(endpoints.categories),
  },

  destinations: {
    list: () =>
      api.get(endpoints.destinations),
    getFeatured: () =>
      api.get(endpoints.destinations, { params: { featured_only: true } }),
    getBySlug: (slug: string) =>
      api.get(`${endpoints.destinations}/${slug}`),
  },

  bookings: {
    list: () =>
      api.get(endpoints.myBookings),
    getById: (ref: string) =>
      api.get(endpoints.bookingDetail(ref)),
    getByRef: (ref: string) =>
      api.get(endpoints.bookingDetail(ref)),
    create: (data: any) =>
      api.post(endpoints.bookings, data),
    cancel: (ref: string) =>
      api.post(endpoints.cancelBooking(ref)),
    getAvailability: (activityId: number, date: string) =>
      api.get(endpoints.availability(activityId), { params: { date } }),
  },

  cart: {
    list: () =>
      api.get(endpoints.cart),
    add: (data: any) =>
      api.post(endpoints.addToCart, data),
    update: (id: number, data: any) =>
      api.put(endpoints.updateCartItem(id), data),
    remove: (id: number) =>
      api.delete(endpoints.removeFromCart(id)),
    clear: () =>
      api.delete(endpoints.clearCart),
    getTotal: () =>
      api.get(endpoints.cartTotal),
  },

  reviews: {
    list: (activityId: number) =>
      api.get(endpoints.activityReviews(activityId)),
    create: (data: any) =>
      api.post(endpoints.reviews, data),
    update: (id: number, data: any) =>
      api.put(`/reviews/${id}`, data),
    delete: (id: number) =>
      api.delete(`/reviews/${id}`),
    markHelpful: (id: number) =>
      api.post(endpoints.markHelpful(id)),
  },

  wishlist: {
    list: () =>
      api.get(endpoints.wishlist),
    add: (activityId: number) =>
      api.post(endpoints.addToWishlist(activityId)),
    remove: (activityId: number) =>
      api.delete(endpoints.removeFromWishlist(activityId)),
    check: (activityId: number) =>
      api.get(endpoints.checkInWishlist(activityId)),
  },

  admin: {
    // Stats
    getStats: () =>
      api.get('/admin/stats'),

    // Users
    listUsers: (params?: any) =>
      api.get('/admin/users', { params }),
    toggleUserStatus: (userId: number) =>
      api.patch(`/admin/users/${userId}/toggle-status`),

    // Vendors
    listVendors: (params?: any) =>
      api.get('/admin/vendors', { params }),
    toggleVendorVerification: (vendorId: number) =>
      api.patch(`/admin/vendors/${vendorId}/verify`),

    // Activities
    listActivities: (params?: any) =>
      api.get('/admin/activities', { params }),
    toggleActivityStatus: (activityId: number) =>
      api.patch(`/admin/activities/${activityId}/toggle-status`),
    deleteActivity: (activityId: number) =>
      api.delete(`/admin/activities/${activityId}`),

    // Bookings
    listBookings: (params?: any) =>
      api.get('/admin/bookings', { params }),

    // Reviews
    listReviews: (params?: any) =>
      api.get('/admin/reviews', { params }),
    deleteReview: (reviewId: number) =>
      api.delete(`/admin/reviews/${reviewId}`),
  },
};