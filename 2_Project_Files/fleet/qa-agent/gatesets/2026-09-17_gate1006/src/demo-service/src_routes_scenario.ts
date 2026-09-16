/**
 * =============================================================================
 * SCENARIO ROUTE — DEMO SERVICE
 * =============================================================================
 * Exposes the current scenario context for a given persona. This is a
 * read-only informational endpoint — the overlay handles all scenario logic
 * client-side, but this endpoint enables future server-side scenario features
 * and external tooling to query the current demo narrative state.
 * =============================================================================
 */

import { Router, Request, Response } from 'express';

import { logger } from '../utils/logger';
import { PersonaKey } from '../types';

export const scenarioRouter = Router();

// =============================================================================
// SCENARIO DATA
// =============================================================================

/**
 * Academic records scenario data mirrored from the overlay config.
 * Defined server-side so the endpoint is self-contained.
 */
interface ScenarioContext {
  active: boolean;
  scenarioId: string;
  scenarioName: string;
  persona: PersonaKey;
  landingUrl: string;
  notification: {
    message: string;
    severity: 'info' | 'success';
  } | null;
  formPreFill: Record<string, string> | null;
}

const SCENARIO_STEPS: Record<PersonaKey, Omit<ScenarioContext, 'active'>> = {
  alice: {
    scenarioId: 'academic-records',
    scenarioName: 'Academic Records Verification',
    persona: 'alice',
    landingUrl: '/documents/new',
    notification: null,
    formPreFill: {
      title: 'Sarah Kim - Bachelor of Computer Science',
      description: 'Meridian University academic degree certification',
    },
  },
  sarah: {
    scenarioId: 'academic-records',
    scenarioName: 'Academic Records Verification',
    persona: 'sarah',
    landingUrl: '/documents',
    notification: {
      message: 'Alice Chen certified your academic record at Meridian University',
      severity: 'success',
    },
    formPreFill: null,
  },
  bob: {
    scenarioId: 'academic-records',
    scenarioName: 'Academic Records Verification',
    persona: 'bob',
    landingUrl: '/verify/',
    notification: {
      message: 'Sarah Kim shared a verified academic record for your review',
      severity: 'info',
    },
    formPreFill: null,
  },
  admin: {
    scenarioId: 'academic-records',
    scenarioName: 'Academic Records Verification',
    persona: 'admin',
    landingUrl: '/admin/',
    notification: {
      message: '3 new verification events recorded across the platform',
      severity: 'info',
    },
    formPreFill: null,
  },
};

// =============================================================================
// GET /demo-api/scenario/context
// =============================================================================

/**
 * Returns the scenario context for a given persona. If no persona is specified
 * via query parameter, returns { active: false }.
 */
scenarioRouter.get('/scenario/context', (req: Request, res: Response) => {
  try {
    const persona = req.query.persona as string | undefined;

    if (!persona || !SCENARIO_STEPS[persona as PersonaKey]) {
      return res.json({ active: false });
    }

    const personaKey = persona as PersonaKey;
    const step = SCENARIO_STEPS[personaKey];

    logger.info('Scenario context requested', { persona: personaKey });

    return res.json({
      active: true,
      ...step,
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    logger.error('Failed to get scenario context', { error: message });
    return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
  }
});
