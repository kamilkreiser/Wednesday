#!/bin/bash
# controls_check.sh — re-grep every §4 positive-control token of the #912 ROUND 2 (tier 1) + #937 STACKED (tier 2) brief
# at the PINNED heads through the GitHub contents API (read-only; GH_TOKEN sourced by NAME from the Secuura .env, never
# printed). Tokens were derived from the PRs' OWN files at 609c44c55 / 323151415 / ae8751f38 / 8861e6216 / 6fd3a8bec —
# never carried from another gate's brief. PRESENT tokens must grep the stated count; ABSENT tokens must grep exactly 0;
# blobs must be the ones stated; the exact lines the brief cites must read as stated; the merge 323151415 must be
# re-derivable in the set's own --shared clone (git's auto-merge CONFLICTS in anchorStateSync.ts only and the hand
# resolution differs from it in that ONE file, 5/12, with `const prior` 2 -> 1); #937's two merges must be mechanical
# unions (tree equalities); the stack compare must read merge_base 609c44c55 / ONE file; the round-1 read (the recovered
# verdict file) must carry its recorded sha256 and the transcription comment 5597511879 its recorded sha256.
# Assembled from model/controls_check.head.sh + lineis_pins.sh (176 exact-line pins derived from `git show` at the pinned
# refs) + model/controls_check.tail.sh. Exit 0 = every control holds · 1 = at least one control failed · 2 = unreadable.
set -u
HEAD="${QA912R2_HEAD:-609c44c55323b5c90320847b6837ca37f6586705}"
MERGE='3231514154aaa8a469e6cdd5f553ee8ce6079b89'
R1='ae8751f380ed361505694ba71ad9bf1308ee0e87'
DEV="${QA912R2_DEVELOP:-8861e62161466c40f08d2b10a30edeb203123993}"
H937="${QA912R2_HEAD937:-6fd3a8bec4e4cc858d38925e00703a37ffcf1b30}"
MDEV937='bda4c74a6deab584df59d9b047f5a1615b2e12a0'
R1_937='cf8b23366f235f37207f7a228a724e9c9cf52fdb'
BASE='e559f7bbace5281668637755410273ff58068c15'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
CLONE='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate912r2/model/clone912'
R1_READ='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/reports/2026-09-09_secuura-ks1004-912-tier1-VERDICT.md'
W="$(mktemp -d "${TMPDIR:-/tmp}/qa912r2ctl.XXXXXX")"
P='Blockchain/Dev/services/originate/src'
ANCHOR="$P/services/anchorStateSync.ts"
KS1004="$P/__tests__/ks1004-anchor-failed-lockout.test.ts"
KS1058="$P/__tests__/ks1058-anchor-failed-preserves-thread-token.test.ts"
KS535="$P/__tests__/ks535-anchor-async-fail-propagates.test.ts"
KS1059="$P/__tests__/ks1059-sim-leg-must-not-resurrect-a-terminal-document.test.ts"
DOCREPO="$P/repositories/documentRepo.ts"
GW='Blockchain/Dev/services/api-gateway/src/routes/verification.ts'
KS1057='Blockchain/Dev/services/api-gateway/src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts'
AUDIT='Blockchain/Dev/scripts/audit/audit-baseline.json'

fetch() { # path ref outfile -> prints blob sha (or UNREADABLE)
  ( set -a; . "$SECUURA_ENV"; set +a
    P="$1" REF="$2" OUT="$3" python3 - <<'PY'
import base64, json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/contents/" + os.environ["P"] + "?ref=" + os.environ["REF"]
try:
    o = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except Exception as e:
    print("UNREADABLE " + type(e).__name__); sys.exit(0)
open(os.environ["OUT"], "wb").write(base64.b64decode(o["content"]))
print(o["sha"])
PY
  )
}
FAILS=0
echo "controls_check.sh — head ${HEAD:0:9}, merge ${MERGE:0:9}, r1 ${R1:0:9}, develop ${DEV:0:9}, head937 ${H937:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
for spec in "anchor:$ANCHOR:$HEAD" "anchor_merge:$ANCHOR:$MERGE" "anchor_r1:$ANCHOR:$R1" "anchor_dev:$ANCHOR:$DEV" "anchor_base:$ANCHOR:$BASE" "anchor_937:$ANCHOR:$H937" \
            "ks1004:$KS1004:$HEAD" "ks1004_merge:$KS1004:$MERGE" "ks1004_r1:$KS1004:$R1" "ks1004_937:$KS1004:$H937" \
            "ks1058:$KS1058:$HEAD" "ks1058_merge:$KS1058:$MERGE" "ks1058_dev:$KS1058:$DEV" "ks1058_937:$KS1058:$H937" \
            "ks535:$KS535:$HEAD" "ks535_merge:$KS535:$MERGE" "ks535_r1:$KS535:$R1" "ks535_dev:$KS535:$DEV" \
            "ks1059:$KS1059:$H937" "ks1059_r1937:$KS1059:$R1_937" \
            "gw:$GW:$HEAD" "gw_dev:$GW:$DEV" "gw_base:$GW:$BASE" "gw_937:$GW:$H937" "ks1057:$KS1057:$HEAD" \
            "docrepo:$DOCREPO:$HEAD" "docrepo_dev:$DOCREPO:$DEV" "docrepo_r1:$DOCREPO:$R1" \
            "audit:$AUDIT:$HEAD" "audit_dev:$AUDIT:$DEV" "audit_r1:$AUDIT:$R1" "audit_937:$AUDIT:$H937"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;; esac
  echo "read $n = ${p##*/} @ ${ref:0:9}: blob ${sha:0:9}, $(wc -c < "$W/$n" | tr -d ' ') bytes, $(wc -l < "$W/$n" | tr -d ' ') lines, sha256 $(shasum -a 256 "$W/$n" | cut -c1-16)"
  echo "${sha:0:9}" > "$W/$n.blob"
