# =============================================================================
# SECUURA GOVERNANCE SERVICE DOCKERFILE
# =============================================================================
# DAO governance and voting
# Port: 4017
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

COPY --from=shared-builder /shared /shared

# Copy package files from service directory
COPY services/governance/package*.json ./

# Install dependencies (including dev for build)
RUN npm ci --ignore-scripts
RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared

# Copy source files (exclude tests)
COPY services/governance/src/ ./src/
COPY services/governance/tsconfig.json ./

# G7 fix 2026-04-27: previously `RUN npm run build` was tail-glued onto
# the comment with no newline so the build never ran and /app/dist was
# never produced. Putting it on its own line.
RUN npm run build

# KS-490: drop the dev tree before the runtime stage copies it.
# `npm ci` above installs devDependencies because the build needs them; the
# production stage then COPYs node_modules wholesale, so every dev dependency
# shipped into a running container. Pruning here — after the build, before the
# copy — is the smallest change: the runtime stage is untouched.
#
# Measured safe before doing it: no file under src/ outside __tests__ imports
# any devDependency in this service (a walk of every import/require in the
# runtime sources against the declared devDependencies).
#
# `@secuura/shared` is a symlink this Dockerfile creates by hand and does not
# declare, so prune removes it — the production stage re-creates it after the
# copy, which is why that is not a problem here.
RUN npm prune --omit=dev

# =============================================================================
# PRODUCTION IMAGE
# =============================================================================
FROM ${REGISTRY_PREFIX}node:24-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=4017

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 secuura

# Copy built files
COPY --from=builder --chown=secuura:nodejs /app/dist ./dist
COPY --from=builder --chown=secuura:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=secuura:nodejs /app/package.json ./package.json
COPY --from=shared-builder /shared /shared
RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared

# SMB-perms fix: host source ships in 700 root; without world-read on /app+/shared
# the runtime non-root user crashes with EACCES (audit follow-up to Dockerfile-perms
# class bug, fixed in api-gateway 2026-04-25 commit).
RUN chmod -R a+rX /app /shared

USER secuura

EXPOSE 4017

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:4017/health || exit 1

CMD ["node", "dist/index.js"]
