'use client';

import { useParams } from 'next/navigation';
import ActivityFormWithLanguages from '@/components/vendor/ActivityFormWithLanguages';

export default function EditActivityPage() {
  const params = useParams();
  const activityId = parseInt(params.id as string);

  return <ActivityFormWithLanguages mode="edit" activityId={activityId} />;
}
