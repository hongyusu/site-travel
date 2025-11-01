import Link from 'next/link';
import { DollarSign, TrendingUp, Users, CheckCircle } from 'lucide-react';

export default function AffiliatePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Affiliate Program</h1>
          <p className="text-xl text-white/90 max-w-3xl">
            Earn commission by promoting the world's best travel experiences
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12">
        {/* Benefits */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <DollarSign className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">Competitive Commission</h3>
            <p className="text-gray-600">
              Earn up to 8% commission on every booking
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6 text-center">
            <TrendingUp className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">Growing Inventory</h3>
            <p className="text-gray-600">
              150,000+ activities across 500+ destinations
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6 text-center">
            <Users className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">Dedicated Support</h3>
            <p className="text-gray-600">
              Expert affiliate team to help you succeed
            </p>
          </div>
        </div>

        {/* How It Works */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">How It Works</h2>

          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="font-bold text-gray-900 mb-2">Sign Up</h3>
              <p className="text-gray-600 text-sm">
                Join our affiliate program for free
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="font-bold text-gray-900 mb-2">Get Your Links</h3>
              <p className="text-gray-600 text-sm">
                Access unique tracking links and creatives
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="font-bold text-gray-900 mb-2">Promote</h3>
              <p className="text-gray-600 text-sm">
                Share links on your website or social media
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                4
              </div>
              <h3 className="font-bold text-gray-900 mb-2">Earn Commission</h3>
              <p className="text-gray-600 text-sm">
                Get paid for every booking you generate
              </p>
            </div>
          </div>
        </div>

        {/* Commission Structure */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Commission Structure</h2>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-bold text-gray-900">Monthly Sales</th>
                  <th className="px-6 py-3 text-left text-sm font-bold text-gray-900">Commission Rate</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr>
                  <td className="px-6 py-4 text-gray-700">$0 - $5,000</td>
                  <td className="px-6 py-4 font-semibold text-primary">5%</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 text-gray-700">$5,001 - $10,000</td>
                  <td className="px-6 py-4 font-semibold text-primary">6%</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 text-gray-700">$10,001 - $20,000</td>
                  <td className="px-6 py-4 font-semibold text-primary">7%</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 text-gray-700">$20,001+</td>
                  <td className="px-6 py-4 font-semibold text-primary">8%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Features */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">What You Get</h2>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-bold text-gray-900 mb-1">Real-time Reporting</h3>
                <p className="text-gray-600">Track clicks, conversions, and earnings in real-time</p>
              </div>
            </div>

            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-bold text-gray-900 mb-1">Marketing Materials</h3>
                <p className="text-gray-600">Access banners, logos, and promotional content</p>
              </div>
            </div>

            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-bold text-gray-900 mb-1">90-Day Cookie Window</h3>
                <p className="text-gray-600">Earn commission on bookings made within 90 days</p>
              </div>
            </div>

            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-bold text-gray-900 mb-1">Monthly Payments</h3>
                <p className="text-gray-600">Receive payments via PayPal or bank transfer</p>
              </div>
            </div>

            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-bold text-gray-900 mb-1">Deep Linking</h3>
                <p className="text-gray-600">Link to any page or activity on our platform</p>
              </div>
            </div>

            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-bold text-gray-900 mb-1">Dedicated Manager</h3>
                <p className="text-gray-600">Personal support from our affiliate team</p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="bg-primary rounded-lg shadow-lg p-8 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to Start Earning?</h2>
          <p className="text-xl mb-6">
            Join thousands of affiliates earning commissions with us
          </p>
          <a href="mailto:affiliates@meetyourtravelpartner.com" className="btn-secondary inline-block">
            Apply Now
          </a>
        </div>
      </div>
    </div>
  );
}
