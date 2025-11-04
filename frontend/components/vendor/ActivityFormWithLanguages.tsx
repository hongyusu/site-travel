'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api, apiClient } from '@/lib/api';
import { Plus, X, Save, Globe, Languages, Info } from 'lucide-react';
import { languages, Language, useLanguage } from '@/contexts/LanguageContext';

interface ActivityFormWithLanguagesProps {
  activityId?: number;
  mode: 'create' | 'edit';
}

interface TranslatableContent {
  [key: string]: {
    title: string;
    short_description: string;
    description: string;
    dress_code: string;
    what_to_bring: string;
    not_suitable_for: string;
    covid_measures: string;
    cancellation_policy: string;
    highlights: string[];
    includes: { item: string; is_included: boolean }[];
    faqs: { question: string; answer: string }[];
  };
}

export default function ActivityFormWithLanguages({ activityId, mode }: ActivityFormWithLanguagesProps) {
  const { getTranslation } = useLanguage();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [categories, setCategories] = useState<any[]>([]);
  const [destinations, setDestinations] = useState<any[]>([]);
  const [activeLanguage, setActiveLanguage] = useState<Language>('en');
  // All 4 languages are always supported
  const enabledLanguages: Language[] = ['en', 'es', 'zh', 'fr'];

  // Non-translatable fields (shared across all languages)
  const [baseData, setBaseData] = useState({
    price_adult: '',
    price_child: '',
    duration_minutes: '',
    max_group_size: '',
    instant_confirmation: true,
    free_cancellation_hours: 24,
    languages: ['English'], // Available guide languages
    is_bestseller: false,
    is_skip_the_line: false,
    category_ids: [] as number[],
    destination_ids: [] as number[],
    // Features
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
    meeting_point: {
      address: '',
      instructions: '',
      latitude: null as number | null,
      longitude: null as number | null,
    },
  });

  // Translatable fields (separate for each language)
  const [translations, setTranslations] = useState<TranslatableContent>({
    en: {
      title: '',
      short_description: '',
      description: '',
      dress_code: '',
      what_to_bring: '',
      not_suitable_for: '',
      covid_measures: '',
      cancellation_policy: '',
      highlights: [''],
      includes: [{ item: '', is_included: true }],
      faqs: [{ question: '', answer: '' }],
    },
    es: {
      title: '',
      short_description: '',
      description: '',
      dress_code: '',
      what_to_bring: '',
      not_suitable_for: '',
      covid_measures: '',
      cancellation_policy: '',
      highlights: [''],
      includes: [{ item: '', is_included: true }],
      faqs: [{ question: '', answer: '' }],
    },
    zh: {
      title: '',
      short_description: '',
      description: '',
      dress_code: '',
      what_to_bring: '',
      not_suitable_for: '',
      covid_measures: '',
      cancellation_policy: '',
      highlights: [''],
      includes: [{ item: '', is_included: true }],
      faqs: [{ question: '', answer: '' }],
    },
    fr: {
      title: '',
      short_description: '',
      description: '',
      dress_code: '',
      what_to_bring: '',
      not_suitable_for: '',
      covid_measures: '',
      cancellation_policy: '',
      highlights: [''],
      includes: [{ item: '', is_included: true }],
      faqs: [{ question: '', answer: '' }],
    },
  });

  useEffect(() => {
    fetchMetadata();
    if (mode === 'edit' && activityId) {
      fetchActivity();
    }
  }, [mode, activityId]);

  const fetchMetadata = async () => {
    try {
      // Force English for vendor interface by making direct calls with explicit English params
      const token = localStorage.getItem('access_token');
      const headers: any = {
        'Content-Type': 'application/json',
      };
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
      
      const [categoriesRes, destinationsRes] = await Promise.all([
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/activities/categories?language=en`, {
          headers,
        }).then(res => res.json()),
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/activities/destinations?language=en`, {
          headers,
        }).then(res => res.json())
      ]);
      
      setCategories(categoriesRes);
      setDestinations(destinationsRes);
    } catch (error) {
      console.error('Error fetching metadata:', error);
    }
  };

  const fetchActivity = async () => {
    if (!activityId) return;
    setLoading(true);
    try {
      // Fetch activity data for all languages by making separate API calls with language parameter
      const promises = languages.map(async (lang) => {
        const token = localStorage.getItem('access_token');
        const headers: any = {
          'Content-Type': 'application/json',
        };
        if (token) {
          headers.Authorization = `Bearer ${token}`;
        }
        
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/activities/${activityId}?language=${lang.code}`,
          { headers }
        );
        const data = await response.json();
        
        return {
          lang: lang.code,
          data: data
        };
      });

      const results = await Promise.all(promises);

      // Set base data from English version
      const englishData = results.find(r => r.lang === 'en')?.data;
      if (englishData) {
        setBaseData({
          price_adult: englishData.price_adult.toString(),
          price_child: englishData.price_child?.toString() || '',
          duration_minutes: englishData.duration_minutes?.toString() || '',
          max_group_size: englishData.max_group_size?.toString() || '',
          instant_confirmation: englishData.instant_confirmation,
          free_cancellation_hours: englishData.free_cancellation_hours,
          languages: englishData.languages || ['English'],
          is_bestseller: englishData.is_bestseller,
          is_skip_the_line: englishData.is_skip_the_line,
          category_ids: englishData.categories?.map((c: any) => c.id) || [],
          destination_ids: englishData.destinations?.map((d: any) => d.id) || [],
          has_mobile_ticket: englishData.has_mobile_ticket || false,
          has_best_price_guarantee: englishData.has_best_price_guarantee || false,
          is_verified_activity: englishData.is_verified_activity || false,
          is_likely_to_sell_out: englishData.is_likely_to_sell_out || false,
          is_wheelchair_accessible: englishData.is_wheelchair_accessible || false,
          is_stroller_accessible: englishData.is_stroller_accessible || false,
          allows_service_animals: englishData.allows_service_animals || false,
          has_infant_seats: englishData.has_infant_seats || false,
          is_giftable: englishData.is_giftable || false,
          allows_reserve_now_pay_later: englishData.allows_reserve_now_pay_later || false,
          has_covid_measures: englishData.has_covid_measures || false,
          weather_dependent: englishData.weather_dependent || false,
          response_time_hours: englishData.response_time_hours?.toString() || '',
          reserve_payment_deadline_hours: englishData.reserve_payment_deadline_hours?.toString() || '',
          video_url: englishData.video_url || '',
          meeting_point: englishData.meeting_point || {
            address: '',
            instructions: '',
            latitude: null,
            longitude: null,
          },
        });
      }

      // Set translations for each language - all 4 languages are always supported
      const newTranslations: TranslatableContent = {};
      
      results.forEach(({ lang, data }) => {
        newTranslations[lang] = {
          title: data.title || '',
          short_description: data.short_description || '',
          description: data.description || '',
          dress_code: data.dress_code || '',
          what_to_bring: data.what_to_bring || '',
          not_suitable_for: data.not_suitable_for || '',
          covid_measures: data.covid_measures || '',
          cancellation_policy: data.cancellation_policy || '',
          highlights: data.highlights?.map((h: any) => h.text) || [''],
          includes: data.includes?.map((i: any) => ({ item: i.item, is_included: i.is_included })) || [{ item: '', is_included: true }],
          faqs: data.faqs?.map((f: any) => ({ question: f.question, answer: f.answer })) || [{ question: '', answer: '' }],
        };
      });
      
      setTranslations(newTranslations);
    } catch (error) {
      console.error('Error fetching activity:', error);
      setError('Failed to load activity');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError('');

    try {
      // Prepare data for submission
      const activityData = {
        ...baseData,
        ...translations['en'], // English is the base language
        price_adult: parseFloat(baseData.price_adult),
        price_child: baseData.price_child ? parseFloat(baseData.price_child) : null,
        duration_minutes: baseData.duration_minutes ? parseInt(baseData.duration_minutes) : null,
        max_group_size: baseData.max_group_size ? parseInt(baseData.max_group_size) : null,
        response_time_hours: baseData.response_time_hours ? parseInt(baseData.response_time_hours) : null,
        reserve_payment_deadline_hours: baseData.reserve_payment_deadline_hours ? parseInt(baseData.reserve_payment_deadline_hours) : null,
        supported_languages: enabledLanguages, // Always all 4 languages
        translations: {
          es: translations['es'],
          zh: translations['zh'],
          fr: translations['fr']
        },
      };

      console.log('Submitting activity data:', activityData);
      console.log('Mode:', mode, 'ActivityId:', activityId);

      if (mode === 'create') {
        const result = await apiClient.activities.create(activityData);
        console.log('Create result:', result);
      } else {
        const result = await apiClient.activities.update(activityId!, activityData);
        console.log('Update result:', result);
      }

      router.push('/vendor/dashboard');
    } catch (error: any) {
      console.error('Error saving activity:', error);
      console.error('Error details:', error.response?.data);
      setError(error.response?.data?.detail || error.message || 'Failed to save activity');
    } finally {
      setSaving(false);
    }
  };

  // Language selection is removed - all languages are always supported

  const updateTranslation = (lang: Language, field: string, value: any) => {
    setTranslations(prev => ({
      ...prev,
      [lang]: {
        ...prev[lang],
        [field]: value,
      },
    }));
  };

  const addHighlight = (lang: Language) => {
    if (lang !== 'en') return; // Only allow editing in English
    updateTranslation(lang, 'highlights', [...translations[lang].highlights, '']);
  };

  const removeHighlight = (lang: Language, index: number) => {
    if (lang !== 'en') return; // Only allow editing in English
    const newHighlights = translations[lang].highlights.filter((_, i) => i !== index);
    updateTranslation(lang, 'highlights', newHighlights);
  };

  const updateHighlight = (lang: Language, index: number, value: string) => {
    if (lang !== 'en') return; // Only allow editing in English
    const newHighlights = [...translations[lang].highlights];
    newHighlights[index] = value;
    updateTranslation(lang, 'highlights', newHighlights);
  };

  const addInclude = (lang: Language) => {
    if (lang !== 'en') return; // Only allow editing in English
    updateTranslation(lang, 'includes', [...translations[lang].includes, { item: '', is_included: true }]);
  };

  const removeInclude = (lang: Language, index: number) => {
    if (lang !== 'en') return; // Only allow editing in English
    const newIncludes = translations[lang].includes.filter((_, i) => i !== index);
    updateTranslation(lang, 'includes', newIncludes);
  };

  const updateInclude = (lang: Language, index: number, field: string, value: any) => {
    if (lang !== 'en') return; // Only allow editing in English
    const newIncludes = [...translations[lang].includes];
    newIncludes[index] = { ...newIncludes[index], [field]: value };
    updateTranslation(lang, 'includes', newIncludes);
  };

  const addFaq = (lang: Language) => {
    if (lang !== 'en') return; // Only allow editing in English
    updateTranslation(lang, 'faqs', [...translations[lang].faqs, { question: '', answer: '' }]);
  };

  const removeFaq = (lang: Language, index: number) => {
    if (lang !== 'en') return; // Only allow editing in English
    const newFaqs = translations[lang].faqs.filter((_, i) => i !== index);
    updateTranslation(lang, 'faqs', newFaqs);
  };

  const updateFaq = (lang: Language, index: number, field: string, value: string) => {
    if (lang !== 'en') return; // Only allow editing in English
    const newFaqs = [...translations[lang].faqs];
    newFaqs[index] = { ...newFaqs[index], [field]: value };
    updateTranslation(lang, 'faqs', newFaqs);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {/* Language Support Information */}
      <div className="mb-8 p-6 bg-white rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Languages className="w-5 h-5" />
          Supported Languages
        </h3>
        <p className="text-sm text-gray-600 mb-4">
          This activity supports all 4 languages. Provide translations for as many languages as possible. Missing translations will show as empty to users in those languages.
        </p>
        <div className="flex flex-wrap gap-3">
          {languages.map((lang) => (
            <div
              key={lang.code}
              className="px-4 py-2 rounded-lg border-2 border-primary bg-primary text-white"
            >
              <span className="mr-2">{lang.flag}</span>
              {lang.name}
              {lang.code === 'en' && <span className="ml-2 text-xs">(Required)</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Language Tabs for Translatable Content */}
      <div className="mb-8 p-6 bg-white rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold mb-4">Content by Language</h3>
        
        {/* Global Translation Notice */}
        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-start gap-3">
            <Info className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="text-sm font-medium text-blue-900 mb-1">Translation System</h4>
              <p className="text-sm text-blue-700">
                <strong>English content is required</strong> - this is the base content for your activity. 
                Other languages are currently <strong>read-only</strong> and will be handled automatically in future updates. 
                Focus on creating great English content, and translations will be available soon.
              </p>
            </div>
          </div>
        </div>

        {/* Language Tab Navigation */}
        <div className="border-b mb-6">
          <nav className="flex space-x-4">
            {enabledLanguages.map((lang) => {
              const langInfo = languages.find(l => l.code === lang);
              return (
                <button
                  key={lang}
                  type="button"
                  onClick={() => setActiveLanguage(lang)}
                  className={`pb-2 px-1 border-b-2 transition-colors ${
                    activeLanguage === lang
                      ? 'border-primary text-primary'
                      : 'border-transparent text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <span className="mr-2">{langInfo?.flag}</span>
                  {langInfo?.name}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Translatable Fields */}
        <div className="space-y-6">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Title <span className="text-red-500">*</span>
              {activeLanguage !== 'en' && (
                <span className="ml-2 text-sm text-amber-600">(Read-only - Translation not available yet)</span>
              )}
            </label>
            <input
              type="text"
              value={translations[activeLanguage].title}
              onChange={(e) => activeLanguage === 'en' ? updateTranslation(activeLanguage, 'title', e.target.value) : null}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none ${
                activeLanguage !== 'en' ? 'bg-gray-100 cursor-not-allowed' : ''
              }`}
              required={activeLanguage === 'en'}
              disabled={activeLanguage !== 'en'}
              placeholder={activeLanguage !== 'en' && !translations[activeLanguage].title ?
                `Translation will be available soon` : activeLanguage === 'en' ? 'Enter activity title' : ''}
            />
            {activeLanguage !== 'en' && (
              <p className="mt-1 text-sm text-blue-600 flex items-center gap-1">
                <Info className="w-4 h-4" />
                Translations will be handled automatically. Currently showing English content.
              </p>
            )}
          </div>

          {/* Short Description */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Short Description
              {activeLanguage !== 'en' && (
                <span className="ml-2 text-sm text-amber-600">(Read-only)</span>
              )}
            </label>
            <textarea
              value={translations[activeLanguage].short_description}
              onChange={(e) => activeLanguage === 'en' ? updateTranslation(activeLanguage, 'short_description', e.target.value) : null}
              rows={2}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none ${
                activeLanguage !== 'en' ? 'bg-gray-100 cursor-not-allowed' : ''
              }`}
              disabled={activeLanguage !== 'en'}
              placeholder={activeLanguage !== 'en' ? 'Translation will be available soon' : 'Brief description of the activity'}
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Full Description <span className="text-red-500">*</span>
              {activeLanguage !== 'en' && (
                <span className="ml-2 text-sm text-amber-600">(Read-only)</span>
              )}
            </label>
            <textarea
              value={translations[activeLanguage].description}
              onChange={(e) => activeLanguage === 'en' ? updateTranslation(activeLanguage, 'description', e.target.value) : null}
              rows={6}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none ${
                activeLanguage !== 'en' ? 'bg-gray-100 cursor-not-allowed' : ''
              }`}
              required={activeLanguage === 'en'}
              disabled={activeLanguage !== 'en'}
              placeholder={activeLanguage !== 'en' ? 'Translation will be available soon' : 'Enter full description of the activity'}
            />
          </div>

          {/* Highlights */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Highlights
              {activeLanguage !== 'en' && (
                <span className="ml-2 text-sm text-amber-600">(Read-only)</span>
              )}
            </label>
            {translations[activeLanguage].highlights.map((highlight, index) => (
              <div key={index} className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={highlight}
                  onChange={(e) => activeLanguage === 'en' ? updateHighlight(activeLanguage, index, e.target.value) : null}
                  className={`flex-1 px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none ${
                    activeLanguage !== 'en' ? 'bg-gray-100 cursor-not-allowed' : ''
                  }`}
                  disabled={activeLanguage !== 'en'}
                  placeholder={activeLanguage !== 'en' ? 'Translation will be available soon' : 'Enter a highlight'}
                />
                {activeLanguage === 'en' && (
                  <button
                    type="button"
                    onClick={() => removeHighlight(activeLanguage, index)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    <X className="w-5 h-5" />
                  </button>
                )}
              </div>
            ))}
            {activeLanguage === 'en' && (
              <button
                type="button"
                onClick={() => addHighlight(activeLanguage)}
                className="mt-2 flex items-center gap-2 px-4 py-2 text-primary border border-primary rounded-lg hover:bg-orange-50"
              >
                <Plus className="w-4 h-4" />
                Add Highlight
              </button>
            )}
            {activeLanguage !== 'en' && (
              <p className="mt-1 text-sm text-blue-600 flex items-center gap-1">
                <Info className="w-4 h-4" />
                Translations will be handled automatically. Currently showing English content.
              </p>
            )}
          </div>

          {/* Included/Excluded Items */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Included/Excluded Items
              {activeLanguage !== 'en' && (
                <span className="ml-2 text-sm text-amber-600">(Read-only)</span>
              )}
            </label>
            {translations[activeLanguage].includes.map((include, index) => (
              <div key={index} className="flex gap-2 mb-2">
                <select
                  value={include.is_included ? 'included' : 'excluded'}
                  onChange={(e) => activeLanguage === 'en' ? updateInclude(activeLanguage, index, 'is_included', e.target.value === 'included') : null}
                  className={`px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none ${
                    activeLanguage !== 'en' ? 'bg-gray-100 cursor-not-allowed' : ''
                  }`}
                  disabled={activeLanguage !== 'en'}
                >
                  <option value="included">Included</option>
                  <option value="excluded">Not Included</option>
                </select>
                <input
                  type="text"
                  value={include.item}
                  onChange={(e) => activeLanguage === 'en' ? updateInclude(activeLanguage, index, 'item', e.target.value) : null}
                  className={`flex-1 px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none ${
                    activeLanguage !== 'en' ? 'bg-gray-100 cursor-not-allowed' : ''
                  }`}
                  disabled={activeLanguage !== 'en'}
                  placeholder={activeLanguage !== 'en' ? 'Translation will be available soon' : 'Enter item'}
                />
                {activeLanguage === 'en' && (
                  <button
                    type="button"
                    onClick={() => removeInclude(activeLanguage, index)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    <X className="w-5 h-5" />
                  </button>
                )}
              </div>
            ))}
            {activeLanguage === 'en' && (
              <button
                type="button"
                onClick={() => addInclude(activeLanguage)}
                className="mt-2 flex items-center gap-2 px-4 py-2 text-primary border border-primary rounded-lg hover:bg-orange-50"
              >
                <Plus className="w-4 h-4" />
                Add Item
              </button>
            )}
            {activeLanguage !== 'en' && (
              <p className="mt-1 text-sm text-blue-600 flex items-center gap-1">
                <Info className="w-4 h-4" />
                Translations will be handled automatically. Currently showing English content.
              </p>
            )}
          </div>

          {/* Cancellation Policy */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Cancellation Policy
              {activeLanguage !== 'en' && (
                <span className="ml-2 text-sm text-amber-600">(Read-only)</span>
              )}
            </label>
            <textarea
              value={translations[activeLanguage].cancellation_policy}
              onChange={(e) => activeLanguage === 'en' ? updateTranslation(activeLanguage, 'cancellation_policy', e.target.value) : null}
              rows={3}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none ${
                activeLanguage !== 'en' ? 'bg-gray-100 cursor-not-allowed' : ''
              }`}
              disabled={activeLanguage !== 'en'}
              placeholder={activeLanguage !== 'en' ? 'Translation will be available soon' : 'Enter cancellation policy details'}
            />
            {activeLanguage !== 'en' && (
              <p className="mt-1 text-sm text-blue-600 flex items-center gap-1">
                <Info className="w-4 h-4" />
                Translations will be handled automatically. Currently showing English content.
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Non-translatable Fields (Base Data) */}
      <div className="mb-8 p-6 bg-white rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold mb-4">Pricing & Details</h3>
        <p className="text-sm text-gray-600 mb-4">
          These settings apply to all languages.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Price Adult */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Adult Price (€) <span className="text-red-500">*</span>
            </label>
            <input
              type="number"
              step="0.01"
              value={baseData.price_adult}
              onChange={(e) => setBaseData({ ...baseData, price_adult: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none"
              required
            />
          </div>

          {/* Price Child */}
          <div>
            <label className="block text-sm font-medium mb-2">Child Price (€)</label>
            <input
              type="number"
              step="0.01"
              value={baseData.price_child}
              onChange={(e) => setBaseData({ ...baseData, price_child: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none"
            />
          </div>

          {/* Duration */}
          <div>
            <label className="block text-sm font-medium mb-2">Duration (minutes)</label>
            <input
              type="number"
              value={baseData.duration_minutes}
              onChange={(e) => setBaseData({ ...baseData, duration_minutes: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none"
            />
          </div>

          {/* Max Group Size */}
          <div>
            <label className="block text-sm font-medium mb-2">Max Group Size</label>
            <input
              type="number"
              value={baseData.max_group_size}
              onChange={(e) => setBaseData({ ...baseData, max_group_size: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none"
            />
          </div>

          {/* Categories */}
          <div>
            <label className="block text-sm font-medium mb-2">Categories</label>
            <select
              multiple
              value={baseData.category_ids.map(String)}
              onChange={(e) => {
                const selected = Array.from(e.target.selectedOptions, option => parseInt(option.value));
                setBaseData({ ...baseData, category_ids: selected });
              }}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none"
              size={4}
            >
              {categories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
            <p className="text-xs text-gray-600 mt-1">Hold Ctrl/Cmd to select multiple</p>
          </div>

          {/* Destinations */}
          <div>
            <label className="block text-sm font-medium mb-2">Destinations</label>
            <select
              multiple
              value={baseData.destination_ids.map(String)}
              onChange={(e) => {
                const selected = Array.from(e.target.selectedOptions, option => parseInt(option.value));
                setBaseData({ ...baseData, destination_ids: selected });
              }}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none"
              size={4}
            >
              {destinations.map(dest => (
                <option key={dest.id} value={dest.id}>{dest.name}</option>
              ))}
            </select>
            <p className="text-xs text-gray-600 mt-1">Hold Ctrl/Cmd to select multiple</p>
          </div>
        </div>

        {/* Features Checkboxes */}
        <div className="mt-6">
          <h4 className="font-medium mb-3">Features</h4>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {[
              { key: 'instant_confirmation', label: 'Instant Confirmation' },
              { key: 'has_mobile_ticket', label: 'Mobile Ticket' },
              { key: 'is_bestseller', label: 'Bestseller' },
              { key: 'is_skip_the_line', label: 'Skip the Line' },
              { key: 'is_wheelchair_accessible', label: 'Wheelchair Accessible' },
              { key: 'allows_reserve_now_pay_later', label: 'Reserve Now, Pay Later' },
              { key: 'is_giftable', label: 'Giftable' },
              { key: 'weather_dependent', label: 'Weather Dependent' },
            ].map(({ key, label }) => (
              <label key={key} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={baseData[key as keyof typeof baseData] as boolean}
                  onChange={(e) => setBaseData({ ...baseData, [key]: e.target.checked })}
                  className="w-4 h-4 text-primary rounded focus:ring-2 focus:ring-primary"
                />
                <span className="text-sm">{label}</span>
              </label>
            ))}
          </div>
        </div>
      </div>

      {/* Submit Buttons */}
      <div className="flex justify-end gap-4">
        <button
          type="button"
          onClick={() => router.push('/vendor/dashboard')}
          className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={saving}
          className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <Save className="w-4 h-4" />
          {saving ? 'Saving...' : mode === 'create' ? 'Create Activity' : 'Update Activity'}
        </button>
      </div>
    </form>
  );
}