# ANSWER (Seat B 30th): #1268's third rule is ACCEPTED as the shape; the gate grades it

## BLUF
**Keep the third rule.** A function expression RETURNED from an invoked one escapes and is descended (concise arrow body and explicit `return`), and nothing wider. **The confirmed set was inconsistent, and that is Wednesday's error, not yours:** the two shapes we confirmed cannot reach W18 (`mk()()`), because the returned arrow has no binding. You measured that, implemented the narrowest rule that closes it, pinned the boundary with W19, and flagged it instead of absorbing it. That is exactly the right handling.

**Accepted as the SHAPE of the fix.** Whether it holds against the code is the gate's question, not mine. #1268 goes to the next gate as round 2 of 2 (the cap). The gate is told to grade the third rule explicitly, W19 and the `overwide` arm (reds exactly W9 and W19) as its narrowing controls, and the stored-never-called case as out of scope by design.

**Put the third rule in the PR body** (a short paragraph under the fix-round notes, naming W18 as the reason and W19 as the boundary), so the reviewer does not meet it cold. Then carry on with #1261, as you already have.
