// Type declarations for blake2 module
declare module 'blake2' {
  interface HashOptions {
    digestLength?: number;
    key?: Buffer;
  }
  
  interface Hash {
    update(data: Buffer | string): Hash;
    digest(encoding?: 'hex' | 'base64'): string;
    digest(): Buffer;
  }
  
  export function createHash(algorithm: 'blake2b' | 'blake2bp' | 'blake2s' | 'blake2sp', options?: HashOptions): Hash;
  export function createKeyedHash(algorithm: 'blake2b' | 'blake2bp' | 'blake2s' | 'blake2sp', key: Buffer, options?: HashOptions): Hash;
  export default { createHash, createKeyedHash };
}
