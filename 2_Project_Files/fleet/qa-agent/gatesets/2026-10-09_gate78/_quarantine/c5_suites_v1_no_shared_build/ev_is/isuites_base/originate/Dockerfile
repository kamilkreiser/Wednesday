# =============================================================================
# SECUURA ORIGINATE SERVICE - DOCKERFILE
# =============================================================================
# Multi-stage build for production-ready container
# Build context: project root (.)
# =============================================================================

# Stage 0: Build shared package
# KS-102: base registry prefix — empty = Docker Hub (local); deploy.sh passes the ACR prefix for cloud builds (dodges the Docker Hub anonymous pull-rate limit).
ARG REGISTRY_PREFIX=
FROM ${REGISTRY_PREFIX}node:24-alpine AS shared-builder
WORKDIR /shared
COPY packages/shared/package*.json ./
RUN npm ci --ignore-scripts
COPY packages/shared/ ./
RUN npm run build

# Stage 1: Builder
FROM ${REGISTRY_PREFIX}node:24-alpine AS builder
WORKDIR /app

# Install dependencies needed for native modules and Prisma
RUN apk add --no-cache python3 make g++ openssl openssl-dev

COPY --from=shared-builder /shared /shared

# Copy package files for originate service
COPY services/originate/package*.json ./

RUN npm ci --ignore-scripts

RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared

# Copy Prisma schema from project root
COPY prisma/ ./prisma/

# Generate Prisma client
RUN npx prisma generate

# Copy originate source code
COPY services/originate/ ./

# Build TypeScript
RUN npm run build

# Copy migration scripts + SQL into the builder stage so they ride into runner
COPY scripts/run-migrations.sh ./scripts/run-migrations.sh
COPY migrations/ ./migrations/

# Stage 2: Production
FROM ${REGISTRY_PREFIX}node:24-alpine AS runner
WORKDIR /app

# Install OpenSSL for Prisma runtime
RUN apk add --no-cache openssl

# Security: Run as non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 secuura

# Copy necessary files
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json /app/package-lock.json ./
# Migration scripts (used by the docker-compose `migrations` service which
# runs from this image as a one-shot init job).
COPY --from=builder /app/scripts ./scripts
COPY --from=builder /app/migrations ./migrations
# Versioned pin (KS-420 #1): the bare postgresql-client meta-package resolves to
# whatever Alpine's current default is (v18 on 3.24) against our postgres:15
# server. Alpine 3.24 no longer packages the 15 client, so pin the closest
# supported line — v16 client tools fully support a v15 server.
RUN apk add --no-cache postgresql16-client

# Set ownership
RUN chown -R secuura:nodejs /app

# Install production dependencies only
RUN npm ci --ignore-scripts --omit=dev

# KS-384 regression fix: this final `npm ci --ignore-scripts` reinstalls node_modules
# from scratch and, with --ignore-scripts, skips Prisma's postinstall — so it drops the
# client generated in the builder (`npx prisma generate`, builder stage). Restore that
# generated client, or the runtime throws `Cannot find module '.prisma/client/default'`
# on every DB access. (A clean/no-cache build exposes this; layer caching can hide it.)
COPY --from=builder /app/node_modules/.prisma ./node_modules/.prisma

COPY --from=shared-builder /shared /shared
RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared

# SMB-perms fix: host source ships in 700 root; without world-read on /app+/shared
# the runtime non-root user crashes with EACCES (audit follow-up to Dockerfile-perms
# class bug, fixed in api-gateway 2026-04-25 commit).
RUN chmod -R a+rX /app /shared

USER secuura

# Environment
ENV NODE_ENV=production
ENV PORT=4000

EXPOSE 4000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:4000/health || exit 1

CMD ["node", "dist/index.js"]