done
# the files that must be ABSENT at the refs the brief says
for spec in "ks1004_dev:$KS1004:$DEV" "ks1004_base:$KS1004:$BASE" "ks1058_r1:$KS1058:$R1" "ks1058_base:$KS1058:$BASE" "ks1059_head912:$KS1059:$HEAD" "ks1059_dev:$KS1059:$DEV"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*) echo "ok   $n ABSENT at ${ref:0:9} (${sha})" ;; *) echo "FAIL $n present at ${ref:0:9}: blob ${sha:0:9}"; FAILS=$((FAILS+1)) ;; esac
done
blobis() { [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis anchor d8e988f7a; blobis anchor_merge 174d122ec; blobis anchor_r1 604c21dbb; blobis anchor_dev 846ebe5bf; blobis anchor_base 55454f715; blobis anchor_937 d8e988f7a
blobis ks1004 4684fb3ad; blobis ks1004_merge da63727ca; blobis ks1004_r1 da63727ca; blobis ks1004_937 4684fb3ad
blobis ks1058 1c78b4a61; blobis ks1058_merge 349be4653; blobis ks1058_dev 349be4653; blobis ks1058_937 1c78b4a61
blobis ks535 b1791e94f; blobis ks535_merge b1791e94f; blobis ks535_r1 b1791e94f; blobis ks535_dev ee08e85b3
blobis ks1059 a972cc6f5; blobis ks1059_r1937 a972cc6f5
blobis gw 95c13b01f; blobis gw_dev 95c13b01f; blobis gw_base 489ac1600; blobis gw_937 95c13b01f
blobis docrepo f715095c1; blobis docrepo_dev f715095c1; blobis docrepo_r1 9c49f6ec8
blobis audit 03d1680e3; blobis audit_dev 03d1680e3; blobis audit_r1 33bc6f29a; blobis audit_937 03d1680e3
for pair in "anchor:anchor_937:anchorStateSync.ts at #912 head == at #937 head (the stack carries no product change)" "ks1004:ks1004_937:ks1004 at #912 head == at #937 head" "ks1058:ks1058_937:ks1058 at #912 head == at #937 head" "ks1004_merge:ks1004_r1:ks1004 at the merge == round 1 (untouched by the merge)" "ks535:ks535_r1:ks535 at head == round 1 (Peter-read bytes)" "ks1058_merge:ks1058_dev:ks1058 at the merge == develop (untouched by the merge)" "gw:gw_dev:gateway verification.ts at head == develop (the F1 fix is develop's)" "docrepo:docrepo_dev:documentRepo.ts at head == develop (Peter's item 2 file untouched)" "ks1059:ks1059_r1937:the ks1059 test at 6fd3a8bec == at cf8b23366 (unchanged since round 1)"; do
  a="${pair%%:*}"; rest="${pair#*:}"; b="${rest%%:*}"; msg="${rest#*:}"
  cmp -s "$W/$a" "$W/$b" && echo "ok   $msg" || { echo "FAIL $msg — DIFFER"; FAILS=$((FAILS+1)); }
done
cmp -s "$W/anchor" "$W/anchor_merge" && { echo "FAIL anchorStateSync.ts at head is byte-identical to the merge commit (the fix changed it)"; FAILS=$((FAILS+1)); } || echo "ok   anchorStateSync.ts at head DIFFERS from the merge commit (the fix)"
cmp -s "$W/ks1058" "$W/ks1058_merge" && { echo "FAIL ks1058 at head is byte-identical to the merge commit"; FAILS=$((FAILS+1)); } || echo "ok   ks1058 at head DIFFERS from the merge commit (the re-stated cell)"
cmp -s "$W/ks1004" "$W/ks1004_merge" && { echo "FAIL ks1004 at head is byte-identical to the merge commit"; FAILS=$((FAILS+1)); } || echo "ok   ks1004 at head DIFFERS from the merge commit (the new cell)"
cmp -s "$W/gw" "$W/gw_base" && { echo "FAIL gateway verification.ts at head == the round-1 base (the F1 fix missing?)"; FAILS=$((FAILS+1)); } || echo "ok   gateway verification.ts at head DIFFERS from the round-1 base (KS-1057/1069/1070/1071 under the head)"
for pair in "anchor:34988176c83f68c6" "anchor_merge:7fbe8f20c9bf5fcb" "anchor_r1:3004ee3adcfb6a1b" "anchor_dev:af4b3a69df24d9c0" "anchor_base:ac9daa89276e81d8" "ks1004:2f3b5d72aae1a2d6" "ks1004_merge:a7563fee1dead2a2" "ks1058:9765ab7bf75b422c" "ks1058_dev:914efe1781b9a37e" "ks535:162735972e348956" "ks535_dev:b433bf1f4092b8bc" "ks1059:c6c51a05a34ff2dd" "gw:5c254b10824c8fa6" "gw_base:8f7383ee19e85a47" "docrepo:625dde8cc0367a02" "audit:6409a37c4dbd9ba8" "audit_r1:564c2d5d72dc965e"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(shasum -a 256 "$W/$f" | cut -c1-16)" = "$want" ] && echo "ok   $f sha256 $want" || { echo "FAIL $f sha256 is not $want"; FAILS=$((FAILS+1)); }
done
for pair in "anchor:396" "anchor_merge:393" "anchor_r1:378" "anchor_dev:359" "anchor_base:343" "ks1004:225" "ks1004_merge:204" "ks1058:198" "ks1058_dev:191" "ks535:257" "ks535_dev:241" "ks1059:199" "gw:1417" "gw_base:1226" "docrepo:945" "docrepo_r1:915" "ks1057:369" "audit:254" "audit_r1:204"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -l < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want lines" || { echo "FAIL $f is not $want lines"; FAILS=$((FAILS+1)); }
done
for pair in "anchor:18382" "anchor_merge:18142" "anchor_r1:17029" "anchor_dev:15888" "ks1004:10467" "ks1058:9452" "ks535:11918" "ks1059:8461" "gw:65726"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -c < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want bytes" || { echo "FAIL $f is not $want bytes"; FAILS=$((FAILS+1)); }
done
lineis() { # file line expected-text
  local got; got="$(sed -n "${2}p" "$W/$1")"
  [ "$got" = "$3" ] && echo "ok   $1:$2 = $3" || { echo "FAIL $1:$2 is: $got"; FAILS=$((FAILS+1)); }
}
lineis anchor 124 " * No-ops when the anchor is already \`confirmed\` — never downgrade a recorded"
lineis anchor 142 " * KS-1058: the write REPLACES the blockchain blob (updateDocument spreads"
lineis anchor 146 "export async function markDocumentAnchorFailed("
lineis anchor 152 "  const doc = await getDocument(documentId, tenantId);"
lineis anchor 153 "  if (!doc) return;"
lineis anchor 154 "  if (doc.blockchain?.status === 'confirmed') return;"
lineis anchor 155 "  const prior = doc.blockchain as (typeof doc.blockchain & { threadToken?: unknown }) | undefined;"
lineis anchor 156 "  const revertStatus: DocumentRecord['status'] = doc.signatures?.length ? 'signed' : 'draft';"
lineis anchor 157 "  await updateDocument(documentId, tenantId, {"
lineis anchor 160 "      status: 'anchor_failed',"
lineis anchor 164 "      txHash: prior?.txHash ?? null,"
lineis anchor 165 "      blockHeight: prior?.blockHeight ?? 0,"
lineis anchor 166 "      ...(prior?.network ? { network: prior.network } : {}),"
lineis anchor 170 "      ...(prior?.txHash && prior?.anchoredAt ? { anchoredAt: prior.anchoredAt } : {}),"
lineis anchor 171 "      ...(anchorId ? { anchorId } : {}),"
lineis anchor 182 "      ...(prior?.threadToken ? { threadToken: prior.threadToken } : {}),"
lineis anchor 183 "      error: errorMessage || 'anchor failed on chain',"
lineis anchor 184 "      failedAt: new Date().toISOString(),"
lineis anchor 186 "  }, undefined, { preserveTerminalStatuses: true });"
lineis anchor 314 "export async function reconcileDocumentAnchorState("
lineis anchor 319 "  const bc = document.blockchain;"
lineis anchor 320 "  if (!bc?.anchorId) return document;"
lineis anchor 321 "  if (bc.simulated) return document;"
lineis anchor 329 "  const inFlight = bc.status !== 'anchor_failed' && bc.status !== 'confirmed';"
lineis anchor 330 "  const failed = bc.status === 'anchor_failed';"
lineis anchor 331 "  if (!inFlight && !failed) return document;"
lineis anchor 342 "  if (confirmed && txHash) {"
lineis anchor 358 "  if (inFlight && anchor.status === 'failed') {"
lineis anchor 359 "    await markDocumentAnchorFailed(document.id, tenantId, bc.anchorId, anchor.errorMessage);"
lineis anchor 377 "  const simFields = simulatedFieldsFromAnchor(anchor);"
lineis anchor 378 "  if (inFlight && !bc.txHash && simFields.simulated) {"
lineis anchor 381 "        txHash: null,"
lineis anchor_merge 150 "  errorMessage?: string | null,"
lineis anchor_merge 151 "): Promise<void> {"
lineis anchor_merge 152 "  const doc = await getDocument(documentId, tenantId);"
lineis anchor_merge 153 "  if (!doc) return;"
lineis anchor_merge 154 "  if (doc.blockchain?.status === 'confirmed') return;"
lineis anchor_merge 163 "      // reproduce the previous values exactly for the no-hash case."
lineis anchor_merge 164 "      txHash: prior?.txHash ?? null,"
lineis anchor_merge 165 "      blockHeight: prior?.blockHeight ?? 0,"
lineis anchor_merge 167 "      ...(prior?.anchoredAt ? { anchoredAt: prior.anchoredAt } : {}),"
lineis anchor_merge 168 "      ...(anchorId ? { anchorId } : {}),"
lineis anchor_merge 179 "      ...(prior?.threadToken ? { threadToken: prior.threadToken } : {}),"
lineis anchor_r1 150 "  if (doc.blockchain?.status === 'confirmed') return;"
lineis anchor_r1 151 "  const prior = doc.blockchain;"
lineis anchor_r1 163 "      ...(prior?.anchoredAt ? { anchoredAt: prior.anchoredAt } : {}),"
lineis anchor_r1 164 "      ...(anchorId ? { anchorId } : {}),"
lineis anchor_dev 140 "  if (doc.blockchain?.txHash || doc.blockchain?.status === 'confirmed') return;"
lineis anchor_dev 142 "  const prior = doc.blockchain as (typeof doc.blockchain & { threadToken?: unknown }) | undefined;"
lineis anchor_dev 147 "      txHash: null,"
lineis anchor_dev 148 "      blockHeight: 0,"
lineis anchor_dev 160 "      ...(prior?.threadToken ? { threadToken: prior.threadToken } : {}),"
lineis anchor_dev 300 "  const inFlight = !bc.txHash && bc.status !== 'anchor_failed' && bc.status !== 'confirmed';"
lineis anchor_dev 341 "  if (inFlight && simFields.simulated) {"
lineis ks1004 54 "    blockchain: { txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1' },"
lineis ks1004 66 "    blockchain: { txHash: REAL_TX, blockHeight: 0, status: 'submitted', anchorId: 'anchor_1' },"
lineis ks1004 89 "  it('REPRO: records the failure on a submitted document carrying a txHash (was: inert)', async () => {"
lineis ks1004 102 "  it('the txHash is CARRIED FORWARD, not nulled — the failed tx keeps its forensic trail', async () => {"
lineis ks1004 114 "    expect(updates.blockchain.txHash).toBe(REAL_TX);"
lineis ks1004 115 "    expect(updates.blockchain.blockHeight).toBe(4242);"
lineis ks1004 116 "    expect(updates.blockchain.network).toBe('preview');"
lineis ks1004 117 "    expect(updates.blockchain.anchoredAt).toBe('2026-02-02T00:00:00.000Z');"
lineis ks1004 120 "  it('CONTROL: a confirmed anchor is still refused — the guard kept its real job', async () => {"
lineis ks1004 125 "    expect(mockUpdateDocument).not.toHaveBeenCalled();"
lineis ks1004 128 "  it('CONTROL: a document with NO txHash still writes null/0, exactly as before', async () => {"
lineis ks1004 136 "  it('CONTRACT: a NO-txHash prior carrying anchoredAt does NOT keep it — an anchor time is retained only alongside a hash', async () => {"
lineis ks1004 151 "    expect('anchoredAt' in updates.blockchain).toBe(false);"
lineis ks1004 153 "    expect(updates.blockchain.status).toBe('anchor_failed');"
lineis ks1004 154 "    expect(updates.blockchain.txHash).toBeNull();"
lineis ks1004 159 "  it('REPRO: a stale submitted-with-hash document whose anchor failed is healed to anchor_failed', async () => {"
lineis ks1004 170 "    expect(updates.blockchain.txHash).toBe(REAL_TX);"
lineis ks1004 182 "  it('REPRO 2: a hashed document could not heal FORWARD either — confirmed now lands', async () => {"
lineis ks1004 192 "    expect(updates.blockchain.status).toBe('confirmed');"
lineis ks1004 197 "  it('CONTROL: an already anchor_failed document is not re-written by the failure branch', async () => {"
lineis ks1004 208 "    expect(mockUpdateDocument).not.toHaveBeenCalled();"
lineis ks1004 211 "  it('CONTROL: the KS-587 simulated-heal leg still requires NO txHash', async () => {"
lineis ks1004 223 "    expect(mockUpdateDocument).not.toHaveBeenCalled();"
lineis ks1058 110 "async function writtenBlobFor(prior: Record<string, unknown>): Promise<Record<string, any>> {"
lineis ks1058 114 "  expect(mockUpdateDocument).toHaveBeenCalledTimes(1);"
lineis ks1058 124 "  it('DEFECT: a prior threadToken survives the anchor_failed write', async () => {"
lineis ks1058 129 "    expect(blob.threadToken).toEqual(THREAD_TOKEN);"
lineis ks1058 136 "  it('CONTRACT: anchoredAt is NOT carried forward — the blob type says it is absent here', async () => {"
lineis ks1058 144 "    expect(blob.anchoredAt).toBeUndefined();"
lineis ks1058 147 "  it('DELIBERATE: confidence is NOT carried forward — it would report a terminal failure as pending', async () => {"
lineis ks1058 157 "    expect(blob.confidence).toBeUndefined();"
lineis ks1058 160 "  it('CONTROL: with no threadToken in the prior blob the written shape is unchanged', async () => {"
lineis ks1058 164 "    expect(Object.keys(blob).sort()).toEqual("
lineis ks1058 165 "      ['anchorId', 'blockHeight', 'error', 'failedAt', 'status', 'txHash'].sort(),"
lineis ks1058 166 "    );"
lineis ks1058 170 "  it('CONTROL (non-zero): the writer still records the failure it is for', async () => {"
lineis ks1058 183 "  it('UNION with KS-1004: a hashed prior IS written — status anchor_failed, txHash and blockHeight carried, threadToken preserved', async () => {"
lineis ks1058 190 "    const blob = await writtenBlobFor({"
lineis ks1058 191 "      txHash: 'd'.repeat(64), blockHeight: 42, status: 'submitted', threadToken: THREAD_TOKEN,"
lineis ks1058 193 "    expect(blob.status).toBe('anchor_failed');"
lineis ks1058 194 "    expect(blob.txHash).toBe('d'.repeat(64));"
lineis ks1058 195 "    expect(blob.blockHeight).toBe(42);"
lineis ks1058 196 "    expect(blob.threadToken).toEqual(THREAD_TOKEN);"
lineis ks535 163 "describe('markDocumentAnchorFailed — never downgrades recorded chain facts', () => {"
lineis ks535 169 "  it('no-ops when the anchor is confirmed — WITHOUT a txHash, so this isolates the confirmed arm', async () => {"
lineis ks535 177 "  it('no-ops on a confirmed anchor even when it also carries a txHash (the original fixture)', async () => {"
lineis ks535 185 "  it('no-ops when the document no longer exists', async () => {"
lineis ks1059 6 " *     if (inFlight && simFields.simulated) {   // anchorStateSync.ts:325 on develop"
lineis ks1059 82 "function terminallyFailedDoc(): DocumentRecord {"
lineis ks1059 95 "      txHash: null,"
lineis ks1059 96 "      blockHeight: 0,"
lineis ks1059 97 "      status: 'anchor_failed',"
lineis ks1059 119 "  it('DEFECT CELL: an anchor_failed document is NOT rewritten to anchored by a simulated anchor', async () => {"
lineis ks1059 133 "    expect(mockUpdateDocument).not.toHaveBeenCalled();"
lineis ks1059 135 "    expect(out.status).toBe('draft');"
lineis ks1059 136 "    expect((out.blockchain as any).status).toBe('anchor_failed');"
lineis ks1059 139 "  it('CONTROL (non-zero): a genuinely in-flight blob with the same simulated anchor IS healed', async () => {"
lineis ks1059 151 "    (doc.blockchain as any).status = 'pending';   // in flight, not terminal"
lineis ks1059 157 "    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);"
lineis ks1059 159 "    expect(updates.status).toBe('anchored');"
lineis ks1059 160 "    expect(updates.blockchain.simulated).toBe(true);"
lineis ks1059 163 "  it('CONTROL: the terminal document is let THROUGH the early returns — it is the sim leg that stops it', async () => {"
lineis ks1059 176 "    expect(mockFetch).toHaveBeenCalledTimes(1);"
lineis ks1059 177 "    expect(String(mockFetch.mock.calls[0][0])).toContain('/api/anchors/anchor_1');"
lineis ks1059 180 "  it('CONTROL: a terminal document whose anchor genuinely confirmed IS still healed forward', async () => {"
lineis ks1059 194 "    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);"
lineis ks1059 196 "    expect(updates.blockchain.status).toBe('confirmed');"
lineis ks1059 197 "    expect(updates.blockchain.txHash).toBe('e'.repeat(64));"
lineis gw 247 "export function confidenceForAnchorStatus("
lineis gw 251 "    case 'confirmed':"
lineis gw 252 "      return 'on-chain';"
lineis gw 256 "    case 'failed':"
lineis gw 257 "      return 'off-chain-only';"
lineis gw 260 "      return 'off-chain-only';"
lineis gw 630 "    const txHash = liveTxHash || persistedTxHash;"
lineis gw 631 "    const blockHeight = liveBlockHeight || persistedBlockHeight;"
lineis gw 633 "    // KS-1057: \`confidence\` used to be keyed on PRESENCE alone — \`txHash &&"
lineis gw 645 "    const liveAnchored = Boolean(liveTxHash && liveBlockHeight);"
lineis gw 681 "    const persistedAnchored = Boolean("
lineis gw 682 "      persistedTxHashIsReal &&           // KS-1069: was \`persistedTxHash &&\`"
lineis gw 683 "      persistedBlockHeightIsHeight &&    // KS-1069: was \`persistedBlockHeight &&\`"
lineis gw 684 "      !persistedDeclaredSimulated &&     // KS-1069: was \`persistedSimulated !== true\`"
lineis gw 685 "      (persistedStatus === 'confirmed' || persistedStatus == null),"
lineis gw 704 "    const confidence: 'on-chain' | 'pending-onchain' | 'off-chain-only' ="
lineis gw 705 "      liveAnchored || persistedAnchored"
lineis gw 706 "        ? 'on-chain'"
lineis gw 707 "        : confidenceForAnchorStatus(persistedStatus) === 'pending-onchain'"
lineis gw 711 "        : 'off-chain-only';"
lineis gw 712 "    const blockchainAnchored = confidence === 'on-chain';"
lineis gw 715 "      verified: !isRevoked && hashValid && blockchainAnchored,"
lineis gw 731 "      blockchain: {"
lineis gw 732 "        anchored: blockchainAnchored,"
lineis gw 733 "        txHash,"
lineis gw 734 "        blockHeight,"
lineis gw 735 "        confidence,"
lineis gw 737 "        source: liveTxHash ? 'cardano-live' : (persistedTxHash ? 'persisted' : 'none'),"
lineis gw_base 513 "    const txHash = liveTxHash || persistedTxHash;"
lineis gw_base 514 "    const blockHeight = liveBlockHeight || persistedBlockHeight;"
lineis gw_base 515 "    const confidence: 'on-chain' | 'pending-onchain' | 'off-chain-only' ="
lineis gw_base 516 "      txHash && blockHeight"
lineis gw_base 517 "        ? 'on-chain'"
lineis gw_base 520 "        : 'off-chain-only';"
lineis gw_base 521 "    const blockchainAnchored = confidence === 'on-chain';"
lineis docrepo 58 "  blockchain?: {"
lineis docrepo 59 "    txHash: string | null;"
lineis docrepo 60 "    blockHeight: number;"
lineis docrepo 61 "    // Absent in the KS-520 fail-closed state — nothing was anchored, so"
lineis docrepo 62 "    // there is no anchor time to record."
lineis docrepo 63 "    anchoredAt?: string;"
lineis docrepo 64 "    network?: string;"
lineis docrepo 65 "    status?: string;"
lineis docrepo 66 "    anchorId?: string;"
lineis ks1057 123 "  originate.listen(0, '127.0.0.1');"
lineis ks1057 136 "  const { createVerificationRoutes } = await import('../routes/verification');"
lineis ks1057 141 "    createVerificationRoutes({"
lineis ks1057 177 "  gateway = app.listen(0, '127.0.0.1');"
lineis ks1057 197 "  const r = await realFetch(\`http://127.0.0.1:\${gatewayPort}/api/documents/\${DOC_ID}/verify\`, {"
lineis ks1057 207 "  it('DEFECT: an anchor_failed blob carrying a hash AND a height must not report on-chain', async () => {"
lineis ks1057 247 "  it('CONTROL (pre-#912 shape): anchor_failed with no hash and zero height stays off-chain', async () => {"
lineis ks1057 258 "  it('CONTROL (non-zero): a confirmed blob still reports on-chain and verified', async () => {"
lineis ks1057 316 "  it('F1 DEFECT: a FAILED anchor reached via tier 2 must not report on-chain', async () => {"
lineis ks1057 357 "  it('REGRESSION: live chain evidence still heals a blob that says anchor_failed', async () => {"
chk() { # file token mode(present|absent|N)
  local f="$1" tok="$2" mode="$3" c
  c="$(/usr/bin/grep -c -i -F -- "$tok" "$W/$f")"
  if [ "$mode" = present ] && [ "$c" -ge 1 ]; then echo "ok   $f  present x$c  $tok"
  elif [ "$mode" = absent ] && [ "$c" -eq 0 ]; then echo "ok   $f  absent      $tok"
  elif [ "$mode" != present ] && [ "$mode" != absent ] && [ "$c" -eq "$mode" ]; then echo "ok   $f  exactly x$c $tok"
  else echo "FAIL $f  $mode expected, count $c: $tok"; FAILS=$((FAILS+1)); fi
}
# --- anchorStateSync.ts at head: the tamper anchors, counts as the brief states
chk anchor "if (doc.blockchain?.status === 'confirmed') return;" 1
chk anchor "if (doc.blockchain?.txHash || doc.blockchain?.status === 'confirmed') return;" absent
chk anchor "const prior = doc.blockchain as (typeof doc.blockchain & { threadToken?: unknown }) | undefined;" 1
chk anchor "const prior = doc.blockchain;" absent
chk anchor "const prior" 1
chk anchor "txHash: prior?.txHash ?? null," 1
chk anchor "blockHeight: prior?.blockHeight ?? 0," 1
chk anchor "...(prior?.network ? { network: prior.network } : {})," 1
chk anchor "...(prior?.txHash && prior?.anchoredAt ? { anchoredAt: prior.anchoredAt } : {})," 1
chk anchor "...(prior?.anchoredAt ? { anchoredAt: prior.anchoredAt } : {})," absent
chk anchor "...(prior?.threadToken ? { threadToken: prior.threadToken } : {})," 1
chk anchor "...(anchorId ? { anchorId } : {})," 1
chk anchor "const inFlight = bc.status !== 'anchor_failed' && bc.status !== 'confirmed';" 1
chk anchor "const inFlight = !bc.txHash && bc.status !== 'anchor_failed' && bc.status !== 'confirmed';" absent
chk anchor "if (inFlight && !bc.txHash && simFields.simulated) {" 1
chk anchor "if (inFlight && simFields.simulated) {" absent
chk anchor "if (inFlight && anchor.status === 'failed') {" 1
chk anchor "if (!inFlight && !failed) return document;" 1
chk anchor "if (confirmed && txHash) {" 1
chk anchor "preserveTerminalStatuses: true" 5
chk anchor "inFlight" 5
chk anchor "anchor_failed" 10
chk anchor "KS-1004" 6
chk anchor "KS-1058" 2
chk anchor "documentRepo.ts:60-61" 2
chk anchor "listen(" absent
chk anchor "<<<<<<<" absent
chk anchor ">>>>>>>" absent
# --- at the merge commit: the unconditional carry, ONE prior
chk anchor_merge "...(prior?.anchoredAt ? { anchoredAt: prior.anchoredAt } : {})," 1
chk anchor_merge "...(prior?.txHash && prior?.anchoredAt ? { anchoredAt: prior.anchoredAt } : {})," absent
chk anchor_merge "const prior" 1
chk anchor_merge "const prior = doc.blockchain as (typeof doc.blockchain & { threadToken?: unknown }) | undefined;" 1
chk anchor_merge "...(prior?.threadToken ? { threadToken: prior.threadToken } : {})," 1
chk anchor_merge "if (doc.blockchain?.status === 'confirmed') return;" 1
chk anchor_merge "<<<<<<<" absent
chk anchor_merge ">>>>>>>" absent
# --- at round 1: untyped prior, no threadToken carry, the unconditional carry
chk anchor_r1 "const prior = doc.blockchain;" 1
chk anchor_r1 "threadToken" absent
chk anchor_r1 "KS-1058" absent
chk anchor_r1 "...(prior?.anchoredAt ? { anchoredAt: prior.anchoredAt } : {})," 1
# --- at develop: base's guard + base's inFlight + the sim leg without !bc.txHash + KS-1058's carry
chk anchor_dev "if (doc.blockchain?.txHash || doc.blockchain?.status === 'confirmed') return;" 1
chk anchor_dev "const inFlight = !bc.txHash && bc.status !== 'anchor_failed' && bc.status !== 'confirmed';" 1
chk anchor_dev "if (inFlight && simFields.simulated) {" 1
chk anchor_dev "...(prior?.threadToken ? { threadToken: prior.threadToken } : {})," 1
chk anchor_dev "KS-1004" absent
chk anchor_dev "txHash: prior?.txHash ?? null," absent
# --- the test files at head
chk ks1004 "  it(" 9
chk ks1004 "describe(" 2
chk ks1004 "listen(" absent
chk ks1004 "'anchoredAt' in updates.blockchain" 1
chk ks1004 "CONTRACT: a NO-txHash prior carrying anchoredAt" 1
chk ks1004 "not.toHaveBeenCalled()" 3
chk ks1004 "toHaveBeenCalledTimes(1)" 2
chk ks1004 "@" absent
chk ks1004_merge "  it(" 8
chk ks1004_merge "CONTRACT: a NO-txHash prior carrying anchoredAt" absent
chk ks1058 "  it(" 6
chk ks1058 "UNION with KS-1004" 1
chk ks1058 "CONTROL: the existing guard still no-ops" absent
chk ks1058 "CONTRACT: anchoredAt is NOT carried forward" 1
chk ks1058 "toBeUndefined()" 2
chk ks1058 "threadToken" 15
chk ks1058 "listen(" absent
chk ks1058 "@" absent
chk ks1058_dev "  it(" 6
chk ks1058_dev "CONTROL: the existing guard still no-ops on a document carrying a real txHash" 1
chk ks1058_dev "UNION with KS-1004" absent
chk ks535 "  it(" 14
chk ks535 "no-ops when the anchor is confirmed — WITHOUT a txHash" 1
chk ks535 "no-ops on a confirmed anchor even when it also carries a txHash" 1
chk ks535 "listen(" absent
chk ks535_dev "  it(" 13
chk ks1059 "  it(" 4
chk ks1059 "DEFECT CELL: an anchor_failed document is NOT rewritten" 1
chk ks1059 "tx_sim_" 4
chk ks1059 "listen(" absent
chk ks1059 "@" absent
chk ks1059 "KS-1004" absent
# --- the gateway at head (= develop): status-aware; at base: presence-keyed
chk gw "export function confidenceForAnchorStatus" 1
chk gw "const liveAnchored = Boolean(liveTxHash && liveBlockHeight);" 1
chk gw "const persistedAnchored = Boolean(" 1
chk gw "(persistedStatus === 'confirmed' || persistedStatus == null)," 1
chk gw "confidenceForAnchorStatus(persistedStatus) === 'pending-onchain'" 1
chk gw "KS-1004 (#912)" 1
chk gw "source: liveTxHash ? 'cardano-live' : (persistedTxHash ? 'persisted' : 'none')," 1
chk gw "txHash && blockHeight" absent
chk gw "txHash &&" 4
chk gw_base "txHash && blockHeight" 1
chk gw_base "confidenceForAnchorStatus" absent
chk gw_base "persistedAnchored" absent
chk ks1057 "  it(" 9
chk ks1057 "app.listen(0, '127.0.0.1')" 1
chk ks1057 "originate.listen(0, '127.0.0.1');" 1
chk ks1057 "createVerificationRoutes" 2
# --- documentRepo.ts at head: Peter's item 2 lines unchanged
chk docrepo "Absent in the KS-520 fail-closed state" 1
chk docrepo "anchoredAt?: string;" 1
chk docrepo "threadToken" absent
# --- the merge re-derivation, the stack, the round-1 reads (python, literal clone path)
cat > "$W/merge.py" <<'PY'
import sys, hashlib, subprocess, json, os, re, urllib.request
W = sys.argv[1]; CLONE = sys.argv[2]; R1_READ = sys.argv[3]
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1
def git(*a): return subprocess.run(["git", "-C", CLONE, *a], capture_output=True, text=True)
DEV='8861e62161466c40f08d2b10a30edeb203123993'; R1='ae8751f380ed361505694ba71ad9bf1308ee0e87'; MERGE='3231514154aaa8a469e6cdd5f553ee8ce6079b89'
HEAD='609c44c55323b5c90320847b6837ca37f6586705'; H937='6fd3a8bec4e4cc858d38925e00703a37ffcf1b30'; MDEV='bda4c74a6deab584df59d9b047f5a1615b2e12a0'; R1937='cf8b23366f235f37207f7a228a724e9c9cf52fdb'
F='Blockchain/Dev/services/originate/src/services/anchorStateSync.ts'
mt = git("merge-tree", "--write-tree", DEV, R1)
ck(mt.returncode == 1 and "CONFLICT (content)" in mt.stdout and mt.stdout.count("CONFLICT") == 1 and F in mt.stdout, f"merge-tree(develop, r1) rc {mt.returncode}: ONE content conflict, in anchorStateSync.ts")
MT = mt.stdout.split("\n")[0].strip()
mtree = git("rev-parse", MERGE + "^{tree}").stdout.strip()
ck(mtree == "632eed5bb623305e08db3eacc464600532059e37", f"merge commit tree {mtree[:9]} == 632eed5bb")
dt = git("diff-tree", "-r", "--name-status", MT, mtree).stdout.strip().split("\n")
ck(dt == ["M\t" + F], f"diff-tree(git's conflicted tree, merge tree) = exactly M anchorStateSync.ts: {dt}")
ns = git("diff", "--numstat", MT, mtree).stdout.strip()
ck(ns == "5\t12\t" + F, f"numstat between them = 5 12 on the one file: {ns!r}")
patch = git("diff", MT, mtree, "--", F).stdout
ck(patch.count("\n@@") == 3, f"the resolution patch has exactly THREE unified-diff hunks = two regions (the doc block's start and end; the prior collapse) ({patch.count(chr(10)+'@@')})")
ck(("-<<<<<<< " + DEV) in patch and ("->>>>>>> " + R1) in patch and "\n-=======\n" in patch, "hunk 1 removes the three conflict markers")
ck("-  const prior = doc.blockchain;" in patch and "+  const prior" not in patch and patch.count("const prior") == 2, "hunk 2 collapses the double `const prior` (the untyped one removed; the typed one is context)")
ck("prior?.threadToken" not in patch and "prior?.anchoredAt" not in patch, "the object literal region is NOT in the patch (the auto-merge as-is)")
blob_conf = git("show", MT + ":" + F).stdout
ck(blob_conf.count("const prior") == 2 and sum(1 for l in blob_conf.split("\n") if l.startswith("<<<<<<<") or l.startswith(">>>>>>>")) == 2, "git's conflicted blob: `const prior` x2 and the marker pair present (positive control for the collapse)")
ck(git("merge-tree", "--write-tree", DEV, DEV).stdout.strip() == git("rev-parse", DEV + "^{tree}").stdout.strip(), "control: merge-tree(develop, develop) == develop's tree")
ck(git("merge-tree", "--write-tree", DEV, MERGE).stdout.strip() == mtree, "control: merge-tree(develop, merge) == the merge's tree (develop is its ancestor)")
htree = git("rev-parse", HEAD + "^{tree}").stdout.strip()
ck(git("merge-tree", "--write-tree", DEV, HEAD).stdout.strip() == htree == "b95db50904732799f5f099a94c298990d32b2727", f"control: merge-tree(develop, head) == head's tree {htree[:9]} == b95db5090")
ck(git("merge-base", HEAD, DEV).stdout.strip() == DEV, "merge-base(head, develop) = develop (an ancestor)")
ck(git("rev-list", "--left-right", "--count", DEV + "..." + HEAD).stdout.split() == ["0", "3"], "rev-list --left-right --count develop...head = 0 3")
ck(git("log", "-1", "--format=%P", MERGE).stdout.split() == [R1, DEV], "the merge's parents = r1 + develop")
ck(git("log", "-1", "--format=%P", HEAD).stdout.split() == [MERGE], "the fix's parent = the merge")
fx = sorted(git("diff", "--numstat", MERGE, HEAD).stdout.strip().split("\n"))
want = sorted(["4\t1\t" + F, "21\t0\tBlockchain/Dev/services/originate/src/__tests__/ks1004-anchor-failed-lockout.test.ts", "13\t6\tBlockchain/Dev/services/originate/src/__tests__/ks1058-anchor-failed-preserves-thread-token.test.ts"])
ck(fx == want, "git diff --numstat merge head = the three fix files 4/1, 21/0, 13/6")
ns4 = sorted(l.split("\t")[-1] for l in git("diff", "--name-status", DEV, HEAD).stdout.strip().split("\n") if l)
ck(len(ns4) == 4 and F in ns4 and all("__tests__/ks" in x for x in ns4 if x != F), f"git diff --name-status develop head = the four PR files ({len(ns4)})")
h1058 = git("diff", MERGE, HEAD, "--", "Blockchain/Dev/services/originate/src/__tests__/ks1058-anchor-failed-preserves-thread-token.test.ts").stdout
ck(h1058.count("\n@@") == 1 and "@@ -180,12 +180,19 @@" in h1058, "the ks1058 fix hunk is @@ -180,12 +180,19 @@ ALONE (header untouched)")
hdr_head = git("show", HEAD + ":Blockchain/Dev/services/originate/src/__tests__/ks1058-anchor-failed-preserves-thread-token.test.ts").stdout.split("\n")[:70]
hdr_dev = git("show", DEV + ":Blockchain/Dev/services/originate/src/__tests__/ks1058-anchor-failed-preserves-thread-token.test.ts").stdout.split("\n")[:70]
ck(hdr_head == hdr_dev, "ks1058 :1-70 at head == develop byte-for-byte")
for c, want_ids in ((MERGE, {"KS-1004"}), (HEAD, {"KS-1004"})):
    m = git("log", "-1", "--format=%B", c).stdout
    ids = set(re.findall(r"KS-\d+", m))
    ck(ids == want_ids and m.count("@") == 0, f"commit {c[:9]} message ids {sorted(ids)} (KS-1004 only), 0 at-signs")
# --- #937: the two merges are unions; the delta onto #912 is one file; the locks are develop's
t_mdev = git("rev-parse", MDEV + "^{tree}").stdout.strip(); t_937 = git("rev-parse", H937 + "^{tree}").stdout.strip()
m1 = git("merge-tree", "--write-tree", DEV, R1937)
ck(m1.returncode == 0 and m1.stdout.strip() == t_mdev, f"merge-tree(develop, cf8b23366) rc {m1.returncode} == bda4c74a6's tree {t_mdev[:9]} (a mechanical union)")
m2 = git("merge-tree", "--write-tree", MDEV, HEAD)
ck(m2.returncode == 0 and m2.stdout.strip() == t_937, f"merge-tree(bda4c74a6, 609c44c55) rc {m2.returncode} == 6fd3a8bec's tree {t_937[:9]} (a mechanical union)")
ck(git("log", "-1", "--format=%P", H937).stdout.split() == [MDEV, HEAD] and git("log", "-1", "--format=%P", MDEV).stdout.split() == [R1937, DEV], "#937's two merges' parents as stated")
d = git("diff", "--numstat", HEAD, H937).stdout.strip()
ck(d == "199\t0\tBlockchain/Dev/services/originate/src/__tests__/ks1059-sim-leg-must-not-resurrect-a-terminal-document.test.ts", f"git diff --numstat 609c44c55 6fd3a8bec = the ks1059 test alone: {d!r}")
ck(git("diff", "--stat", DEV, H937, "--", "systemTest/").stdout.strip() == "", "git diff --stat develop 6fd3a8bec -- systemTest/ is EMPTY (the locks left by ancestry)")
ck(git("merge-base", "--is-ancestor", "cd8509faf", DEV).returncode == 0, "cd8509faf (#934's head) is develop's ancestor")
ck(git("rev-parse", H937 + ":" + F).stdout.strip() == git("rev-parse", HEAD + ":" + F).stdout.strip(), "anchorStateSync.ts blob at 6fd3a8bec == at 609c44c55")
ck(git("rev-list", "--left-right", "--count", HEAD + "..." + H937).stdout.split() == ["0", "4"], "rev-list --left-right --count 609c44c55...6fd3a8bec = 0 4")
# --- the stack compare at the API and the round-1 reads
env = {}
for line in open("/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env", encoding="utf-8"):
    if line.startswith("GH_TOKEN="): env["t"] = line.split("=", 1)[1].strip().strip('"').strip("'")
def api(p):
    return json.load(urllib.request.urlopen(urllib.request.Request("https://api.github.com/repos/Secuura/Distributed_Secuura" + p, headers={"Authorization": "Bearer " + env.get("t", ""), "Accept": "application/vnd.github+json"}), timeout=60))
try:
    c = api("/compare/" + HEAD + "..." + H937)
    ck(c["merge_base_commit"]["sha"] == HEAD and c["ahead_by"] == 4 and len(c["files"]) == 1, f"API compare 609c44c55...6fd3a8bec: merge_base {c['merge_base_commit']['sha'][:9]} ahead {c['ahead_by']} files {len(c['files'])}")
    c2 = api("/compare/develop..." + HEAD)
    ck(c2["merge_base_commit"]["sha"] == DEV and c2["ahead_by"] == 3 and len(c2["files"]) == 4, f"API compare develop...609c44c55: merge_base {c2['merge_base_commit']['sha'][:9]} ahead {c2['ahead_by']} files {len(c2['files'])}")
    cm = api("/issues/comments/5597511879")
    ck(hashlib.sha256(cm["body"].encode()).hexdigest()[:16] == "b27fbc1f6206efca" and len(cm["body"]) == 4200 and cm["user"]["login"] == "kksecura", f"the transcription comment 5597511879: sha256 {hashlib.sha256(cm['body'].encode()).hexdigest()[:16]}, {len(cm['body'])} chars, {cm['user']['login']} {cm['created_at']}")
    ck("NO GO" in cm["body"] and "5517d9d0" in cm["body"] and "13,654" in cm["body"], "the transcription names the verdict file's size and sha prefix")
    cp = api("/issues/comments/5602883901")
    ck(hashlib.sha256(cp["body"].encode()).hexdigest()[:16] == "cd0c1f0d7d8fcd17" and len(cp["body"]) == 10083, f"Peter's comment 5602883901: sha256 {hashlib.sha256(cp['body'].encode()).hexdigest()[:16]}, {len(cp['body'])} chars")
    ca = api("/issues/comments/5656435630")
    ck(hashlib.sha256(ca["body"].encode()).hexdigest()[:16] == "b4f54e59ff9ea135" and HEAD[:9] in ca["body"] and MERGE[:9] in ca["body"] and ca["body"].count("@") == 0, f"the round-2 answer 5656435630: sha256 {hashlib.sha256(ca['body'].encode()).hexdigest()[:16]}, names the head + the merge, 0 at-signs")
except Exception as e:
    ck(False, "an API read failed: " + type(e).__name__ + " " + str(e)[:80])
disk = open(R1_READ, "rb").read()
ck(hashlib.sha256(disk).hexdigest() == "5517d9d0fd208b04b96125955c6d68cbbdef6a377ecd1f19b2868e448ded3c16" and len(disk) == 13654, f"the round-1 verdict file on disk: sha256 {hashlib.sha256(disk).hexdigest()[:16]}, {len(disk)} bytes")
ck(disk.count(b"NO GO") == 3 and disk.count(b"F1") == 5, "the verdict file reads NO GO x3 (the recovery header + the verdict line + the closing) and F1 x5")
# raw control bytes in the five PR files at head
for f in ["anchor", "ks1004", "ks1058", "ks535", "ks1059"]:
    b = open(f"{W}/{f}", "rb").read()
    ck(not [i for i, x in enumerate(b) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f], f"{f}: 0 raw control bytes")

# --- M21 content-judged guard (Wednesday's 2026-09-14 12:1x AEST instruction): the launcher's M21_ALLOWED dict
# clears four M21 (KS-764/#799) paths by BLOB, not by path. Two checks: (a) the four pinned blobs in the launcher
# source are what git itself reads at M21 RIGHT NOW (a live re-derivation, not trust-the-constant); (b) a
# reimplementation of the launcher's exact hits/cleared/remaining algorithm, fed a synthetic compare-API file list
# where ONE of the four paths carries a THIRD blob (neither M18-absent nor the pinned M21 blob) -- NEGATIVE
# CONTROL: this must stay GUARDED (the clearance is blob-exact, not a path exemption).
M21 = '5210ddf317b2b1ed547e5d8488c3d011ceb087e1'
M21_ALLOWED = {
    "Blockchain/Dev/services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts": "5a78c4181281f360ebd4481593fd73bf98bb4d9c",
    "Blockchain/Dev/services/originate/src/middleware/auth.ts": "f08ee1a895bc878bc2656f649833706f665686e7",
    "Blockchain/Dev/services/originate/src/routes/adminConfig.ts": "26cec03de665ef75a8f6e4f2532dfc42a59a25b8",
    "Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts": "ab8e46d795d268822924a57e2630403be1963497",
}
LAUNCHER_SRC = open('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate912r2/launch_qa_secuura_ks1004_912_r2_ks1059_937_stacked.sh', encoding='utf-8').read()
for path, blob in M21_ALLOWED.items():
    live = git("rev-parse", M21 + ":" + path).stdout.strip()
    ck(live == blob, f"M21 live blob for {path.split('/')[-1]}: git rev-parse {M21[:9]}:{path.split('/')[-1]} = {live[:9]} == pinned {blob[:9]}")
    ck(f'"{path}": "{blob}"' in LAUNCHER_SRC, f"launcher source pins {path.split('/')[-1]} at exactly this blob (live-verified)")
GUARDED_TEST = [
    "Blockchain/Dev/services/originate/src/services/anchorStateSync.ts",
    "Blockchain/Dev/services/originate/src/",
    "Blockchain/Dev/packages/shared/src/__tests__/",
]
def judge_hits(files):
    by_name = {f["filename"]: f for f in files}
    hits = sorted({f["filename"] for f in files for g in GUARDED_TEST if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
    cleared = sorted(h for h in hits if h in M21_ALLOWED and by_name.get(h, {}).get("sha") == M21_ALLOWED[h])
    remaining = sorted(h for h in hits if h not in cleared)
    return remaining, cleared
# positive: all four at their pinned blob, plus a disjoint file -> remaining empty, all four cleared
pos_files = [{"filename": p, "sha": b} for p, b in M21_ALLOWED.items()] + [{"filename": "Blockchain/Dev/scripts/preflight/preflight.sh", "sha": "deadbeef"}]
rem, clr = judge_hits(pos_files)
ck(rem == [] and len(clr) == 4, f"guard simulation, all four at pinned blob: remaining={rem} cleared={len(clr)}")
# NEGATIVE CONTROL: one of the four at a THIRD blob (neither M18-absent nor the pinned M21 blob) -> stays GUARDED
tampered_path = "Blockchain/Dev/services/originate/src/middleware/auth.ts"
neg_files = [{"filename": p, "sha": (b if p != tampered_path else "0000000000000000000000000000000000dead")} for p, b in M21_ALLOWED.items()]
rem2, clr2 = judge_hits(neg_files)
ck(tampered_path in rem2 and len(clr2) == 3, f"NEGATIVE CONTROL, {tampered_path.split('/')[-1]} at a third blob: remaining={rem2} (must include it) cleared={len(clr2)} (must be 3, not 4)")
sys.exit(1 if fails else 0)
PY
python3 "$W/merge.py" "$W" "$CLONE" "$R1_READ" || FAILS=$((FAILS+1))
echo "work dir (kept): $W"
echo "controls_check: FAILS=$FAILS"
[ "$FAILS" -eq 0 ] && exit 0 || exit 1
