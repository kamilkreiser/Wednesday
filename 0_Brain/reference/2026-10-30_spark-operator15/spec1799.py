# KS-1799 (gate 12 finding 1795-1, Spark operator 15, 2026-10-30): no cell plants a thrown value whose `message` getter alone throws. test_only, gen/mk_testonly.py.
PROD = 'Blockchain/Dev/services/originate/src/utils/pgErrors.ts'
TEST = 'Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts'
ANCHOR = "  });\n\n  it('control KS-1780 C1 a Prisma-wrapped 42804"
CELL = '''  // KS-1799 (gate 12 finding 1795-1): B2 plants a throwing `code` getter and B4 a throwing `meta` getter, but nothing planted a throwing `message` getter, the third thing extractPgCode reads (the message-text fallback).
  // A plain object (not a Proxy) with only a `message` getter that throws must give undefined, not a throw.
  it('RED KS-1799 B5 extractPgCode of an object whose message getter throws is undefined, not a throw', () => {
    const hostile = {
      get message(): string {
        throw new Error('ks1799 message getter');
      },
    };
    expect(pgCodeOrThrew(hostile)).toBeUndefined();
  });

'''
FROM = "  } catch {"
TO = "  } catch (thrown) { if (thrown instanceof Error && thrown.message === 'ks1799 message getter') { throw thrown; }"
T = dict(dir='ks_1799_p1_message_getter',
 ticket='KS-1799',
 title="originate ks1780 extractPgCode test: no cell plants a thrown value whose `message` getter alone throws (gate 12 finding 1795-1): add one direct-call cell B5 beside B4 (RUNG 3, TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 15 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1799 (gate 12 finding 1795-1, Info). The product is right today: the one `try` in `extractPgCode` covers a `message` getter that throws. The gap is a missing pin. Link the PR as Refs KS-1799 and KS-1780, never a close-word.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/originate/src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts',
 tamper_line=57, tamper_from=FROM, tamper_to=TO,
 statement_ok="line 57 is the `} catch {` of the single try in `extractPgCode` (lines 55-59); the tamper keeps the catch and adds a rethrow only for an Error whose message is the text the new cell's getter throws, so every other thrown value (the revoked Proxy, the code getter, the meta getter) still reaches `return undefined;` and the file compiles; it stands for a narrowing of the guard that leaves a throwing `message` getter unguarded while the other reads stay guarded",
 edit=(ANCHOR, "  });\n\n" + CELL + "  it('control KS-1780 C1 a Prisma-wrapped 42804"),
 nh_txt='1 hunk, the new cell B5 added after cell B4 and before control C1',
 red=['RED KS-1799 B5 extractPgCode of an object whose message getter throws is undefined, not a throw'],
 runner='jest` (`npx jest src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts` from `Blockchain/Dev/services/originate',
 rung='3 (test-only mode: a planted tamper must redden the new cell; the hunk is given byte-exact)',
 what_wrong="`extractPgCode` (`utils/pgErrors.ts:52-60`) wraps `readPgCode(err)` in one `try` that returns `undefined` on any throw. `readPgCode` reads three things off the thrown value: `e?.code`, `e?.meta?.code` and, as the fallback, `e?.message`. The test file plants a throwing `code` getter (B2, through the route), a throwing `meta` getter (B4, direct) and a revoked Proxy (B1, B3), but no cell plants a throwing `message` getter, so a change that leaves only that read unguarded for a plain object is not pinned by name. Add cell B5: a plain object with only a `get message()` that throws, passed directly to `extractPgCode`, expecting `undefined`.",
 where="- `src/utils/pgErrors.ts:55-59` - (correct, STAYS) the `try { return readPgCode(err); } catch { return undefined; }`; line 57 `  } catch {` is the line the tamper replaces in the checker's clone.\n- Test file: cell B4 is :98-105 (its closing `  });` is :105); :106 is blank; :107 starts `control KS-1780 C1`. **The new cell B5, with its two comment lines, goes between :106 and :107** (a blank line after it, before C1). `pgCodeOrThrew` (:69) is in scope; it returns the string THREW if `extractPgCode` throws.",
 cells="- RED under the tamper: `RED KS-1799 B5 ...` fails by assertion (`extractPgCode` rethrows the getter's Error, `pgCodeOrThrew` returns THREW, `toBeUndefined` fails).\n- GREEN at the untouched tip: B5 (the single try swallows the throw) and every other cell.\n- The tamper rethrows only an Error whose message is exactly `ks1799 message getter`, so B1 to B4 and C1 to C4 stay green under it: B5 is the only red.\n- CONTROL: B4 (a throwing `meta` getter) is the same direct-call shape and stays green on both trees.",
 unmeasured="- The drafter did NOT run jest through the round machinery for the brief; the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- The tamper is a message-keyed rethrow, a stand-in for \"only the message read is unguarded\". The operator also measured the literal narrowing (a `void err?.message` placed before the `try`): it reddens B1 and B3 (the revoked Proxy throws on any read) as well, so the ticket's claim that every existing cell would stay green under a narrowing is not true for that mutant; B5 pins the plain-object getter path by name regardless.\n- Whether `message` is read by anything else on the by-route path (routes/webhooks.ts catch) was not measured.\n- Open PRs touching either file: see the overlap count in the operator report.",
 scope="**Closes KS-1799 (Low, Info), test half.** Link the PR as Refs KS-1799 / KS-1780. No product file changes. Not in scope: a route-level message-getter cell (the ticket says `if wanted`), any change to `pgErrors.ts`.",
)
