# =============================================================================
# DEMO-SERVICE DOCKERFILE
# =============================================================================
# Multi-stage build. Build context: project root (.)
# Pattern matches services/originate/Dockerfile so the @secuura/shared
# workspace package resolves the same way everywhere.
# =============================================================================

# Stage 0: Build shared package
FROM node:24-alpine AS shared-builder
WORKDIR /shared
COPY packages/shared/package*.json ./
RUN npm ci --ignore-scripts
COPY packages/shared/ ./
RUN npm run build

# Stage 1: Builder
FROM node:24-alpine AS builder
WORKDIR /app

COPY --from=shared-builder /shared /shared

# Copy demo-service package files and install
COPY services/demo-service/package*.json ./
RUN npm ci --ignore-scripts

# Symlink the built shared package so @secuura/shared imports resolve.
RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared

# Copy demo-service source and build
COPY services/demo-service/ ./
RUN npm run build

# =============================================================================
# Stage 2: Runtime
# =============================================================================
FROM node:24-alpine
WORKDIR /app

COPY --from=shared-builder /shared /shared

# Re-install runtime-only deps + symlink shared
COPY services/demo-service/package*.json ./
RUN npm ci --ignore-scripts --omit=dev \
    && mkdir -p node_modules/@secuura \
    && ln -s /shared node_modules/@secuura/shared

COPY --from=builder /app/dist ./dist

# pg_restore needed for demo reset endpoint (Plan 02-03).
# Versioned pin (KS-420 #1): the bare postgresql-client meta-package resolves to
# whatever Alpine's current default is (v18 on 3.24) against our postgres:15
# server. Alpine 3.24 no longer packages the 15 client, so pin the closest
# supported line — v16 client tools fully support a v15 server.
RUN apk add --no-cache postgresql16-client

RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
# SMB-perms fix: host source ships in 700 root; without world-read on /app+/shared
# the runtime nodejs user crashes with EACCES (audit follow-up to Dockerfile-perms
# class bug, fixed in api-gateway 2026-04-25 commit).
RUN chmod -R a+rX /app /shared

USER nodejs

EXPOSE 4030

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:4030/demo-api/health || exit 1

CMD ["node", "dist/index.js"]
