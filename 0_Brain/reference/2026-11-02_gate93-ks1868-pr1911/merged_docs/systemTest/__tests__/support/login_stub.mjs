#!/usr/bin/env node
/**
 * login_stub.mjs — a throwaway "gateway" that answers POST /api/auth/login with ONE fixed status
 * (KS-1167 B1). Used by `bootstrap_login_diagnosis.test.sh` to drive the shared pre-suite step
 * through each login outcome without a stack: the point of the cells is what the step SAYS about
 * a 429 versus a 401, and a real gateway cannot be asked to answer 429 on demand.
 *
 * Binds an ephemeral port on 127.0.0.1 (never a slot's gateway port), prints `PORT=<n>` once it
 * is listening, and serves until killed. Every other route is 404.
 *
 *   STUB_LOGIN_STATUS   the status to answer login with (default 429)
 *   STUB_LOGIN_BODY     JSON body to answer with (default depends on the status)
 */
import { createServer } from 'node:http';

const status = Number(process.env.STUB_LOGIN_STATUS ?? '429');
const defaultBody =
    status === 200
        ? // A 200 that carries NO accessToken — the "gateway is up but unhealthy" shape.
          { success: true, data: { user: { id: 'stub-user', role: 'SYSTEM_ADMIN' } } }
        : { success: false, error: { code: status === 429 ? 'RATE_LIMITED' : 'LOGIN_FAILED', message: `stub ${String(status)}` } };
const body = process.env.STUB_LOGIN_BODY ?? JSON.stringify(defaultBody);

const server = createServer((req, res) => {
    if (req.method === 'POST' && req.url === '/api/auth/login') {
        // Drain the request body so the client does not see a reset.
        req.on('data', () => {});
        req.on('end', () => {
            res.writeHead(status, { 'Content-Type': 'application/json' });
            res.end(body);
        });
        return;
    }
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end('{"error":"stub: not found"}');
});

server.listen(0, '127.0.0.1', () => {
    const address = server.address();
    const port = typeof address === 'object' && address !== null ? address.port : 0;
    process.stdout.write(`PORT=${String(port)}\n`);
});
