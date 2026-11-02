import { query } from './db.js';
import { encrypt, decrypt, generateToken } from './crypto.js';

interface TokeniseResult {
  name: string;
  token: string;
}

interface DetokeniseResult {
  token: string;
  value: string | null;
}

export async function tokenise(
  tenantId: string,
  fields: Array<{ name: string; value: string }>,
  base64Key: string,
): Promise<TokeniseResult[]> {
  const results: TokeniseResult[] = [];

  for (const field of fields) {
    if (!field.value || field.value.startsWith('tok_')) {
      results.push({ name: field.name, token: field.value || '' });
      continue;
    }

    const token = generateToken();
    const { ciphertext, iv, authTag } = encrypt(field.value, base64Key);

    await query(
      `INSERT INTO vault_entries (tenant_id, token, encrypted_value, iv, auth_tag, field_type)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [tenantId, token, ciphertext, iv, authTag, field.name],
    );

    results.push({ name: field.name, token });
  }

  return results;
}

export async function detokenise(
  tenantId: string,
  tokens: string[],
  base64Key: string,
): Promise<DetokeniseResult[]> {
  if (tokens.length === 0) return [];

  const placeholders = tokens.map((_, i) => `$${i + 2}`).join(',');
  const rows = await query<{
    token: string;
    encrypted_value: Buffer;
    iv: string;
    auth_tag: Buffer;
  }>(
    `SELECT token, encrypted_value, iv, auth_tag FROM vault_entries
     WHERE tenant_id = $1 AND token IN (${placeholders})`,
    [tenantId, ...tokens],
  );

  const map = new Map<string, { encrypted_value: Buffer; iv: string; auth_tag: Buffer }>();
  for (const r of rows.rows) {
    map.set(r.token, r);
  }

  return tokens.map((tok) => {
    const entry = map.get(tok);
    if (!entry) return { token: tok, value: null };
    try {
      const value = decrypt(entry.encrypted_value, entry.iv, entry.auth_tag, base64Key);
      return { token: tok, value };
    } catch (err) {
      // AUDIT B-11: do not silently swallow decrypt failures. PII-loss /
      // key-rotation incidents become invisible if these don't reach a log.
      // Tenant id + token hash (NOT the token itself, NOT the plaintext —
      // the token is the lookup key and is auditable in the vault_entries
      // table directly).
      const tokenHash = require('node:crypto').createHash('sha256').update(tok).digest('hex').slice(0, 16);
      // eslint-disable-next-line no-console
      console.error('[tokenisation/vault] decrypt failed', {
        tenantId, tokenHash, error: (err as Error)?.message ?? String(err),
      });
      return { token: tok, value: null };
    }
  });
}

export async function rotateKey(
  tenantId: string,
  oldKey: string,
  newKey: string,
): Promise<{ rotated: number; failed: number }> {
  const rows = await query<{
    id: string;
    token: string;
    encrypted_value: Buffer;
    iv: string;
    auth_tag: Buffer;
  }>(
    `SELECT id, token, encrypted_value, iv, auth_tag FROM vault_entries WHERE tenant_id = $1`,
    [tenantId],
  );

  let rotated = 0;
  let failed = 0;

  for (const row of rows.rows) {
    try {
      const plaintext = decrypt(row.encrypted_value, row.iv, row.auth_tag, oldKey);
      const { ciphertext, iv, authTag } = encrypt(plaintext, newKey);
      await query(
        `UPDATE vault_entries SET encrypted_value = $1, iv = $2, auth_tag = $3 WHERE id = $4`,
        [ciphertext, iv, authTag, row.id],
      );
      rotated++;
    } catch {
      failed++;
    }
  }

  return { rotated, failed };
}
