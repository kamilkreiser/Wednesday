/**
 * =============================================================================
 * PERSONA ROUTE — DEMO SERVICE
 * =============================================================================
 * Handles persona switching for the demo overlay. Validates the requested
 * persona, authenticates via the auth service, and proxies the httpOnly
 * refresh token cookie back to the browser.
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { z } from 'zod';

import { PERSONAS } from '../config/personas';
import { authenticatePersona } from '../services/authClient';
import { logger } from '../utils/logger';
import { PersonaKey } from '../types';

export const personaRouter = Router();

// =============================================================================
// VALIDATION SCHEMA
// =============================================================================

const switchSchema = z.object({
  persona: z.enum(['alice', 'sarah', 'bob', 'admin']),
});

// =============================================================================
// POST /demo-api/persona/switch
// =============================================================================

/**
 * Switches the current demo persona by authenticating against the auth service
 * and proxying the Set-Cookie header for the httpOnly refresh token.
 */
personaRouter.post('/persona/switch', async (req: Request, res: Response) => {
  try {
    const parsed = switchSchema.safeParse(req.body);

    if (!parsed.success) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Invalid persona', details: parsed.error.issues },
      });
    }

    const personaKey = parsed.data.persona as PersonaKey;
    const persona = PERSONAS[personaKey];

    logger.info('Switching persona', { persona: personaKey });

    const authResult = await authenticatePersona(persona.email, persona.password);

    if (!authResult.success) {
      logger.error('Persona auth failed', { persona: personaKey, error: authResult.error });
      return res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Persona auth failed' } });
    }

    // Proxy the Set-Cookie header from auth service (httpOnly refresh_token)
    if (authResult.setCookieHeader) {
      res.setHeader('Set-Cookie', authResult.setCookieHeader);
    }

    return res.json({
      success: true,
      data: {
        accessToken: authResult.accessToken,
        user: authResult.user,
        frontendRoute: persona.frontendRoute,
        organizationName: persona.organizationName,
        roles: persona.roles,
        roleColor: persona.roleColor,
      },
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    logger.error('Persona switch error', { error: message });
    return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
  }
});
