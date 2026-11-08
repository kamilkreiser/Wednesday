import difflib,os,subprocess,sys
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator105'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
NEW=BR+'ks_2099_o105_p2_originate_email_smtp_failure_log_redacts_echoed_recipient/'
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
PIN=sys.argv[1]
FP='Blockchain/Dev/services/originate/src/services/email.ts'
TF='Blockchain/Dev/services/originate/src/__tests__/ks2099-email-smtp-failure-log-never-carries-an-echoed-recipient-address.test.ts'
tip=subprocess.run(['git','-C',S,'show',PIN+':'+FP],capture_output=True,text=True).stdout
L=tip.split('\n')
OLD="    console.error(`[Email/SMTP] Failed to send: ${error.message}`);"
assert L[209]==OLD,L[209]
NEWL=["    // KS-2099 item 1: an SMTP server echoes the recipient in its refusal (and nodemailer builds `Invalid recipient \"addr\"`), so any address-shaped token is replaced before the text is logged.",
"    console.error(`[Email/SMTP] Failed to send: ${String(error.message).replace(/[^\\s<>\"',;:()[\\]]+@[^\\s<>\"',;:()[\\]]+/g, '[address]')}`);"]
new='\n'.join(L[:209]+NEWL+L[210:])
ud=list(difflib.unified_diff(tip.splitlines(True),new.splitlines(True),n=3))
prod='--- a/%s\n+++ b/%s\n'%(FP,FP)+''.join(ud[2:])
test=open(O+'/gen/p3/test.ts').read().rstrip('\n').split('\n')
tsec='diff --git a/%s b/%s\nnew file mode 100644\n--- /dev/null\n+++ b/%s\n@@ -0,0 +1,%d @@\n'%(TF,TF,TF,len(test))+''.join('+'+l+'\n' for l in test)
os.makedirs(NEW,exist_ok=True)
open(NEW+'golden.diff','w').write('diff --git a/%s b/%s\n'%(FP,FP)+prod+tsec)
md='''# KS-2099 item 1 originate: the SMTP failure line of `sendEmail` in `src/services/email.ts` must not print the recipient address an SMTP server echoes in its refusal (RUNG 3, code_patch2: 1 product hunk given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 105 for Wednesday, 2026-11-09 AEDT, on Wednesday's priority request. Secuura (originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-2099 item 1 (gate 235 finding F2, MEDIUM, MEASURED AT RUNTIME with a loopback SMTP stub and nodemailer 10.2.1): PR 2056 (KS-1937, `90b500e19883`) took the recipient address out of ten originate log lines, but the SMTP failure line prints `error.message`, and an SMTP server echoes the address in its refusal (`Can't send mail - all recipients were rejected: 550 5.1.1 <addr>: Recipient address rejected: User unknown`); nodemailer builds `'Invalid recipient ' + JSON.stringify(address)`. This brief changes ONE log line in ONE file, inline, no helper. Item 2 (thirdPartyVerifiers.ts) and item 3 (PR 2094, cells E8/E9 in the ks1937 test file, test-only) are NOT part of this brief. No open PR lists `email.ts`: PR 2094 changes only `ks1937-email-service-logs-never-carry-the-recipient-address.test.ts`; this brief's cells live in a NEW test file with its own cell ids E10 to E12, so they cannot collide with PR 2094's E8/E9.

File: `%s`  (product, modified in place: EXACTLY 1 hunk)
Test file: `%s`  (NEW file, jest, given in full below; 6 cells: C1 and C2 controls, E10 and E11 red, E12 green)
Tip: `%s` (origin develop; every line number and quote below was read from it)
Runner: `jest` (`npx jest src/__tests__/ks2099-email-smtp-failure-log-never-carries-an-echoed-recipient-address.test.ts` from `Blockchain/Dev/services/originate`)
Tier: `code_patch2`
Rung: **3 (1 product hunk, skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `%s` - modified in place: EXACTLY the 1 hunk under "The exact change", byte for byte.
2. `%s` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,%d @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

`sendEmail` logs a failed SMTP send as `console.error(`[Email/SMTP] Failed to send: ${error.message}`)` (line 210). nodemailer and the SMTP server put the recipient's address INTO that message (a refused recipient is echoed as `<addr>`; an invalid one as `Invalid recipient "addr"`), so the address that KS-1937 removed from the other lines still reaches the log here. The fix keeps the line and its text, and replaces every address-shaped token in the message with the word `[address]` before printing: `String(error.message).replace(/[^\\s<>"',;:()[\\]]+@[^\\s<>"',;:()[\\]]+/g, '[address]')`. The address still reaches the mailer (`to: options.to` is untouched); only the log changes. Every message with no address in it prints exactly as before (for an absent message `String(undefined)` is the same word the template printed).

## Where

`%s`: line 210 (the `catch (error: any)` of `sendEmail`, after `transport.sendMail`). CALLERS: `sendEmail` is called by this module's own notification helpers, awaited by the certification, revocation and sharing routes; the return value (`false`) does not change. WHAT AN ORDINARY ERROR GETS: logged at error level with its message, `sendEmail` answers false. After: the same, with any address replaced. **BEHAVIOUR CHANGE the raise PR must state:** a failed SMTP send no longer logs an email address that the server echoed; nothing else changes. Persisted state: none. NOTE for the raise seat: held READY KS-1868-O105-P1 (same file, a thrown-value guard on three catches) edits the same catch at the same line, so the two hunks overlap there; raise one after the other and re-apply.

## The exact change

EXACTLY 1 hunk in the product file. The file header lines and the `@@` headers are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/%s b/%s`).**

```diff
%s```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any other catch block of the file, any other log line, or any other line.

## The test

File: `%s`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The harness is copied from the merged sibling `ks1937-email-service-logs-never-carry-the-recipient-address.test.ts` (the real email module re-required per cell through `jest.isolateModules`, only `nodemailer` and `@azure/communication-email` replaced, every argument of every console call recorded); pinned ref `Blockchain/Dev/services/originate/src/__tests__/ks1937-email-service-logs-never-carry-the-recipient-address.test.ts`. The test file contains backslashes, quotes and template strings: keep every character exactly as given.

```diff
%s```

## Red cells
- E10 RED
- E11 RED

## Cells and controls

- RED at the tip, GREEN after: `E10` (the server echoes the address in angle brackets in its refusal) and `E11` (nodemailer's `Invalid recipient "addr"` shape). At the tip the failed line carries the address, so `leaks()` is not empty; after the edit it carries `[address]` and the rest of the server text.
- GREEN at the tip and after: `C1` (the capture sees an address on the console channel), `C2` (an SMTP failure text with no address is logged as it was), `E12` (the address still reaches `sendMail` as `to`).

## Premises (each one measured, with where)

- Premise: `email.ts` line 210 is `    console.error(`[Email/SMTP] Failed to send: ${error.message}`);` at `%s` (read with `git show`); KS-2099 item 1 quotes the same line at `90b500e19883` and the runtime print from gate 235.
- Open PRs: 43 read 2026-11-09 via the GitHub REST API (pulls?state=open, then pulls/N/files); none lists `Blockchain/Dev/services/originate/src/services/email.ts` or the new test file (311 file entries; planted control services/originate appears in 8 file entries). PR 2094 lists only the ks1937 email test file.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator and proved by the harness `--control` run, not by this text. A real SMTP server's echo shapes beyond the two in the cells (a quoted display name, an address in a response code line) are not measured. The ACS error object, `err?.message` in the ACS send catch and the WARN lines are the same class and are NOT touched. tsc and eslint on the new file were not run outside the checker.

## Scope

**This one line only.** Refs KS-2099 (item 1); does NOT close it; no new helper, no other site.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
'''%(FP,TF,PIN,FP,TF,len(test),FP,FP,FP,prod,TF,tsec,PIN[:12])
open(NEW+'KS-2099.md','w').write(md)
open(NEW+'spark.pins','w').write('''# code_patch2: email.ts (1 hunk) + a NEW test file; ref = shape only; line = the first changed line.
tier=code_patch2
ref=Blockchain/Dev/services/originate/src/__tests__/ks1937-email-service-logs-never-carry-the-recipient-address.test.ts
line=210
ctx=65536
started_ok=KS-2099_item_1_only;_Wednesday_priority_request;_ticket_In_Progress_item_1_unfixed_per_PR_2094_comment;_email.ts_in_no_open_PR_(43_PRs_311_files_read_2026-11-09_by_op105,_planted_control_services/originate_in_8_entries);_overlaps_held_O105-P1_at_line_210
''')
print(prod)
