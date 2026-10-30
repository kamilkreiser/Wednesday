import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common18 import *
TEST = TDIR + 'ks1836-read-gate-wallet-selector-compares-exactly.test.ts'
CONTENT = '''// KS-1836 (gate 23 mutant Mf): selectReadableCertificates (services/nftReadGate.ts) documents that the `walletAddress` selector "must
// equal the row's wallet". The comparison is exact: a wallet address is an opaque string, so a selector or a row value that differs
// only by surrounding whitespace is a DIFFERENT wallet and matches nothing. The PR's own cells use well-formed wallets only, so a
// compare that trims both sides stayed green. Unit level: the pure function, no router, no database.
import { describe, it, expect } from 'vitest';
import { selectReadableCertificates } from '../services/nftReadGate';
import type { NFTCertificate } from '../types';

const OWNER = 'user-A';
const WALLET = 'addr_test1_ks1836_exact_wallet';

function cert(id: string, walletAddress: string): NFTCertificate {
  return { id, userId: OWNER, walletAddress } as unknown as NFTCertificate;
}

const ids = (list: readonly NFTCertificate[]) => list.map(c => c.id);

describe('KS-1836 read gate: the walletAddress selector compares exactly', () => {
  it('RED KS-1836 W1 a selector padded with spaces does not match the unpadded row wallet', () => {
    expect(ids(selectReadableCertificates([cert('c1', WALLET)], OWNER, { walletAddress: ` ${WALLET} ` }))).toEqual([]);
  });

  it('RED KS-1836 W2 a row wallet padded with spaces is not matched by the unpadded selector', () => {
    expect(ids(selectReadableCertificates([cert('c1', ` ${WALLET}`)], OWNER, { walletAddress: WALLET }))).toEqual([]);
  });

  it('CONTROL KS-1836 W3 the exact selector returns the row', () => {
    expect(ids(selectReadableCertificates([cert('c1', WALLET)], OWNER, { walletAddress: WALLET }))).toEqual(['c1']);
  });

  it('CONTROL KS-1836 W4 a different wallet returns nothing', () => {
    expect(ids(selectReadableCertificates([cert('c1', WALLET)], OWNER, { walletAddress: `${WALLET}_other` }))).toEqual([]);
  });

  it('CONTROL KS-1836 W5 no walletAddress selector returns every row the owner holds', () => {
    expect(ids(selectReadableCertificates([cert('c1', WALLET), cert('c2', 'addr_other')], OWNER, {}))).toEqual(['c1', 'c2']);
  });
});
'''
T = dict(dir='ks_1836_p3_wallet_selector_exact', ticket='KS-1836', test=TEST, product=GATE, ref=REF, runner=RUNNER,
 content=CONTENT, ncells='5 cells',
 title="nft-certificate read gate: pin that the walletAddress selector compares exactly, no trimming (gate 23 mutant Mf; RUNG 3, TEST-ONLY: one NEW vitest file with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 18 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / nft-certificate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: " + GATE_NOTE + " (mutant Mf, survived). The product is right at the tip; the gap is a missing pin on behaviour the code's own doc comment states. Gate 23 judged Mf low: it only alters narrowing within the caller's own rows, never a cross-owner leak.",
 scope="**Refs KS-1836, never a close-word.** Unit pin of the exact wallet compare in `selectReadableCertificates`. NOT touched, because choosing the right behaviour is a product decision: F2 (the row-owner trim asymmetry between the two read paths; mutant Mc), F3, F4. NOT done because it is near-equivalent: mutant Md (drop the row non-string guard), the column is `user_id TEXT NOT NULL`. No product line changes; one new test file, no existing file edited.",
 wrong="`selectReadableCertificates` in `services/nftReadGate.ts` filters rows with `cert.walletAddress !== selectors.walletAddress` (exact compare) and its doc comment says the selector `must equal the row's wallet`. Gate 23 mutant Mf (`cert.walletAddress.trim() !== String(selectors.walletAddress).trim()`) survived every cell because no fixture has a padded wallet. Add unit cells on the pure function: a selector padded with spaces must not match an unpadded row, a padded row must not match the unpadded selector. Three controls keep the exact, other-wallet and no-selector cases honest.",
 where="- `services/nftReadGate.ts:91` - (correct, STAYS) `    if (selectors.walletAddress !== undefined && cert.walletAddress !== selectors.walletAddress) return false;`; the line the tamper replaces in the checker's clone. The doc comment is :77-83. The function and the `ListSelectors` shape are :56-59 and :84-95.\n- The new test imports only `selectReadableCertificates` and the `NFTCertificate` type (`../types`, as nftReadGate.ts itself does); no router, no mocks.",
 tamper_line=91, tamper_from="    if (selectors.walletAddress !== undefined && cert.walletAddress !== selectors.walletAddress) return false;",
 tamper_to="    if (selectors.walletAddress !== undefined && cert.walletAddress.trim() !== String(selectors.walletAddress).trim()) return false;",
 statement_ok="line 91 is one complete `if (...) return false;` statement; the replacement compares trimmed values (gate mutant Mf), still uses both operands, and compiles (`cert.walletAddress` is a string); the exact-equal and different-wallet cases behave as before",
 red=['RED KS-1836 W1 a selector padded with spaces does not match the unpadded row wallet', 'RED KS-1836 W2 a row wallet padded with spaces is not matched by the unpadded selector'],
 cells="- RED under the tamper: W1 and W2 fail by assertion (the padded value matches after trimming, so the list holds c1 instead of nothing).\n- GREEN at the untouched tip: all five cells.\n- Controls W3, W4, W5 stay green under the tamper.",
 unmeasured="- The drafter did NOT run vitest for the brief; RED-under-tamper / GREEN-at-tip is the `round.sh --control` run on this golden.\n- `NFTCertificate` is cast through `unknown` because only `id`, `userId` and `walletAddress` matter to the function; the brief did not read the whole type.\n- Whether a padded wallet can reach the function in production (the route passes the raw query string to the wallet reader first): not measured; this is a unit pin of the function's stated contract.\n- Open PRs touching nft-certificate: only 1360 and 649 (both `package*.json`), read 2026-10-30; none touches a `__tests__` path.",
)
