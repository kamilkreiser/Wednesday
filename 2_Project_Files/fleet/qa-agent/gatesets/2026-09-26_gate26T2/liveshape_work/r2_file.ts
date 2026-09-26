/**
 * The offline unit suite gives the same answer from every worktree, whatever slot that worktree's
 * shell exports (KS-1167 C2). Port of platform-s `tests-unit/unit_suite_slot_independence.test.ts`;
 * Playwright's `unit-suite-slot-independence.test.ts` landed alongside under the same ticket.
 *
 * WHY THIS FILE EXISTS — MEASURED 2026-09-14, before the fix, over the whole suite:
 *
 *   no slot exported        1077 pass / 0 fail
 *   SECUURA_STACK_SLOT=1    1067 / 10
 *   SECUURA_STACK_SLOT=2    1060 / 17
 *   STACK_SLOT=3            1062 / 15
 *
 * Three guards:
 *   1. no test file hands a child `{ ...process.env }` directly — `envWithoutSlot()` is the door;
 *   2. the strip runs BEFORE each test file is imported — `vitest.unit.config.ts` wires
 *      `tests/unit/support/clearSlotEnv.setup.ts`, because runner modules freeze their slot at import
 *      and a `beforeEach` is too late (run_dir.ts's `LATEST_LINK`);
 *   3. the files that were red, re-run as a child vitest from a shell on NO slot and on every slot
 *      1..4 (and the platform-s alias, and the wrapper's suffix shape), give identical pass/fail
 *      counts with zero failures — compared to the unslotted run, never to a typed number.
 */

import { spawnSync } from 'node:child_process';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { describe, expect, it } from 'vitest';

import { envWithoutSlot } from '../support/slotEnv.ts';
import {
    S10_STDOUT,
    S17_STDERR,
    S17_STDOUT,
    S18_STDERR,
    S18_STDOUT,
    S19_STDOUT,
} from '../support/capturedChildOutput.ts';

const PACKAGE_ROOT = fileURLToPath(new URL('../../..', import.meta.url));
const UNIT_DIR = path.join(PACKAGE_ROOT, 'tests', 'unit');
const VITEST_BIN = path.join(PACKAGE_ROOT, 'node_modules', '.bin', 'vitest');
const SELF = fileURLToPath(import.meta.url);

const SLOTS = [1, 2, 3, 4];

/**
 * The files that were red from a slotted shell before KS-1167, plus the shared-fixtures tests they
 * sit beside. Running these (not all 60 files) keeps the matrix under ~15 s while still executing
 * every case that was observed to leak. A file added to this list is a file that failed the outer
 * proof; a file removed from it needs the outer proof re-run.
 */
const SLOT_SENSITIVE_FILES: readonly string[] = [
    'tests/unit/fixtures/fixturesSlot.test.ts',
    'tests/unit/fixtures/manifestPaths.test.ts',
    'tests/unit/runner/actorManifestPath.test.ts',
    'tests/unit/memory/collect.test.ts',
    'tests/unit/memory/container_meta.test.ts',
    'tests/unit/runner/env_flags.test.ts',
    'tests/unit/runner/run_dir.test.ts',
];

/**
 * Every `*.test.ts` under tests/unit/, recursively, as absolute paths.
 *
 * @param {string} dir - Directory to walk.
 * @returns {string[]} Absolute paths.
 * @example
 *   testFilesUnder(UNIT_DIR).length; // > 50
 */
function testFilesUnder(dir: string): string[] {
    return readdirSync(dir).flatMap((name) => {
        const full = path.join(dir, name);
        if (statSync(full).isDirectory()) {
            return testFilesUnder(full);
        }
        return name.endsWith('.test.ts') ? [full] : [];
    });
}

interface SuiteCounts {
    readonly passed: number;
    readonly failed: number;
}

/**
 * Every label vitest's FINAL summary can print, in the order it prints them.
 *
 * READ AT SOURCE, vitest 4.1.11, `node_modules/vitest/dist/chunks/utils.BS4fH3nR.js` `getStateString`:
 * each segment is `n ? … : null`, so **every one of these is conditional — `passed` included** — and the
 * list is `.filter(Boolean).join(" | ")` followed by ` (total)`. There is a SECOND `getStateString`, in
 * `dist/chunks/index.UpGiHP7g.js`, belonging to the TTY-only live reporter, where `passed` is
 * unconditional. That one does not render this line. Reading it instead is how the previous attempt came
 * to require a `passed` segment.
 *
 * `expected fail` is TWO WORDS, and in the same renderer it is EXCLUDED from `passed`, so
 * failed + passed + expected fail + skipped + todo === total. That is what makes the sum check below a
 * real check rather than a restatement.
 */
