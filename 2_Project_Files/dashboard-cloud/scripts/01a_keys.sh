#!/usr/bin/env bash
# Step 1a — key material. PRIVATE keys -> 4_Credentials/dashboard-cloud (600). PUBLIC halves -> app/keys (tracked).
set -eu
CRED=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud
PUB=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/app/keys
mkdir -p "$PUB"; chmod 700 "$CRED"
umask 077
# Kam's pilot envelope keypair (RSA-OAEP, 4096, SHA-256 in WebCrypto) — private half NEVER leaves 4_Credentials.
if [ ! -f "$CRED/kam-pilot-private.pem" ]; then
  openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out "$CRED/kam-pilot-private.pem"
  echo "generated kam-pilot-private.pem"
fi
openssl pkey -in "$CRED/kam-pilot-private.pem" -pubout -out "$PUB/kam-pilot-public.pub"
chmod 644 "$PUB/kam-pilot-public.pub"
# Seat certificates (self-signed, 12 months) — one per seat; private key stays in 4_Credentials.
for seat in wednesday-seat tuesday-seat; do
  if [ ! -f "$CRED/$seat.pem" ]; then
    openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes \
      -keyout "$CRED/$seat.pem" -out "$CRED/$seat.crt" \
      -subj "/CN=$seat.wednesday-dashboard.pilot/O=Wednesday pilot" 2>&1 | grep -v '^\.\+$' || true
    echo "generated $seat.pem (private) + $seat.crt (public cert)"
  fi
  chmod 644 "$CRED/$seat.crt"
  # thumbprint (SHA-1 hex, what MSAL/Entra call it)
  openssl x509 -in "$CRED/$seat.crt" -noout -fingerprint -sha1 | sed 's/://g' | sed "s/^.*=/$seat thumbprint=/"
  openssl x509 -in "$CRED/$seat.crt" -noout -enddate | sed "s/^/$seat /"
done
ls -la "$CRED" "$PUB"
