'use client';

import { useState } from 'react';
import { ChevronLeft, ChevronRight, Calendar as CalendarIcon } from 'lucide-react';
import {
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
  addDays,
  addMonths,
  subMonths,
  format,
  isSameMonth,
  isSameDay,
  parseISO,
  isToday
} from 'date-fns';

interface Booking {
  id: number;
  booking_ref: string;
  activity: {
    title: string;
  };
  customer_name: string;
  booking_date: string;
  booking_time: string | null;
  adults: number;
  children: number;
  total_price: string;
  status: string;
}

interface BookingCalendarProps {
  bookings: Booking[];
  onBookingClick: (booking: Booking) => void;
}

export default function BookingCalendar({ bookings, onBookingClick }: BookingCalendarProps) {
  const [currentMonth, setCurrentMonth] = useState(new Date());

  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(monthStart);
  const calendarStart = startOfWeek(monthStart);
  const calendarEnd = endOfWeek(monthEnd);

  const getBookingsForDate = (date: Date) => {
    return bookings.filter(booking => {
      const bookingDate = parseISO(booking.booking_date);
      return isSameDay(bookingDate, date);
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'pending':
      case 'pending_vendor_approval':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'completed':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'cancelled':
      case 'rejected':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const renderHeader = () => {
    return (
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">
          {format(currentMonth, 'MMMM yyyy')}
        </h2>
        <div className="flex gap-2">
          <button
            onClick={() => setCurrentMonth(subMonths(currentMonth, 1))}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button
            onClick={() => setCurrentMonth(new Date())}
            className="px-4 py-2 hover:bg-gray-100 rounded-lg transition-colors text-sm font-medium"
          >
            Today
          </button>
          <button
            onClick={() => setCurrentMonth(addMonths(currentMonth, 1))}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    );
  };

  const renderDaysOfWeek = () => {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    return (
      <div className="grid grid-cols-7 gap-2 mb-2">
        {days.map(day => (
          <div key={day} className="text-center text-sm font-semibold text-gray-600 py-2">
            {day}
          </div>
        ))}
      </div>
    );
  };

  const renderCells = () => {
    const rows = [];
    let days = [];
    let day = calendarStart;

    while (day <= calendarEnd) {
      for (let i = 0; i < 7; i++) {
        const currentDay = day;
        const dayBookings = getBookingsForDate(currentDay);
        const isCurrentMonth = isSameMonth(currentDay, monthStart);
        const isTodayDate = isToday(currentDay);

        days.push(
          <div
            key={currentDay.toString()}
            className={`min-h-[120px] border rounded-lg p-2 ${
              isCurrentMonth ? 'bg-white' : 'bg-gray-50'
            } ${isTodayDate ? 'ring-2 ring-primary' : ''}`}
          >
            <div className={`text-sm font-medium mb-1 ${
              isCurrentMonth ? 'text-gray-900' : 'text-gray-400'
            } ${isTodayDate ? 'text-primary font-bold' : ''}`}>
              {format(currentDay, 'd')}
            </div>
            <div className="space-y-1">
              {dayBookings.slice(0, 3).map(booking => (
                <button
                  key={booking.id}
                  onClick={() => onBookingClick(booking)}
                  className={`w-full text-left text-xs px-2 py-1 rounded border ${getStatusColor(booking.status)} hover:opacity-80 transition-opacity`}
                  title={`${booking.activity.title} - ${booking.customer_name}`}
                >
                  <div className="truncate font-medium">
                    {booking.booking_time || 'All day'}
                  </div>
                  <div className="truncate text-[10px]">
                    {booking.activity.title}
                  </div>
                </button>
              ))}
              {dayBookings.length > 3 && (
                <div className="text-xs text-gray-500 px-2">
                  +{dayBookings.length - 3} more
                </div>
              )}
            </div>
          </div>
        );
        day = addDays(day, 1);
      }
      rows.push(
        <div key={day.toString()} className="grid grid-cols-7 gap-2">
          {days}
        </div>
      );
      days = [];
    }
    return <div className="space-y-2">{rows}</div>;
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      {renderHeader()}
      {renderDaysOfWeek()}
      {renderCells()}

      {/* Legend */}
      <div className="mt-6 pt-6 border-t">
        <div className="flex flex-wrap gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-yellow-100 border border-yellow-300" />
            <span>Pending</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-green-100 border border-green-300" />
            <span>Confirmed</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-blue-100 border border-blue-300" />
            <span>Completed</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-red-100 border border-red-300" />
            <span>Cancelled/Rejected</span>
          </div>
        </div>
      </div>
    </div>
  );
}
