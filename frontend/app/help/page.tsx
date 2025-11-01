import Link from 'next/link';
import { Search, HelpCircle, Mail, MessageCircle, Book, CreditCard, MapPin, Users } from 'lucide-react';

export default function HelpPage() {
  const categories = [
    {
      icon: Book,
      title: 'Booking & Reservations',
      description: 'How to book, modify, or cancel your activities',
      articles: 12,
    },
    {
      icon: CreditCard,
      title: 'Payments & Refunds',
      description: 'Payment methods, pricing, and refund policies',
      articles: 8,
    },
    {
      icon: MapPin,
      title: 'At Your Destination',
      description: 'Meeting points, what to bring, and local tips',
      articles: 15,
    },
    {
      icon: Users,
      title: 'Account & Profile',
      description: 'Managing your account and preferences',
      articles: 6,
    },
  ];

  const popularQuestions = [
    'How do I change or cancel my booking?',
    'What is the cancellation policy?',
    'How do I receive my tickets?',
    'Can I book for a group?',
    'What payment methods are accepted?',
    'How do I contact my activity provider?',
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Help Center</h1>
          <p className="text-xl text-white/90 mb-8 max-w-3xl">
            Find answers to your questions and get the help you need
          </p>

          {/* Search */}
          <div className="max-w-2xl">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search for help..."
                className="w-full pl-12 pr-4 py-4 rounded-lg text-gray-900 text-lg"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12">
        {/* Categories */}
        <div className="mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Browse by Category</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {categories.map((category, index) => {
              const Icon = category.icon;
              return (
                <Link
                  key={index}
                  href="#"
                  className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
                >
                  <Icon className="w-10 h-10 text-primary mb-3" />
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{category.title}</h3>
                  <p className="text-gray-600 text-sm mb-3">{category.description}</p>
                  <span className="text-primary text-sm font-medium">
                    {category.articles} articles
                  </span>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Popular Questions */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Popular Questions</h2>
          <div className="space-y-4">
            {popularQuestions.map((question, index) => (
              <Link
                key={index}
                href="#"
                className="flex items-center justify-between p-4 rounded-lg hover:bg-gray-50 transition-colors group"
              >
                <div className="flex items-center">
                  <HelpCircle className="w-5 h-5 text-primary mr-3" />
                  <span className="text-gray-900 font-medium">{question}</span>
                </div>
                <span className="text-gray-400 group-hover:text-primary transition-colors">→</span>
              </Link>
            ))}
          </div>
        </div>

        {/* Contact Options */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <Mail className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">Email Support</h3>
            <p className="text-gray-600 mb-4">
              Get help via email within 24 hours
            </p>
            <a href="mailto:support@meetyourtravelpartner.com" className="text-primary hover:text-primary-600 font-medium">
              Send Email
            </a>
          </div>

          <div className="bg-white rounded-lg shadow p-6 text-center">
            <MessageCircle className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">Live Chat</h3>
            <p className="text-gray-600 mb-4">
              Chat with our team in real-time
            </p>
            <button className="text-primary hover:text-primary-600 font-medium">
              Start Chat
            </button>
          </div>

          <div className="bg-white rounded-lg shadow p-6 text-center">
            <HelpCircle className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">FAQ</h3>
            <p className="text-gray-600 mb-4">
              Browse frequently asked questions
            </p>
            <Link href="#" className="text-primary hover:text-primary-600 font-medium">
              View FAQ
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
