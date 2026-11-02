/**
 * =============================================================================
 * DATABASE CONNECTION POOLING
 * =============================================================================
 * Generic connection pool manager for database connections
 */

import { EventEmitter } from 'events';
import { logger } from '../utils/logger';

export interface PoolConfig {
  min: number;               // Minimum connections in pool
  max: number;               // Maximum connections in pool
  acquireTimeoutMs: number;  // Max time to wait for connection
  idleTimeoutMs: number;     // Time before idle connection is closed
  createRetryMs: number;     // Time between create retries
  maxRetries: number;        // Max create attempts
}

export interface PoolStats {
  total: number;
  available: number;
  pending: number;
  borrowed: number;
}

export interface Connection {
  id: string;
  createdAt: Date;
  lastUsedAt: Date;
  isValid: () => Promise<boolean>;
  close: () => Promise<void>;
}

type ConnectionFactory<T extends Connection> = () => Promise<T>;
type ConnectionValidator<T extends Connection> = (conn: T) => Promise<boolean>;

const DEFAULT_CONFIG: PoolConfig = {
  min: 2,
  max: 10,
  acquireTimeoutMs: 30000,
  idleTimeoutMs: 60000,
  createRetryMs: 1000,
  maxRetries: 3,
};

/**
 * Generic connection pool
 */
export class ConnectionPool<T extends Connection> extends EventEmitter {
  private config: PoolConfig;
  private connections: T[] = [];
  private available: T[] = [];
  private waitQueue: Array<{
    resolve: (conn: T) => void;
    reject: (err: Error) => void;
    timeout: NodeJS.Timeout;
  }> = [];
  
  private factory: ConnectionFactory<T>;
  private validator: ConnectionValidator<T>;
  private isClosing = false;
  private maintenanceInterval: NodeJS.Timeout | null = null;

  constructor(
    factory: ConnectionFactory<T>,
    validator: ConnectionValidator<T> = async (conn) => conn.isValid(),
    config: Partial<PoolConfig> = {}
  ) {
    super();
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.factory = factory;
    this.validator = validator;
  }

  /**
   * Initialize pool with minimum connections
   */
  async initialize(): Promise<void> {
    logger.info('Pool initializing', { min: this.config.min, max: this.config.max });
    
    // Results are discarded — the catch below turns a rejection into a
    // logged no-op, which widens the element type beyond Promise<void>.
    const createPromises: Promise<unknown>[] = [];
    for (let i = 0; i < this.config.min; i++) {
      createPromises.push(this.createConnection().catch(err => {
        logger.error('Pool failed to create initial connection', { error: String(err) });
      }));
    }
    
    await Promise.all(createPromises);
    
    // Start maintenance
    this.startMaintenance();
    
    logger.info('Pool initialized', { connections: this.connections.length });
  }

  /**
   * Create a new connection
   */
  private async createConnection(): Promise<T> {
    let lastError: Error | null = null;
    
    for (let attempt = 0; attempt < this.config.maxRetries; attempt++) {
      try {
        const conn = await this.factory();
        
        this.connections.push(conn);
        this.available.push(conn);
        
        this.emit('connectionCreated', conn);
        return conn;
      } catch (error) {
        lastError = error as Error;
        logger.error('Pool create attempt failed', { attempt: attempt + 1, error: String(error) });
        
        if (attempt < this.config.maxRetries - 1) {
          await new Promise(resolve => setTimeout(resolve, this.config.createRetryMs));
        }
      }
    }
    
    throw lastError || new Error('Failed to create connection');
  }

  /**
   * Acquire a connection from the pool
   */
  async acquire(): Promise<T> {
    if (this.isClosing) {
      throw new Error('Pool is closing');
    }

    // Try to get an available connection
    while (this.available.length > 0) {
      const conn = this.available.pop()!;
      
      // Validate connection
      try {
        if (await this.validator(conn)) {
          conn.lastUsedAt = new Date();
          this.emit('connectionAcquired', conn);
          return conn;
        }
      } catch {
        // Connection invalid, remove it
        this.removeConnection(conn);
        continue;
      }
    }

    // No available connections - can we create more?
    if (this.connections.length < this.config.max) {
      try {
        const conn = await this.createConnection();
        // Remove from available since we're returning it directly
        const idx = this.available.indexOf(conn);
        if (idx !== -1) {
          this.available.splice(idx, 1);
        }
        conn.lastUsedAt = new Date();
        this.emit('connectionAcquired', conn);
        return conn;
      } catch (error) {
        // Fall through to wait queue
      }
    }

    // All connections busy - wait in queue
    return new Promise<T>((resolve, reject) => {
      const timeout = setTimeout(() => {
        const idx = this.waitQueue.findIndex(w => w.resolve === resolve);
        if (idx !== -1) {
          this.waitQueue.splice(idx, 1);
        }
        reject(new Error('Acquire timeout - pool exhausted'));
      }, this.config.acquireTimeoutMs);

      this.waitQueue.push({ resolve, reject, timeout });
    });
  }

