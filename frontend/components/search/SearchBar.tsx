'use client';

import { useState } from 'react';
import { Search, Calendar, MapPin } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface SearchBarProps {
  placeholder?: string;
  className?: string;
  showDatePicker?: boolean;
  autoFocus?: boolean;
}

export default function SearchBar({
  placeholder = "Search for activities, tours, or destinations...",
  className = "",
  showDatePicker = false,
  autoFocus = false
}: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [selectedDate, setSelectedDate] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() || selectedDate) {
      const params = new URLSearchParams();
      if (query.trim()) {
        params.append('q', query);
      }
      if (selectedDate) {
        params.append('date', selectedDate);
      }
      router.push(`/search?${params.toString()}`);
    }
  };

  return (
    <form onSubmit={handleSearch} className={`search-bar ${className}`}>
      <div className="bg-white rounded-full shadow-lg flex items-center p-2">
        <div className="flex-1 flex items-center">
          <MapPin className="w-5 h-5 text-gray-400 ml-4 mr-2" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={placeholder}
            autoFocus={autoFocus}
            className="flex-1 py-3 px-2 outline-none text-gray-700"
          />
        </div>

        {showDatePicker && (
          <div className="border-l border-gray-200 pl-4 pr-2">
            <div className="flex items-center">
              <Calendar className="w-5 h-5 text-gray-400 mr-2" />
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="outline-none text-gray-700"
                min={new Date().toISOString().split('T')[0]}
              />
            </div>
          </div>
        )}

        <button
          type="submit"
          className="bg-primary hover:bg-primary-600 text-white rounded-full p-3 ml-2 transition-colors"
        >
          <Search className="w-6 h-6" />
        </button>
      </div>
    </form>
  );
}