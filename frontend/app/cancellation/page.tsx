import Link from 'next/link';
import { Clock, AlertCircle, CheckCircle, XCircle } from 'lucide-react';

export default function CancellationPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-primary text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Cancellation Policy</h1>
          <p className="text-xl text-white/90">Last updated: January 2024</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          {/* Overview */}
          <section className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Overview</h2>
            <p className="text-gray-700 mb-4">
              We understand that plans change. Our cancellation policy varies depending on the activity
              and when you cancel. Most activities offer free cancellation up to 24 hours before the start time.
            </p>
          </section>

          {/* Cancellation Timeline */}
          <section className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Cancellation Timeline</h2>

            <div className="space-y-4">
              <div className="border-l-4 border-green-500 bg-green-50 p-4 rounded-r">
                <div className="flex items-start">
                  <CheckCircle className="w-6 h-6 text-green-500 mr-3 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-bold text-gray-900 mb-1">More than 24 Hours</h3>
                    <p className="text-gray-700">
                      Cancel up to 24 hours before the activity starts for a full refund. Processing
                      takes 5-10 business days.
                    </p>
                  </div>
                </div>
              </div>

              <div className="border-l-4 border-yellow-500 bg-yellow-50 p-4 rounded-r">
                <div className="flex items-start">
                  <AlertCircle className="w-6 h-6 text-yellow-500 mr-3 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-bold text-gray-900 mb-1">Within 24 Hours</h3>
                    <p className="text-gray-700">
                      Cancellations within 24 hours may be subject to fees or no refund, depending on
                      the activity provider's specific policy.
                    </p>
                  </div>
                </div>
              </div>

              <div className="border-l-4 border-red-500 bg-red-50 p-4 rounded-r">
                <div className="flex items-start">
                  <XCircle className="w-6 h-6 text-red-500 mr-3 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-bold text-gray-900 mb-1">No Show</h3>
                    <p className="text-gray-700">
                      If you don't show up for your booked activity, you will not receive a refund.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* How to Cancel */}
          <section className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">How to Cancel Your Booking</h2>
            <ol className="list-decimal list-inside space-y-3 text-gray-700">
              <li>Log in to your account and go to "My Bookings"</li>
              <li>Find the booking you want to cancel</li>
              <li>Click "Cancel Booking" and follow the prompts</li>
              <li>You'll receive a confirmation email with your refund details</li>
            </ol>
          </section>

          {/* Special Cases */}
          <section className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Special Circumstances</h2>

            <h3 className="text-xl font-bold text-gray-900 mb-3">Weather Cancellations</h3>
            <p className="text-gray-700 mb-4">
              If an activity is cancelled due to poor weather conditions, you'll receive a full refund
              or the option to reschedule.
            </p>

            <h3 className="text-xl font-bold text-gray-900 mb-3">Provider Cancellations</h3>
            <p className="text-gray-700 mb-4">
              If the activity provider cancels your booking, you'll receive a full refund automatically
              within 5-10 business days.
            </p>

            <h3 className="text-xl font-bold text-gray-900 mb-3">Medical Emergencies</h3>
            <p className="text-gray-700 mb-4">
              For cancellations due to medical emergencies, please contact our support team with
              documentation. We'll work with the provider to find a solution.
            </p>
          </section>

          {/* Non-Refundable */}
          <section className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Non-Refundable Activities</h2>
            <p className="text-gray-700 mb-4">
              Some activities are marked as non-refundable. These are clearly labeled during the booking
              process. For non-refundable bookings:
            </p>
            <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
              <li>No refund is available for any cancellation</li>
              <li>Changes to dates or times may not be possible</li>
              <li>The booking cannot be transferred to another person</li>
            </ul>
          </section>

          {/* Contact */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Need Help?</h2>
            <p className="text-gray-700 mb-4">
              If you have questions about cancellations or need assistance with a specific booking,
              our customer support team is here to help.
            </p>
            <Link href="/contact" className="btn-primary inline-block">
              Contact Support
            </Link>
          </section>
        </div>
      </div>
    </div>
  );
}
