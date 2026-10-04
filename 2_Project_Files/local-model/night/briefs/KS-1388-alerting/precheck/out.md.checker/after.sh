# =============================================================================
# Secuura Observability — alert routing configuration (EXAMPLE)
# =============================================================================
#
# Copy this file to `alerting.env` (gitignored) and fill in your values:
#   cp observability/config/alerting.env.example observability/config/alerting.env
#
# This single file is the canonical reference for every alert-routing knob.
# Enabling a channel is a one-line change here plus a stack restart — no Grafana
# UI interaction and no provisioning-file edits.
#
# The start command (`cd observability && npm run start`, i.e. scripts/observability.sh)
# passes `--env-file observability/config/alerting.env` automatically when the file
# exists. A bare `docker compose -f observability/docker-compose.yml up -d` uses the
# built-in compose defaults below — i.e. both channels disabled, stack silent.
#
# ── Email alerts (disabled by default) ─────────────────────────────────────
# Set to true to enable Grafana's SMTP mailer. When false the email contact
# point is still provisioned but Grafana sends nothing.
GRAFANA_EMAIL_ENABLED=false

# Recipient address for all alert notifications.
# To send to multiple addresses, use a comma-separated list.
GRAFANA_EMAIL_TO=alerts@example.com

# SMTP server settings — fill these in for your mail provider.
GRAFANA_SMTP_HOST=smtp.example.com
GRAFANA_SMTP_PORT=587
GRAFANA_SMTP_USER=
GRAFANA_SMTP_PASSWORD=
GRAFANA_SMTP_FROM=grafana-alerts@example.com

# ── Slack alerts (disabled by default) ─────────────────────────────────────
# Set to true and supply a webhook URL to enable Slack notifications.
GRAFANA_SLACK_ENABLED=false

# Incoming webhook URL from your Slack app configuration.
# Leave blank to keep Slack disabled even if GRAFANA_SLACK_ENABLED=true — when
# blank, the stack substitutes an inert placeholder so Grafana still boots, and
# nothing is delivered to a real channel. Set a real webhook URL to enable Slack.
GRAFANA_SLACK_WEBHOOK_URL=

# Channel to post alerts into (include the # prefix).
GRAFANA_SLACK_CHANNEL=#platform-alerts

# Optional: Slack bot username shown on alert messages.
GRAFANA_SLACK_USERNAME=Secuura Observability

# ── Exporter data sources (optional overrides) ─────────────────────────────
# The infrastructure exporters default to local-dev credentials. Override here
# when pointing the stack at a dev/demo database, Redis, gateway, or Kafka.
# SECUURA_PG_DSN=postgresql://secuura:secuura_dev_password@secuura-postgres:5432/secuura?sslmode=disable
# SECUURA_REDIS_ADDR=redis://secuura-redis:6379
# SECUURA_REDIS_PASSWORD=secuura_redis_dev
# SECUURA_NGINX_STATUS_URI=http://secuura-nginx-gateway:80/stub_status
# SECUURA_KAFKA_BROKER=secuura-kafka:9092
