'use client';

import { useEffect, useState } from 'react';

export default function APITestPage() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('APITestPage useEffect running');
    
    fetch('http://localhost:8000/api/v1/activities/search?limit=5')
      .then(res => {
        console.log('Response status:', res.status);
        return res.json();
      })
      .then(data => {
        console.log('Data received:', data);
        setData(data);
      })
      .catch(err => {
        console.error('Error:', err);
        setError(err.message);
      });
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">API Test Page</h1>
      
      {error && (
        <div className="bg-red-100 p-4 mb-4 rounded">
          Error: {error}
        </div>
      )}
      
      {data && (
        <div className="bg-green-100 p-4 rounded">
          <p>Success! Received {data.data?.length || 0} activities</p>
          <p>First activity: {data.data?.[0]?.title || 'None'}</p>
        </div>
      )}
      
      {!data && !error && (
        <div className="bg-yellow-100 p-4 rounded">
          Loading...
        </div>
      )}
      
      <pre className="mt-4 bg-gray-100 p-4 rounded overflow-auto text-xs">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}