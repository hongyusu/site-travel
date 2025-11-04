'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { User, Mail, Phone, Calendar, Shield } from 'lucide-react';
import { apiClient } from '@/lib/api';
import { useLanguage } from '@/contexts/LanguageContext';

export default function MyAccountPage() {
  const { getTranslation } = useLanguage();
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    full_name: '',
    phone: ''
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/login?return=/my-account');
        return;
      }

      const response = await apiClient.auth.getProfile();
      setUser(response.data);
      setFormData({
        full_name: response.data.full_name || '',
        phone: response.data.phone || ''
      });
    } catch (error) {
      console.error('Error fetching profile:', error);
      // If unauthorized, redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      router.push('/login?return=/my-account');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.auth.updateProfile(formData);
      setUser({ ...user, ...formData });
      setEditing(false);
    } catch (error) {
      console.error('Error updating profile:', error);
      alert('Failed to update profile. Please try again.');
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto" />
          <p className="mt-4 text-gray-600">{getTranslation('account.loading')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">{getTranslation('account.my_account')}</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Sidebar */}
          <aside className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-center mb-6">
                <div className="w-24 h-24 bg-primary rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4">
                  {user?.full_name?.[0]?.toUpperCase() || 'U'}
                </div>
                <h2 className="text-xl font-semibold text-gray-900">{user?.full_name}</h2>
                <p className="text-gray-600">{user?.email}</p>
                {user?.role && (
                  <span className="inline-block mt-2 px-3 py-1 bg-primary-50 text-primary rounded-full text-sm">
                    {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
                  </span>
                )}
              </div>

              <nav className="space-y-2">
                <Link
                  href="/my-account"
                  className="block px-4 py-2 bg-primary-50 text-primary rounded-lg font-medium"
                >
                  {getTranslation('account.profile')}
                </Link>
                <Link
                  href="/bookings"
                  className="block px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg"
                >
                  {getTranslation('account.my_bookings')}
                </Link>
                <Link
                  href="/wishlist"
                  className="block px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg"
                >
                  {getTranslation('account.wishlist')}
                </Link>
                <Link
                  href="/settings"
                  className="block px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg"
                >
                  {getTranslation('account.settings')}
                </Link>
              </nav>
            </div>
          </aside>

          {/* Main Content */}
          <main className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">{getTranslation('account.profile_information')}</h2>
                {!editing && (
                  <button
                    onClick={() => setEditing(true)}
                    className="text-primary hover:text-primary-600 font-medium"
                  >
                    {getTranslation('account.edit_profile')}
                  </button>
                )}
              </div>

              {editing ? (
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                    <label htmlFor="full_name" className="block text-sm font-medium text-gray-700 mb-2">
                      {getTranslation('account.full_name')}
                    </label>
                    <input
                      type="text"
                      id="full_name"
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleInputChange}
                      required
                      className="input-field"
                    />
                  </div>

                  <div>
                    <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
                      {getTranslation('account.phone_number')}
                    </label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      className="input-field"
                    />
                  </div>

                  <div className="flex space-x-4">
                    <button type="submit" className="btn-primary">
                      {getTranslation('account.save_changes')}
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setEditing(false);
                        setFormData({
                          full_name: user?.full_name || '',
                          phone: user?.phone || ''
                        });
                      }}
                      className="btn-secondary"
                    >
                      {getTranslation('account.cancel')}
                    </button>
                  </div>
                </form>
              ) : (
                <div className="space-y-6">
                  <div className="flex items-start">
                    <User className="w-5 h-5 text-gray-400 mr-3 mt-1" />
                    <div>
                      <div className="text-sm text-gray-500">{getTranslation('account.full_name')}</div>
                      <div className="text-gray-900 font-medium">{user?.full_name || getTranslation('account.not_set')}</div>
                    </div>
                  </div>

                  <div className="flex items-start">
                    <Mail className="w-5 h-5 text-gray-400 mr-3 mt-1" />
                    <div>
                      <div className="text-sm text-gray-500">{getTranslation('account.email_address')}</div>
                      <div className="text-gray-900 font-medium">{user?.email}</div>
                      {user?.email_verified ? (
                        <span className="inline-flex items-center text-xs text-success mt-1">
                          <Shield className="w-3 h-3 mr-1" />
                          {getTranslation('account.verified')}
                        </span>
                      ) : (
                        <span className="text-xs text-gray-500 mt-1">{getTranslation('account.not_verified')}</span>
                      )}
                    </div>
                  </div>

                  <div className="flex items-start">
                    <Phone className="w-5 h-5 text-gray-400 mr-3 mt-1" />
                    <div>
                      <div className="text-sm text-gray-500">{getTranslation('account.phone_number')}</div>
                      <div className="text-gray-900 font-medium">{user?.phone || getTranslation('account.not_set')}</div>
                    </div>
                  </div>

                  <div className="flex items-start">
                    <Calendar className="w-5 h-5 text-gray-400 mr-3 mt-1" />
                    <div>
                      <div className="text-sm text-gray-500">{getTranslation('account.member_since')}</div>
                      <div className="text-gray-900 font-medium">
                        {new Date(user?.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Account Statistics */}
            <div className="grid grid-cols-3 gap-4 mt-6">
              <div className="bg-white rounded-lg shadow p-6 text-center">
                <div className="text-3xl font-bold text-primary mb-2">0</div>
                <div className="text-sm text-gray-600">{getTranslation('account.total_bookings')}</div>
              </div>
              <div className="bg-white rounded-lg shadow p-6 text-center">
                <div className="text-3xl font-bold text-primary mb-2">0</div>
                <div className="text-sm text-gray-600">{getTranslation('account.wishlist_items')}</div>
              </div>
              <div className="bg-white rounded-lg shadow p-6 text-center">
                <div className="text-3xl font-bold text-primary mb-2">0</div>
                <div className="text-sm text-gray-600">{getTranslation('account.reviews')}</div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}