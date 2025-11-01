export default function CookiesPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Cookie Policy</h1>
          <p className="text-xl text-white/90">Last updated: January 2024</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="prose max-w-none">
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">What Are Cookies?</h2>
              <p className="text-gray-700 mb-4">
                Cookies are small text files that are placed on your device when you visit our website. They help us
                provide you with a better experience by remembering your preferences and understanding how you use our site.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Types of Cookies We Use</h2>

              <h3 className="text-xl font-bold text-gray-900 mb-3">Essential Cookies</h3>
              <p className="text-gray-700 mb-4">
                These cookies are necessary for the website to function properly. They enable basic functions like
                page navigation and access to secure areas. The website cannot function without these cookies.
              </p>

              <h3 className="text-xl font-bold text-gray-900 mb-3">Performance Cookies</h3>
              <p className="text-gray-700 mb-4">
                These cookies help us understand how visitors interact with our website by collecting and reporting
                information anonymously. This helps us improve our website's performance.
              </p>

              <h3 className="text-xl font-bold text-gray-900 mb-3">Functionality Cookies</h3>
              <p className="text-gray-700 mb-4">
                These cookies enable the website to remember choices you make (such as your language or currency
                preference) and provide enhanced, personalized features.
              </p>

              <h3 className="text-xl font-bold text-gray-900 mb-3">Targeting/Advertising Cookies</h3>
              <p className="text-gray-700 mb-4">
                These cookies are used to deliver advertisements that are relevant to you and your interests. They
                may also limit the number of times you see an advertisement and help measure the effectiveness of
                advertising campaigns.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Third-Party Cookies</h2>
              <p className="text-gray-700 mb-4">
                We use services from third parties that may also set cookies on your device. These include:
              </p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
                <li><strong>Google Analytics:</strong> For website analytics and performance tracking</li>
                <li><strong>Payment Processors:</strong> For secure payment processing</li>
                <li><strong>Social Media Platforms:</strong> For social sharing features</li>
                <li><strong>Advertising Networks:</strong> For targeted advertising</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Managing Cookies</h2>
              <p className="text-gray-700 mb-4">
                You can control and manage cookies in various ways. Please note that removing or blocking cookies
                may impact your user experience and some features may no longer be fully functional.
              </p>

              <h3 className="text-xl font-bold text-gray-900 mb-3">Browser Settings</h3>
              <p className="text-gray-700 mb-4">
                Most browsers allow you to control cookies through their settings preferences. You can set your
                browser to refuse cookies or delete certain cookies.
              </p>

              <h3 className="text-xl font-bold text-gray-900 mb-3">Opt-Out Tools</h3>
              <p className="text-gray-700 mb-4">
                You can opt out of targeted advertising by visiting:
              </p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
                <li>Network Advertising Initiative opt-out page</li>
                <li>Digital Advertising Alliance opt-out page</li>
                <li>Your Online Choices (for EU users)</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Cookie Duration</h2>
              <p className="text-gray-700 mb-4">
                Cookies may be session cookies (deleted when you close your browser) or persistent cookies (remain
                on your device for a set period or until you delete them).
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Updates to This Policy</h2>
              <p className="text-gray-700 mb-4">
                We may update this Cookie Policy from time to time. Any changes will be posted on this page with
                an updated revision date.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Contact Us</h2>
              <p className="text-gray-700 mb-4">
                If you have questions about our use of cookies, please contact us at:
              </p>
              <p className="text-gray-700">
                Email: privacy@meetyourtravelpartner.com<br />
                Address: 123 Market Street, San Francisco, CA 94103
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}
