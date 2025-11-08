'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { Trash2, ShoppingCart } from 'lucide-react';
import { CartItem } from '@/types';
import { apiClient } from '@/lib/api';
import { getImageUrl } from '@/lib/utils';
import { useLocation } from '@/contexts/LocationContext';

export default function CartPage() {
  const router = useRouter();
  const { formatPrice } = useLocation();
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [removing, setRemoving] = useState<number | null>(null);
  const [updating, setUpdating] = useState<number | null>(null);

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const response = await apiClient.cart.list();
      const items = response.data?.data || response.data || [];
      setCartItems(Array.isArray(items) ? items : []);
    } catch (error) {
      console.error('Error fetching cart:', error);
      setCartItems([]);
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (itemId: number) => {
    setRemoving(itemId);
    try {
      await apiClient.cart.remove(itemId);
      setCartItems(cartItems.filter(item => item.id !== itemId));
    } catch (error) {
      console.error('Error removing item:', error);
      alert('Failed to remove item. Please try again.');
    } finally {
      setRemoving(null);
    }
  };

  const handleUpdateQuantity = async (itemId: number, adults: number, children: number) => {
    setUpdating(itemId);
    const item = cartItems.find(i => i.id === itemId);
    if (!item) return;

    const newPrice = (adults * item.activity.price_adult) +
                     (children * (item.activity.price_child || 0));

    try {
      await apiClient.cart.update(itemId, {
        activity_id: item.activity.id,
        booking_date: item.booking_date,
        booking_time: item.booking_time,
        adults,
        children
      });

      setCartItems(cartItems.map(i =>
        i.id === itemId
          ? { ...i, adults, children, price: newPrice }
          : i
      ));
    } catch (error) {
      console.error('Error updating quantity:', error);
      alert('Failed to update quantity. Please try again.');
    } finally {
      setUpdating(null);
    }
  };

  const handleCheckout = () => {
    router.push('/checkout');
  };

  const subtotal = cartItems.reduce((sum, item) => sum + (Number(item.price) || 0), 0);
  const tax = 0; // No tax for now
  const total = subtotal + tax;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8" />
            <div className="grid grid-cols-3 gap-8">
              <div className="col-span-2 space-y-4">
                <div className="h-32 bg-gray-200 rounded" />
                <div className="h-32 bg-gray-200 rounded" />
              </div>
              <div className="h-64 bg-gray-200 rounded" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (cartItems.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <ShoppingCart className="w-24 h-24 text-gray-300 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Your cart is empty</h1>
          <p className="text-gray-600 mb-8">
            Looks like you haven't added any activities yet
          </p>
          <Link href="/search" className="btn-primary">
            Browse Activities
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow">
              {cartItems.map((item) => (
                <div
                  key={item.id}
                  className="p-6 border-b last:border-0 flex gap-4"
                >
                  {/* Image */}
                  <div className="relative w-32 h-32 flex-shrink-0 rounded-lg overflow-hidden">
                    <Image
                      src={getImageUrl(item.activity.primary_image)}
                      alt={item.activity.title}
                      fill
                      className="object-cover"
                    />
                  </div>

                  {/* Details */}
                  <div className="flex-1">
                    <Link
                      href={`/activities/${item.activity.slug}`}
                      className="font-semibold text-gray-900 hover:text-primary mb-2 block"
                    >
                      {item.activity.title}
                    </Link>

                    <div className="text-sm text-gray-600 space-y-1">
                      <div>
                        Date: {new Date(item.booking_date).toLocaleDateString('en-US', {
                          weekday: 'long',
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </div>
                      {item.booking_time && <div>Time: {item.booking_time}</div>}
                    </div>

                    {/* Quantity Controls */}
                    <div className="mt-3 flex items-center space-x-6">
                      <div className="flex items-center">
                        <label className="text-sm text-gray-600 mr-2">Adults:</label>
                        <div className="flex items-center">
                          <button
                            onClick={() => handleUpdateQuantity(item.id, Math.max(1, item.adults - 1), item.children)}
                            disabled={updating === item.id || item.adults <= 1}
                            className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            -
                          </button>
                          <span className="w-8 text-center">{item.adults}</span>
                          <button
                            onClick={() => handleUpdateQuantity(item.id, item.adults + 1, item.children)}
                            disabled={updating === item.id}
                            className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50 disabled:opacity-50"
                          >
                            +
                          </button>
                        </div>
                      </div>

                      <div className="flex items-center">
                        <label className="text-sm text-gray-600 mr-2">Children:</label>
                        <div className="flex items-center">
                          <button
                            onClick={() => handleUpdateQuantity(item.id, item.adults, Math.max(0, item.children - 1))}
                            disabled={updating === item.id || item.children <= 0}
                            className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            -
                          </button>
                          <span className="w-8 text-center">{item.children}</span>
                          <button
                            onClick={() => handleUpdateQuantity(item.id, item.adults, item.children + 1)}
                            disabled={updating === item.id}
                            className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50 disabled:opacity-50"
                          >
                            +
                          </button>
                        </div>
                      </div>
                    </div>

                    <div className="mt-4 flex items-center justify-between">
                      <div className="text-xl font-bold text-gray-900">
                        {formatPrice(item.price)}
                      </div>

                      <button
                        onClick={() => handleRemove(item.id)}
                        disabled={removing === item.id}
                        className="text-red-600 hover:text-red-700 flex items-center disabled:opacity-50"
                      >
                        <Trash2 className="w-4 h-4 mr-1" />
                        {removing === item.id ? 'Removing...' : 'Remove'}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6 sticky top-24">
              <h2 className="text-xl font-bold mb-4">Order Summary</h2>

              <div className="space-y-3 mb-6">
                <div className="flex justify-between text-gray-600">
                  <span>Subtotal</span>
                  <span>{formatPrice(subtotal)}</span>
                </div>
                {tax > 0 && (
                  <div className="flex justify-between text-gray-600">
                    <span>Tax</span>
                    <span>{formatPrice(tax)}</span>
                  </div>
                )}
                <div className="border-t pt-3 flex justify-between text-lg font-bold">
                  <span>Total</span>
                  <span>{formatPrice(total)}</span>
                </div>
              </div>

              <button
                onClick={handleCheckout}
                className="btn-primary w-full mb-4"
              >
                Proceed to Checkout
              </button>

              <Link
                href="/search"
                className="block text-center text-primary hover:text-primary-600"
              >
                Continue Shopping
              </Link>

              {/* Security Badge */}
              <div className="mt-6 pt-6 border-t text-center text-sm text-gray-600">
                <div className="flex items-center justify-center mb-2">
                  <svg className="w-5 h-5 text-success mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                  </svg>
                  Secure Checkout
                </div>
                <p className="text-xs">
                  Your payment information is encrypted and secure
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}