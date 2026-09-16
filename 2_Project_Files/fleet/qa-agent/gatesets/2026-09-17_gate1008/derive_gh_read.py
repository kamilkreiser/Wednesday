#!/usr/bin/env python3
"""derive_gh_read.py — writes gh_read.py for the #1008 set from the sibling tier-1 set's gh_read.py by asserted replacements + a residual guard. Reads only."""
import sys, re
s = open(sys.argv[1]).read()
reps = [
 ('#1006 (KS-844)', '#1008 (KS-1087)', 1),
 ('derived from the #1005 set by sed + one asserted replacement', 'derived from the sibling tier-1 set by asserted replacements', 1),
 ("H = '86fe59e6bf07108142fb3dbd06bef8747d2a4687'", "H = 'dd7086d5aa574285beffc515f9371a438621f25d'", 1),
 ("'/pulls/1006'", "'/pulls/1008'", 1),
 ("'pr1006.json'", "'pr1008.json'", 1),
 ("print('PR #1006'", "print('PR #1008'", 1),
 ("'pr1006_body.md'", "'pr1008_body.md'", 1),
 ("'Closes KS-844', body.count('Closes KS-844')", "'Part of KS-1087', body.count('Part of KS-1087')", 1),
 ("'/pulls/1006/files?per_page=100'", "'/pulls/1008/files?per_page=100'", 1),
 ("'pr1006_files.json'", "'pr1008_files.json'", 1),
 ("'/pulls/1006/commits?per_page=100'", "'/pulls/1008/commits?per_page=100'", 1),
 ("'pr1006_commits.json'", "'pr1008_commits.json'", 1),
 ("'/pulls/1006/reviews'", "'/pulls/1008/reviews'", 1),
 ("'/pulls/1006/comments'", "'/pulls/1008/comments'", 1),
 ("'/issues/1006/comments?per_page=100'", "'/issues/1008/comments?per_page=100'", 1),
 ("'pr1006_issue_comments.json'", "'pr1008_issue_comments.json'", 1),
 ("if p['number'] == 1006: continue", "if p['number'] == 1008: continue", 1),
 ("touch = [n for n in names if n.startswith('services/demo-service/') or n.startswith('packages/shared/src/__tests__/ks727') or n.startswith('packages/shared/src/__tests__/ks781-p3-3') or n.startswith('packages/shared/src/__tests__/entrypoint-corpus') or n.startswith('packages/shared/src/middleware/') or n.endswith('package-lock.json') or '/middleware/errorHandler' in n]",
  "touch = [n for n in names if n.startswith('services/api-gateway/') or n.startswith('services/originate/src/routes/documents') or n.startswith('frontend/issuer/src/components/DocumentList') or n.startswith('services/mcp-server/src/api-client') or n.endswith('package-lock.json') or n == 'eslint.config.mjs']", 1),
 ("'  open #%d head %s base %s files %d | demo-service/guard-file/errorHandler/lockfile overlap %s | %s'", "'  open #%d head %s base %s files %d | api-gateway/originate-documents/consumer/lockfile/eslint overlap %s | %s'", 1),
]
for a, b, n in reps:
    c = s.count(a); assert c == n, (a[:60], c)
    s = s.replace(a, b)
left = [s[m.start()-40:m.start()+20] for m in re.finditer(r'1006|KS-844', s)]
assert not left, ('residual', left)
open(sys.argv[2], 'w').write(s); print('gh_read.py written, replacements', len(reps))
