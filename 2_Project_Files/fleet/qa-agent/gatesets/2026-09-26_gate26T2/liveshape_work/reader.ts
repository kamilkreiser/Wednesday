type SuiteCounts = { passed: number; failed: number };
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
 * vitest's default reporter closes its summary block with `   Start at  HH:MM:SS`, printed only once
 * the run has reached the end. It is the gate's own oracle for "this is the real block", and it is the
 * line a killed child never gets to print.
 */
const SUMMARY_END_LINE = /^\s*Start at\s+\d{1,2}:\d{2}:\d{2}\s*$/;

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
    // ROUND 3, and the anchor MOVED. Round 2 anchored on the LAST ' Test Files ' line and took the
    // first `Tests` line after it. gate24T2c measured what that costs: a child whose test printed a
    // COMPLETE summary-block lookalike to stdout and was then KILLED (status 143, error ETIMEDOUT, no
    // summary of vitest's own) read `{ passed: 7, failed: 0 }` — a CLEAN PASS for a run that never
    // finished. A test can print ' Test Files ' as easily as it can print `Tests`, so that anchor
    // cannot tell vitest's block from a fixture's imitation of it.
    //
    // `   Start at` can too, of course. What it cannot do is appear in the right PLACE: vitest prints
    // it immediately AFTER the `Tests` line of its own block, and only when the run reached the end.
    // So the read is anchored on the LAST `Start at` and walks BACKWARDS to the nearest `Tests` line
    // above it, which is the gate's own independent oracle. A run with no `Start at` never reached its
    // summary and there is nothing to vouch for: null.
    //
    // This is why the H1 family is three cells rather than one. H1b and H1c already read null under the
    // round-2 anchor — for the accidental reason that their lookalikes were incomplete — so only H1
    // discriminates the two anchors, and the other two exist to prove the change did not buy H1 at
    // their expense.
    let anchor = -1;
    for (let i = 0; i < lines.length; i += 1) {
        if (SUMMARY_END_LINE.test(lines[i] ?? '')) {
            anchor = i;
        }
    }
    if (anchor < 0) {
        return null;
    }
    for (let i = anchor - 1; i >= 0; i -= 1) {
        const line = lines[i] ?? '';
        if (TESTS_LINE.test(line)) {
            return readSuiteCounts(line);
        }
        // Only vitest's own `Test Files` line may sit between `Tests` and `Start at`. Anything else
        // means this `Start at` is not the end of a summary block, so the walk stops rather than
        // reaching further back for a line that belongs to something else.
        if (line.trim() !== '' && !line.includes(TEST_FILES_LINE)) {
            return null;
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

