'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Calendar, Users, Clock, TrendingUp, Eye, Zap, Award } from 'lucide-react';
import { ActivityDetailResponse } from '@/types';
import { formatPrice } from '@/lib/utils';
import { apiClient } from '@/lib/api';
import TimeSlotsSelector from '@/components/activities/TimeSlotsSelector';
import PricingTiersSelector from '@/components/activities/PricingTiersSelector';
import AddOnsSelector from '@/components/activities/AddOnsSelector';

interface BookingWidgetProps {
  activity: ActivityDetailResponse;
}

export default function BookingWidget({ activity }: BookingWidgetProps) {
  const router = useRouter();
  const [bookingDate, setBookingDate] = useState('');
  const [adults, setAdults] = useState(1);
  const [children, setChildren] = useState(0);
  const [selectedTimeSlotId, setSelectedTimeSlotId] = useState<number | undefined>();
  const [selectedTierId, setSelectedTierId] = useState<number | undefined>();
  const [selectedAddOns, setSelectedAddOns] = useState<{ id: number; quantity: number }[]>([]);
  const [loading, setLoading] = useState(false);
  const [viewingCount, setViewingCount] = useState(0);
  const [spotsLeft, setSpotsLeft] = useState(0);

  // Simulate viewing count and limited spots
  useEffect(() => {
    setViewingCount(Math.floor(Math.random() * 30) + 15);
    setSpotsLeft(Math.floor(Math.random() * 10) + 3);
  }, []);

  const totalParticipants = adults + children;

  // Calculate total price including pricing tiers, time slots, and add-ons
  const calculateTotalPrice = () => {
    let basePrice = parseFloat(String(activity.price_adult)) || 0;
    let childPrice = parseFloat(String(activity.price_child || 0)) || 0;

    // Use pricing tier prices if selected
    if (selectedTierId) {
      const tier = activity.pricing_tiers?.find(t => t.id === selectedTierId);
      if (tier) {
        basePrice = parseFloat(String(tier.price_adult)) || 0;
        childPrice = parseFloat(String(tier.price_child || 0)) || 0;
      }
    }

    // Add time slot price adjustment
    if (selectedTimeSlotId) {
      const slot = activity.time_slots?.find(s => s.id === selectedTimeSlotId);
      if (slot?.price_adjustment) {
        const adjustment = parseFloat(String(slot.price_adjustment)) || 0;
        basePrice += adjustment;
        childPrice += adjustment;
      }
    }

    // Calculate participant costs
    let total = basePrice * adults + childPrice * children;

    // Add add-ons
    selectedAddOns.forEach(selected => {
      const addOn = activity.add_ons?.find(a => a.id === selected.id);
      if (addOn) {
        const addOnPrice = parseFloat(String(addOn.price)) || 0;
        total += addOnPrice * selected.quantity;
      }
    });

    return total;
  };

  const totalPrice = calculateTotalPrice();

  const handleAddToCart = async () => {
    if (!bookingDate) {
      alert('Please select a date');
      return;
    }

    setLoading(true);
    try {
      const cartData: any = {
        activity_id: activity.id,
        booking_date: bookingDate,
        adults,
        children
      };

      // Add optional enhanced booking fields if selected
      if (selectedTimeSlotId) {
        cartData.time_slot_id = selectedTimeSlotId;
      }

      if (selectedTierId) {
        cartData.pricing_tier_id = selectedTierId;
      }

      if (selectedAddOns.length > 0) {
        cartData.add_on_ids = selectedAddOns.map(a => a.id);
        cartData.add_on_quantities = selectedAddOns.reduce((acc, a) => {
          acc[a.id] = a.quantity;
          return acc;
        }, {} as Record<number, number>);
      }

      await apiClient.cart.add(cartData);

      // Redirect to cart
      router.push('/cart');
    } catch (error) {
      console.error('Error adding to cart:', error);
      alert('Failed to add to cart. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const minDate = new Date().toISOString().split('T')[0];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 sticky top-24">
      {/* Social Proof Indicators */}
      {(viewingCount > 0 || spotsLeft < 10) && (
        <div className="mb-4 space-y-2">
          {viewingCount > 0 && (
            <div className="flex items-center text-sm text-orange-600 bg-orange-50 rounded-lg p-2">
              <Eye className="w-4 h-4 mr-2" />
              <span className="font-medium">{viewingCount} people</span>
              <span className="ml-1">viewing this activity now</span>
            </div>
          )}
          {spotsLeft < 10 && spotsLeft > 0 && (
            <div className="flex items-center text-sm text-red-600 bg-red-50 rounded-lg p-2">
              <Zap className="w-4 h-4 mr-2" />
              <span className="font-medium">Only {spotsLeft} spots left</span>
              <span className="ml-1">for selected date!</span>
            </div>
          )}
        </div>
      )}

      <div className="mb-6">
        {activity.is_bestseller && (
          <div className="inline-flex items-center bg-gradient-to-r from-orange-500 to-pink-500 text-white text-xs font-semibold px-3 py-1 rounded-full mb-3">
            <Award className="w-3 h-3 mr-1" />
            POPULAR CHOICE
          </div>
        )}
        <div className="text-sm text-gray-500 mb-1">From</div>
        <div className="text-3xl font-bold text-gray-900">
          {formatPrice(activity.price_adult)}
        </div>
        <div className="text-sm text-gray-500">per person</div>
      </div>

      {/* Date Selection */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <Calendar className="w-4 h-4 inline mr-1" />
          Select Date
        </label>
        <input
          type="date"
          value={bookingDate}
          onChange={(e) => setBookingDate(e.target.value)}
          min={minDate}
          className="input-field"
          required
        />
      </div>

      {/* Time Slots */}
      {activity.time_slots && activity.time_slots.length > 0 && (
        <TimeSlotsSelector
          timeSlots={activity.time_slots}
          selectedSlotId={selectedTimeSlotId}
          onSlotSelect={setSelectedTimeSlotId}
        />
      )}

      {/* Pricing Tiers */}
      {activity.pricing_tiers && activity.pricing_tiers.length > 0 && (
        <PricingTiersSelector
          pricingTiers={activity.pricing_tiers}
          selectedTierId={selectedTierId}
          onTierSelect={setSelectedTierId}
        />
      )}

      {/* Add-ons */}
      {activity.add_ons && activity.add_ons.length > 0 && (
        <AddOnsSelector
          addOns={activity.add_ons}
          selectedAddOns={selectedAddOns}
          onAddOnsChange={setSelectedAddOns}
        />
      )}

      {/* Participants */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <Users className="w-4 h-4 inline mr-1" />
          Participants
        </label>

        {/* Adults */}
        <div className="flex items-center justify-between mb-3 p-3 border border-gray-200 rounded-lg">
          <div>
            <div className="font-medium">Adults</div>
            <div className="text-sm text-gray-500">Age 18+</div>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setAdults(Math.max(1, adults - 1))}
              className="w-8 h-8 rounded-full border border-gray-300 hover:border-primary hover:text-primary"
            >
              -
            </button>
            <span className="w-8 text-center font-medium">{adults}</span>
            <button
              onClick={() => setAdults(adults + 1)}
              className="w-8 h-8 rounded-full border border-gray-300 hover:border-primary hover:text-primary"
            >
              +
            </button>
          </div>
        </div>

        {/* Children */}
        {activity.price_child && (
          <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
            <div>
              <div className="font-medium">Children</div>
              <div className="text-sm text-gray-500">Age 0-17</div>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setChildren(Math.max(0, children - 1))}
                className="w-8 h-8 rounded-full border border-gray-300 hover:border-primary hover:text-primary"
              >
                -
              </button>
              <span className="w-8 text-center font-medium">{children}</span>
              <button
                onClick={() => setChildren(children + 1)}
                className="w-8 h-8 rounded-full border border-gray-300 hover:border-primary hover:text-primary"
              >
                +
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Duration & Group Size Info */}
      <div className="mb-6 space-y-2 text-sm text-gray-600">
        {activity.duration_minutes && (
          <div className="flex items-center">
            <Clock className="w-4 h-4 mr-2" />
            Duration: {Math.floor(activity.duration_minutes / 60)}h {activity.duration_minutes % 60}m
          </div>
        )}
        {activity.max_group_size && (
          <div className="flex items-center">
            <Users className="w-4 h-4 mr-2" />
            Max group size: {activity.max_group_size}
          </div>
        )}
      </div>

      {/* Total */}
      <div className="border-t pt-4 mb-4">
        {(() => {
          let basePrice = parseFloat(String(activity.price_adult)) || 0;
          let childPrice = parseFloat(String(activity.price_child || 0)) || 0;

          // Get pricing tier info if selected
          const selectedTier = selectedTierId
            ? activity.pricing_tiers?.find(t => t.id === selectedTierId)
            : null;

          if (selectedTier) {
            basePrice = parseFloat(String(selectedTier.price_adult)) || 0;
            childPrice = parseFloat(String(selectedTier.price_child || 0)) || 0;
          }

          // Get time slot adjustment if selected
          const selectedSlot = selectedTimeSlotId
            ? activity.time_slots?.find(s => s.id === selectedTimeSlotId)
            : null;

          if (selectedSlot?.price_adjustment) {
            const adjustment = parseFloat(String(selectedSlot.price_adjustment)) || 0;
            basePrice += adjustment;
            childPrice += adjustment;
          }

          return (
            <>
              {/* Adults */}
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-600">
                  {adults} adult{adults > 1 ? 's' : ''} × {formatPrice(basePrice)}
                  {selectedTier && <span className="text-xs ml-1">({selectedTier.tier_name})</span>}
                </span>
                <span className="font-medium">
                  {formatPrice(basePrice * adults)}
                </span>
              </div>

              {/* Children */}
              {children > 0 && childPrice > 0 && (
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">
                    {children} child{children > 1 ? 'ren' : ''} × {formatPrice(childPrice)}
                    {selectedTier && <span className="text-xs ml-1">({selectedTier.tier_name})</span>}
                  </span>
                  <span className="font-medium">
                    {formatPrice(childPrice * children)}
                  </span>
                </div>
              )}

              {/* Add-ons */}
              {selectedAddOns.map(selected => {
                const addOn = activity.add_ons?.find(a => a.id === selected.id);
                if (!addOn) return null;
                return (
                  <div key={addOn.id} className="flex justify-between items-center mb-2">
                    <span className="text-gray-600 text-sm">
                      {addOn.name} × {selected.quantity}
                    </span>
                    <span className="font-medium">
                      {formatPrice(addOn.price * selected.quantity)}
                    </span>
                  </div>
                );
              })}
            </>
          );
        })()}

        <div className="flex justify-between items-center text-lg font-bold border-t pt-2 mt-2">
          <span>Total</span>
          <span>{formatPrice(totalPrice)}</span>
        </div>
      </div>

      {/* Book Button */}
      <button
        onClick={handleAddToCart}
        disabled={loading || !bookingDate}
        className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Adding...' : 'Add to Cart'}
      </button>

      {/* Features */}
      <div className="mt-4 space-y-2 text-sm text-gray-600">
        {activity.free_cancellation_hours > 0 && (
          <div className="flex items-center text-success">
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            Free cancellation up to {activity.free_cancellation_hours} hours before
          </div>
        )}
        {activity.instant_confirmation && (
          <div className="flex items-center text-success">
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            Instant confirmation
          </div>
        )}
      </div>
    </div>
  );
}