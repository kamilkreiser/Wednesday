/**
 * =============================================================================
 * AUTH CLIENT — DEMO SERVICE
 * =============================================================================
 * Makes internal HTTP calls to the auth service to obtain real JWTs for demo
 * personas. Returns structured result objects rather than throwing on failure.
 * =============================================================================
 */

import { logger } from '../utils/logger';
import { AuthResponse } from '../types';

// =============================================================================
// CONFIGURATION
// =============================================================================

const AUTH_HOST = process.env.AUTH_HOST || 'auth';
const AUTH_PORT = process.env.AUTH_PORT || '4003';

// =============================================================================
// AUTHENTICATE PERSONA
// =============================================================================

/**
 * Authenticates a demo persona via the auth service login endpoint.
 * Returns a structured response object; does NOT throw on failure.
 */
export async function authenticatePersona(
  email: string,
  password: string,
): Promise<AuthResponse> {
  const url = `http://${AUTH_HOST}:${AUTH_PORT}/api/auth/login`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      logger.error('Auth service login failed', {
        status: response.status,
        email,
      });
      return {
        success: false,
        error: `Auth service returned ${response.status}`,
      };
    }

    const setCookieHeader = response.headers.get('set-cookie');
    const body = await response.json() as Record<string, any>;

    return {
      success: true,
      accessToken: body.data?.accessToken || body.accessToken,
      user: body.data?.user || body.user || {},
      setCookieHeader,
    };
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    logger.error('Auth service request failed', { error: message, email });
    return {
      success: false,
      error: message,
    };
  }
}
