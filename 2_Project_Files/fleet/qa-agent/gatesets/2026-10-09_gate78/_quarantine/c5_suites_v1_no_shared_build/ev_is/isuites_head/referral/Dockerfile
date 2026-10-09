# =============================================================================
# SECUURA REFERRAL SERVICE DOCKERFILE
# =============================================================================
# Referral program management
# Port: 4016
# =============================================================================

# KS-102: base registry prefix — empty = Docker Hub (local); deploy.sh passes the ACR prefix for cloud builds (dodges the Docker Hub anonymous pull-rate limit).
ARG REGISTRY_PREFIX=
FROM ${REGISTRY_PREFIX}node:24-alpine AS base

# Copy and build shared package first
FROM base AS shared-builder
WORKDIR /shared
# Install build tools for native dependencies (blake2)
RUN apk add --no-cache python3 make g++
COPY packages/shared/package*.json ./
RUN npm ci --ignore-scripts
COPY packages/shared/ ./
RUN npm run build

# Builder stage
FROM base AS builder
WORKDIR /app

# Install build tools for native dependencies
RUN apk add --no-cache python3 make g++

# Copy shared package
COPY --from=shared-builder /shared /shared

# Copy package files from service directory
COPY services/referral/package*.json ./

# G7: explicit symlink instead of file:/shared rewrite (the file: spec
# didn't make @secuura/shared TS-resolvable in this Dockerfile setup;
# matches the originate/auth pattern that works).
RUN sed -i '/"@secuura\/shared":/d' package.json
RUN npm ci --ignore-scripts
RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared

# Copy source files
COPY services/referral/ ./

# Build TypeScript
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
FROM base AS runner
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
ENV PORT=4016

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 secuura

# Copy built files
COPY --from=builder --chown=secuura:nodejs /app/dist ./dist
COPY --from=builder --chown=secuura:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=secuura:nodejs /app/package.json ./package.json
COPY --from=shared-builder --chown=secuura:nodejs /shared /shared

# KS-490 (2) FIX: re-create the `@secuura/shared` symlink in the runtime stage.
# The builder's `npm prune --omit=dev` above removes it — it is a hand-made,
# undeclared symlink, so prune treats it as extraneous — and the COPY of
# node_modules therefore carries no `@secuura/shared`. governance's runtime
# stage already re-linked; these three did not, so the pruned image started
# with `Cannot find module '@secuura/shared'`. Measured, not reasoned: at
# d602a1536 the nft-certificate runtime image had an EMPTY node_modules/@secuura
# and crashed on start, against a governance control in the same build that
# printed `shared ok`. Placed before `chmod -R a+rX` so the link is covered,
# and before `USER secuura`, exactly as governance does.
RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared

# SMB-perms fix: host source ships in 700 root; without world-read on /app+/shared
# the runtime non-root user crashes with EACCES (audit follow-up to Dockerfile-perms
# class bug, fixed in api-gateway 2026-04-25 commit).
RUN chmod -R a+rX /app /shared

USER secuura

EXPOSE 4016

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:4016/health || exit 1

CMD ["node", "dist/index.js"]
