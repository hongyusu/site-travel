'use client';

import { X, Calendar, Clock, Users, DollarSign, MapPin, Phone, Mail } from 'lucide-react';

interface Booking {
  id: number;
  booking_ref: string;
  activity: {
    id?: number;
    title: string;
    slug?: string;
  };
  customer_name: string;
  customer_email: string;
  customer_phone: string | null;
  booking_date: string;
  booking_time: string | null;
  adults: number;
  children: number;
  total_price: string;
  currency: string;
  status: string;
  special_requirements?: string | null;
  created_at: string;
  confirmed_at?: string | null;
  pricing_tier?: string | null;
  time_slot?: string | null;
  add_ons?: Array<{ name: string; quantity: number; price: number }>;
}

interface BookingDetailsModalProps {
  booking: Booking;
  onClose: () => void;
}

export default function BookingDetailsModal({ booking, onClose }: BookingDetailsModalProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed':
        return 'bg-green-100 text-green-800';
      case 'pending':
      case 'pending_vendor_approval':
        return 'bg-yellow-100 text-yellow-800';
      case 'completed':
        return 'bg-blue-100 text-blue-800';
      case 'cancelled':
      case 'rejected':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatDateTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Booking Details</h2>
            <p className="text-sm text-gray-500 mt-1">Ref: {booking.booking_ref}</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Status */}
          <div>
            <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(booking.status)}`}>
              {booking.status.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
            </span>
          </div>

          {/* Activity Info */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="font-semibold text-gray-900 mb-2">Activity</h3>
            <p className="text-gray-700">{booking.activity.title}</p>
          </div>

          {/* Booking Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <Calendar className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <div className="text-sm text-gray-500">Date</div>
                  <div className="font-medium text-gray-900">{formatDate(booking.booking_date)}</div>
                </div>
              </div>

              {booking.booking_time && (
                <div className="flex items-start gap-3">
                  <Clock className="w-5 h-5 text-gray-400 mt-0.5" />
                  <div>
                    <div className="text-sm text-gray-500">Time</div>
                    <div className="font-medium text-gray-900">{booking.booking_time}</div>
                  </div>
                </div>
              )}

              <div className="flex items-start gap-3">
                <Users className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <div className="text-sm text-gray-500">Participants</div>
                  <div className="font-medium text-gray-900">
                    {booking.adults} adult{booking.adults > 1 ? 's' : ''}
                    {booking.children > 0 && `, ${booking.children} child${booking.children > 1 ? 'ren' : ''}`}
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <DollarSign className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <div className="text-sm text-gray-500">Total Price</div>
                  <div className="font-medium text-gray-900">
                    {booking.currency} {Number(booking.total_price).toFixed(2)}
                  </div>
                </div>
              </div>
            </div>

            {/* Customer Info */}
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-900 mb-2">Customer Information</h3>

              <div className="flex items-start gap-3">
                <Users className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <div className="text-sm text-gray-500">Name</div>
                  <div className="font-medium text-gray-900">{booking.customer_name}</div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Mail className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <div className="text-sm text-gray-500">Email</div>
                  <div className="font-medium text-gray-900">{booking.customer_email}</div>
                </div>
              </div>

              {booking.customer_phone && (
                <div className="flex items-start gap-3">
                  <Phone className="w-5 h-5 text-gray-400 mt-0.5" />
                  <div>
                    <div className="text-sm text-gray-500">Phone</div>
                    <div className="font-medium text-gray-900">{booking.customer_phone}</div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Enhanced Booking Details */}
          {(booking.pricing_tier || booking.time_slot || (booking.add_ons && booking.add_ons.length > 0)) && (
            <div className="bg-blue-50 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-3">Booking Options</h3>
              <div className="space-y-2 text-sm">
                {booking.pricing_tier && (
                  <div><span className="text-gray-600">Pricing Tier:</span> <span className="font-medium">{booking.pricing_tier}</span></div>
                )}
                {booking.time_slot && (
                  <div><span className="text-gray-600">Time Slot:</span> <span className="font-medium">{booking.time_slot}</span></div>
                )}
                {booking.add_ons && booking.add_ons.length > 0 && (
                  <div>
                    <div className="text-gray-600 mb-1">Add-ons:</div>
                    <ul className="list-disc list-inside space-y-1">
                      {booking.add_ons.map((addon, idx) => (
                        <li key={idx} className="font-medium">
                          {addon.name} × {addon.quantity} ({booking.currency} {addon.price.toFixed(2)} each)
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Special Requirements */}
          {booking.special_requirements && (
            <div className="bg-yellow-50 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">Special Requirements</h3>
              <p className="text-gray-700 text-sm">{booking.special_requirements}</p>
            </div>
          )}

          {/* Timeline */}
          <div className="border-t pt-4">
            <h3 className="font-semibold text-gray-900 mb-3">Booking Timeline</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Created</span>
                <span className="font-medium">{formatDateTime(booking.created_at)}</span>
              </div>
              {booking.confirmed_at && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Confirmed</span>
                  <span className="font-medium">{formatDateTime(booking.confirmed_at)}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t px-6 py-4 bg-gray-50">
          <button
            onClick={onClose}
            className="w-full btn-secondary"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
