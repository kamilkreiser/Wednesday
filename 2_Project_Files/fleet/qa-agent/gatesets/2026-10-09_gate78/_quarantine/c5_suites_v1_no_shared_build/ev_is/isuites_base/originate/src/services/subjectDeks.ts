/**
 * SUBJECT DEK PROVIDER — originate service singleton (KS-291).
 *
 * Resolves per-subject DEKs (pii_subject_keys) over the prisma raw-query
 * interface. Subjects here are users.id — consent records and data-subject
 * requests encrypt under the requesting user's DEK, and executeErasure
 * destroys that DEK as the final erasure step (true crypto-shred).
 */

import { SubjectDekProvider } from '@secuura/shared';
import { prisma } from '../db';

export const subjectDeks = new SubjectDekProvider(async (text, params) => {
  const rows = (await prisma.$queryRawUnsafe(text, ...params)) as Array<Record<string, unknown>>;
  return { rows };
});
