# Gate PR #1489 (KS-1305) head 80be89ee8c1809cf47c6181095bd8f5d22f8c243 -- GO WITH NOTE
Bundle sha256 4a61011b5a51123d OK; reconstructed. Develop (40ed3573) is an ancestor -> merge trivial, tree == head.
But head sits on a 24-commit unmerged stack (parent 524db0ce6 KS-1124): the PR's own diff is only 80be89ee; it cannot merge before the stack.
Ran: seat cells 9/9; originate 98/1116; tsc 0; eslint 0 errors; real e2e (MODULE_NOT_FOUND -> npm run generate rc0 -> function, staging gone, rerun/other cwd/spaces/x2,x4 concurrent OK; invalid schema rc1, staging removed, no client).
Mutations (7 own): 6 red; signal-null-status->0 survives (test gap).
Defects (all Minor):
1. prisma-generate.cjs:68-75: SIGINT/SIGTERM skips finally -> node_modules/.generate left behind (rc 130/143); SIGTERM orphans prisma child. Next run cleans.
2. :66-69: pre-existing symlinked .generate: link removed, target survives but target/schema.prisma overwritten. Needs node_modules write access.
3. :79: OK only checks default.js exists; exit-0-without-writing passes if stale client present.
4. :65: .generate being a file -> uncaught stack, rc1.
5. :86: path.relative from another drive/cwd prints ../../.. noise.
6. test: no cell for prisma killed by signal (status null->1 unguarded).
