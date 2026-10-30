# KS-1815 (anchoring anchorSubmission.ts: the ALREADY_INCLUDED_REPLY clause that makes the ruled retry unreachable for the node's real reply is pinned by no cell). Spark operator 24. test_only, ONE existing test modified in place.
PROD='Blockchain/Dev/services/anchoring/src/anchorSubmission.ts'
TEST='Blockchain/Dev/services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts'
REF='Blockchain/Dev/services/anchoring/src/__tests__/ks705-submission-idempotency.test.ts'
ANCHOR="""  it('CONTROL — a 400 "already been included" after onSigned → re-polled and confirmed, scheduleRetry NOT called (the hash IS on chain)', async () => {
"""
CELLS="""  // KS-1815: the cell above feeds the guard a PARAPHRASE of the node's reply ("All inputs are spent"). The node's real text (stored in
  // ks705-submission-idempotency.test.ts) also says "already been included", and the ALREADY_INCLUDED_REPLY clause of `refusedAndAbsent`
  // turns the ruled retry OFF for any text that contains it. These cells pin that clause with the real text.
  const REAL_NODE_REPLY =
    'Transaction submission failed: ConwayMempoolFailure "All inputs are spent. ' +
    'Transaction has probably already been included in a successfully applied block."';
  const definitiveAbsent = () =>
    vi.fn(async () => ({
      confirmed: false,
      polled: ABSENT_MIN_ANSWERED_POLLS,
      errored: 0,
      lastAnsweredAttempt: ABSENT_MIN_ANSWERED_POLLS,
      lastAnsweredElapsedMs: ABSENT_MIN_LAST_ANSWER_MS + 1_000,
    }));

  it('RED KS-1815 R1 the node REAL reply ("... already been included ...") after onSigned, with a DEFINITIVE absent re-poll, is NOT retried: the row rests in submitting', async () => {
    const h = makeHarness({ over: { submit: throwingSubmit(refused(REAL_NODE_REPLY)), confirm: definitiveAbsent() } });
    await createAnchorSubmitter(h.deps)(ANCHOR_ID);

    expect(h.deps.confirm).toHaveBeenCalledTimes(1);
    expect(h.deps.scheduleRetry).toHaveBeenCalledTimes(0);
    expect(h.row.status).toBe('submitting');
  });

  it('control KS-1815 C1 the same DEFINITIVE absent re-poll with the paraphrase "All inputs are spent" (no "already been included") IS retried', async () => {
    const h = makeHarness({
      over: { submit: throwingSubmit(refused('Transaction submission failed: ConwayMempoolFailure "All inputs are spent"')), confirm: definitiveAbsent() },
    });
    await createAnchorSubmitter(h.deps)(ANCHOR_ID);

    expect(h.deps.confirm).toHaveBeenCalledTimes(1);
    expect(h.deps.scheduleRetry).toHaveBeenCalledTimes(1);
    expect(h.row.status).not.toBe('submitting');
  });

"""+ANCHOR
T=dict(dir='ks_1815_p4_real_node_reply_not_retried',ticket='KS-1815',test=TEST,product=PROD,ref=REF,
 runner='vitest` (`npx vitest run src/__tests__/ks726-write-ahead-tx-hash.test.ts` from `Blockchain/Dev/services/anchoring',
 rung='3-4 (test HARDENING: a clause that no cell pins gets a killing cell; the cells are given byte-exact, the tamper is the deletion the ticket names)',
 title="anchoring: pin the ALREADY_INCLUDED_REPLY clause of the ruled retry with the node's REAL reply (KS-1815; TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 24 for Wednesday, 2026-10-30 AEDT. Secuura (anchoring, anchorSubmission.ts and its ks726 test only; NOT index.ts, NOT KS-1384) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1815. The ruled retry after a node rejection (`refusedAndAbsent` in `anchorSubmission.ts`) has a clause `!ALREADY_INCLUDED_REPLY.test(message ?? '')` that turns the retry off for any reply containing 'already been included'. The node's real reply (ks705-submission-idempotency.test.ts) contains it; the only retry cell (ks726 :414) uses a paraphrase without it, so deleting the clause breaks no cell. This task adds the killing cell (R1, real reply is not retried) and the control C1 (the paraphrase is retried).",
 tamper_line=640,
 tamper_from="            !ALREADY_INCLUDED_REPLY.test(message ?? '');",
 tamper_to="            true;",
 statement_ok="lines 637-640 are ONE statement, `const refusedAndAbsent = found === 'absent' && known === writtenAheadTxHash && !ALREADY_INCLUDED_REPLY.test(message ?? '');`; the tamper replaces ONLY its last operand (line 640) with `true;`, so the statement stays complete and the file compiles (ALREADY_INCLUDED_REPLY is still used at :115-124)",
 edit=(ANCHOR,CELLS),
 red=['RED KS-1815 R1'],
 what_wrong="`ks726-write-ahead-tx-hash.test.ts:414` feeds the guard `ConwayMempoolFailure \"All inputs are spent\"`, a paraphrase. The node's real text is `ConwayMempoolFailure \"All inputs are spent. Transaction has probably already been included in a successfully applied block.\"` (ks705-submission-idempotency.test.ts:47-50), and `refusedAndAbsent` in `anchorSubmission.ts:637-640` ends with `!ALREADY_INCLUDED_REPLY.test(message ?? '')`, which makes the retry unreachable for that text. No cell pairs the real text with a write-ahead hash and a definitive absent re-poll, so deleting the clause leaves every cell green. This task adds, inside the same describe, a helper `REAL_NODE_REPLY`, a helper `definitiveAbsent` and two cells: R1 (real reply + definitive absent re-poll: `scheduleRetry` is NOT called and the row rests in `submitting`) and C1 (the paraphrase with the same re-poll IS retried: the clause is not over-broad).",
 where="- `services/anchoring/src/anchorSubmission.ts:640` - (correct, STAYS) the last operand of `refusedAndAbsent`; the line the tamper edits in the checker's clone (it becomes `true;`).\n- The test hunk inserts the helpers and the two cells directly BEFORE the existing cell `CONTROL — a 400 \"already been included\" after onSigned → re-polled and confirmed ...` (:452), after the cell `KS-1171 — the SAME 400 whose re-poll carries NO evidence rests instead of retrying`, inside the same describe (so `makeHarness`, `throwingSubmit`, `refused`, `ABSENT_MIN_ANSWERED_POLLS`, `ABSENT_MIN_LAST_ANSWER_MS`, `createAnchorSubmitter`, `ANCHOR_ID` are all in scope).",
 cells="- RED under the tamper: `RED KS-1815 R1` fails by assertion (the retry is scheduled once, not zero times).\n- GREEN at the untouched tip: all cells, R1 and C1 included.\n- C1 stays green under the tamper (the paraphrase never contained 'already been included').",
 unmeasured="- The drafter did NOT run vitest for the brief: RED-under-tamper / GREEN-at-tip is the `round.sh --control` run on this golden. In particular the resting status 'submitting' for R1 is read from the neighbouring cell 'KS-1171 - the SAME 400 whose re-poll carries NO evidence rests' (:441-450), not run.\n- The ticket also proposes correcting the :414 cell's fixture to the real text; this task leaves :414 as it is and adds beside it.\n- Open PRs touching anchoring: 1821 (index.ts) and 1825 (reconciler.ts and two tests). None touches anchorSubmission.ts or ks726 (read 2026-10-30 from the PR heads). KS-1384 (seat W 11th) is a persistence change in index.ts; this brief does not touch it.",
 scope="**Refs KS-1815, never a close-word.** Pins the ALREADY_INCLUDED_REPLY clause only.",
)
