import Link from 'next/link';
import { Users, Globe, Award, Heart } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">About Us</h1>
          <p className="text-xl text-white/90 max-w-3xl">
            Connecting travelers with unforgettable experiences worldwide
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-12">
        {/* Mission Section */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Mission</h2>
          <p className="text-lg text-gray-700 mb-4">
            At MeetYourTravelPartner, we believe that travel is more than just visiting new places—it's about
            creating meaningful connections, discovering authentic experiences, and making memories that last a lifetime.
          </p>
          <p className="text-lg text-gray-700">
            We partner with local experts and activity providers worldwide to bring you the best tours,
            activities, and experiences. Whether you're seeking adventure, culture, relaxation, or something
            completely unique, we're here to help you find your perfect travel partner.
          </p>
        </div>

        {/* Values */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <Users className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">Community</h3>
            <p className="text-gray-600">
              Building connections between travelers and local experts
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6 text-center">
            <Globe className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">Global Reach</h3>
            <p className="text-gray-600">
              150,000+ activities in destinations worldwide
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6 text-center">
            <Award className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">Quality</h3>
            <p className="text-gray-600">
              Verified vendors and authentic experiences only
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6 text-center">
            <Heart className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">Passion</h3>
            <p className="text-gray-600">
              Driven by love for travel and discovery
            </p>
          </div>
        </div>

        {/* Story */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Story</h2>
          <p className="text-lg text-gray-700 mb-4">
            Founded in 2020, MeetYourTravelPartner was born from a simple idea: every traveler deserves
            to connect with authentic local experiences. Our founders, passionate travelers themselves,
            saw the gap between tourists and the incredible people who truly know their destinations.
          </p>
          <p className="text-lg text-gray-700 mb-4">
            Today, we've grown into a global platform connecting millions of travelers with thousands
            of verified vendors across hundreds of destinations. But our mission remains the same—to
            make every journey extraordinary.
          </p>
        </div>

        {/* Stats */}
        <div className="grid md:grid-cols-4 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-4xl font-bold text-primary mb-2">150K+</div>
            <div className="text-gray-600">Activities</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-4xl font-bold text-primary mb-2">500+</div>
            <div className="text-gray-600">Destinations</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-4xl font-bold text-primary mb-2">10M+</div>
            <div className="text-gray-600">Happy Travelers</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-4xl font-bold text-primary mb-2">5K+</div>
            <div className="text-gray-600">Verified Vendors</div>
          </div>
        </div>

        {/* CTA */}
        <div className="bg-primary rounded-lg shadow-lg p-8 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to Start Your Journey?</h2>
          <p className="text-xl mb-6">Explore thousands of amazing experiences waiting for you</p>
          <Link href="/" className="btn-secondary inline-block">
            Explore Activities
          </Link>
        </div>
      </div>
    </div>
  );
}
