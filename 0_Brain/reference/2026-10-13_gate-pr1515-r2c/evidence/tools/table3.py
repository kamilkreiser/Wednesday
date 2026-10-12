import sys; sys.path.insert(0, '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3/tools')
from harness import *
from table1 import sa, DT, JT
import os
STALE_B = ('index.js', 'index.d.ts', JT)
echo = 'export const e: "a" = "Cannot find module \'@secuura/shared/thing\'";\n'
echo2 = 'type Msg = `Could not find a declaration file for module \'@secuura/shared/thing\'`;\nexport const e: Msg = "nope";\n'
T = [
 ('E1_echo_literal_TS2322_unimported_target_absent', {**base(dist=STALE_B, use=None), 'src/__tests__/echo.test.ts': echo}, None),
 ('E1b_echo_literal_TS2322_BASELINED_target_absent', {**base(dist=STALE_B, use=None), 'src/__tests__/echo.test.ts': echo}, 'dev'),
 ('E1c_echo_literal_complete_build', {**base(use=None), 'src/__tests__/echo.test.ts': echo}, None),
 ('E2_echo_template_type_TS2322_target_absent', {**base(dist=STALE_B, use=None), 'src/__tests__/echo.test.ts': echo2}, None),
 ('E3_LANG_de_env_stale', base(dist=STALE_B), None),
]
for n, f, init in T:
    env = dict(os.environ, LANG='de_DE.UTF-8', LC_ALL='de_DE.UTF-8') if 'LANG' in n else None
    measure(n, f, init_with=init, env=env)
