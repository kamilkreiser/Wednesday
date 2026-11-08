src=open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator106/gen/mkdoc.py',encoding='utf-8').read()
head=src.split('# ---- KS-2107')[0]
exec(head)
RF=B+'sdk/javascript/README.md'
orr=rd('README.md')
nr=rep(orr,"// Approve a transfer\n","// NOTE: the transfer write routes (initiate, approve and cancel) refuse every API key with 403 (KS-2081).\n// Build the client with an accessToken for these calls, not with the apiKey from Quick Start.\n\n// Then approve it\n")
nr=nr  # one edit point only
brief('ks_2117_o106_p1b_sdk_readme_transfer_calls_need_an_access_token','KS-2117',
 'KS-2117 pass 1 (rebuilt brief): the JavaScript SDK README sets up an API key and then shows transfer calls that PR 2077 now answers with 403 (DOC-ONLY: sdk/javascript/README.md)',
 'KS-2117 (seat S 38th filing, 2026-11-09; Backlog; Low; from gate 240 F1). Pass 1 of 2; pass 2 (O106-P2) is the SDK docstrings in src/modules/transfers.ts. The first draft of this brief (two hunks, with markdown code-fence lines in their context) failed its control at A1/A2a/A5 because fence lines inside a diff block break the one-fenced-block check; this version has one hunk whose context holds no fence line. It is the same round-1 ticket pass, not a rebrief: nothing was sent to the model',
 [RF],
 'PR 2077 (KS-2081) made the six transfer write doors refuse every API key with 403. `sdk/javascript/README.md` Quick Start (lines 18-29) builds a client with `apiKey`, and "Transfers & Delegations" (line 128 on) then shows `client.transfers.initiate` and `client.transfers.approve`. A reader who follows both gets 403. `src/client.ts` sends the key as `X-Api-Key` when no access token is set; `src/modules/transfers.ts` posts to `/api/transfers/initiate`, `/api/transfers/{id}/approve` and `/api/transfers/{id}/cancel`. The 403 is measured at the transfer service by gate 240; the SDK path itself is read, not run.',
 'ONE edit point, inside the existing ```typescript example under "Transfers & Delegations", between the `initiate` call and the `approve` call. The comment line `// Approve a transfer` (line 139) is replaced by FOUR lines: a two-line NOTE comment, a blank line, and the comment `// Then approve it`. No code line of the example changes. The new text is in the diff below, verbatim.',
 dd(RF,orr,nr),
 "expect_absent: `// Approve a transfer`\nexpect_present: `refuse every API key with 403 (KS-2081).`\nexpect_present: `// Build the client with an accessToken for these calls`\nexpect_present: `// Then approve it`\n",
 'No SDK run, no request sent. The Quick Start line `// Initialize with API key` is left unchanged (its context holds a code fence, which breaks the diff block). Whether the other SDK modules or any docs site carry an API-key example on these doors is not searched (the ticket says the same). The docstrings in src/modules/transfers.ts are pass 2.')
