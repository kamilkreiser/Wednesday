/**
 * =============================================================================
 * APP FACTORY — DEMO SERVICE
 * =============================================================================
 * Builds the express app. Split out of index.ts (KS-641) so the real
 * middleware wiring — including the inbound auth guard — can be exercised in
 * tests. index.ts previously called app.listen() at module load, so importing
 * it started a listener; nothing could assert that the guard was actually
 * MOUNTED, only that it existed.
 * =============================================================================
 */

import express, { Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import cookieParser from 'cookie-parser';
import morgan from 'morgan';
import { rejectNulBytes } from '@secuura/shared';

import { createLogger } from './utils/logger';
import { requireDemoKey } from './middleware/demoGuard';
import { errorHandler } from './middleware/errorHandler';
import { healthRouter } from './routes/health';
import { personaRouter } from './routes/persona';
import { stateRouter } from './routes/state';
import { resetRouter } from './routes/reset';
import { scenarioRouter } from './routes/scenario';

const logger = createLogger('demo-service');

export function createApp() {
  const app = express();

  // ===========================================================================
  // MIDDLEWARE
  // ===========================================================================

  app.use(helmet());
  app.use(cors({
    origin: process.env.CORS_ORIGINS?.split(',') || [
      'http://localhost:6882',
      'http://localhost:6881',
    ],
    credentials: true,
  }));
  app.use(cookieParser());
  app.use(express.json());
  // KS-800: the control-byte guard inspects `req.body`, so it MUST be mounted
  // after every body parser — a guard above the parser walks an empty object and
  // passes everything. demo-service mounted a parser and no guard at all, which
  // the KS-781 class test could not see: its scan returns null for a file with no
  // guard, so an unguarded service was invisible rather than failing. That hole is
  // closed by LEG E in ks781-p3-3-body-parser-order.test.ts.
  app.use(rejectNulBytes());
  app.use(morgan('combined', {
    stream: { write: (message: string) => logger.info(message.trim()) },
  }));

  // ===========================================================================
  // ROUTES
  // ===========================================================================

  // /health stays PUBLIC and must be mounted before the guard: the compose
  // healthcheck calls it unauthenticated
  // (`wget --spider http://localhost:4030/demo-api/health`), so guarding it
  // would fail the container rather than secure it.
  app.use('/demo-api', healthRouter);

  // KS-641: everything below this line requires the shared demo key. It sits
  // between the routers rather than inside them so that adding a new /demo-api
  // router inherits the guard by default instead of opting into it.
  app.use('/demo-api', requireDemoKey);

  app.use('/demo-api', personaRouter);
  app.use('/demo-api', stateRouter);
  app.use('/demo-api', resetRouter);
  app.use('/demo-api', scenarioRouter);

  // 404 handler
  app.use((_req: Request, res: Response) => {
    res.status(404).json({
      success: false,
      error: { code: 'NOT_FOUND', message: `Cannot ${_req.method} ${_req.path}` },
    });
  });

  // KS-844: JSON error envelope, never express's default HTML page (stack
  // trace + absolute paths). Exported module, not inline — see errorHandler.ts.
  app.use(errorHandler);

  return app;
}
