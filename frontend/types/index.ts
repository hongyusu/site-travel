export interface User {
  id: number;
  email: string;
  full_name: string;
  phone?: string;
  role: 'customer' | 'vendor' | 'admin';
  email_verified: boolean;
  created_at: string;
  vendor_profile?: VendorProfile;
}

export interface VendorProfile {
  id: number;
  company_name: string;
  description?: string;
  logo_url?: string;
  is_verified: boolean;
  commission_rate: number;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  icon?: string;
}

export interface Destination {
  id: number;
  name: string;
  slug: string;
  country?: string;
  country_code?: string;
  image_url?: string;
  latitude?: number;
  longitude?: number;
  is_featured: boolean;
}

export interface ActivityTimeline {
  id: number;
  step_number: number;
  title: string;
  description?: string;
  duration_minutes?: number;
  image_url?: string;
  order_index: number;
}

export interface ActivityTimeSlot {
  id: number;
  slot_time: string;
  slot_label?: string;
  max_capacity?: number;
  is_available: boolean;
  price_adjustment: number;
}

export interface ActivityPricingTier {
  id: number;
  tier_name: string;
  tier_description?: string;
  price_adult: number;
  price_child?: number;
  is_active: boolean;
  order_index: number;
}

export interface ActivityAddOn {
  id: number;
  name: string;
  description?: string;
  price: number;
  is_optional: boolean;
  order_index: number;
}

export interface Activity {
  id: number;
  title: string;
  slug: string;
  short_description?: string;
  description?: string;
  price_adult: number;
  price_child?: number;
  duration_minutes?: number;
  max_group_size?: number;
  instant_confirmation: boolean;
  free_cancellation_hours: number;
  languages: string[];
  is_bestseller: boolean;
  is_skip_the_line: boolean;
  is_active?: boolean;
  average_rating: number;
  total_reviews: number;
  total_bookings: number;
  primary_image?: ActivityImage;
  images?: ActivityImage[];
  categories: Category[];
  destinations: Destination[];
  highlights?: ActivityHighlight[];
  includes?: ActivityInclude[];
  faqs?: ActivityFAQ[];
  meeting_point?: MeetingPoint;
  vendor?: {
    id: number;
    company_name: string;
    is_verified: boolean;
  };

  // New enhanced fields
  has_multiple_tiers?: boolean;
  discount_percentage?: number;
  original_price_adult?: number;
  original_price_child?: number;
  is_likely_to_sell_out?: boolean;
  has_mobile_ticket?: boolean;
  has_best_price_guarantee?: boolean;
  is_verified_activity?: boolean;
  response_time_hours?: number;
  is_wheelchair_accessible?: boolean;
  is_stroller_accessible?: boolean;
  allows_service_animals?: boolean;
  has_infant_seats?: boolean;
  video_url?: string;
  dress_code?: string;
  weather_dependent?: boolean;
  not_suitable_for?: string;
  what_to_bring?: string;
  has_covid_measures?: boolean;
  covid_measures?: string;
  is_giftable?: boolean;
  allows_reserve_now_pay_later?: boolean;
  reserve_payment_deadline_hours?: number;

  // New relationships
  timelines?: ActivityTimeline[];
  time_slots?: ActivityTimeSlot[];
  pricing_tiers?: ActivityPricingTier[];
  add_ons?: ActivityAddOn[];
}

export interface ActivityImage {
  id: number;
  url: string;
  alt_text?: string;
  caption?: string;
  is_primary: boolean;
  is_hero: boolean;
  order_index: number;
}

export interface ActivityHighlight {
  id: number;
  text: string;
  order_index: number;
}

export interface ActivityInclude {
  id: number;
  item: string;
  is_included: boolean;
  order_index: number;
}

export interface ActivityFAQ {
  id: number;
  question: string;
  answer: string;
  order_index: number;
}

export interface MeetingPointPhoto {
  id: number;
  url: string;
  caption?: string;
  order_index: number;
}

export interface MeetingPoint {
  id: number;
  address: string;
  instructions?: string;
  latitude?: number;
  longitude?: number;
  parking_info?: string;
  public_transport_info?: string;
  nearby_landmarks?: string;
  photos?: MeetingPointPhoto[];
}

export interface Booking {
  id: number;
  booking_ref: string;
  activity: {
    id: number;
    title: string;
    slug: string;
    primary_image?: string;
    duration_minutes?: number;
  };
  booking_date: string;
  booking_time?: string;
  adults: number;
  children: number;
  total_participants: number;
  total_price: number;
  currency: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';
  customer_name?: string;
  customer_email?: string;
  customer_phone?: string;
  special_requirements?: string;
  created_at: string;
  confirmed_at?: string;
}

export interface CartItem {
  id: number;
  activity: {
    id: number;
    title: string;
    slug: string;
    primary_image?: string;
    duration_minutes?: number;
    price_adult: number;
    price_child?: number;
  };
  booking_date: string;
  booking_time?: string;
  adults: number;
  children: number;
  price: number;
  created_at: string;
}

export interface ReviewCategory {
  id: number;
  category_name: string;
  rating: number;
}

export interface Review {
  id: number;
  user: {
    id: number;
    name: string;
    avatar?: string;
  };
  rating: number;
  title?: string;
  comment?: string;
  is_verified_booking: boolean;
  helpful_count: number;
  created_at: string;
  images?: ReviewImage[];
  category_ratings?: ReviewCategory[];
}

export interface ReviewImage {
  id: number;
  url: string;
  caption?: string;
}

export interface Availability {
  id: number;
  date: string;
  start_time?: string;
  end_time?: string;
  spots_available: number;
  spots_total: number;
  price_adult?: number;
  price_child?: number;
  is_available: boolean;
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  message?: string;
  pagination: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
    has_next: boolean;
    has_prev: boolean;
  };
}

export interface ActivityHighlight {
  id: number;
  text: string;
  order_index: number;
}

export interface ActivityInclude {
  id: number;
  item: string;
  is_included: boolean;
  order_index: number;
}

export interface ActivityFAQ {
  id: number;
  question: string;
  answer: string;
  order_index: number;
}

export interface MeetingPoint {
  id: number;
  address: string;
  instructions?: string;
  latitude: number;
  longitude: number;
}

export interface ActivityDetailResponse extends Activity {
  description: string;
  max_group_size: number;
  instant_confirmation: boolean;
  images: ActivityImage[];
  highlights: ActivityHighlight[];
  includes: ActivityInclude[];
  faqs: ActivityFAQ[];
  meeting_point?: MeetingPoint;
  vendor: {
    id: number;
    company_name: string;
    is_verified: boolean;
  };

  // Ensure new fields are present
  timelines: ActivityTimeline[];
  time_slots: ActivityTimeSlot[];
  pricing_tiers: ActivityPricingTier[];
  add_ons: ActivityAddOn[];
}

export interface SearchParams {
  q?: string;
  destination_id?: number;
  destination_slug?: string;
  category_id?: number;
  category_slug?: string;
  min_price?: number;
  max_price?: number;
  min_duration?: number;
  max_duration?: number;
  min_rating?: number;
  languages?: string[];
  free_cancellation?: boolean;
  instant_confirmation?: boolean;
  skip_the_line?: boolean;
  bestseller?: boolean;
  sort_by?: 'recommended' | 'price_asc' | 'price_desc' | 'rating' | 'duration';
  page?: number;
  per_page?: number;
}