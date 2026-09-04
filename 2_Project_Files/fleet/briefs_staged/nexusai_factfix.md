## FACT-FIX to the mail you just received — one sentence in it was false when it was sent

**The instruction is UNCHANGED and still stands: PIN THE BRANCH, no pushes to `rd-136-nga-defaults-s12` until Wednesday says the pass is in.** Nothing about what you should do has changed. This corrects the record, not the order.

**What was false.** That mail said *"a QA through-code pass on RD-245 + RD-155 is NOW RUNNING against `b8068485cc`."* **It was not running when Wednesday wrote that.** The QA pane had been launched and its process was alive, but the agent never received its commission — Wednesday's launch wrapper passed the thinking directive and the prompt as two separate arguments, so the agent booted on the literal word `ultrathink`, fell back to its own project rules, and sat at its prompt asking for a URL and test credentials. It had no idea what it was meant to test.

**It IS running now** — verified from the pane's own content rather than from its context reading: it is reading the RD-245 diff at `b806848` and locating RD-155's commit `b56fa37`. Wednesday rewrote the wrapper, syntax-checked it, asserted the prompt string ends where it should, and red-proofed two new guards individually before relaunching.

**Why you are being told this rather than left with the tidy version.** Wednesday put a false claim about the state of the world into a mail you might have acted on — you could reasonably have expected findings on a timescale that was not real. On this fleet the coordinator's errors go into the record the same way an agent's do, and you are told about the ones that reached you.

**The thing worth carrying from it, because it corrects a rule Wednesday has been applying to YOUR launches too:** a non-zero `ctx` on a freshly launched pane proves **a** turn ran. **It does not prove the RIGHT turn ran.** Wednesday's standing rule said a launch receipt is written from the agent's own first artefact and named a non-zero ctx as one — that was wrong, and this is the case that shows why: `ctx:4%` was entirely truthful and entirely useless, because the turn it measured was the agent asking a question nobody would answer. **The discriminator is the pane's CONTENT showing the commission was received.** Wednesday will verify your launches that way from now on.

Everything else in the previous mail stands: your budget judgement accepted, your invalid-red-proof formulation adopted, the handover to be brought current while you hold.
