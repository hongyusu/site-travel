'use client';

import { Check, Clock, X, Calendar } from 'lucide-react';

export type OrderStatus =
  | 'pending'
  | 'pending_vendor_approval'
  | 'confirmed'
  | 'rejected'
  | 'cancelled'
  | 'completed';

interface TimelineStep {
  label: string;
  description?: string;
  timestamp?: string;
  status: 'completed' | 'current' | 'pending' | 'rejected' | 'cancelled';
}

interface OrderTimelineProps {
  bookingStatus: OrderStatus;
  createdAt: string;
  confirmedAt?: string;
  vendorApprovedAt?: string;
  vendorRejectedAt?: string;
  cancelledAt?: string;
  completedAt?: string;
  bookingDate: string;
  rejectionReason?: string;
}

export default function OrderTimeline({
  bookingStatus,
  createdAt,
  confirmedAt,
  vendorApprovedAt,
  vendorRejectedAt,
  cancelledAt,
  completedAt,
  bookingDate,
  rejectionReason
}: OrderTimelineProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getSteps = (): TimelineStep[] => {
    const steps: TimelineStep[] = [];

    // Step 1: Order Placed
    steps.push({
      label: 'Order Placed',
      description: 'Your booking has been created',
      timestamp: createdAt,
      status: 'completed'
    });

    // Handle different status flows
    if (bookingStatus === 'cancelled') {
      steps.push({
        label: 'Order Cancelled',
        description: 'You cancelled this booking',
        timestamp: cancelledAt,
        status: 'cancelled'
      });
      return steps;
    }

    if (bookingStatus === 'rejected') {
      steps.push({
        label: 'Awaiting Vendor Approval',
        description: 'Vendor is reviewing your booking',
        timestamp: createdAt,
        status: 'completed'
      });
      steps.push({
        label: 'Booking Rejected',
        description: rejectionReason || 'Vendor rejected this booking',
        timestamp: vendorRejectedAt,
        status: 'rejected'
      });
      return steps;
    }

    // Step 2: Awaiting Vendor Approval (if not instant confirmation)
    if (bookingStatus === 'pending_vendor_approval') {
      steps.push({
        label: 'Awaiting Vendor Approval',
        description: 'Vendor is reviewing your booking',
        status: 'current'
      });
      steps.push({
        label: 'Booking Confirmed',
        description: 'Vendor will confirm your booking',
        status: 'pending'
      });
    } else if (bookingStatus === 'confirmed' || bookingStatus === 'completed') {
      // If vendor approval happened
      if (vendorApprovedAt) {
        steps.push({
          label: 'Awaiting Vendor Approval',
          description: 'Vendor reviewed your booking',
          timestamp: vendorApprovedAt,
          status: 'completed'
        });
      }

      steps.push({
        label: 'Booking Confirmed',
        description: 'Your booking is confirmed',
        timestamp: confirmedAt,
        status: 'completed'
      });
    }

    // Step 3: Activity Date
    const activityDatePassed = new Date(bookingDate) < new Date();
    if (bookingStatus === 'completed') {
      steps.push({
        label: 'Activity Completed',
        description: 'You enjoyed your activity',
        timestamp: completedAt,
        status: 'completed'
      });
    } else if (bookingStatus === 'confirmed') {
      steps.push({
        label: 'Activity Date',
        description: `Scheduled for ${formatDate(bookingDate)}`,
        timestamp: bookingDate,
        status: activityDatePassed ? 'completed' : 'pending'
      });
    }

    return steps;
  };

  const steps = getSteps();

  const getStepIcon = (status: TimelineStep['status']) => {
    switch (status) {
      case 'completed':
        return <Check className="w-5 h-5 text-white" />;
      case 'current':
        return <Clock className="w-5 h-5 text-white" />;
      case 'rejected':
      case 'cancelled':
        return <X className="w-5 h-5 text-white" />;
      case 'pending':
        return <div className="w-2 h-2 bg-gray-400 rounded-full" />;
    }
  };

  const getStepColor = (status: TimelineStep['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500';
      case 'current':
        return 'bg-blue-500';
      case 'rejected':
      case 'cancelled':
        return 'bg-red-500';
      case 'pending':
        return 'bg-gray-300';
    }
  };

  const getStepTextColor = (status: TimelineStep['status']) => {
    switch (status) {
      case 'completed':
        return 'text-gray-900';
      case 'current':
        return 'text-blue-600 font-semibold';
      case 'rejected':
      case 'cancelled':
        return 'text-red-600 font-semibold';
      case 'pending':
        return 'text-gray-500';
    }
  };

  return (
    <div className="space-y-6">
      {steps.map((step, index) => (
        <div key={index} className="relative flex items-start">
          {/* Vertical Line */}
          {index < steps.length - 1 && (
            <div
              className={`absolute left-5 top-11 w-0.5 h-14 ${
                step.status === 'completed' ? 'bg-green-500' : 'bg-gray-200'
              }`}
            />
          )}

          {/* Icon Circle */}
          <div
            className={`relative z-10 flex items-center justify-center w-10 h-10 rounded-full ${getStepColor(
              step.status
            )}`}
          >
            {getStepIcon(step.status)}
          </div>

          {/* Content */}
          <div className="ml-4 flex-1">
            <div className={`text-base font-medium ${getStepTextColor(step.status)}`}>
              {step.label}
            </div>
            {step.description && (
              <div className="text-sm text-gray-600 mt-1">{step.description}</div>
            )}
            {step.timestamp && (
              <div className="flex items-center text-xs text-gray-500 mt-1">
                <Calendar className="w-3 h-3 mr-1" />
                {formatDate(step.timestamp)}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
