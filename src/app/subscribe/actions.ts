'use server';

import { db } from '@/lib/firebase';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import type { FormValues } from './page';

export async function addSubscription(data: FormValues) {
  try {
    await addDoc(collection(db, 'subscriptions'), {
      ...data,
      submittedAt: serverTimestamp(),
    });
  } catch (e) {
    console.error('Error adding document: ', e);
    // Let the client-side catch the error and display a message.
    throw new Error('Failed to submit form.');
  }
}
