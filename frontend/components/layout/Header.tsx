'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { ShoppingCart, User, Menu, X, Search } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import LanguageSelector from '@/components/LanguageSelector';
import { useLanguage } from '@/contexts/LanguageContext';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [cartCount, setCartCount] = useState(0);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState<string | null>(null);
  const router = useRouter();
  const { getTranslation } = useLanguage();

  useEffect(() => {
    // Check if user is logged in
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      setIsLoggedIn(!!token);

      if (token) {
        try {
          const response = await apiClient.auth.getProfile();
          setUserRole(response.data.role);
        } catch (error) {
          console.error('Error fetching user role:', error);
          // If token is invalid, clear it
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          setIsLoggedIn(false);
          setUserRole(null);
        }
      } else {
        setUserRole(null);
      }
    };

    checkAuth();
    fetchCartCount();

    // Listen for storage changes (e.g., login/logout in another tab)
    window.addEventListener('storage', checkAuth);

    // Also check on focus (when user comes back to the tab)
    window.addEventListener('focus', checkAuth);

    return () => {
      window.removeEventListener('storage', checkAuth);
      window.removeEventListener('focus', checkAuth);
    };
  }, []);

  const fetchCartCount = async () => {
    try {
      const response = await apiClient.cart.getTotal();
      setCartCount(response.data.item_count || 0);
    } catch (error) {
      console.error('Error fetching cart count:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsLoggedIn(false);
    router.push('/');
  };

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center">
            <span className="text-2xl font-bold text-primary">FindTravelMate</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link href="/search" className="text-gray-700 hover:text-primary transition-colors">
              {getTranslation('nav.activities')}
            </Link>
            <Link href="/destinations" className="text-gray-700 hover:text-primary transition-colors">
              {getTranslation('nav.destinations')}
            </Link>
          </nav>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center space-x-4">
            <LanguageSelector />
            <Link href="/cart" className="relative p-2">
              <ShoppingCart className="w-6 h-6 text-gray-700" />
              {cartCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-primary text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {cartCount}
                </span>
              )}
            </Link>

            {isLoggedIn ? (
              <div className="relative group">
                <button className="flex items-center space-x-2 p-2">
                  <User className="w-6 h-6 text-gray-700" />
                </button>
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                  {userRole === 'admin' && (
                    <>
                      <Link href="/admin/dashboard" className="block px-4 py-2 text-sm text-purple-600 font-semibold hover:bg-gray-100">
                        Admin Dashboard
                      </Link>
                      <hr className="my-1" />
                    </>
                  )}
                  {userRole === 'vendor' && (
                    <>
                      <Link href="/vendor/dashboard" className="block px-4 py-2 text-sm text-primary font-semibold hover:bg-gray-100">
                        Vendor Dashboard
                      </Link>
                      <hr className="my-1" />
                    </>
                  )}
                  <Link href="/my-account" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    {getTranslation('nav.profile')}
                  </Link>
                  <Link href="/bookings" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    {getTranslation('nav.bookings')}
                  </Link>
                  <Link href="/wishlist" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    {getTranslation('nav.wishlist')}
                  </Link>
                  <hr className="my-1" />
                  <button
                    onClick={handleLogout}
                    className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    {getTranslation('nav.logout')}
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link href="/login" className="text-gray-700 hover:text-primary transition-colors px-3 py-2">
                  {getTranslation('nav.signin')}
                </Link>
                <Link href="/register" className="btn-primary py-2 px-4 text-sm">
                  {getTranslation('nav.signup')}
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t">
            <nav className="flex flex-col space-y-4">
              <Link href="/search" className="text-gray-700 hover:text-primary transition-colors">
                {getTranslation('nav.activities')}
              </Link>
              <Link href="/destinations" className="text-gray-700 hover:text-primary transition-colors">
                {getTranslation('nav.destinations')}
              </Link>
              <Link href="/cart" className="text-gray-700 hover:text-primary transition-colors">
                {getTranslation('nav.cart')} ({cartCount})
              </Link>
              {isLoggedIn ? (
                <>
                  {userRole === 'admin' && (
                    <Link href="/admin/dashboard" className="text-purple-600 font-semibold hover:text-purple-700 transition-colors">
                      Admin Dashboard
                    </Link>
                  )}
                  {userRole === 'vendor' && (
                    <Link href="/vendor/dashboard" className="text-primary font-semibold hover:text-primary-600 transition-colors">
                      Vendor Dashboard
                    </Link>
                  )}
                  <Link href="/my-account" className="text-gray-700 hover:text-primary transition-colors">
                    {getTranslation('nav.profile')}
                  </Link>
                  <Link href="/bookings" className="text-gray-700 hover:text-primary transition-colors">
                    {getTranslation('nav.bookings')}
                  </Link>
                  <Link href="/wishlist" className="text-gray-700 hover:text-primary transition-colors">
                    {getTranslation('nav.wishlist')}
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="text-left text-gray-700 hover:text-primary transition-colors"
                  >
                    {getTranslation('nav.logout')}
                  </button>
                </>
              ) : (
                <>
                  <Link href="/login" className="text-gray-700 hover:text-primary transition-colors">
                    {getTranslation('nav.signin')}
                  </Link>
                  <Link href="/register" className="text-primary font-medium">
                    {getTranslation('nav.signup')}
                  </Link>
                </>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}