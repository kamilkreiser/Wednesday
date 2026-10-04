#!/bin/bash
# probe_pki_gateD2.sh — builds the gateD2 forgery probe's TEST PKI with the OpenSSL CLI, INDEPENDENT of pkijs / asn1js (the product's
# parser) and of the PR's own ks1404-pki.ts. Test keys only: they live in <outdir> under /private/tmp/claude-501/ and are never committed.
#   rootA  trusted RSA root (the probe passes it as the anchor)       rootB  an UNTRUSTED RSA root (PF1)
#   interA RSA intermediate CA under rootA (PF5)                      tsaA   RSA TSA cert under rootA, EKU timeStamping critical (G0, PF2..)
#   tsaB   the same profile under rootB (PF1)                        tsaI   TSA cert under interA (PF5)
#   tsaNoEku  under rootA with EKU serverAuth only (PF9)             tsaE   ECDSA P-256 TSA cert under rootA (PF12)
#   data.bin + data.sha256 (the hashed document), and two tokens made by OpenSSL ITSELF (`openssl ts -reply -token_out`):
#   openssl_token_rsa.der (signer tsaA) and openssl_token_ec.der (signer tsaE) — PF11 / PF12, a third encoder beside pkijs and the probe's.
# Usage: probe_pki_gateD2.sh <outdir>   (outdir must lie under /private/tmp/claude-501/; checked LEXICALLY before any mkdir)
# Exit 0 every artefact made (each command's rc on its own line in <outdir>/pki.log); 1 a step failed; 2 usage / refusal.
set -u
OUT="${1:-}"
[ -n "$OUT" ] || { sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
[ "$OUT" = "--help" ] && { sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0; }
L="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$OUT")"
case "$L" in /private/tmp/claude-501/*) ;; *) echo "REFUSING: $L is not under /private/tmp/claude-501/ (nothing was created)"; exit 2;; esac
mkdir -p "$L" || exit 2; OUT="$L"; LOG="$OUT/pki.log"; : > "$LOG"
O=/opt/homebrew/bin/openssl; [ -x "$O" ] || O="$(command -v openssl)"
echo "probe_pki_gateD2 $(date -u +%Y-%m-%dT%H:%M:%SZ) | $($O version) | outdir $OUT" | tee -a "$LOG"
BAD=0
s() { _n="$1"; shift; "$@" > "$OUT/$_n.out" 2> "$OUT/$_n.err"; _rc=$?; echo "$_n rc=$_rc" >> "$LOG"; [ $_rc -eq 0 ] || { BAD=1; echo "  STEP $_n FAILED rc $_rc: $(head -c 300 "$OUT/$_n.err")"; }; }
cat > "$OUT/ext.cnf" <<'EOF'
[ca]
basicConstraints=critical,CA:TRUE
keyUsage=critical,keyCertSign,cRLSign
subjectKeyIdentifier=hash
[tsa]
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,nonRepudiation
extendedKeyUsage=critical,timeStamping
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid
[noeku]
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature
extendedKeyUsage=serverAuth
EOF
for R in rootA rootB; do
  s "key_$R" $O genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out "$OUT/$R.key"
  s "crt_$R" $O req -x509 -new -key "$OUT/$R.key" -subj "/CN=gateD2 probe $R/O=gateD2 QA" -days 3650 -sha256 -extensions ca -config "$OUT/ext.cnf" -out "$OUT/$R.pem"
done
s key_interA $O genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out "$OUT/interA.key"
s csr_interA $O req -new -key "$OUT/interA.key" -subj "/CN=gateD2 probe interA/O=gateD2 QA" -out "$OUT/interA.csr"
s crt_interA $O x509 -req -in "$OUT/interA.csr" -CA "$OUT/rootA.pem" -CAkey "$OUT/rootA.key" -set_serial 0x1001 -days 3650 -sha256 -extfile "$OUT/ext.cnf" -extensions ca -out "$OUT/interA.pem"
mk() {  # mk <name> <issuer> <ext> <alg>
  if [ "$4" = ec ]; then s "key_$1" $O genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out "$OUT/$1.key"; else s "key_$1" $O genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out "$OUT/$1.key"; fi
  s "csr_$1" $O req -new -key "$OUT/$1.key" -subj "/CN=gateD2 probe $1/O=gateD2 QA" -out "$OUT/$1.csr"
  s "crt_$1" $O x509 -req -in "$OUT/$1.csr" -CA "$OUT/$2.pem" -CAkey "$OUT/$2.key" -set_serial "0x$(printf '%x' $((RANDOM + 4096)))" -days 825 -sha256 -extfile "$OUT/ext.cnf" -extensions "$3" -out "$OUT/$1.pem"
}
mk tsaA rootA tsa rsa; mk tsaB rootB tsa rsa; mk tsaI interA tsa rsa; mk tsaNoEku rootA noeku rsa; mk tsaE rootA tsa ec
for c in rootA rootB interA tsaA tsaB tsaI tsaNoEku tsaE; do s "der_$c" $O x509 -in "$OUT/$c.pem" -outform DER -out "$OUT/$c.der"; done
printf 'gateD2 probe document %s\n' "$(date -u +%s)" > "$OUT/data.bin"
s sha_data $O dgst -sha256 -r "$OUT/data.bin"; cut -d' ' -f1 "$OUT/sha_data.out" > "$OUT/data.sha256"
cat > "$OUT/ts.cnf" <<EOF
[tsa]
default_tsa = tsa_config1
[tsa_config1]
dir = $OUT
serial = $OUT/tsaserial
crypto_device = builtin
signer_digest = sha256
default_policy = 1.2.3.4.1
other_policies = 1.2.3.4.5
digests = sha256, sha384, sha512
accuracy = secs:1
ordering = no
tsa_name = no
ess_cert_id_chain = no
ess_cert_id_alg = sha256
EOF
echo 01 > "$OUT/tsaserial"
s tsq $O ts -query -data "$OUT/data.bin" -sha256 -cert -no_nonce -out "$OUT/data.tsq"
s tok_rsa $O ts -reply -config "$OUT/ts.cnf" -queryfile "$OUT/data.tsq" -signer "$OUT/tsaA.pem" -inkey "$OUT/tsaA.key" -token_out -out "$OUT/openssl_token_rsa.der"
s tok_ec $O ts -reply -config "$OUT/ts.cnf" -queryfile "$OUT/data.tsq" -signer "$OUT/tsaE.pem" -inkey "$OUT/tsaE.key" -token_out -out "$OUT/openssl_token_ec.der"
s vfy_rsa $O ts -verify -in "$OUT/openssl_token_rsa.der" -token_in -data "$OUT/data.bin" -CAfile "$OUT/rootA.pem" -untrusted "$OUT/tsaA.pem"
s vfy_ec $O ts -verify -in "$OUT/openssl_token_ec.der" -token_in -data "$OUT/data.bin" -CAfile "$OUT/rootA.pem" -untrusted "$OUT/tsaE.pem"
s asn1_rsa $O asn1parse -inform DER -in "$OUT/openssl_token_rsa.der"
echo "  OpenSSL's own verify of its tokens (the control that the tokens are GENUINE): rsa '$(cat "$OUT/vfy_rsa.out" | tr -d '\n')' ec '$(cat "$OUT/vfy_ec.out" | tr -d '\n')'" | tee -a "$LOG"
echo "  SignerInfo signatureAlgorithm OpenSSL wrote (rsa token): $(grep -E 'rsaEncryption|sha256WithRSAEncryption' "$OUT/asn1_rsa.out" | tail -1 | sed 's/.*OBJECT *://')" | tee -a "$LOG"
ls "$OUT" > "$OUT/manifest.txt"
echo "PKI $([ $BAD -eq 0 ] && echo OK || echo FAILED) | $(wc -l < "$OUT/manifest.txt" | tr -d ' ') files in $OUT" | tee -a "$LOG"
exit $BAD
