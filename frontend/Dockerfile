# ============================================
# Base Stage - Common setup
# ============================================
FROM node:20-alpine AS base

# Install security updates and required packages
RUN apk update && apk upgrade && \
    apk add --no-cache libc6-compat curl && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# ============================================
# Dependencies Stage - Install node_modules
# ============================================
FROM base AS deps

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies (use ci if lockfile exists, otherwise install)
RUN if [ -f package-lock.json ]; then \
        npm ci --omit=dev --ignore-scripts; \
    else \
        npm install --production --ignore-scripts; \
    fi && \
    npm cache clean --force

# Install all dependencies (including dev) for builder stage
RUN if [ -f package-lock.json ]; then \
        npm ci --ignore-scripts; \
    else \
        npm install --ignore-scripts; \
    fi && \
    npm cache clean --force

# ============================================
# Development Stage - For local development
# ============================================
FROM base AS development

# Copy all dependencies
COPY --from=deps /app/node_modules ./node_modules

# Copy application code (will be overridden by volume mounts)
COPY . .

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs && \
    chown -R nextjs:nodejs /app

USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

ENV PORT=3000 \
    HOSTNAME="0.0.0.0" \
    NODE_ENV=development

# Run development server
CMD ["npm", "run", "dev"]

# ============================================
# Builder Stage - Build Next.js application
# ============================================
FROM base AS builder

# Copy dependencies
COPY --from=deps /app/node_modules ./node_modules

# Copy application code
COPY . .

# Accept build arguments
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# Build application
RUN npm run build

# ============================================
# Production Stage - Optimized for production
# ============================================
FROM base AS production

ENV NODE_ENV=production \
    PORT=3000 \
    HOSTNAME="0.0.0.0"

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy only necessary files
COPY --from=builder /app/public ./public

# Copy standalone build
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Run production server
CMD ["node", "server.js"]
