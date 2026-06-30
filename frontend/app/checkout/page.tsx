'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { CreditCard, Shield, ArrowLeft, Info, Check } from 'lucide-react';
import { CartItem } from '@/types';
import { apiClient } from '@/lib/api';
import { getImageUrl } from '@/lib/utils';
import { useLocation } from '@/contexts/LocationContext';
import { useLanguage } from '@/contexts/LanguageContext';
import { toast } from 'react-hot-toast';

interface TravelerInfo {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  country: string;
  specialRequirements: string;
}

export default function CheckoutPage() {
  const router = useRouter();
  const { formatPrice } = useLocation();
  const { getTranslation, getCountryName } = useLanguage();
  const [user, setUser] = useState<any>(null);
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [isGuest, setIsGuest] = useState(true);
  const [paymentMethod, setPaymentMethod] = useState('card');
  const [agreeToTerms, setAgreeToTerms] = useState(false);
  const [travelerInfo, setTravelerInfo] = useState<TravelerInfo>({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    country: 'United States',
    specialRequirements: ''
  });

  useEffect(() => {
    checkAuth();
    fetchCart();
  }, []);

  const checkAuth = async () => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (token) {
      try {
        const response = await apiClient.auth.getProfile();
        const userData = response.data;
        setUser(userData);
        setIsGuest(false);
        setTravelerInfo(prev => ({
          ...prev,
          email: userData.email,
          firstName: userData.full_name?.split(' ')[0] || '',
          lastName: userData.full_name?.split(' ').slice(1).join(' ') || '',
          phone: userData.phone || ''
        }));
      } catch (error) {
        console.error('Error fetching user:', error);
        // Stay as guest if authentication fails
      }
    }
  };

  const fetchCart = async () => {
    try {
      const response = await apiClient.cart.list();
      const items = response.data?.data || response.data || [];

      if (!Array.isArray(items) || items.length === 0) {
        router.push('/cart');
        return;
      }

      setCartItems(items);
    } catch (error) {
      console.error('Error fetching cart:', error);
      toast.error('Failed to load cart items');
      router.push('/cart');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: keyof TravelerInfo, value: string) => {
    setTravelerInfo(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const validateForm = () => {
    if (!travelerInfo.firstName || !travelerInfo.lastName) {
      toast.error(getTranslation('checkout.validate_name'));
      return false;
    }
    if (!travelerInfo.email) {
      toast.error(getTranslation('checkout.validate_email'));
      return false;
    }
    if (!travelerInfo.phone) {
      toast.error(getTranslation('checkout.validate_phone'));
      return false;
    }
    if (!agreeToTerms) {
      toast.error(getTranslation('checkout.validate_terms'));
      return false;
    }
    return true;
  };

  // Fallback when Stripe is not configured: create bookings directly (no charge).
  const completeWithoutPayment = async () => {
    const bookingResponses = await Promise.all(
      cartItems.map(item =>
        apiClient.bookings.create({
          activity_id: item.activity.id,
          booking_date: item.booking_date,
          booking_time: item.booking_time,
          adults: item.adults,
          children: item.children,
          customer_name: `${travelerInfo.firstName} ${travelerInfo.lastName}`,
          customer_email: travelerInfo.email,
          customer_phone: travelerInfo.phone,
          special_requirements: travelerInfo.specialRequirements
        })
      )
    );
    await Promise.all(cartItems.map(item => apiClient.cart.remove(item.id)));
    toast.success(getTranslation('checkout.booking_success'));
    const firstBookingRef = bookingResponses[0]?.data?.booking_ref;
    router.push(firstBookingRef ? `/order-confirmation?ref=${firstBookingRef}` : '/orders');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setProcessing(true);
    try {
      // Create a Stripe Checkout Session and redirect to the hosted payment page.
      const res = await apiClient.payments.createCheckoutSession({
        origin: window.location.origin,
        customer_name: `${travelerInfo.firstName} ${travelerInfo.lastName}`,
        customer_email: travelerInfo.email,
        customer_phone: travelerInfo.phone,
        special_requirements: travelerInfo.specialRequirements,
      });

      if (res.data?.url) {
        window.location.href = res.data.url; // leave the spinner up while navigating away
        return;
      }

      // Payments disabled on the backend → fall back to the no-charge flow.
      await completeWithoutPayment();
      setProcessing(false);
    } catch (error) {
      console.error('Error starting checkout:', error);
      toast.error(getTranslation('checkout.booking_error'));
      setProcessing(false);
    }
  };

  const subtotal = cartItems.reduce((sum, item) => sum + (Number(item.price) || 0), 0);
  const serviceFee = subtotal * 0.05; // 5% service fee
  const total = subtotal + serviceFee;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8" />
            <div className="grid grid-cols-3 gap-8">
              <div className="col-span-2 space-y-4">
                <div className="h-96 bg-gray-200 rounded" />
              </div>
              <div className="h-96 bg-gray-200 rounded" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <Link href="/cart" className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            {getTranslation('checkout.back_to_cart')}
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">{getTranslation('checkout.title')}</h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Form */}
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit}>
              {/* Login/Guest Option */}
              {!user && (
                <div className="bg-paper rounded-lg shadow p-6 mb-6">
                  <h2 className="text-xl font-bold mb-4">{getTranslation('checkout.account')}</h2>
                  <div className="space-y-3">
                    <label className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
                      <input
                        type="radio"
                        checked={!isGuest}
                        onChange={() => setIsGuest(false)}
                        className="mr-3"
                      />
                      <div>
                        <div className="font-medium">{getTranslation('checkout.login_create')}</div>
                        <div className="text-sm text-gray-600">{getTranslation('checkout.login_create_sub')}</div>
                      </div>
                    </label>
                    <label className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
                      <input
                        type="radio"
                        checked={isGuest}
                        onChange={() => setIsGuest(true)}
                        className="mr-3"
                      />
                      <div>
                        <div className="font-medium">{getTranslation('checkout.guest')}</div>
                        <div className="text-sm text-gray-600">{getTranslation('checkout.guest_sub')}</div>
                      </div>
                    </label>
                  </div>
                  {!isGuest && (
                    <div className="mt-4 pt-4 border-t">
                      <Link href="/login?redirect=/checkout" className="btn-primary">
                        {getTranslation('checkout.login_signup')}
                      </Link>
                    </div>
                  )}
                </div>
              )}

              {/* Traveler Information */}
              <div className="bg-paper rounded-lg shadow p-6 mb-6">
                <h2 className="text-xl font-bold mb-4">{getTranslation('checkout.traveler_info')}</h2>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {getTranslation('checkout.first_name')}
                    </label>
                    <input
                      type="text"
                      value={travelerInfo.firstName}
                      onChange={(e) => handleInputChange('firstName', e.target.value)}
                      className="input-field"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {getTranslation('checkout.last_name')}
                    </label>
                    <input
                      type="text"
                      value={travelerInfo.lastName}
                      onChange={(e) => handleInputChange('lastName', e.target.value)}
                      className="input-field"
                      required
                    />
                  </div>
                </div>

                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {getTranslation('checkout.email')}
                  </label>
                  <input
                    type="email"
                    value={travelerInfo.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    className="input-field"
                    required
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    {getTranslation('checkout.email_helper')}
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {getTranslation('checkout.phone')}
                    </label>
                    <input
                      type="tel"
                      value={travelerInfo.phone}
                      onChange={(e) => handleInputChange('phone', e.target.value)}
                      className="input-field"
                      placeholder="+1 (555) 123-4567"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {getTranslation('checkout.country')}
                    </label>
                    <select
                      value={travelerInfo.country}
                      onChange={(e) => handleInputChange('country', e.target.value)}
                      className="input-field"
                    >
                      <option value="United States">{getCountryName('United States')}</option>
                      <option value="United Kingdom">{getCountryName('United Kingdom')}</option>
                      <option value="Canada">{getCountryName('Canada')}</option>
                      <option value="Australia">{getCountryName('Australia')}</option>
                      <option value="Germany">{getCountryName('Germany')}</option>
                      <option value="France">{getCountryName('France')}</option>
                      <option value="Spain">{getCountryName('Spain')}</option>
                      <option value="Italy">{getCountryName('Italy')}</option>
                      <option value="Japan">{getCountryName('Japan')}</option>
                      <option value="Other">{getCountryName('Other')}</option>
                    </select>
                  </div>
                </div>

                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {getTranslation('checkout.special_requirements')}
                  </label>
                  <textarea
                    value={travelerInfo.specialRequirements}
                    onChange={(e) => handleInputChange('specialRequirements', e.target.value)}
                    rows={4}
                    className="input-field"
                    placeholder={getTranslation('checkout.special_placeholder')}
                  />
                </div>

                {/* Important Information */}
                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-start">
                    <Info className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
                    <div className="text-sm text-blue-900">
                      <p className="font-medium mb-1">{getTranslation('checkout.important')}</p>
                      <ul className="list-disc list-inside space-y-1">
                        <li>{getTranslation('checkout.important_1')}</li>
                        <li>{getTranslation('checkout.important_2')}</li>
                        <li>{getTranslation('checkout.important_3')}</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              {/* Payment Method */}
              <div className="bg-paper rounded-lg shadow p-6 mb-6">
                <h2 className="text-xl font-bold mb-4">{getTranslation('checkout.payment_method')}</h2>

                <div className="space-y-3">
                  <label className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
                    <input
                      type="radio"
                      value="card"
                      checked={paymentMethod === 'card'}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                      className="mr-3"
                    />
                    <CreditCard className="w-6 h-6 mr-3 text-gray-600" />
                    <div>
                      <div className="font-medium">{getTranslation('checkout.card')}</div>
                      <div className="text-sm text-gray-600">{getTranslation('checkout.card_sub')}</div>
                    </div>
                  </label>

                  <label className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 opacity-50">
                    <input
                      type="radio"
                      value="paypal"
                      checked={paymentMethod === 'paypal'}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                      className="mr-3"
                      disabled
                    />
                    <div className="w-6 h-6 mr-3 bg-gray-200 rounded" />
                    <div>
                      <div className="font-medium">{getTranslation('checkout.paypal')}</div>
                      <div className="text-sm text-gray-600">{getTranslation('checkout.paypal_sub')}</div>
                    </div>
                  </label>
                </div>

                {paymentMethod === 'card' && (
                  <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600">
                      {getTranslation('checkout.redirect_note')}
                    </p>
                  </div>
                )}
              </div>

              {/* Terms and Conditions */}
              <div className="bg-paper rounded-lg shadow p-6">
                <label className="flex items-start cursor-pointer">
                  <input
                    type="checkbox"
                    checked={agreeToTerms}
                    onChange={(e) => setAgreeToTerms(e.target.checked)}
                    className="mt-1 mr-3"
                  />
                  <div className="text-sm">
                    {getTranslation('checkout.agree_prefix')}{' '}
                    <Link href="/terms" className="text-primary hover:underline">
                      {getTranslation('checkout.terms_link')}
                    </Link>
                    {' '}{getTranslation('checkout.and')}{' '}
                    <Link href="/privacy" className="text-primary hover:underline">
                      {getTranslation('checkout.privacy_link')}
                    </Link>
                    . I understand that my booking is subject to the activity provider's cancellation policy.
                  </div>
                </label>
              </div>
            </form>
          </div>

          {/* Order Summary Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-paper rounded-lg shadow p-6 sticky top-24">
              <h2 className="text-xl font-bold mb-4">{getTranslation('checkout.order_summary')}</h2>

              {/* Cart Items */}
              <div className="space-y-4 mb-6">
                {cartItems.map(item => (
                  <div key={item.id} className="flex space-x-3">
                    <div className="relative w-20 h-20 rounded-lg overflow-hidden flex-shrink-0">
                      <Image
                        src={getImageUrl(item.activity.primary_image)}
                        alt={item.activity.title}
                        fill
                        className="object-cover"
                      />
                    </div>
                    <div className="flex-1">
                      <h4 className="font-medium text-sm text-gray-900 line-clamp-2">
                        {item.activity.title}
                      </h4>
                      <p className="text-xs text-gray-600 mt-1">
                        {new Date(item.booking_date).toLocaleDateString()}
                      </p>
                      <p className="text-xs text-gray-600">
                        {item.adults} {item.adults > 1 ? getTranslation('common.adults') : getTranslation('common.adult')}
                        {item.children > 0 && `, ${item.children} ${item.children > 1 ? getTranslation('common.children') : getTranslation('common.child')}`}
                      </p>
                      <p className="text-sm font-medium text-gray-900 mt-1">
                        {formatPrice(item.price)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Price Breakdown */}
              <div className="space-y-3 border-t pt-4">
                <div className="flex justify-between text-gray-600">
                  <span>{getTranslation('cart.subtotal')}</span>
                  <span>{formatPrice(subtotal)}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>{getTranslation('checkout.service_fee')}</span>
                  <span>{formatPrice(serviceFee)}</span>
                </div>
                <div className="border-t pt-3 flex justify-between text-lg font-bold">
                  <span>{getTranslation('cart.total')}</span>
                  <span>{formatPrice(total)}</span>
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                onClick={handleSubmit}
                disabled={processing}
                className="btn-primary w-full mt-6 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {processing ? getTranslation('checkout.processing') : `${getTranslation('checkout.complete_booking')} • ${formatPrice(total)}`}
              </button>

              {/* Security Badge */}
              <div className="mt-6 pt-6 border-t text-center">
                <div className="flex items-center justify-center text-sm text-gray-600 mb-2">
                  <Shield className="w-5 h-5 text-success mr-2" />
                  {getTranslation('checkout.secure_payment')}
                </div>
                <p className="text-xs text-gray-500">
                  {getTranslation('cart.secure_note')}. {getTranslation('checkout.no_card_storage')}
                </p>
              </div>

              {/* Cancellation Info */}
              <div className="mt-4 p-3 bg-green-50 rounded-lg">
                <p className="text-xs text-green-800">
                  <span className="font-medium">Free Cancellation:</span> Most activities offer free cancellation up to 24 hours before the start time.
                </p>
              </div>

              {/* Features */}
              <div className="mt-4 space-y-2 text-sm text-gray-600">
                <div className="flex items-center">
                  <Check className="w-4 h-4 text-success mr-2" />
                  <span>Instant confirmation</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-4 h-4 text-success mr-2" />
                  <span>Mobile tickets accepted</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}