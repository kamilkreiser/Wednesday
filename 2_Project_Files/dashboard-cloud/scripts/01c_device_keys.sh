#!/usr/bin/env bash
# Phase 3 (Kam 12:50:55: "please generate a new key for my laptop and one for my iPad") — device keypairs, 01a's pattern.
# PRIVATE halves -> 4_Credentials/dashboard-cloud/kam-<device>-private.pem (600). PUBLIC halves -> app/keys/kam-<device>-public.pub
# (tracked; the seats and the browser wrap every record's data key to EVERY kam-*-public.pub in that folder = Kam's key ring).
# Also exports the two seat certificates' PUBLIC keys (SPKI PEM) into app/keys/<seat>-seat-public.pub so the browser can wrap
# Kam's replies to the addressed seat (D-2(b)). Idempotent: an existing private key is never regenerated or overwritten.
set -eu
CRED=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud
PUB=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/app/keys
mkdir -p "$PUB"; chmod 700 "$CRED"
umask 077
for dev in laptop ipad; do
  if [ ! -f "$CRED/kam-$dev-private.pem" ]; then
    openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out "$CRED/kam-$dev-private.pem" 2>/dev/null
    echo "generated kam-$dev-private.pem (RSA-4096, PKCS8)"
  else echo "kam-$dev-private.pem already exists — kept"; fi
  chmod 600 "$CRED/kam-$dev-private.pem"
  openssl pkey -in "$CRED/kam-$dev-private.pem" -pubout -out "$PUB/kam-$dev-public.pub"
  chmod 644 "$PUB/kam-$dev-public.pub"
done
for seat in wednesday-seat tuesday-seat; do
  openssl x509 -in "$CRED/$seat.crt" -pubkey -noout > "$PUB/$seat-public.pub"
  chmod 644 "$PUB/$seat-public.pub"
done
# kids (sha256(SPKI DER)[:16]) — the same function as seat/envelope.py kid_of / common.js
for f in "$PUB"/kam-*-public.pub "$PUB"/*-seat-public.pub; do
  kid=$(openssl pkey -pubin -in "$f" -outform DER 2>/dev/null | openssl dgst -sha256 | sed 's/^.*= //' | cut -c1-16)
  printf '%-28s kid=%s  %s\n' "$(basename "$f")" "$kid" "$(openssl pkey -pubin -in "$f" -text -noout | /usr/bin/grep -o 'Public-Key: ([0-9]* bit)')"
done
ls -la "$CRED" "$PUB"
