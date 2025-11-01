'use client';

import { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';

export default function DestinationRedirect() {
  const params = useParams();
  const router = useRouter();
  const slug = params.slug as string;

  useEffect(() => {
    // Redirect to the new /destinations/ route
    router.replace(`/destinations/${slug}`);
  }, [slug, router]);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <p className="text-gray-600">Redirecting...</p>
    </div>
  );
}
