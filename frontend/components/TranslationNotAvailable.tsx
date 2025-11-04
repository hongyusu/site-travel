'use client'

import { useLanguage } from '@/contexts/LanguageContext'
import { Globe } from 'lucide-react'

interface TranslationNotAvailableProps {
  fieldName?: string
  className?: string
}

export default function TranslationNotAvailable({
  fieldName = 'content',
  className = ''
}: TranslationNotAvailableProps) {
  const { language, languageOptions, getTranslation } = useLanguage()

  // Only show for non-English languages
  if (language === 'en') return null

  const currentLanguage = languageOptions.find(l => l.code === language)

  return (
    <div className={`bg-amber-50 border border-amber-200 rounded-lg p-4 ${className}`}>
      <div className="flex items-start gap-3">
        <Globe className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
        <div>
          <p className="text-sm text-amber-900 font-medium">
            {fieldName} {getTranslation('message.not_available_in')} {currentLanguage?.name}
          </p>
          <p className="text-xs text-amber-700 mt-1">
            {getTranslation('message.not_translated')}
          </p>
        </div>
      </div>
    </div>
  )
}
