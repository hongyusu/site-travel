'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

export type Location = 'eu' | 'cn'

export interface LocationOption {
  code: Location
  name: string
  flag: string
  currency: string
}

export const locations: LocationOption[] = [
  { code: 'eu', name: 'Europe', flag: '🇪🇺', currency: 'EUR' },
  { code: 'cn', name: 'China', flag: '🇨🇳', currency: 'CNY' },
]

// Conversion rates (EUR as base currency)
export const CONVERSION_RATES = {
  EUR_TO_CNY: 10,
  CNY_TO_EUR: 0.1,
}

interface LocationContextType {
  location: Location
  setLocation: (location: Location) => void
  getCurrentCurrency: () => string
  convertPrice: (price: number, fromCurrency: string, toCurrency: string) => number
  formatPrice: (price: number, targetLocation?: Location) => string
  locationOptions: LocationOption[]
}

const LocationContext = createContext<LocationContextType | undefined>(undefined)

export function LocationProvider({ children }: { children: ReactNode }) {
  const [location, setLocationState] = useState<Location>('eu') // Default to EU

  // Load location from localStorage on mount
  useEffect(() => {
    const savedLocation = localStorage.getItem('user_location') as Location
    if (savedLocation && ['eu', 'cn'].includes(savedLocation)) {
      setLocationState(savedLocation)
    }
  }, [])

  // Save location to localStorage when it changes
  const setLocation = (newLocation: Location) => {
    setLocationState(newLocation)
    localStorage.setItem('user_location', newLocation)
  }

  // Get current currency based on location
  const getCurrentCurrency = (): string => {
    const currentLocation = locations.find(l => l.code === location)
    return currentLocation?.currency || 'EUR'
  }

  // Convert price between currencies
  const convertPrice = (price: number, fromCurrency: string, toCurrency: string): number => {
    if (fromCurrency === toCurrency) return price
    
    const validPrice = Number(price) || 0
    
    // Convert EUR to CNY
    if (fromCurrency === 'EUR' && toCurrency === 'CNY') {
      return validPrice * CONVERSION_RATES.EUR_TO_CNY
    }
    
    // Convert CNY to EUR
    if (fromCurrency === 'CNY' && toCurrency === 'EUR') {
      return validPrice * CONVERSION_RATES.CNY_TO_EUR
    }
    
    // If conversion not supported, return original price
    return validPrice
  }

  // Format price for display based on location
  const formatPrice = (price: number, targetLocation?: Location): string => {
    const validPrice = Number(price) || 0
    const currentLocation = targetLocation || location
    const targetCurrency = locations.find(l => l.code === currentLocation)?.currency || 'EUR'
    
    // Assume input price is always in EUR (database default)
    // Convert to target currency if needed
    const convertedPrice = convertPrice(validPrice, 'EUR', targetCurrency)
    
    // Format based on currency
    if (targetCurrency === 'CNY') {
      // Chinese Yuan: ¥1000 (symbol before, no decimals for whole numbers)
      return `¥${Math.round(convertedPrice).toLocaleString('zh-CN')}`
    } else {
      // Euro: €100 (existing format)
      return new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
      }).format(convertedPrice)
    }
  }

  const value = {
    location,
    setLocation,
    getCurrentCurrency,
    convertPrice,
    formatPrice,
    locationOptions: locations,
  }

  return (
    <LocationContext.Provider value={value}>
      {children}
    </LocationContext.Provider>
  )
}

export function useLocation() {
  const context = useContext(LocationContext)
  if (context === undefined) {
    throw new Error('useLocation must be used within a LocationProvider')
  }
  return context
}