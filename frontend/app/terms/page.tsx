export default function TermsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Terms of Service</h1>
          <p className="text-xl text-white/90">Last updated: January 2024</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="prose max-w-none">
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Acceptance of Terms</h2>
              <p className="text-gray-700 mb-4">
                By accessing and using MeetYourTravelPartner (the "Platform"), you accept and agree to be bound by
                these Terms of Service. If you do not agree to these terms, please do not use our Platform.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Use of Platform</h2>
              <p className="text-gray-700 mb-4">You agree to use the Platform only for lawful purposes. You agree not to:</p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
                <li>Violate any applicable laws or regulations</li>
                <li>Infringe on the rights of others</li>
                <li>Interfere with or disrupt the Platform</li>
                <li>Attempt to gain unauthorized access to any systems</li>
                <li>Use automated systems to access the Platform</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">3. Bookings and Payments</h2>
              <p className="text-gray-700 mb-4">
                When you make a booking through our Platform, you enter into a contract with the activity provider,
                not with MeetYourTravelPartner. We act as an intermediary to facilitate the booking.
              </p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
                <li>All bookings are subject to availability</li>
                <li>Prices are displayed in the currency specified</li>
                <li>Payment must be made at the time of booking</li>
                <li>You are responsible for providing accurate information</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Cancellations and Refunds</h2>
              <p className="text-gray-700 mb-4">
                Cancellation and refund policies vary by activity provider. Please review the specific cancellation
                policy before booking. For more details, see our Cancellation Policy.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">5. User Accounts</h2>
              <p className="text-gray-700 mb-4">
                To use certain features, you must create an account. You are responsible for:
              </p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
                <li>Maintaining the confidentiality of your account credentials</li>
                <li>All activities that occur under your account</li>
                <li>Notifying us immediately of any unauthorized access</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Content and Reviews</h2>
              <p className="text-gray-700 mb-4">
                Users may post reviews and other content on the Platform. By posting content, you grant us a
                non-exclusive, royalty-free license to use, reproduce, and display your content.
              </p>
              <p className="text-gray-700 mb-4">
                You agree that your content will not:
              </p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
                <li>Be false, inaccurate, or misleading</li>
                <li>Violate any laws or third-party rights</li>
                <li>Contain offensive or harmful material</li>
                <li>Include promotional or commercial content</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Intellectual Property</h2>
              <p className="text-gray-700 mb-4">
                The Platform and its content are protected by copyright, trademark, and other intellectual property
                laws. You may not copy, modify, or distribute any content without our permission.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">8. Limitation of Liability</h2>
              <p className="text-gray-700 mb-4">
                MeetYourTravelPartner is not liable for any indirect, incidental, or consequential damages arising
                from your use of the Platform or participation in activities booked through the Platform.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Disputes with Providers</h2>
              <p className="text-gray-700 mb-4">
                Any disputes regarding activities or services should be resolved directly with the activity provider.
                We will assist where possible but are not responsible for provider actions.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">10. Modifications to Terms</h2>
              <p className="text-gray-700 mb-4">
                We reserve the right to modify these Terms at any time. Continued use of the Platform after changes
                constitutes acceptance of the modified Terms.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">11. Governing Law</h2>
              <p className="text-gray-700 mb-4">
                These Terms are governed by the laws of the State of California, United States, without regard to
                conflict of law principles.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">12. Contact Information</h2>
              <p className="text-gray-700 mb-4">
                For questions about these Terms, please contact us at:
              </p>
              <p className="text-gray-700">
                Email: legal@meetyourtravelpartner.com<br />
                Address: 123 Market Street, San Francisco, CA 94103
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}
