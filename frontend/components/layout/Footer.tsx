'use client';

import Link from 'next/link';
import { Facebook, Twitter, Instagram, Youtube } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

export default function Footer() {
  const { getTranslation } = useLanguage();
  return (
    <footer className="bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company */}
          <div>
            <h3 className="text-lg font-semibold mb-4">{getTranslation('footer.company')}</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/about" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.about_us')}
                </Link>
              </li>
              <li>
                <Link href="/careers" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.careers')}
                </Link>
              </li>
              <li>
                <Link href="/press" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.press')}
                </Link>
              </li>
              <li>
                <Link href="/blog" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.blog')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-lg font-semibold mb-4">{getTranslation('footer.support')}</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/help" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.help_center')}
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.contact_us')}
                </Link>
              </li>
              <li>
                <Link href="/cancellation" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.cancellation_policy')}
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.privacy_policy')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Partner */}
          <div>
            <h3 className="text-lg font-semibold mb-4">{getTranslation('footer.vendors')}</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/vendor/register" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.list_experience')}
                </Link>
              </li>
              <li>
                <Link href="/vendor/login" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.vendor_login')}
                </Link>
              </li>
              <li>
                <Link href="/vendor/dashboard" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.vendor_dashboard')}
                </Link>
              </li>
              <li>
                <Link href="/affiliate" className="text-gray-400 hover:text-white transition-colors">
                  {getTranslation('page.affiliate_program')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Connect */}
          <div>
            <h3 className="text-lg font-semibold mb-4">{getTranslation('footer.connect')}</h3>
            <div className="flex space-x-4 mb-6">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <Facebook className="w-6 h-6" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <Twitter className="w-6 h-6" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <Instagram className="w-6 h-6" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <Youtube className="w-6 h-6" />
              </a>
            </div>
            <div>
              <h4 className="text-sm font-semibold mb-2">{getTranslation('footer.newsletter')}</h4>
              <p className="text-gray-400 text-sm mb-3">
                {getTranslation('footer.newsletter_desc')}
              </p>
              <form className="flex">
                <input
                  type="email"
                  placeholder={getTranslation('footer.your_email')}
                  className="bg-gray-800 text-white px-4 py-2 rounded-l flex-1 outline-none focus:ring-2 focus:ring-primary"
                />
                <button type="submit" className="bg-primary hover:bg-primary-600 px-4 py-2 rounded-r transition-colors">
                  {getTranslation('footer.subscribe')}
                </button>
              </form>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              {getTranslation('footer.copyright')}
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <Link href="/terms" className="text-gray-400 hover:text-white text-sm transition-colors">
                {getTranslation('page.terms')}
              </Link>
              <Link href="/privacy" className="text-gray-400 hover:text-white text-sm transition-colors">
                {getTranslation('page.privacy_policy')}
              </Link>
              <Link href="/cookies" className="text-gray-400 hover:text-white text-sm transition-colors">
                {getTranslation('page.cookies')}
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}