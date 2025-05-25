# Multi-stage build for Quantum ZKP implementation
# Author: Nick Cloutier
# ORCID: 0009-0008-5289-5324
# Affiliation: Hydra Research & Labs

# Build stage
FROM golang:1.24-alpine AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache git ca-certificates tzdata

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY quantumzkp/ ./quantumzkp/

# Build the application
WORKDIR /app/quantumzkp
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o qzkp .

# Test stage (optional, can be skipped in production builds)
FROM builder AS tester
RUN go test -v ./...

# Production stage
FROM alpine:latest

# Install runtime dependencies
RUN apk --no-cache add ca-certificates tzdata

# Create non-root user for security
RUN addgroup -g 1001 qzkp && \
    adduser -D -s /bin/sh -u 1001 -G qzkp qzkp

# Set working directory
WORKDIR /app

# Copy binary from builder stage
COPY --from=builder /app/quantumzkp/qzkp .

# Copy documentation (optional)
COPY --from=builder /app/quantumzkp/*.md ./docs/

# Change ownership to non-root user
RUN chown -R qzkp:qzkp /app

# Switch to non-root user
USER qzkp

# Expose port (if needed for future web interface)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ./qzkp help || exit 1

# Default command
CMD ["./qzkp", "help"]

# Labels for metadata
LABEL maintainer="Nicolas Cloutier <ncloutier@hydraresearch.io>"
LABEL version="1.0.0"
LABEL description="Secure Quantum Zero-Knowledge Proof Implementation"
LABEL org.opencontainers.image.title="Quantum ZKP"
LABEL org.opencontainers.image.description="Production-ready quantum zero-knowledge proof system with post-quantum security"
LABEL org.opencontainers.image.authors="Nick Cloutier <ncloutier@hydraresearch.io>"
LABEL org.opencontainers.image.vendor="Hydra Research & Labs"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.url="https://github.com/hydraresearch/qzkp"
LABEL org.opencontainers.image.source="https://github.com/hydraresearch/qzkp"
LABEL org.opencontainers.image.documentation="https://github.com/hydraresearch/qzkp/blob/main/README.md"
LABEL org.opencontainers.image.licenses="MIT"