  /**
   * Release a connection back to the pool
   */
  release(conn: T): void {
    // Check if anyone is waiting
    if (this.waitQueue.length > 0) {
      const waiter = this.waitQueue.shift()!;
      clearTimeout(waiter.timeout);
      conn.lastUsedAt = new Date();
      waiter.resolve(conn);
      return;
    }

    // Return to available pool
    if (!this.available.includes(conn)) {
      this.available.push(conn);
    }
    
    this.emit('connectionReleased', conn);
  }

  /**
   * Remove a connection from the pool
   */
  private async removeConnection(conn: T): Promise<void> {
    const connIdx = this.connections.indexOf(conn);
    if (connIdx !== -1) {
      this.connections.splice(connIdx, 1);
    }

    const availIdx = this.available.indexOf(conn);
    if (availIdx !== -1) {
      this.available.splice(availIdx, 1);
    }

    try {
      await conn.close();
    } catch (error) {
      logger.error('Pool error closing connection', { error: String(error) });
    }

    this.emit('connectionRemoved', conn);
  }

  /**
   * Start maintenance routine
   */
  private startMaintenance(): void {
    this.maintenanceInterval = setInterval(async () => {
      await this.performMaintenance();
    }, this.config.idleTimeoutMs / 2);
  }

  /**
   * Perform pool maintenance
   */
  private async performMaintenance(): Promise<void> {
    if (this.isClosing) return;

    const now = Date.now();
    const toRemove: T[] = [];

    // Check for idle connections
    for (const conn of this.available) {
      const idleTime = now - conn.lastUsedAt.getTime();
      
      // Keep minimum connections even if idle
      if (this.connections.length > this.config.min && 
          idleTime > this.config.idleTimeoutMs) {
        toRemove.push(conn);
      }
    }

    // Remove idle connections
    for (const conn of toRemove) {
      await this.removeConnection(conn);
    }

    // Ensure minimum connections
    while (this.connections.length < this.config.min) {
      try {
        await this.createConnection();
      } catch (error) {
        logger.error('Pool maintenance: failed to create connection', { error: String(error) });
        break;
      }
    }

    // Validate available connections
    for (const conn of [...this.available]) {
      try {
        if (!await this.validator(conn)) {
          await this.removeConnection(conn);
        }
      } catch {
        await this.removeConnection(conn);
      }
    }
  }

  /**
   * Get pool statistics
   */
  getStats(): PoolStats {
    return {
      total: this.connections.length,
      available: this.available.length,
      pending: this.waitQueue.length,
      borrowed: this.connections.length - this.available.length,
    };
  }

  /**
   * Execute function with pooled connection
   */
  async withConnection<R>(fn: (conn: T) => Promise<R>): Promise<R> {
    const conn = await this.acquire();
    try {
      return await fn(conn);
    } finally {
      this.release(conn);
    }
  }

  /**
   * Close the pool
   */
  async close(): Promise<void> {
    this.isClosing = true;

    // Stop maintenance
    if (this.maintenanceInterval) {
      clearInterval(this.maintenanceInterval);
      this.maintenanceInterval = null;
    }

    // Reject waiting requests
    for (const waiter of this.waitQueue) {
      clearTimeout(waiter.timeout);
      waiter.reject(new Error('Pool is closing'));
    }
    this.waitQueue = [];

    // Close all connections
    const closePromises = this.connections.map(conn => 
      conn.close().catch(err => logger.error('Pool error closing', { error: String(err) }))
    );
    
    await Promise.all(closePromises);
    
    this.connections = [];
    this.available = [];
    
    logger.info('Pool closed');
    this.emit('closed');
  }
}

/**
 * Create a simple mock connection for demonstration
 */
export function createMockConnection(): Connection {
  const id = `conn_${require('crypto').randomUUID()}`;
  
  return {
    id,
    createdAt: new Date(),
    lastUsedAt: new Date(),
    isValid: async () => true,
    close: async () => {
      logger.info('Mock connection closed', { id });
    },
  };
}

// Database pool singleton (configure per service)
export const dbPool = {
  pool: null as ConnectionPool<Connection> | null,
  
  async initialize(config?: Partial<PoolConfig>): Promise<void> {
    if (this.pool) return;
    
    this.pool = new ConnectionPool(
      async () => createMockConnection(),
      async (conn) => conn.isValid(),
      config
    );
    
    await this.pool.initialize();
  },
  
  async acquire(): Promise<Connection> {
    if (!this.pool) {
      throw new Error('Pool not initialized');
    }
    return this.pool.acquire();
  },
  
  release(conn: Connection): void {
    this.pool?.release(conn);
  },
  
  async withConnection<R>(fn: (conn: Connection) => Promise<R>): Promise<R> {
    if (!this.pool) {
      throw new Error('Pool not initialized');
    }
    return this.pool.withConnection(fn);
  },
  
  getStats(): PoolStats | null {
    return this.pool?.getStats() || null;
  },
  
  async close(): Promise<void> {
    await this.pool?.close();
    this.pool = null;
  },
};

export default ConnectionPool;
