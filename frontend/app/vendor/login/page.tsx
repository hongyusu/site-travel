'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api';

export default function VendorLoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const returnUrl = searchParams.get('return') || '/vendor/dashboard';

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await apiClient.auth.login(formData.email, formData.password);

      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);

      // Verify user is a vendor
      try {
        const profileResponse = await apiClient.auth.getProfile();
        if (profileResponse.data.role !== 'vendor') {
          setError('Access denied. Vendor account required.');
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          setLoading(false);
          return;
        }
      } catch (profileError) {
        console.error('Profile check error:', profileError);
        setError('Failed to verify vendor account. Please try again.');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setLoading(false);
        return;
      }

      // Trigger auth change event
      window.dispatchEvent(new Event('storage'));
      window.dispatchEvent(new CustomEvent('auth-change'));

      // Small delay to ensure localStorage is written
      await new Promise(resolve => setTimeout(resolve, 100));

      // Use Next.js router for redirect
      console.log('Redirecting to:', returnUrl);
      router.replace(returnUrl);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Vendor Login</h2>
            <p className="mt-2 text-gray-600">Sign in to manage your activities</p>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
                className="input-field"
                placeholder="vendor@example.com"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                required
                className="input-field"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary disabled:opacity-50"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Don't have a vendor account?{' '}
              <Link href="/vendor/register" className="text-primary hover:text-primary-600 font-medium">
                Register here
              </Link>
            </p>
            <p className="mt-2 text-sm text-gray-600">
              <Link href="/" className="text-primary hover:text-primary-600 font-medium">
                Back to Home
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
