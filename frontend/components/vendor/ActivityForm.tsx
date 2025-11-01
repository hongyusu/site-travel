'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { Plus, X, Save } from 'lucide-react';

interface ActivityFormProps {
  activityId?: number;
  mode: 'create' | 'edit';
}

export default function ActivityForm({ activityId, mode }: ActivityFormProps) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [categories, setCategories] = useState<any[]>([]);
  const [destinations, setDestinations] = useState<any[]>([]);

  const [formData, setFormData] = useState({
    title: '',
    short_description: '',
    description: '',
    price_adult: '',
    price_child: '',
    duration_minutes: '',
    max_group_size: '',
    instant_confirmation: true,
    free_cancellation_hours: 24,
    languages: ['English'],
    is_bestseller: false,
    is_skip_the_line: false,
    category_ids: [] as number[],
    destination_ids: [] as number[],
    images: [{ url: '', alt_text: '' }],
    highlights: [''],
    includes: [{ item: '', is_included: true }],
    faqs: [{ question: '', answer: '' }],
    meeting_point: {
      address: '',
      instructions: '',
      latitude: null as number | null,
      longitude: null as number | null,
      photos: [] as Array<{ url: string; caption: string }>,
    },
    // Enhanced features
    has_mobile_ticket: false,
    has_best_price_guarantee: false,
    is_verified_activity: false,
    is_likely_to_sell_out: false,
    is_wheelchair_accessible: false,
    is_stroller_accessible: false,
    allows_service_animals: false,
    has_infant_seats: false,
    is_giftable: false,
    allows_reserve_now_pay_later: false,
    has_covid_measures: false,
    weather_dependent: false,
    response_time_hours: '',
    reserve_payment_deadline_hours: '',
    video_url: '',
    dress_code: '',
    what_to_bring: '',
    not_suitable_for: '',
    covid_measures: '',
    // Enhanced relationships
    timelines: [] as any[],
    time_slots: [] as any[],
    pricing_tiers: [] as any[],
    add_ons: [] as any[],
  });

  useEffect(() => {
    fetchMetadata();
    if (mode === 'edit' && activityId) {
      fetchActivity();
    }
  }, [mode, activityId]);

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

  const fetchActivity = async () => {
    if (!activityId) return;

    setLoading(true);
    try {
      const response = await apiClient.activities.getById(activityId);
      const activity = response.data;

      setFormData({
        title: activity.title,
        short_description: activity.short_description || '',
        description: activity.description || '',
        price_adult: activity.price_adult.toString(),
        price_child: activity.price_child?.toString() || '',
        duration_minutes: activity.duration_minutes?.toString() || '',
        max_group_size: activity.max_group_size?.toString() || '',
        instant_confirmation: activity.instant_confirmation,
        free_cancellation_hours: activity.free_cancellation_hours,
        languages: activity.languages || ['English'],
        is_bestseller: activity.is_bestseller,
        is_skip_the_line: activity.is_skip_the_line,
        category_ids: activity.categories?.map((c: any) => c.id) || [],
        destination_ids: activity.destinations?.map((d: any) => d.id) || [],
        images: activity.images?.map((img: any) => ({ url: img.url, alt_text: img.alt_text || '' })) || [{ url: '', alt_text: '' }],
        highlights: activity.highlights?.map((h: any) => h.text) || [''],
        includes: activity.includes?.map((i: any) => ({ item: i.item, is_included: i.is_included })) || [{ item: '', is_included: true }],
        faqs: activity.faqs?.map((f: any) => ({ question: f.question, answer: f.answer })) || [{ question: '', answer: '' }],
        meeting_point: activity.meeting_point || {
          address: '',
          instructions: '',
          latitude: null,
          longitude: null,
        },
        // Enhanced features
        has_mobile_ticket: activity.has_mobile_ticket || false,
        has_best_price_guarantee: activity.has_best_price_guarantee || false,
        is_verified_activity: activity.is_verified_activity || false,
        is_likely_to_sell_out: activity.is_likely_to_sell_out || false,
        is_wheelchair_accessible: activity.is_wheelchair_accessible || false,
        is_stroller_accessible: activity.is_stroller_accessible || false,
        allows_service_animals: activity.allows_service_animals || false,
        has_infant_seats: activity.has_infant_seats || false,
        is_giftable: activity.is_giftable || false,
        allows_reserve_now_pay_later: activity.allows_reserve_now_pay_later || false,
        has_covid_measures: activity.has_covid_measures || false,
        weather_dependent: activity.weather_dependent || false,
        response_time_hours: activity.response_time_hours?.toString() || '',
        reserve_payment_deadline_hours: activity.reserve_payment_deadline_hours?.toString() || '',
        video_url: activity.video_url || '',
        dress_code: activity.dress_code || '',
        what_to_bring: activity.what_to_bring || '',
        not_suitable_for: activity.not_suitable_for || '',
        covid_measures: activity.covid_measures || '',
        // Enhanced relationships
        timelines: activity.timelines || [],
        time_slots: activity.time_slots || [],
        pricing_tiers: activity.pricing_tiers || [],
        add_ons: activity.add_ons || [],
      });
    } catch (error: any) {
      console.error('Error fetching activity:', error);
      setError(error.response?.data?.detail || 'Failed to load activity');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSaving(true);

    try {
      const submitData = {
        ...formData,
        price_adult: parseFloat(formData.price_adult),
        price_child: formData.price_child ? parseFloat(formData.price_child) : null,
        duration_minutes: formData.duration_minutes ? parseInt(formData.duration_minutes) : null,
        max_group_size: formData.max_group_size ? parseInt(formData.max_group_size) : null,
        response_time_hours: formData.response_time_hours ? parseInt(formData.response_time_hours) : null,
        reserve_payment_deadline_hours: formData.reserve_payment_deadline_hours ? parseInt(formData.reserve_payment_deadline_hours) : null,
        highlights: formData.highlights.filter(h => h.trim() !== ''),
        includes: formData.includes.filter(i => i.item.trim() !== ''),
        faqs: formData.faqs.filter(f => f.question.trim() !== '' && f.answer.trim() !== ''),
        images: formData.images.filter(img => img.url.trim() !== ''),
        timelines: formData.timelines.filter(t => t.title?.trim()),
        time_slots: formData.time_slots.filter(s => s.slot_time?.trim()),
        pricing_tiers: formData.pricing_tiers.filter(p => p.tier_name?.trim() && p.price_adult),
        add_ons: formData.add_ons.filter(a => a.name?.trim() && a.price),
      };

      if (mode === 'create') {
        await apiClient.activities.create(submitData);
      } else if (activityId) {
        await apiClient.activities.update(activityId, submitData);
      }

      router.push('/vendor/dashboard');
    } catch (error: any) {
      console.error('Error saving activity:', error);
      setError(error.response?.data?.detail || 'Failed to save activity');
    } finally {
      setSaving(false);
    }
  };

  const addArrayItem = (field: string, defaultValue: any) => {
    setFormData({
      ...formData,
      [field]: [...(formData as any)[field], defaultValue]
    });
  };

  const removeArrayItem = (field: string, index: number) => {
    setFormData({
      ...formData,
      [field]: (formData as any)[field].filter((_: any, i: number) => i !== index)
    });
  };

  const updateArrayItem = (field: string, index: number, value: any) => {
    const newArray = [...(formData as any)[field]];
    newArray[index] = value;
    setFormData({ ...formData, [field]: newArray });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-4xl mx-auto py-8 px-4">
      <div className="bg-white rounded-lg shadow p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          {mode === 'create' ? 'Create New Activity' : 'Edit Activity'}
        </h1>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        {/* Basic Information */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Basic Information</h2>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Activity Title *
            </label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="input-field"
              placeholder="e.g., Paris City Walking Tour"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Short Description
            </label>
            <textarea
              value={formData.short_description}
              onChange={(e) => setFormData({ ...formData, short_description: e.target.value })}
              className="input-field"
              rows={2}
              placeholder="Brief description (shown in listings)"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Full Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="input-field"
              rows={6}
              placeholder="Detailed description of the activity"
            />
          </div>
        </div>

        {/* Pricing & Duration */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Pricing & Duration</h2>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Adult Price ($) *
              </label>
              <input
                type="number"
                step="0.01"
                required
                value={formData.price_adult}
                onChange={(e) => setFormData({ ...formData, price_adult: e.target.value })}
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Child Price ($)
              </label>
              <input
                type="number"
                step="0.01"
                value={formData.price_child}
                onChange={(e) => setFormData({ ...formData, price_child: e.target.value })}
                className="input-field"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Duration (minutes)
              </label>
              <input
                type="number"
                value={formData.duration_minutes}
                onChange={(e) => setFormData({ ...formData, duration_minutes: e.target.value })}
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Group Size
              </label>
              <input
                type="number"
                value={formData.max_group_size}
                onChange={(e) => setFormData({ ...formData, max_group_size: e.target.value })}
                className="input-field"
              />
            </div>
          </div>
        </div>

        {/* Categories & Destinations */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Categories & Destinations</h2>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Categories
            </label>
            <div className="grid grid-cols-2 gap-2">
              {categories.map(category => (
                <label key={category.id} className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.category_ids.includes(category.id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setFormData({
                          ...formData,
                          category_ids: [...formData.category_ids, category.id]
                        });
                      } else {
                        setFormData({
                          ...formData,
                          category_ids: formData.category_ids.filter(id => id !== category.id)
                        });
                      }
                    }}
                    className="rounded border-gray-300"
                  />
                  <span className="text-sm">{category.name}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Destinations
            </label>
            <div className="grid grid-cols-2 gap-2">
              {destinations.map(destination => (
                <label key={destination.id} className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.destination_ids.includes(destination.id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setFormData({
                          ...formData,
                          destination_ids: [...formData.destination_ids, destination.id]
                        });
                      } else {
                        setFormData({
                          ...formData,
                          destination_ids: formData.destination_ids.filter(id => id !== destination.id)
                        });
                      }
                    }}
                    className="rounded border-gray-300"
                  />
                  <span className="text-sm">{destination.name}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Images */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Images</h2>
          {formData.images.map((image, index) => (
            <div key={index} className="flex gap-4">
              <div className="flex-1">
                <input
                  type="url"
                  value={image.url}
                  onChange={(e) => updateArrayItem('images', index, { ...image, url: e.target.value })}
                  className="input-field"
                  placeholder="Image URL"
                />
              </div>
              <button
                type="button"
                onClick={() => removeArrayItem('images', index)}
                className="text-red-600 hover:text-red-700"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          ))}
          <button
            type="button"
            onClick={() => addArrayItem('images', { url: '', alt_text: '' })}
            className="btn-secondary text-sm"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Image
          </button>
        </div>

        {/* Meeting Point */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Meeting Point</h2>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Address
            </label>
            <input
              type="text"
              value={formData.meeting_point.address}
              onChange={(e) => setFormData({
                ...formData,
                meeting_point: { ...formData.meeting_point, address: e.target.value }
              })}
              className="input-field"
              placeholder="Meeting point address"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Instructions
            </label>
            <textarea
              value={formData.meeting_point.instructions}
              onChange={(e) => setFormData({
                ...formData,
                meeting_point: { ...formData.meeting_point, instructions: e.target.value }
              })}
              className="input-field"
              rows={3}
              placeholder="Additional instructions for finding the meeting point"
            />
          </div>

          {/* Meeting Point Photos */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Meeting Point Photos
            </label>
            <div className="space-y-3">
              {formData.meeting_point.photos.map((photo, index) => (
                <div key={index} className="flex gap-2">
                  <div className="flex-1 space-y-2">
                    <input
                      type="text"
                      value={photo.url}
                      onChange={(e) => {
                        const newPhotos = [...formData.meeting_point.photos];
                        newPhotos[index] = { ...photo, url: e.target.value };
                        setFormData({
                          ...formData,
                          meeting_point: { ...formData.meeting_point, photos: newPhotos }
                        });
                      }}
                      className="input-field"
                      placeholder="Photo URL"
                    />
                    <input
                      type="text"
                      value={photo.caption}
                      onChange={(e) => {
                        const newPhotos = [...formData.meeting_point.photos];
                        newPhotos[index] = { ...photo, caption: e.target.value };
                        setFormData({
                          ...formData,
                          meeting_point: { ...formData.meeting_point, photos: newPhotos }
                        });
                      }}
                      className="input-field"
                      placeholder="Caption (optional)"
                    />
                  </div>
                  {photo.url && (
                    <div className="w-20 h-20 rounded-lg overflow-hidden border border-gray-200">
                      <img
                        src={photo.url}
                        alt={`Meeting point ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )}
                  <button
                    type="button"
                    onClick={() => {
                      const newPhotos = formData.meeting_point.photos.filter((_, i) => i !== index);
                      setFormData({
                        ...formData,
                        meeting_point: { ...formData.meeting_point, photos: newPhotos }
                      });
                    }}
                    className="btn-secondary self-start"
                  >
                    Remove
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={() => {
                  setFormData({
                    ...formData,
                    meeting_point: {
                      ...formData.meeting_point,
                      photos: [...formData.meeting_point.photos, { url: '', caption: '' }]
                    }
                  });
                }}
                className="btn-secondary"
              >
                + Add Photo
              </button>
            </div>
          </div>
        </div>

        {/* Options */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Options</h2>

          <div className="space-y-4">
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.instant_confirmation}
                onChange={(e) => setFormData({ ...formData, instant_confirmation: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm font-medium">Instant Confirmation</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.is_skip_the_line}
                onChange={(e) => setFormData({ ...formData, is_skip_the_line: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm font-medium">Skip the Line</span>
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Free Cancellation (hours before)
            </label>
            <input
              type="number"
              value={formData.free_cancellation_hours}
              onChange={(e) => setFormData({ ...formData, free_cancellation_hours: parseInt(e.target.value) || 0 })}
              className="input-field"
            />
          </div>
        </div>

        {/* Enhanced Features */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Enhanced Features</h2>

          <div className="grid grid-cols-2 gap-4">
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.has_mobile_ticket}
                onChange={(e) => setFormData({ ...formData, has_mobile_ticket: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">Mobile Ticket Available</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.has_best_price_guarantee}
                onChange={(e) => setFormData({ ...formData, has_best_price_guarantee: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">Best Price Guarantee</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.is_verified_activity}
                onChange={(e) => setFormData({ ...formData, is_verified_activity: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">Verified Activity</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.is_likely_to_sell_out}
                onChange={(e) => setFormData({ ...formData, is_likely_to_sell_out: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">Likely to Sell Out</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.is_wheelchair_accessible}
                onChange={(e) => setFormData({ ...formData, is_wheelchair_accessible: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">Wheelchair Accessible</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.is_stroller_accessible}
                onChange={(e) => setFormData({ ...formData, is_stroller_accessible: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">Stroller Accessible</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.allows_service_animals}
                onChange={(e) => setFormData({ ...formData, allows_service_animals: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">Service Animals Allowed</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.has_infant_seats}
                onChange={(e) => setFormData({ ...formData, has_infant_seats: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">Infant Seats Available</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.is_giftable}
                onChange={(e) => setFormData({ ...formData, is_giftable: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">Gift Option Available</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.allows_reserve_now_pay_later}
                onChange={(e) => setFormData({ ...formData, allows_reserve_now_pay_later: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">Reserve Now, Pay Later</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.has_covid_measures}
                onChange={(e) => setFormData({ ...formData, has_covid_measures: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">COVID-19 Safety Measures</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.weather_dependent}
                onChange={(e) => setFormData({ ...formData, weather_dependent: e.target.checked })}
                className="rounded border-gray-300"
              />
              <span className="text-sm">Weather Dependent</span>
            </label>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Response Time (hours)
              </label>
              <input
                type="number"
                value={formData.response_time_hours}
                onChange={(e) => setFormData({ ...formData, response_time_hours: e.target.value })}
                className="input-field"
                placeholder="e.g., 24"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Payment Deadline (hours before)
              </label>
              <input
                type="number"
                value={formData.reserve_payment_deadline_hours}
                onChange={(e) => setFormData({ ...formData, reserve_payment_deadline_hours: e.target.value })}
                className="input-field"
                placeholder="e.g., 48"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Video URL
            </label>
            <input
              type="url"
              value={formData.video_url}
              onChange={(e) => setFormData({ ...formData, video_url: e.target.value })}
              className="input-field"
              placeholder="https://youtube.com/watch?v=..."
            />
          </div>
        </div>

        {/* Additional Information */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Additional Information</h2>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dress Code
            </label>
            <textarea
              value={formData.dress_code}
              onChange={(e) => setFormData({ ...formData, dress_code: e.target.value })}
              className="input-field"
              rows={2}
              placeholder="e.g., Casual attire, no shorts in religious sites"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              What to Bring
            </label>
            <textarea
              value={formData.what_to_bring}
              onChange={(e) => setFormData({ ...formData, what_to_bring: e.target.value })}
              className="input-field"
              rows={3}
              placeholder="e.g., Passport or ID, Comfortable shoes, Water bottle"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Not Suitable For
            </label>
            <textarea
              value={formData.not_suitable_for}
              onChange={(e) => setFormData({ ...formData, not_suitable_for: e.target.value })}
              className="input-field"
              rows={2}
              placeholder="e.g., People with mobility issues, pregnant women"
            />
          </div>

          {formData.has_covid_measures && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                COVID-19 Safety Measures
              </label>
              <textarea
                value={formData.covid_measures}
                onChange={(e) => setFormData({ ...formData, covid_measures: e.target.value })}
                className="input-field"
                rows={3}
                placeholder="e.g., Masks required, social distancing, sanitizer provided"
              />
            </div>
          )}
        </div>

        {/* Timeline/Itinerary */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Timeline / Itinerary</h2>
          {formData.timelines.map((timeline, index) => (
            <div key={index} className="p-4 border border-gray-200 rounded-lg space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">Step {index + 1}</span>
                <button
                  type="button"
                  onClick={() => removeArrayItem('timelines', index)}
                  className="text-red-600 hover:text-red-700"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <input
                  type="text"
                  value={timeline.title || ''}
                  onChange={(e) => updateArrayItem('timelines', index, { ...timeline, title: e.target.value })}
                  className="input-field"
                  placeholder="Step title"
                />
                <input
                  type="number"
                  value={timeline.duration_minutes || ''}
                  onChange={(e) => updateArrayItem('timelines', index, { ...timeline, duration_minutes: parseInt(e.target.value) || 0 })}
                  className="input-field"
                  placeholder="Duration (min)"
                />
              </div>

              <textarea
                value={timeline.description || ''}
                onChange={(e) => updateArrayItem('timelines', index, { ...timeline, description: e.target.value })}
                className="input-field"
                rows={2}
                placeholder="Step description"
              />

              <input
                type="url"
                value={timeline.image_url || ''}
                onChange={(e) => updateArrayItem('timelines', index, { ...timeline, image_url: e.target.value })}
                className="input-field"
                placeholder="Step image URL (optional)"
              />
            </div>
          ))}
          <button
            type="button"
            onClick={() => addArrayItem('timelines', { step_number: formData.timelines.length + 1, title: '', description: '', duration_minutes: 0, order_index: formData.timelines.length })}
            className="btn-secondary text-sm"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Timeline Step
          </button>
        </div>

        {/* Time Slots */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Available Time Slots</h2>
          {formData.time_slots.map((slot, index) => (
            <div key={index} className="p-4 border border-gray-200 rounded-lg">
              <div className="flex gap-3 items-start">
                <div className="flex-1 grid grid-cols-3 gap-3">
                  <input
                    type="time"
                    value={slot.slot_time || ''}
                    onChange={(e) => updateArrayItem('time_slots', index, { ...slot, slot_time: e.target.value })}
                    className="input-field"
                    placeholder="Time"
                  />
                  <input
                    type="text"
                    value={slot.slot_label || ''}
                    onChange={(e) => updateArrayItem('time_slots', index, { ...slot, slot_label: e.target.value })}
                    className="input-field"
                    placeholder="Label (Morning/Afternoon)"
                  />
                  <input
                    type="number"
                    step="0.01"
                    value={slot.price_adjustment || 0}
                    onChange={(e) => updateArrayItem('time_slots', index, { ...slot, price_adjustment: parseFloat(e.target.value) || 0 })}
                    className="input-field"
                    placeholder="Price +/- adjustment"
                  />
                </div>
                <button
                  type="button"
                  onClick={() => removeArrayItem('time_slots', index)}
                  className="text-red-600 hover:text-red-700"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))}
          <button
            type="button"
            onClick={() => addArrayItem('time_slots', { slot_time: '', is_available: true, price_adjustment: 0 })}
            className="btn-secondary text-sm"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Time Slot
          </button>
        </div>

        {/* Pricing Tiers */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Pricing Tiers</h2>
          {formData.pricing_tiers.map((tier, index) => (
            <div key={index} className="p-4 border border-gray-200 rounded-lg space-y-3">
              <div className="flex justify-between items-center">
                <input
                  type="text"
                  value={tier.tier_name || ''}
                  onChange={(e) => updateArrayItem('pricing_tiers', index, { ...tier, tier_name: e.target.value })}
                  className="input-field flex-1 mr-3"
                  placeholder="Tier name (Standard/Premium/VIP)"
                />
                <button
                  type="button"
                  onClick={() => removeArrayItem('pricing_tiers', index)}
                  className="text-red-600 hover:text-red-700"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <textarea
                value={tier.tier_description || ''}
                onChange={(e) => updateArrayItem('pricing_tiers', index, { ...tier, tier_description: e.target.value })}
                className="input-field"
                rows={2}
                placeholder="Tier description"
              />

              <div className="grid grid-cols-2 gap-3">
                <input
                  type="number"
                  step="0.01"
                  value={tier.price_adult || ''}
                  onChange={(e) => updateArrayItem('pricing_tiers', index, { ...tier, price_adult: parseFloat(e.target.value) || 0 })}
                  className="input-field"
                  placeholder="Adult price"
                />
                <input
                  type="number"
                  step="0.01"
                  value={tier.price_child || ''}
                  onChange={(e) => updateArrayItem('pricing_tiers', index, { ...tier, price_child: parseFloat(e.target.value) || 0 })}
                  className="input-field"
                  placeholder="Child price (optional)"
                />
              </div>
            </div>
          ))}
          <button
            type="button"
            onClick={() => addArrayItem('pricing_tiers', { tier_name: '', price_adult: 0, is_active: true, order_index: formData.pricing_tiers.length })}
            className="btn-secondary text-sm"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Pricing Tier
          </button>
        </div>

        {/* Add-ons */}
        <div className="space-y-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 border-b pb-2">Add-ons</h2>
          {formData.add_ons.map((addOn, index) => (
            <div key={index} className="p-4 border border-gray-200 rounded-lg space-y-3">
              <div className="flex gap-3 items-start">
                <div className="flex-1">
                  <input
                    type="text"
                    value={addOn.name || ''}
                    onChange={(e) => updateArrayItem('add_ons', index, { ...addOn, name: e.target.value })}
                    className="input-field mb-2"
                    placeholder="Add-on name"
                  />
                  <textarea
                    value={addOn.description || ''}
                    onChange={(e) => updateArrayItem('add_ons', index, { ...addOn, description: e.target.value })}
                    className="input-field"
                    rows={2}
                    placeholder="Description"
                  />
                </div>
                <button
                  type="button"
                  onClick={() => removeArrayItem('add_ons', index)}
                  className="text-red-600 hover:text-red-700"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <input
                  type="number"
                  step="0.01"
                  value={addOn.price || ''}
                  onChange={(e) => updateArrayItem('add_ons', index, { ...addOn, price: parseFloat(e.target.value) || 0 })}
                  className="input-field"
                  placeholder="Price"
                />
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={!addOn.is_optional}
                    onChange={(e) => updateArrayItem('add_ons', index, { ...addOn, is_optional: !e.target.checked })}
                    className="rounded border-gray-300"
                  />
                  <span className="text-sm">Required</span>
                </label>
              </div>
            </div>
          ))}
          <button
            type="button"
            onClick={() => addArrayItem('add_ons', { name: '', price: 0, is_optional: true, order_index: formData.add_ons.length })}
            className="btn-secondary text-sm"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Extra
          </button>
        </div>

        {/* Submit Buttons */}
        <div className="flex justify-end space-x-4 pt-6 border-t">
          <button
            type="button"
            onClick={() => router.back()}
            className="btn-secondary"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="btn-primary flex items-center disabled:opacity-50"
          >
            <Save className="w-5 h-5 mr-2" />
            {saving ? 'Saving...' : mode === 'create' ? 'Create Activity' : 'Save Changes'}
          </button>
        </div>
      </div>
    </form>
  );
}
