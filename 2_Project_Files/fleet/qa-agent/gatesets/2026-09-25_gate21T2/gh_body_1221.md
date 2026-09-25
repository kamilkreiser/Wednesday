#1221 KS-1266: keep seven originate unit files off the network, and correct the port-1 cells that never opened a socket
head 0a561a5db393e8f0ced82b86af572c7231330d64

## BLUF

Seven originate unit files reached the network. Left at its default, `ANCHORING_SERVICE_URL` is `http://anchoring:4005`, so any cell touching an anchoring call does a **DNS lookup of the host `anchoring` and a TCP connect to `:4005`** — the suite's result depends on the host's resolver. Each file now sets the base to `http://127.0.0.1:2` at import scope. **Test-only, no product bytes.**

## Port 2, not port 1 — and two files in the tree were already on port 1

Port 1 is on the Fetch-spec bad-port list, and **undici refuses it before opening a socket**, so a cell written for `ECONNREFUSED` never gets one. `ks1228-a-refused-request-writes-no-provenance-row.test.ts` and `ks520-anchor-fail-closed.test.ts` were both on port 1, and both carry comments calling it *"a closed port"* — which was not the mechanism. Both move to port 2, which makes those comments true.

**Searched before folding them in** (literal census, 1,280 KS issues / 823 archived, 3,594 comments): `127.0.0.1:1` → 3 issues. KS-1228 carries a *record* of this exact fact, not a fix; KS-973's instance is `scripts/pre_suite.test.sh`, **outside `services/originate/**` and already owned by that ticket — left alone**; KS-485 is a review-stream roll-up. Controls: `KS-1265` → 4 hits, a nonsense token → 0. No ticket owns the two originate files, so the fix lands here.

## ks1213 needed more than an assignment

Two of its cells point the base at the loopback stub and then `delete process.env.ANCHORING_SERVICE_URL` in their `finally`. An import-scope value would have been **wiped by those deletes**, dropping every later cell in the file back onto `anchoring:4005`. Both now restore the refused base through a named constant.

## File set, chosen by measurement

The ticket names *"the `ks1213`, `ks444`, `ks445` and `ks543` tests"* without filenames. At this base there are **five** `ks444-*`, **four** `ks445-*` and one `ks543-*`. The set here is the files whose imported route can reach the anchoring base — `ks444-certifications-issue-body-types`, `ks444-documents-create-title-guard`, `ks445-certifications-issue-unstorable-payload`, `ks543-certify-boundary-strip` — one more `ks444` file than the ticket's count, plus `ks1213` and the two port-1 files.

## Test Evidence

* **Touched:** seven test files under `services/originate/src/__tests__/`. No product file.
* **Ran:** originate `jest --runInBand` → **74 suites / 863 tests, rc 0**, identical to the bare serial baseline at this base (**74 / 863**). `tsc --noEmit` rc 0. `packages/shared` `vitest run` → **46 files / 918 tests, rc 0**.
* **Positive control — the point of the change, measured rather than asserted.** The seven files were run under a `--require` probe recording every `dns.lookup` and every `net.connect` target, bare and patched, **157 tests green on both sides**:

  | | DNS `anchoring` | TCP `anchoring:4005` | TCP `127.0.0.1:1` | TCP `127.0.0.1:2` |
  |---|---|---|---|---|
  | bare | **17** | **17** | 0 | 0 |
  | patched | **0** | **0** | 0 | **26** |

  The probe is not blind in either direction — it recorded **8 lookups of `127.0.0.1` on both sides**. The 26-vs-17 gap is the port-1 finding proving itself: neither port-1 file appears **anywhere** in the bare log, because undici refused those URLs before a socket existed, so those nine connection attempts were never made at all.
* **NOT run:** the integration config (`jest --config jest.integration.config.js`) — it needs a live Postgres and none of these seven files is in it. No service image was rebuilt; this change has no runtime surface. The probe measures this host's behaviour only; it does not prove what a CI host's resolver would have done.
* **Migrations + config:** none.

Refs KS-1266

🤖 Generated with [Claude Code](https://claude.com/claude-code)

