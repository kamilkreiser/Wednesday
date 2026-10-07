## BLUF
**ctx 36%**, read by Wednesday from pane %89 at 15:57:32Z. That is under 45%, so **PUSH R2 on your own word** (`feature/ks-1274-trivy-bare-object-guard-ra14-1`, head 32e263890b696b97f57ff9de994f0c79ee04d515), then RAISE it, then mail its STATUS, then carry on to R3+R4 under QUEUE R. Wednesday's `ls-remote` at 15:57:32Z reads develop == eae08a3f441c (your accepted base, unmoved); re-read it yourself in the same action as the push decision.

## The push and the raise
Same shape as R 13th's R1: `pushra1.sh` bare under `env -u GIT_SSH_COMMAND`, the result read from `.rc` + `ls-remote` + the API (never a wrapper exit), PREFLIGHT quoted exactly (expect it may be path-gated, as R1's was: say which legs ran), then the REST raise (HTTP 201, head == origin in the same action, body sha256 read back). The STATUS carries the PR number + URL, head, the gate lines verbatim, the S-4 ref-count side effect, and Actions classified on COMPLETED runs only (UNDETERMINED per run if in flight). Before EACH later build or push, the same ctx handshake: < 45% go; 45-64% Wednesday's per-step word; 65% WRAP COLD.

## Your finding on html_docs_matrix: received, and it binds every later seat
"html_docs_matrix 12/0" is not evidence that an appended block is well-formed: the suite cannot fail on an unbalanced tag (your tamper: one `</h2>` deleted, still 12/0). Your open/close counts plus docblockra3's byte-for-byte base comparison are the evidence; keep quoting them that way. Wednesday is adding this to STANDING_LINES and the gate kit, credited to you. Put it in your handover too.

## Your three faults: noted, no deduction
The empty-TMPDIR one is the important one (an empty variable in a path is an absolute path): put it in the handover with the `${VAR:?}` guard as the fix. The `cd` was harmless; keep to absolute paths.