const SUMMARY_LABELS = ['failed', 'passed', 'expected fail', 'skipped', 'todo'] as const;
const SUMMARY_LABEL_SET: ReadonlySet<string> = new Set<string>(SUMMARY_LABELS);

/** The whole `Tests …` line; group 1 is everything after the word. */
const TESTS_LINE = /^\s*Tests\s+(.+?)\s*$/;
/** Splits `2 failed | 2 passed (4)` into its segment list and its total. `no tests` has no total. */
const SEGMENTS_AND_TOTAL = /^(.*\S)\s+\((\d+)\)$/;
/** One segment: a count then a label, which may contain a space (`1 expected fail`). */
const SEGMENT = /^(\d+) (.+)$/;
/** Colour codes, absent when the child is piped, present if it ever runs on a TTY. */
const ANSI = /\u001B\[[0-9;]*m/g;

/**
 * The last `Tests …` line's content, with colour stripped, or null when the output carries none.
 *
 * THE LAST, never the first: a test that logs a summary-shaped line comes earlier in the stream, and
 * first-match then reads that line as the run's verdict.
 *
 * @param {string} output - The child's combined stdout and stderr.
 * @returns {string | null} Everything after the word `Tests`, trimmed; null if there is no such line.
 *
 * @internal
 */
function lastSummaryLine(output: string): string | null {
    const summaries = output
        .replace(ANSI, '')
        .split('\n')
        .filter((line) => TESTS_LINE.test(line));
    const last = summaries.at(-1);
    return last === undefined ? null : (TESTS_LINE.exec(last)?.[1] ?? null);
}

/**
 * The `n label` segments of a summary line, keyed by label.
 *
 * An ALLOWED-LABEL SET, not "anything that is not `failed` is `passed`": a label this vitest does not
 * print is a version we have not read, and guessing its arithmetic is how the previous defect began.
 *
 * @param {string} segmentsText - The `|`-separated segment list, without the total.
 * @returns {Map<string, number> | null} Counts by label, or null on an unknown label, a repeated label,
 *   or a segment that is not `<digits> <label>`.
 *
 * @internal
 */
function parseSegments(segmentsText: string): Map<string, number> | null {
    const counts = new Map<string, number>();
    for (const raw of segmentsText.split('|')) {
        const segment = SEGMENT.exec(raw.trim());
        const count = segment?.[1];
        const label = segment?.[2];
        if (count === undefined || label === undefined) {
            return null;
        }
        if (!SUMMARY_LABEL_SET.has(label) || counts.has(label)) {
            return null;
        }
        counts.set(label, Number(count));
    }
    return counts;
}

/**
 * Whether the segments account for every test vitest counted.
 *
 * `expected fail` is EXCLUDED from `passed` by the renderer, so a real summary satisfies
 * failed + passed + expected fail + skipped + todo === total. A line that does not is not the shape the
 * label set describes, and a partial reading of it would be worse than no reading.
 *
 * @param {Map<string, number>} counts - Counts by label.
 * @param {string} totalText - The digits inside the trailing `(…)`.
 * @returns {boolean} True when the segments sum exactly to the total.
 *
 * @internal
 */
function sumsToTotal(counts: Map<string, number>, totalText: string): boolean {
    let sum = 0;
    for (const value of counts.values()) {
        sum += value;
    }
    return sum === Number(totalText);
}

/** vitest's summary block opens with this line; the run's real `Tests` line is the next one after it. */
const TEST_FILES_LINE = ' Test Files ';

/**
 * Read `{ passed, failed }` from a child vitest run's OUTPUT — the function `childSuiteCounts` calls.
 *
 * PRIOR BEHAVIOUR (round 1 of this ticket, NO GO): the last `Tests`-shaped line of `stdout + stderr`
 * joined. MEASURED, and this is why it failed: a `Tests`-shaped line reaches stderr in at least two
 * ordinary ways, and both come AFTER the real summary in that join —
 *   S17  a test calls `console.error('      Tests  5 passed (5)')`  -> the last line is that, so a child
 *        with 1 failure read `{ passed: 5, failed: 0 }`;
 *   S18  an ordinary MULTI-LINE string diff prints its unchanged context lines, so a fixture whose middle
 *        line is `      Tests  9 passed (9)` puts that on stderr -> `{ passed: 9, failed: 0 }`.
 * Both captured from real vitest 4.1.11; the outputs are in
 * `5_Project_History/2026-09-25_seatL6/evidence/vitest-capture-round2/`.
 *
 * THE RULE NOW: take the `Tests` line that follows the LAST ` Test Files ` line. vitest prints that block
 * once, at the end, so a line a TEST emitted — on either stream — is always before it. MEASURED on 14
 * captured shapes, including one where a test deliberately logs BOTH a ` Test Files ` line and a `Tests`
 * line to stdout (S19): the rule still reads the real summary.
 *
 * `childSuiteCounts` passes `result.stdout` alone, so stderr cannot reach this at all. The anchor is
 * nevertheless applied to whatever it is given, and is measured to hold on the JOINED text too — belt and
 * braces, because the round-1 defect was exactly someone joining the streams.
 *
 * @param {string} output - The child's stdout (or any text containing its summary block).
 * @returns {SuiteCounts | null} The counts, or null when there is no summary block to vouch for.
 * @example
 *   readChildOutput(stdoutOfAChildThatFailedOnce); // { passed: 1, failed: 1 }
 */
export function readChildOutput(output: string): SuiteCounts | null {
    const lines = output.replace(ANSI, '').split('\n');
    let anchor = -1;
    for (let i = 0; i < lines.length; i += 1) {
        if ((lines[i] ?? '').includes(TEST_FILES_LINE)) {
            anchor = i;
        }
    }
    if (anchor < 0) {
        return null;
    }
    for (const line of lines.slice(anchor + 1)) {
        if (TESTS_LINE.test(line)) {
            return readSuiteCounts(line);
        }
    }
    return null;
}

/**
 * Read `{ passed, failed }` out of a child vitest run's own output, or `null` when the output carries no
 * summary this function is willing to vouch for.
 *
 * Pure, and exported to the suite, so a cell can feed it REAL CAPTURED OUTPUT rather than a line composed
 * to match the parser. Every fixture in the cells below was captured from vitest 4.1.11 with
 * `--reporter=default`, piped, from throwaway projects outside this package.
 *
 * PRIOR BEHAVIOUR: one regex, `Tests\s+(?:(\d+) failed \| )?(\d+) passed \((\d+)\)`. It REQUIRED a
 * `passed` segment, so every real summary without one — `1 failed (1)`, `1 skipped (1)`, `1 todo (1)`,
 * `1 expected fail (1)` — read as no match at all, and the caller then blamed the parser for a child where
 * everything failed: exactly the case the reading has to survive. It also took the FIRST match, so an
 * earlier console line spelling `Tests  5 passed (5)` was read as the summary of a run that had failures.
 *
 * @param {string} output - The child's combined stdout and stderr.
 * @returns {SuiteCounts | null} The counts, or null if there is no summary, the total is missing (`no
 *   tests`), a label is not one vitest prints, a label repeats, or the segments do not sum to the total.
 * @example
 *   readSuiteCounts('      Tests  1 failed (1)'); // { passed: 0, failed: 1 }
 */
export function readSuiteCounts(output: string): SuiteCounts | null {
    const line = lastSummaryLine(output);
    if (line === null) {
        return null;
    }
    const split = SEGMENTS_AND_TOTAL.exec(line);
    const segmentsText = split?.[1];
    const totalText = split?.[2];
    if (segmentsText === undefined || totalText === undefined) {
        // `Tests  no tests` — vitest prints this for zero tasks, with no total. Nothing to vouch for.
        return null;
    }
    const counts = parseSegments(segmentsText);
    if (counts === null || !sumsToTotal(counts, totalText)) {
        return null;
    }
    return { passed: counts.get('passed') ?? 0, failed: counts.get('failed') ?? 0 };
}

/**
 * Run the slot-sensitive files as a child vitest with exactly the given slot variables and return
 * vitest's own `Tests` totals, parsed from its summary line.
 *
 * @param {Record<string, string>} vars - The slot family for the child's shell (empty = no slot).
 * @returns {SuiteCounts} `{ passed, failed }` as `readSuiteCounts` reads them from the child's output.
 * @example
 *   childSuiteCounts({ SECUURA_STACK_SLOT: '2' }).failed; // 0
 */
function childSuiteCounts(vars: Record<string, string>): SuiteCounts {
    const env = envWithoutSlot(vars);
    // vitest marks its own worker processes; the child is a fresh top-level run, not a worker.
    Reflect.deleteProperty(env, 'VITEST');
    Reflect.deleteProperty(env, 'VITEST_WORKER_ID');
    Reflect.deleteProperty(env, 'VITEST_POOL_ID');
    const result = spawnSync(
        VITEST_BIN,
        ['run', '--config', 'vitest.unit.config.ts', '--reporter=default', ...SLOT_SENSITIVE_FILES],
        { env, cwd: PACKAGE_ROOT, encoding: 'utf8', timeout: 180_000 },
    );
    // STDOUT ALONE. stderr carries `Tests`-shaped lines that are not the summary — a test's own
    // console.error, and the context lines of an ordinary multi-line string diff — and reading the two
    // joined is what made round 1 report a clean run for a child that had failures.
    const counts = readChildOutput(result.stdout);
    if (counts === null) {
        const tail = `${result.stdout}\n${result.stderr}`.slice(-1500);
        throw new Error(`could not read the child vitest summary:\n${tail}`);
    }
    return counts;
}

describe('unit-suite slot independence', () => {
    it('no test file spawns a child on a bare process.env spread — envWithoutSlot() is the only door', () => {
        const offenders = testFilesUnder(UNIT_DIR)
            // This file describes the pattern in its own header; it spawns only through envWithoutSlot().
            .filter((file) => file !== SELF)
            .filter((file) => /\.\.\.process\.env\b/.test(readFileSync(file, 'utf8')))
            .map((file) => path.relative(PACKAGE_ROOT, file));
        expect(offenders, 'route through tests/unit/support/slotEnv.ts').toEqual([]);
    });

    it('the strip is wired to run BEFORE each test file is imported', () => {
        // A source pin, deliberately: the behavioural proof is the matrix below, which goes red the
        // moment this line is removed (run_dir.ts freezes its slot at import).
        const config = readFileSync(path.join(PACKAGE_ROOT, 'vitest.unit.config.ts'), 'utf8');
        expect(config).toMatch(/setupFiles:\s*\[\s*'\.\/tests\/unit\/support\/clearSlotEnv\.setup\.ts'\s*\]/);
        // And it ran for THIS file too: whatever the shell exported, the slot family is gone here.
        for (const key of ['SECUURA_STACK_SLOT', 'STACK_SLOT', 'SECUURA_ARTIFACT_SUFFIX', 'PERF_BASE_URL']) {
            expect(process.env[key], key).toBeUndefined();
        }
    });

    it('the slot-sensitive files pass identically from a shell on NO slot and on every slot — the measured regression', () => {
        const baseline = childSuiteCounts({});
        expect(baseline.failed, `the unslotted run is red on its own: ${JSON.stringify(baseline)}`).toBe(0);
        expect(baseline.passed, 'the child ran a real suite').toBeGreaterThan(100);
        for (const slot of SLOTS) {
            const shapes: Record<string, string>[] = [
                { SECUURA_STACK_SLOT: String(slot) },
                { STACK_SLOT: String(slot) },
                // What slot-target.sh exports: the slot AND its artefact suffix.
                { SECUURA_STACK_SLOT: String(slot), SECUURA_ARTIFACT_SUFFIX: `-slot${String(slot)}` },
            ];
            for (const vars of shapes) {
                expect(childSuiteCounts(vars), JSON.stringify(vars)).toEqual(baseline);
            }
        }
    });
});

/**
 * Every fixture below is CAPTURED, not composed: each string is the `Tests` line vitest 4.1.11 actually
 * printed for a throwaway project OUTSIDE this package, run with `--reporter=default` and piped, on
 * 2026-09-25. The captures and the fixtures that produced them are in
 * `5_Project_History/2026-09-25_seatL6/evidence/vitest-capture/`.
 *
 * Shapes captured: fail-only, skip-only, todo-only, expected-fail-only, pass-only, all-failed, every label
 * at once, the two-line case, and `no tests`.
 *
 * Shapes deliberately NOT captured, and why:
 * - a TTY run (colour codes present): the caller pipes, and `ANSI` strips them unconditionally, so the
 *   difference cannot reach the parse. Stated rather than claimed as covered.
 * - `--reporter` other than `default`: the caller passes `--reporter=default` explicitly.
 * - a vitest other than 4.1.11: the label set is read from THIS version's renderer, and an unknown label
 *   is exactly what returns null rather than a guess.
 */
const CAPTURED = {
    failOnly: '      Tests  1 failed (1)',
    skipOnly: '      Tests  1 skipped (1)',
    todoOnly: '      Tests  1 todo (1)',
    expectedFailOnly: '      Tests  1 expected fail (1)',
    passOnly: '      Tests  1 passed (1)',
    allFailed: '      Tests  3 failed (3)',
    mixed: '      Tests  1 failed | 2 passed | 1 skipped | 1 todo (5)',
    everyLabel: '      Tests  2 failed | 2 passed | 1 expected fail | 2 skipped | 1 todo (8)',
    noTests: '      Tests  no tests',
    /** A test that logs a summary-shaped line, then a real summary with a failure. Both lines, in order. */
    twoLine: ['      Tests  5 passed (5)', '', '      Tests  1 failed | 1 passed (2)'].join('\n'),
} as const;

describe('KS-1313: readSuiteCounts reads every real vitest summary, or says it cannot', () => {
    it.each([
        { label: 'fail-only', text: CAPTURED.failOnly, want: { passed: 0, failed: 1 } },
        { label: 'skip-only', text: CAPTURED.skipOnly, want: { passed: 0, failed: 0 } },
        { label: 'todo-only', text: CAPTURED.todoOnly, want: { passed: 0, failed: 0 } },
        { label: 'expected-fail', text: CAPTURED.expectedFailOnly, want: { passed: 0, failed: 0 } },
        { label: 'pass-only', text: CAPTURED.passOnly, want: { passed: 1, failed: 0 } },
        { label: 'all-failed', text: CAPTURED.allFailed, want: { passed: 0, failed: 3 } },
        { label: 'mixed', text: CAPTURED.mixed, want: { passed: 2, failed: 1 } },
        { label: 'every label', text: CAPTURED.everyLabel, want: { passed: 2, failed: 2 } },
    ])('reads a captured $label summary', ({ text, want }) => {
        // The first four are the shapes the previous attempt returned null for: they carry NO `passed`
        // segment, and the final-summary renderer emits `passed` only when it is non-zero.
        expect(readSuiteCounts(text)).toEqual(want);
    });

    it('takes the LAST Tests line, so a logged lookalike is not read as the summary', () => {
        // Captured: a test that console.logs `      Tests  5 passed (5)` before a run that then fails.
        // First-match reads {5,0} — a silent wrong answer on a run with a failure, which is worse than null.
        expect(readSuiteCounts(CAPTURED.twoLine)).toEqual({ passed: 1, failed: 1 });
    });

    it.each([
        { label: 'no Tests line at all', text: 'some other output\n' },
        { label: 'the captured `no tests` line', text: CAPTURED.noTests },
        { label: 'segments that do not sum to the total', text: '      Tests  1 failed | 1 passed (5)' },
        { label: 'a label vitest does not print', text: '      Tests  1 flaky (1)' },
        { label: 'a repeated label', text: '      Tests  1 passed | 1 passed (2)' },
        // This row exists because a tamper found nothing to break. Dropping the duplicate check left the
        // whole set green: with duplicates allowed the Map simply overwrites, and `1 passed | 1 passed (2)`
        // then sums to 1 against a total of 2, so the SUM check rejected it anyway. The duplicate check was
        // therefore not load-bearing and a later edit could have dropped it in silence. This shape is the
        // one where it is: the second value overwrites the first so the sum DOES reach the total.
        { label: 'a repeat that survives the sum check', text: '      Tests  2 passed | 1 passed (1)' },
        { label: 'a segment with no count', text: '      Tests  passed (1)' },
    ])('returns null on $label', ({ text }) => {
        // Null is the honest answer; the caller turns it into a loud throw carrying the output tail.
        expect(readSuiteCounts(text)).toBeNull();
    });

    it('the sum check is a real check: every captured shape satisfies it', () => {
        // If `expected fail` were counted inside `passed`, `everyLabel` would sum to 9 against a total of 8
        // and would be rejected. It is excluded (read at source), so the check passes on real output and
        // still rejects the malformed rows above. Without this cell the sum rule could be vacuous.
        expect(readSuiteCounts(CAPTURED.everyLabel)).toEqual({ passed: 2, failed: 2 });
        expect(
            readSuiteCounts('      Tests  2 failed | 2 passed | 1 expected fail | 2 skipped | 1 todo (9)'),
        ).toBeNull();
    });

    it.each([
        {
            label: 'S17 stdout — a run whose test console.errored a lookalike',
            text: S17_STDOUT,
            want: { passed: 1, failed: 1 },
        },
        {
            label: 'S17 JOINED as the caller used to join them',
            text: `${S17_STDOUT}\n${S17_STDERR}`,
            want: { passed: 1, failed: 1 },
        },
        { label: 'S18 stdout — a multi-line string diff', text: S18_STDOUT, want: { passed: 1, failed: 1 } },
        { label: 'S18 JOINED', text: `${S18_STDOUT}\n${S18_STDERR}`, want: { passed: 1, failed: 1 } },
        { label: 'S19 stdout — a test logs a Test Files line too', text: S19_STDOUT, want: { passed: 1, failed: 1 } },
        { label: 'S10 stdout — the ticket mixed line', text: S10_STDOUT, want: { passed: 3, failed: 2 } },
    ])('KS-1313 whole-run: readChildOutput reads $label', ({ text, want }) => {
        // These are COMPLETE captured runs, not summary lines. Round 1 was proven against lines and the
        // defect lived in WHICH line of a whole run gets picked, so the regression cells have to be runs.
        // The three adversarial ones each put a Tests-shaped line where the round-1 rule would take it:
        // S17 via console.error, S18 via a diff's unchanged context lines, S19 via a logged anchor.
        expect(readChildOutput(text)).toEqual(want);
    });

    it('KS-1313 E5: a failing child whose stderr carries a lookalike reports the FAILURE, not a clean run', () => {
        // The cost the gate named: childSuiteCounts read {5,0} for this child, so a run with a real
        // failure was reported as a clean pass. This is the same captured run, read the new way.
        const counts = readChildOutput(S17_STDOUT);

        expect(counts).not.toBeNull();
        expect(counts?.failed, 'a child with a failing test must not read as zero failures').toBe(1);
        // And the round-1 answer is named, so a regression cannot be mistaken for a different number.
        expect(counts).not.toEqual({ passed: 5, failed: 0 });
    });

    it('KS-1313 the anchor is what does it: without a Test Files block there is nothing to vouch for', () => {
        // CONTROL for the cells above. If readChildOutput ignored the anchor and simply took the last
        // Tests-shaped line, this would return {5,0} instead of null — which is exactly round 1.
        expect(readChildOutput('      Tests  5 passed (5)\n')).toBeNull();
        expect(readChildOutput('no summary here at all\n')).toBeNull();
    });

    it('the call site still goes through readChildOutput — behaviourally, not by reading the source', () => {
        // The gate asked for this to be BEHAVIOURAL rather than a text pin, and it is right: a text pin
        // passes for a call site that calls the function and ignores its answer. readChildOutput is pure
        // and exported, so the property "the call site's reading is this function's reading" is checked
        // by giving that function the real captured output of the same kind of child and asserting the
        // answer the call site would then return.
        //
        // The text pin is kept BESIDE it, not instead of it: it is what notices an inline regex creeping
        // back in, which the behavioural cell alone cannot see.
        expect(readChildOutput(S17_STDOUT)).toEqual({ passed: 1, failed: 1 });

        const own = readFileSync(SELF, 'utf8');
        const body = own.slice(own.indexOf('function childSuiteCounts('));
        const end = body.indexOf('\ndescribe(');
        const callSite = end > 0 ? body.slice(0, end) : body;

        expect(callSite).toContain('readChildOutput(result.stdout)');
        // CONTROL: the same search for a call that is NOT there must fail, so a pass above means something.
        expect(callSite).not.toContain('readChildOutput(somethingElse)');
        // And the joined-streams read that caused round 1 must not have come back.
        expect(callSite).not.toMatch(/readChildOutput\(`\$\{result\.stdout\}/);
    });
});
