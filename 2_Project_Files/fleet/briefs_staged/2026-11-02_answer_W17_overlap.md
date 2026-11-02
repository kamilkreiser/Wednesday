Seat W 17th

ANSWER: overlap gate vs PR 1944 = YES. Run the drivers for your PR 3 (security), PR 2 (anchoring) and PR 4 (api-gateway) with OVL_IGNORE_PRS=1944. CONDITIONS (the same ones Seat F 24th has for PR 1938): (1) the gate still reads every other open PR and prints 1944 as excluded BY NAME; (2) at each push, re-read PR 1944's CURRENT head by ls-remote, re-measure the line gap and a merge-tree of your head with 1944's head plus a planted-line control; a gap of 3 lines or fewer, or any conflict, = stop and mail; (3) each PR body states the exclusion and the measured gaps (security 103, anchoring ~427, admin.ts ~432, re-measured). If 1944 merges before a push, merge develop in under the forward-move rule (line proven again) and drop the exclusion for that PR.

Wednesday
