'use client'

import { useState, useRef, useEffect } from 'react'
import { useLanguage } from '@/contexts/LanguageContext'
import { ChevronDown } from 'lucide-react'

export default function LanguageSelector() {
  const { language, setLanguage, languageOptions } = useLanguage()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Get current language details
  const currentLanguage = languageOptions.find(l => l.code === language)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleLanguageChange = (code: string) => {
    setLanguage(code as any)
    setIsOpen(false)
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 rounded-lg hover:bg-gray-100 transition-colors"
        aria-label="Select language"
      >
        <span className="text-lg">{currentLanguage?.flag}</span>
        <span className="hidden sm:inline">{currentLanguage?.name}</span>
        <ChevronDown
          className={`h-4 w-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
        />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 z-50">
          <div className="py-1">
            {languageOptions.map((option) => (
              <button
                key={option.code}
                onClick={() => handleLanguageChange(option.code)}
                className={`flex items-center gap-3 w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors ${
                  option.code === language ? 'bg-gray-50 font-medium' : ''
                }`}
              >
                <span className="text-lg">{option.flag}</span>
                <span>{option.name}</span>
                {option.code === language && (
                  <span className="ml-auto text-orange-600">✓</span>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}