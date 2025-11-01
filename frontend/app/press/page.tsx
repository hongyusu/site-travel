import Link from 'next/link';
import { Download, Mail, FileText } from 'lucide-react';

export default function PressPage() {
  const pressReleases = [
    {
      date: 'January 15, 2024',
      title: 'MeetYourTravelPartner Reaches 10 Million Happy Travelers',
      excerpt: 'Platform celebrates major milestone as global travel continues strong recovery...',
    },
    {
      date: 'December 1, 2023',
      title: 'New Partnerships Expand Activity Offerings in Asia-Pacific',
      excerpt: 'Strategic partnerships with local vendors bring 5,000 new experiences to the platform...',
    },
    {
      date: 'October 20, 2023',
      title: 'MeetYourTravelPartner Launches Enhanced Vendor Dashboard',
      excerpt: 'New features empower activity providers with better insights and booking management...',
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Press & Media</h1>
          <p className="text-xl text-white/90 max-w-3xl">
            Latest news, press releases, and media resources
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12">
        {/* Contact */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Media Contact</h2>

          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Press Inquiries</h3>
              <div className="space-y-3 text-gray-700">
                <p className="flex items-center">
                  <Mail className="w-5 h-5 text-primary mr-2" />
                  <a href="mailto:press@meetyourtravelpartner.com" className="text-primary hover:underline">
                    press@meetyourtravelpartner.com
                  </a>
                </p>
                <p className="text-gray-600">
                  For media inquiries, interview requests, and press kit access
                </p>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Media Kit</h3>
              <p className="text-gray-600 mb-4">
                Download our complete media kit including logos, brand guidelines, and high-resolution images
              </p>
              <button className="btn-primary flex items-center">
                <Download className="w-4 h-4 mr-2" />
                Download Media Kit
              </button>
            </div>
          </div>
        </div>

        {/* Press Releases */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Recent Press Releases</h2>

          <div className="space-y-6">
            {pressReleases.map((release, index) => (
              <div
                key={index}
                className="border-b border-gray-200 last:border-0 pb-6 last:pb-0"
              >
                <div className="text-sm text-gray-500 mb-2">{release.date}</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{release.title}</h3>
                <p className="text-gray-700 mb-3">{release.excerpt}</p>
                <button className="text-primary hover:text-primary-600 font-medium flex items-center">
                  <FileText className="w-4 h-4 mr-1" />
                  Read Full Release
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Fast Facts */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Fast Facts</h2>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <ul className="space-y-3 text-gray-700">
                <li><span className="font-semibold">Founded:</span> 2020</li>
                <li><span className="font-semibold">Headquarters:</span> San Francisco, CA</li>
                <li><span className="font-semibold">Activities:</span> 150,000+</li>
                <li><span className="font-semibold">Destinations:</span> 500+</li>
              </ul>
            </div>
            <div>
              <ul className="space-y-3 text-gray-700">
                <li><span className="font-semibold">Travelers Served:</span> 10+ million</li>
                <li><span className="font-semibold">Verified Vendors:</span> 5,000+</li>
                <li><span className="font-semibold">Countries:</span> 100+</li>
                <li><span className="font-semibold">Languages:</span> 15</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Media Coverage */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">In the News</h2>
          <p className="text-gray-600 mb-6">
            MeetYourTravelPartner has been featured in leading travel and technology publications worldwide
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 items-center opacity-60">
            <div className="text-center text-2xl font-bold text-gray-400">TechCrunch</div>
            <div className="text-center text-2xl font-bold text-gray-400">Forbes Travel</div>
            <div className="text-center text-2xl font-bold text-gray-400">Travel + Leisure</div>
            <div className="text-center text-2xl font-bold text-gray-400">Wired</div>
          </div>
        </div>

        {/* CTA */}
        <div className="bg-primary rounded-lg shadow-lg p-8 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">Want to Feature Our Story?</h2>
          <p className="text-xl mb-6">
            Get in touch with our press team for interviews, quotes, and exclusive content
          </p>
          <a href="mailto:press@meetyourtravelpartner.com" className="btn-secondary inline-block">
            Contact Press Team
          </a>
        </div>
      </div>
    </div>
  );
}
