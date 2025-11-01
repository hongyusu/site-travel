'use client';

import { Clock, CheckCircle, XCircle, Ban, Package } from 'lucide-react';

export type OrderStatus =
  | 'pending'
  | 'pending_vendor_approval'
  | 'confirmed'
  | 'rejected'
  | 'cancelled'
  | 'completed';

interface OrderStatusBadgeProps {
  status: OrderStatus;
  className?: string;
}

export default function OrderStatusBadge({ status, className = '' }: OrderStatusBadgeProps) {
  const getStatusConfig = () => {
    switch (status) {
      case 'pending':
        return {
          label: 'Pending',
          icon: Clock,
          bgColor: 'bg-yellow-100',
          textColor: 'text-yellow-800',
          iconColor: 'text-yellow-600'
        };
      case 'pending_vendor_approval':
        return {
          label: 'Awaiting Approval',
          icon: Clock,
          bgColor: 'bg-blue-100',
          textColor: 'text-blue-800',
          iconColor: 'text-blue-600'
        };
      case 'confirmed':
        return {
          label: 'Confirmed',
          icon: CheckCircle,
          bgColor: 'bg-green-100',
          textColor: 'text-green-800',
          iconColor: 'text-green-600'
        };
      case 'rejected':
        return {
          label: 'Rejected',
          icon: XCircle,
          bgColor: 'bg-red-100',
          textColor: 'text-red-800',
          iconColor: 'text-red-600'
        };
      case 'cancelled':
        return {
          label: 'Cancelled',
          icon: Ban,
          bgColor: 'bg-gray-100',
          textColor: 'text-gray-800',
          iconColor: 'text-gray-600'
        };
      case 'completed':
        return {
          label: 'Completed',
          icon: Package,
          bgColor: 'bg-purple-100',
          textColor: 'text-purple-800',
          iconColor: 'text-purple-600'
        };
      default:
        return {
          label: 'Unknown',
          icon: Clock,
          bgColor: 'bg-gray-100',
          textColor: 'text-gray-800',
          iconColor: 'text-gray-600'
        };
    }
  };

  const config = getStatusConfig();
  const Icon = config.icon;

  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${config.bgColor} ${config.textColor} ${className}`}
    >
      <Icon className={`w-4 h-4 mr-1.5 ${config.iconColor}`} />
      {config.label}
    </span>
  );
}
