export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Privacy Policy</h1>
          <p className="text-xl text-white/90">Last updated: January 2024</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="prose max-w-none">
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Introduction</h2>
              <p className="text-gray-700 mb-4">
                FindTravelMate ("we," "our," or "us") is committed to protecting your privacy. This Privacy
                Policy explains how we collect, use, disclose, and safeguard your information when you use our platform.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Information We Collect</h2>

              <h3 className="text-xl font-bold text-gray-900 mb-3">Personal Information</h3>
              <p className="text-gray-700 mb-4">We collect information that you provide directly to us, including:</p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4 mb-4">
                <li>Name, email address, and phone number</li>
                <li>Billing and payment information</li>
                <li>Profile information and preferences</li>
                <li>Booking and travel history</li>
                <li>Communications with us</li>
              </ul>

              <h3 className="text-xl font-bold text-gray-900 mb-3">Automatically Collected Information</h3>
              <p className="text-gray-700 mb-4">When you use our services, we automatically collect:</p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4 mb-4">
                <li>Device information and IP address</li>
                <li>Browser type and version</li>
                <li>Usage data and analytics</li>
                <li>Cookies and similar technologies</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">How We Use Your Information</h2>
              <p className="text-gray-700 mb-4">We use the information we collect to:</p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
                <li>Process and manage your bookings</li>
                <li>Communicate with you about your reservations</li>
                <li>Provide customer support</li>
                <li>Improve our services and develop new features</li>
                <li>Send marketing communications (with your consent)</li>
                <li>Prevent fraud and ensure platform security</li>
                <li>Comply with legal obligations</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Information Sharing</h2>
              <p className="text-gray-700 mb-4">We may share your information with:</p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
                <li><strong>Activity Providers:</strong> To facilitate your bookings</li>
                <li><strong>Service Providers:</strong> Who help us operate our platform</li>
                <li><strong>Payment Processors:</strong> To process transactions securely</li>
                <li><strong>Legal Authorities:</strong> When required by law</li>
              </ul>
              <p className="text-gray-700 mt-4">We do not sell your personal information to third parties.</p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Data Security</h2>
              <p className="text-gray-700 mb-4">
                We implement appropriate technical and organizational measures to protect your personal information.
                However, no method of transmission over the Internet is 100% secure, and we cannot guarantee absolute security.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Rights</h2>
              <p className="text-gray-700 mb-4">You have the right to:</p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
                <li>Access your personal information</li>
                <li>Correct inaccurate data</li>
                <li>Request deletion of your data</li>
                <li>Object to processing of your data</li>
                <li>Export your data</li>
                <li>Withdraw consent at any time</li>
              </ul>
              <p className="text-gray-700 mt-4">
                To exercise these rights, please contact us at privacy@findtravelmate.com
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Cookies</h2>
              <p className="text-gray-700 mb-4">
                We use cookies and similar tracking technologies to improve your experience. You can control
                cookies through your browser settings. For more information, see our Cookie Policy.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Children's Privacy</h2>
              <p className="text-gray-700 mb-4">
                Our services are not directed to children under 13. We do not knowingly collect personal
                information from children under 13.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Changes to This Policy</h2>
              <p className="text-gray-700 mb-4">
                We may update this Privacy Policy from time to time. We will notify you of any changes by
                posting the new policy on this page and updating the "Last updated" date.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Contact Us</h2>
              <p className="text-gray-700 mb-4">
                If you have questions about this Privacy Policy, please contact us at:
              </p>
              <p className="text-gray-700">
                Email: privacy@findtravelmate.com<br />
                Address: 123 Market Street, San Francisco, CA 94103
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}
