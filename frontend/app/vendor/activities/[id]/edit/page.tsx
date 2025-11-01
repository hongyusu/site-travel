'use client';

import { useParams } from 'next/navigation';
import ActivityForm from '@/components/vendor/ActivityForm';

export default function EditActivityPage() {
  const params = useParams();
  const activityId = parseInt(params.id as string);

  return <ActivityForm mode="edit" activityId={activityId} />;
}
