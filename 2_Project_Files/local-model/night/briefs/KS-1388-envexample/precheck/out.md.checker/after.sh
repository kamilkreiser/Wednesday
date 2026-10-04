# =============================================================================
# Secuura Observability — stack environment (EXAMPLE)
# =============================================================================
#
# Copy to `observability/.env` (gitignored) and override anything you need:
#   cp observability/.env.example observability/.env
#
# Resolution precedence (highest wins):
#   1. Azure — values exported into the shell from Key Vault before bring-up
#      (e.g. by a sync-secrets step). Docker Compose interpolation always lets a
#      shell env var override the .env file, so Azure wins automatically.
#   2. observability/.env — this file's local copy.
#   3. The built-in defaults baked into docker-compose.yml.
#
# Both the Grafana SERVER (GF_SECURITY_ADMIN_*) and the test-framework CLIENTS
# that push annotations (Akto, k6) read the SAME variables below, so rotating the
# password in one place keeps the dashboards reachable everywhere.
#
# The start scripts load this file with `--env-file` automatically when present.
# Alert routing (email/Slack) lives separately in config/alerting.env.

# ── Grafana access (URL + admin credentials) ───────────────────────────────
# Base URL of the Grafana instance the stack serves and clients annotate.
GRAFANA_URL=http://localhost:3000

# Admin user + password. Set GRAFANA_ADMIN_PASSWORD from Azure Key Vault in the
# cloud; this local value is only a development fallback.
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=secuura_perf

# ── Optional: Prometheus Pushgateway (run-completion metrics) ───────────────
# Host URL test frameworks push summary metrics to. Default matches the stack.
# PUSHGATEWAY_URL=http://localhost:9099

# ── Optional: Grafana PostgreSQL datasource (direct-SQL business panels) ────
# Grafana connects to the platform DB over the shared secuura_default network.
# Defaults match the local platform; override to point at a dev/demo database.
# POSTGRES_DB=secuura
# POSTGRES_USER=secuura
# POSTGRES_PASSWORD=secuura_dev_password

# ── Optional: infrastructure exporter data sources ─────────────────────────
# Override when pointing the stack at a dev/demo database, Redis, gateway, or Kafka.
# SECUURA_PG_DSN=postgresql://secuura:secuura_dev_password@secuura-postgres:5432/secuura?sslmode=disable
# SECUURA_REDIS_ADDR=redis://secuura-redis:6379
# SECUURA_REDIS_PASSWORD=secuura_redis_dev
# SECUURA_NGINX_STATUS_URI=http://secuura-nginx-gateway:80/stub_status
# SECUURA_KAFKA_BROKER=secuura-kafka:9092
