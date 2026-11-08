/**
 * KS-2038: who may approve, reject, execute or cancel a transfer.
 *
 * This file is the ONE place the rule lives. Before KS-2038 the four doors checked no caller at all: any signed-in user of any
 * tenant could act on any transfer, and approve and reject recorded whoever the request body named. To reshape the rule, change
 * `WHO_MAY` below and nothing else; the doors in index.ts only ask `decideTransferAccess`.
 *
 * Where each clause comes from, because almost nothing in the repo says who may act:
 *   - approve, simple: PUBLISHED, transfer.openapi.ts POST /api/transfers: "single approve from the recipient".
 *   - approve, sale: a code comment in index.ts ("Both parties") and the seeded Sale workflow (Seller, Buyer).
 *   - approve, inheritance: a code comment in index.ts ("Executor + beneficiary").
 *   - approve, corporate: nobody. The comment says "Board members" but no field names one, so naming an approver would be invented.
 *   - reject: proposed for KS-2038. The current owner must be able to refuse a transfer someone else opened.
 *   - execute: proposed for KS-2038. This is where the owner's consent lands, because POST /api/transfers takes the owner from the
 *     body and checks it against nothing; so the initiator is deliberately not admitted here.
 *   - cancel: PUBLISHED, transfer.openapi.ts: "Cancel a transfer (initiator only, before execution)".
 * Kam ruled the whole rule: card secuura-ks2038-who-may-approve-transfers-1106 = a, live board 2026-11-06 14:57:33 AEDT, "Use the party rule above (recommended)".
 *
 * KS-2081: this rule is for people. A non-user principal never reaches it: `isNonUserPrincipal` below refuses it first.
 */

export type TransferVerb = 'approve' | 'reject' | 'execute' | 'cancel';
type TransferKind = 'simple' | 'sale' | 'inheritance' | 'corporate';
type PartyField = 'currentOwnerId' | 'newOwnerId' | 'initiatedBy' | 'executorId';

/** The fields of a transfer this rule reads. `executorId` has no column, so it is absent after a restart: see KS-2038's PR. */
export interface TransferParties {
  transferType: string;
  currentOwnerId?: string;
  newOwnerId?: string;
  initiatedBy?: string;
  executorId?: string;
}

const WHO_MAY: Record<TransferVerb, Record<TransferKind, readonly PartyField[]>> = {
  approve: {
    simple: ['newOwnerId'],
    sale: ['currentOwnerId', 'newOwnerId'],
    inheritance: ['executorId', 'newOwnerId'],
    corporate: [],
  },
  reject: {
    simple: ['currentOwnerId', 'newOwnerId', 'executorId'],
    sale: ['currentOwnerId', 'newOwnerId', 'executorId'],
    inheritance: ['currentOwnerId', 'newOwnerId', 'executorId'],
    corporate: ['currentOwnerId', 'newOwnerId', 'executorId'],
  },
  execute: {
    simple: ['currentOwnerId'],
    sale: ['currentOwnerId'],
    inheritance: ['executorId'],
    corporate: ['currentOwnerId'],
  },
  cancel: {
    simple: ['initiatedBy'],
    sale: ['initiatedBy'],
    inheritance: ['initiatedBy'],
    corporate: ['initiatedBy'],
  },
};

/** Everyone a transfer names. Anyone else is a stranger, who gets the same 404 as an unknown id. */
const PARTY_FIELDS: readonly PartyField[] = ['currentOwnerId', 'newOwnerId', 'initiatedBy', 'executorId'];

/**
 * True when two ids name the same person. POST /api/transfers accepts a uuid in either case and stores it as sent, while the token
 * carries the id as the auth service wrote it. An ASCII fold only (the KS-1591 lesson): a non-ASCII character never folds into a match.
 */
export function sameId(a: string | undefined, b: string | undefined): boolean {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length === 0) return false;
  const fold = (s: string) => s.replace(/[A-Z]/g, (ch) => ch.toLowerCase());
  return fold(a) === fold(b);
}

export type TransferAccess = { allow: true } | { allow: false; status: 403 | 404 };

/**
 * The decision for one signed-in caller, one verb and one transfer.
 * No role is read: as on KS-1851, a platform or tenant administrator who is no party is refused like anyone else.
 * A transfer type outside the table admits nobody, so a row written by something other than POST /api/transfers fails closed.
 */
export function decideTransferAccess(callerId: string, verb: TransferVerb, transfer: TransferParties): TransferAccess {
  const named = (field: PartyField) => sameId(transfer[field], callerId);
  if (!PARTY_FIELDS.some(named)) return { allow: false, status: 404 };
  const fields = WHO_MAY[verb][transfer.transferType as TransferKind];
  if (Array.isArray(fields) && fields.some(named)) return { allow: true };
  return { allow: false, status: 403 };
}

export interface SignedInCaller {
  userId: string;
  role: string;
}

/**
 * The verified identity on the request, or null when it names no user. Every door answers 401 on null: before KS-2038 execute and
 * cancel fell back to 'system' and 'unknown', so a token with no user id could act and be recorded as nobody.
 */
export function signedInCaller(user: unknown): SignedInCaller | null {
  const claims = user as { userId?: unknown; role?: unknown } | null | undefined;
  if (typeof claims?.userId !== 'string' || claims.userId.length === 0) return null;
  return { userId: claims.userId, role: typeof claims.role === 'string' && claims.role.length > 0 ? claims.role : 'unknown' };
}

// The shape of a users.id: that column is UUID in docker/init/01-schema.sql, migrations/001 and deployment/azure/migrate/init.sql. Either case, as z.string().guid().
const GUID_SHAPE = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;

/**
 * KS-2081: true when the verified token is not a person. Kam ruled that keys are never a party on these doors: card
 * secuura-ks2038-connector-principals-on-transfer-doors-1106 = a, "Keys are never a party on these doors (recommended)". Any one signal decides:
 *   - type, role or verificationLevel as auth's generateConnectorToken stamps them. A key cannot shed them, because they are constants in that mint.
 *     A person cannot gain them, because the login mints read role and level through closed tables that hold neither.
 *   - a user id that cannot be a users row. This also refuses a machine principal nobody has minted yet, which then comes back to Kam, as his card says.
 * So "no person's answer changes" rests on the schema and the mint, not on the shape of this test.
 * A missing, empty or non-string user id is NOT decided here: such a token keeps its answers, 401 at the id doors and the body fallback at the open door.
 * An OAuth token is a person's and reads false: it carries that person's user.id. What an app may do with it is not this rule.
 */
export function isNonUserPrincipal(user: unknown): boolean {
  const claims = user as { userId?: unknown; role?: unknown; type?: unknown; verificationLevel?: unknown } | null | undefined;
  if (claims?.type === 'connector' || claims?.role === 'connector' || claims?.verificationLevel === 'api_key') return true;
  return typeof claims?.userId === 'string' && claims.userId.length > 0 && !GUID_SHAPE.test(claims.userId);
}
