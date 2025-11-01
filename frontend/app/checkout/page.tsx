'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { CreditCard, Shield, ArrowLeft, Info, Check } from 'lucide-react';
import { CartItem } from '@/types';
import { apiClient } from '@/lib/api';
import { formatPrice, getImageUrl } from '@/lib/utils';
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
      toast.error('Please enter your full name');
      return false;
    }
    if (!travelerInfo.email) {
      toast.error('Please enter your email address');
      return false;
    }
    if (!travelerInfo.phone) {
      toast.error('Please enter your phone number');
      return false;
    }
    if (!agreeToTerms) {
      toast.error('Please agree to the terms and conditions');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setProcessing(true);
    try {
      // Create bookings for each cart item
      const bookingPromises = cartItems.map(item =>
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
      );

      const bookingResponses = await Promise.all(bookingPromises);

      // Clear cart
      const clearPromises = cartItems.map(item => apiClient.cart.remove(item.id));
      await Promise.all(clearPromises);

      toast.success('Booking completed successfully!');

      // Redirect to order confirmation page with the first booking reference
      const firstBookingRef = bookingResponses[0]?.data?.booking_ref;
      if (firstBookingRef) {
        router.push(`/order-confirmation?ref=${firstBookingRef}`);
      } else {
        router.push('/orders');
      }
    } catch (error) {
      console.error('Error creating booking:', error);
      toast.error('Failed to complete booking. Please try again.');
    } finally {
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
            Back to Cart
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Checkout</h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Form */}
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit}>
              {/* Login/Guest Option */}
              {!user && (
                <div className="bg-white rounded-lg shadow p-6 mb-6">
                  <h2 className="text-xl font-bold mb-4">Account</h2>
                  <div className="space-y-3">
                    <label className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
                      <input
                        type="radio"
                        checked={!isGuest}
                        onChange={() => setIsGuest(false)}
                        className="mr-3"
                      />
                      <div>
                        <div className="font-medium">Login or create account</div>
                        <div className="text-sm text-gray-600">Save your booking details and earn rewards</div>
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
                        <div className="font-medium">Continue as guest</div>
                        <div className="text-sm text-gray-600">Quick checkout without creating an account</div>
                      </div>
                    </label>
                  </div>
                  {!isGuest && (
                    <div className="mt-4 pt-4 border-t">
                      <Link href="/login?redirect=/checkout" className="btn-primary">
                        Login / Sign Up
                      </Link>
                    </div>
                  )}
                </div>
              )}

              {/* Traveler Information */}
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h2 className="text-xl font-bold mb-4">Traveler Information</h2>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      First Name *
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
                      Last Name *
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
                    Email Address *
                  </label>
                  <input
                    type="email"
                    value={travelerInfo.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    className="input-field"
                    required
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    We'll send your booking confirmation here
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Phone Number *
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
                      Country/Region *
                    </label>
                    <select
                      value={travelerInfo.country}
                      onChange={(e) => handleInputChange('country', e.target.value)}
                      className="input-field"
                    >
                      <option value="United States">United States</option>
                      <option value="United Kingdom">United Kingdom</option>
                      <option value="Canada">Canada</option>
                      <option value="Australia">Australia</option>
                      <option value="Germany">Germany</option>
                      <option value="France">France</option>
                      <option value="Spain">Spain</option>
                      <option value="Italy">Italy</option>
                      <option value="Japan">Japan</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>

                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Special Requirements (Optional)
                  </label>
                  <textarea
                    value={travelerInfo.specialRequirements}
                    onChange={(e) => handleInputChange('specialRequirements', e.target.value)}
                    rows={4}
                    className="input-field"
                    placeholder="Any special requests or requirements..."
                  />
                </div>

                {/* Important Information */}
                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-start">
                    <Info className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
                    <div className="text-sm text-blue-900">
                      <p className="font-medium mb-1">Important:</p>
                      <ul className="list-disc list-inside space-y-1">
                        <li>Please ensure all names match your travel documents</li>
                        <li>You'll receive confirmation and tickets via email</li>
                        <li>Some activities may require additional information</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              {/* Payment Method */}
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h2 className="text-xl font-bold mb-4">Payment Method</h2>

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
                      <div className="font-medium">Credit / Debit Card</div>
                      <div className="text-sm text-gray-600">Secure payment with card</div>
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
                      <div className="font-medium">PayPal (Coming Soon)</div>
                      <div className="text-sm text-gray-600">Fast and secure checkout</div>
                    </div>
                  </label>
                </div>

                {paymentMethod === 'card' && (
                  <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600">
                      You will be redirected to our secure payment provider to complete your purchase.
                    </p>
                  </div>
                )}
              </div>

              {/* Terms and Conditions */}
              <div className="bg-white rounded-lg shadow p-6">
                <label className="flex items-start cursor-pointer">
                  <input
                    type="checkbox"
                    checked={agreeToTerms}
                    onChange={(e) => setAgreeToTerms(e.target.checked)}
                    className="mt-1 mr-3"
                  />
                  <div className="text-sm">
                    I agree to the{' '}
                    <Link href="/terms" className="text-primary hover:underline">
                      Terms and Conditions
                    </Link>
                    {' '}and{' '}
                    <Link href="/privacy" className="text-primary hover:underline">
                      Privacy Policy
                    </Link>
                    . I understand that my booking is subject to the activity provider's cancellation policy.
                  </div>
                </label>
              </div>
            </form>
          </div>

          {/* Order Summary Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6 sticky top-24">
              <h2 className="text-xl font-bold mb-4">Order Summary</h2>

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
                        {item.adults} adult{item.adults > 1 ? 's' : ''}
                        {item.children > 0 && `, ${item.children} child${item.children > 1 ? 'ren' : ''}`}
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
                  <span>Subtotal</span>
                  <span>{formatPrice(subtotal)}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Service Fee</span>
                  <span>{formatPrice(serviceFee)}</span>
                </div>
                <div className="border-t pt-3 flex justify-between text-lg font-bold">
                  <span>Total</span>
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
                {processing ? 'Processing...' : `Complete Booking • ${formatPrice(total)}`}
              </button>

              {/* Security Badge */}
              <div className="mt-6 pt-6 border-t text-center">
                <div className="flex items-center justify-center text-sm text-gray-600 mb-2">
                  <Shield className="w-5 h-5 text-success mr-2" />
                  Secure Payment
                </div>
                <p className="text-xs text-gray-500">
                  Your payment information is encrypted and secure.
                  We never store your card details.
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