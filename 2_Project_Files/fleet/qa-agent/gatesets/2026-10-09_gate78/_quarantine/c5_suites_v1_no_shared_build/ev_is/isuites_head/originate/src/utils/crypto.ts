/**
 * =============================================================================
 * CRYPTOGRAPHIC UTILITIES
 * =============================================================================
 * BLAKE2b hashing and cryptographic operations for document authenticity
 * =============================================================================
 */

import blake2 from 'blake2';
import crypto from 'crypto';

/**
 * Generate BLAKE2b hash of a buffer
 * @param data - Buffer to hash
 * @param digestLength - Output hash length in bytes (default: 32 = 256 bits)
 * @returns Hex-encoded hash string
 */
export function generateHash(data: Buffer, digestLength: number = 32): string {
  const hash = blake2.createHash('blake2b', { digestLength });
  hash.update(data);
  return hash.digest('hex');
}

/**
 * Verify that data matches a given hash
 * @param data - Buffer to verify
 * @param expectedHash - Expected hex-encoded hash
 * @returns True if hash matches
 */
export function verifyHash(data: Buffer, expectedHash: string): boolean {
  const actualHash = generateHash(data);
  return actualHash === expectedHash.toLowerCase();
}

/**
 * Generate hash of a string (UTF-8 encoded)
 * @param str - String to hash
 * @returns Hex-encoded hash string
 */
export function hashString(str: string): string {
  return generateHash(Buffer.from(str, 'utf-8'));
}

/**
 * Generate a random bytes buffer
 * @param length - Number of random bytes
 * @returns Buffer of random bytes
 */
export function randomBytes(length: number): Buffer {
  return crypto.randomBytes(length);
}

/**
 * Generate a random hex string
 * @param length - Number of bytes (output will be 2x this length)
 * @returns Hex-encoded random string
 */
export function randomHex(length: number): string {
  return crypto.randomBytes(length).toString('hex');
}

/**
 * Encrypt data using AES-256-GCM
 * @param data - Data to encrypt
 * @param key - 32-byte encryption key
 * @returns Object with encrypted data, iv, and auth tag
 */
export function encrypt(data: Buffer, key: Buffer): {
  encrypted: Buffer;
  iv: Buffer;
  authTag: Buffer;
} {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  
  const encrypted = Buffer.concat([
    cipher.update(data),
    cipher.final(),
  ]);
  
  const authTag = cipher.getAuthTag();
  
  return { encrypted, iv, authTag };
}

/**
 * Decrypt data using AES-256-GCM
 * @param encrypted - Encrypted data
 * @param key - 32-byte encryption key
 * @param iv - Initialization vector used for encryption
 * @param authTag - Authentication tag from encryption
 * @returns Decrypted data buffer
 */
export function decrypt(
  encrypted: Buffer,
  key: Buffer,
  iv: Buffer,
  authTag: Buffer
): Buffer {
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(authTag);
  
  return Buffer.concat([
    decipher.update(encrypted),
    decipher.final(),
  ]);
}

/**
 * Generate a Merkle root from an array of hashes
 * @param hashes - Array of hex-encoded hashes
 * @returns Merkle root hash
 */
export function generateMerkleRoot(hashes: string[]): string {
  if (hashes.length === 0) {
    throw new Error('Cannot generate Merkle root from empty array');
  }
  
  if (hashes.length === 1) {
    return hashes[0];
  }
  
  // Ensure even number of hashes
  const leaves = [...hashes];
  if (leaves.length % 2 !== 0) {
    leaves.push(leaves[leaves.length - 1]);
  }
  
  // Build tree level by level
  const nextLevel: string[] = [];
  for (let i = 0; i < leaves.length; i += 2) {
    const combined = leaves[i] + leaves[i + 1];
    nextLevel.push(hashString(combined));
  }
  
  return generateMerkleRoot(nextLevel);
}

/**
 * Generate Merkle proof for a leaf
 * @param hashes - Array of all leaf hashes
 * @param targetHash - Hash to generate proof for
 * @returns Merkle proof array
 */
export function generateMerkleProof(
  hashes: string[],
  targetHash: string
): { hash: string; position: 'left' | 'right' }[] {
  const proof: { hash: string; position: 'left' | 'right' }[] = [];
  
  // Find target index
  let index = hashes.findIndex(h => h === targetHash);
  if (index === -1) {
    throw new Error('Target hash not found in leaves');
  }
  
  let leaves = [...hashes];
  if (leaves.length % 2 !== 0) {
    leaves.push(leaves[leaves.length - 1]);
  }
  
  while (leaves.length > 1) {
    const nextLevel: string[] = [];
    
    for (let i = 0; i < leaves.length; i += 2) {
      // If current pair contains our target, add sibling to proof
      if (i === index || i + 1 === index) {
        if (index % 2 === 0) {
          proof.push({ hash: leaves[i + 1], position: 'right' });
        } else {
          proof.push({ hash: leaves[i], position: 'left' });
        }
        index = Math.floor(index / 2);
      }
      
      const combined = leaves[i] + leaves[i + 1];
      nextLevel.push(hashString(combined));
    }
    
    leaves = nextLevel;
  }
  
  return proof;
}

/**
 * Verify a Merkle proof
 * @param leafHash - Hash of the leaf to verify
 * @param proof - Merkle proof
 * @param root - Expected Merkle root
 * @returns True if proof is valid
 */
export function verifyMerkleProof(
  leafHash: string,
  proof: { hash: string; position: 'left' | 'right' }[],
  root: string
): boolean {
  let currentHash = leafHash;
  
  for (const step of proof) {
    if (step.position === 'left') {
      currentHash = hashString(step.hash + currentHash);
    } else {
      currentHash = hashString(currentHash + step.hash);
    }
  }
  
  return currentHash === root;
}
