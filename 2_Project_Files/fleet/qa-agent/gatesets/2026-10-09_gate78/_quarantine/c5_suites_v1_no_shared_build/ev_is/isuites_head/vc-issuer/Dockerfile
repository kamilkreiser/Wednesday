# =============================================================================
# SECUURA VC ISSUER SERVICE DOCKERFILE
# =============================================================================
# Build from project root: docker build -f services/vc-issuer/Dockerfile .

# KS-102: base registry prefix — empty = Docker Hub (local); deploy.sh passes the ACR prefix for cloud builds (dodges the Docker Hub anonymous pull-rate limit).
ARG REGISTRY_PREFIX=
FROM ${REGISTRY_PREFIX}node:24-alpine AS base

# Install build dependencies for native modules
RUN apk add --no-cache python3 make g++

# Build shared package first
FROM base AS shared-builder
WORKDIR /shared

# Copy and build shared package
COPY packages/shared/package*.json ./
RUN npm ci --ignore-scripts

COPY packages/shared/ ./
# Relax strict unused-variable checks for production build (the shared
# package has multiple TS6133s flagged for cleanup; same workaround as
# api-gateway/Dockerfile uses).
# G7 fix 2026-04-27: previously `RUN npm run build` was tail-glued onto
# the comment above (no newline) so the build never ran and /shared/dist
# was empty. Putting it on its own line.
RUN npm run build

# Build service
FROM base AS builder
WORKDIR /app

# Copy built shared package
COPY --from=shared-builder /shared /shared

# Copy service package files
COPY services/vc-issuer/package*.json ./

# KS-647: the KS-384 exception recorded here is resolved. This service used to
# declare '@secuura/shared: *' and strip it back out with `sed` before
# installing — the declaration 404'd against the public registry, and the strip
# is what made `npm ci` impossible. It no longer declares it, matching the 22
# other services, which never did. This service also had NO standalone lockfile
# at all (the only one of 28) — it has one now, so it is finally covered by the
# KS-531 standalone-lock audit gate.
# G7: explicit symlink (file:/shared doesn't make @secuura/shared
# TS-resolvable; matches the originate/auth pattern that works).
RUN npm ci --ignore-scripts
RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared

# Copy service source
COPY services/vc-issuer/ ./

# Relax strict unused-variable checks for production build (same workaround
# as api-gateway/Dockerfile + the shared-builder stage above).
# Build service
RUN npm run build

# Production stage - use slim image
FROM ${REGISTRY_PREFIX}node:24-alpine AS runner
WORKDIR /app

# KS-490: no build toolchain in the runtime image.
# This stage COPIES the finished node_modules from the builder, so a compiler
# here compiled nothing. It was copied from the auth Dockerfile — and auth does
# not need it either (see that file). Measured: `argon2`, the estate's only
# native dependency, appears in 1 of 25 service package.json files, and it ships
# PREBUILT binaries (`node_modules/argon2/prebuilds/linux-*/*.node`), so nothing
# is ever compiled at image-build time. What the line did add was a working C
# toolchain inside a running production container.

ENV NODE_ENV=production
ENV PORT=4014

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 secuura

# Copy built shared package
COPY --from=shared-builder --chown=secuura:nodejs /shared /shared

# Copy package.json and install production deps. G7: same pattern as the
# builder stage — npm ci + symlink (KS-647).
COPY services/vc-issuer/package*.json ./
RUN npm ci --ignore-scripts --omit=dev
RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared

# Copy built files
COPY --from=builder --chown=secuura:nodejs /app/dist ./dist

# SMB-perms fix: host source ships in 700 root; without world-read on /app+/shared
# the runtime non-root user crashes with EACCES (audit follow-up to Dockerfile-perms
# class bug, fixed in api-gateway 2026-04-25 commit).
RUN chmod -R a+rX /app /shared

USER secuura

EXPOSE 4014

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:4014/health || exit 1

CMD ["node", "dist/index.js"]
