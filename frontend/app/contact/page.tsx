'use client';

import { useState } from 'react';
import { Mail, MapPin, Phone, Clock } from 'lucide-react';
import { toast } from 'react-hot-toast';

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Simulate form submission
    setTimeout(() => {
      toast.success('Message sent! We\'ll get back to you soon.');
      setFormData({ name: '', email: '', subject: '', message: '' });
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Contact Us</h1>
          <p className="text-xl text-white/90 max-w-3xl">
            We're here to help. Get in touch with our team
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Contact Form */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Send us a Message</h2>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                    Your Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                    className="input-field"
                    placeholder="John Doe"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                    className="input-field"
                    placeholder="john@example.com"
                  />
                </div>

                <div>
                  <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-2">
                    Subject
                  </label>
                  <input
                    type="text"
                    id="subject"
                    value={formData.subject}
                    onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                    required
                    className="input-field"
                    placeholder="How can we help?"
                  />
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                    Message
                  </label>
                  <textarea
                    id="message"
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                    required
                    rows={6}
                    className="input-field resize-none"
                    placeholder="Tell us more about your inquiry..."
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full btn-primary disabled:opacity-50"
                >
                  {loading ? 'Sending...' : 'Send Message'}
                </button>
              </form>
            </div>
          </div>

          {/* Contact Info */}
          <div className="space-y-6">
            {/* Email */}
            <div className="bg-white rounded-lg shadow p-6">
              <Mail className="w-10 h-10 text-primary mb-3" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">Email</h3>
              <p className="text-gray-600 mb-2">General Inquiries:</p>
              <a href="mailto:support@findtravelmate.com" className="text-primary hover:underline">
                support@findtravelmate.com
              </a>
              <p className="text-gray-600 mt-3 mb-2">Vendor Support:</p>
              <a href="mailto:vendors@findtravelmate.com" className="text-primary hover:underline">
                vendors@findtravelmate.com
              </a>
            </div>

            {/* Phone */}
            <div className="bg-white rounded-lg shadow p-6">
              <Phone className="w-10 h-10 text-primary mb-3" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">Phone</h3>
              <p className="text-gray-700 mb-2">US: +1 (555) 123-4567</p>
              <p className="text-gray-700 mb-2">UK: +44 20 1234 5678</p>
              <p className="text-gray-700">International: +1 (555) 987-6543</p>
            </div>

            {/* Office */}
            <div className="bg-white rounded-lg shadow p-6">
              <MapPin className="w-10 h-10 text-primary mb-3" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">Office</h3>
              <p className="text-gray-700">
                123 Market Street<br />
                San Francisco, CA 94103<br />
                United States
              </p>
            </div>

            {/* Hours */}
            <div className="bg-white rounded-lg shadow p-6">
              <Clock className="w-10 h-10 text-primary mb-3" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">Support Hours</h3>
              <p className="text-gray-700 mb-1">Monday - Friday: 9am - 6pm PST</p>
              <p className="text-gray-700 mb-1">Saturday: 10am - 4pm PST</p>
              <p className="text-gray-700">Sunday: Closed</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
