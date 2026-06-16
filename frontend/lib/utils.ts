import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPrice(price: number, currency = 'EUR') {
  const validPrice = Number(price) || 0;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(validPrice);
}

export function formatDuration(minutes: number) {
  if (!minutes || minutes < 60) {
    return `${minutes || 0} min`;
  }
  // Multi-day experiences (e.g. 3-day tours): show days rather than "72 hours".
  if (minutes >= 1440) {
    const days = Math.floor(minutes / 1440);
    const leftoverHours = Math.floor((minutes % 1440) / 60);
    const dayLabel = days === 1 ? '1 day' : `${days} days`;
    return leftoverHours > 0 ? `${dayLabel} ${leftoverHours}h` : dayLabel;
  }
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  if (mins === 0) {
    return hours === 1 ? '1 hour' : `${hours} hours`;
  }
  return `${hours}h ${mins}min`;
}

export function formatDate(date: string | Date) {
  return new Intl.DateTimeFormat('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  }).format(new Date(date));
}

export function formatShortDate(date: string | Date) {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
  }).format(new Date(date));
}

export function getImageUrl(url: string | null | undefined): string {
  if (!url) return '/placeholder.jpg';
  // Absolute URLs and same-origin root-relative paths (e.g. self-hosted /media/...) pass through.
  if (url.startsWith('http') || url.startsWith('/')) return url;
  return `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${url}`;
}

export function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

export function getSessionId(): string {
  if (typeof window === 'undefined') return '';

  let sessionId = localStorage.getItem('session_id');
  if (!sessionId) {
    sessionId = generateSessionId();
    localStorage.setItem('session_id', sessionId);
  }
  return sessionId;
}