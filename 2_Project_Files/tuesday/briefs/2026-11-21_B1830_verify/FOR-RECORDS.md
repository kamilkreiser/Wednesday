FOR RECORDS (what a records pass should file after the OXPd 2 contracts lane lands; nothing below was decided by the
product owner except where his words are quoted; every other line is decided by nobody until a records pass or a kit
settles it)

1. THE PROJECT RULE ON SUPPLIED FILES (`<project>/CLAUDE.md:50-51`), still reading, at the time of this gate:
   "Nothing under `Source_Documents/` is ever committed or copied into `2_Project_Files/`." It needs the exception for
   exactly the 37 OXPd 2 specification files listed in `contracts/oxpd2/inputs.sha256` (list sha256
   6760314d9fd8c56bf7ce6b815deb5c26adc78f1098878b06616c4315b5013d7e), and nothing else. The same sentence repeats in
   the 2026-11-20 additions (`CLAUDE.md:86`, "Source_Documents. Nothing under it is committed or copied into the
   repository."): amend both.

2. A CLARIFICATIONS ENTRY for the ruling of 2026-11-21 (none exists: the kit measured 0 hits for "hp files"). His
   words, verbatim, from the live board at 09:40: "hp files have been provided to us. we can store them where we want
   (and will try to do it safely)"; and his choice on card `datasec-oxpd-hp-spec-files-in-repo-1121`, option b, "Keep
   HP's files in the repository" (ruled 09:41:45), whose detail reads "The spec files are committed beside the
   generated code. Simpler to rebuild anywhere, but HP's beta files sit in Datasec's repository." The entry records
   that ruling only; the input set, the generator, the parser limits and the stub are the build's choices (the kit's
   Q1 to Q16 as stamped and the builder's D1 to D11), not his.

3. THE R5 FOLLOW-UP (a `build/**` kit, G1): teach `build/repo_rules.py` R5 to exempt exactly the files that
   `contracts/oxpd2/inputs.sha256` lists, matched by path AND hash, read from the list (not a constant), so a later
   beta's regenerated list carries its own exemption. This lane does not make it harder: the list is a closed,
   path-and-hash list and the 37 R5 lines are set-equal to it. Until it lands, every local R5 run with the supplied
   folder prints those 37 lines (a noisy guard); later kits carry them as the same closed list. **Add to that kit:**
   the R5 hash half must not open the SDK's `tools/certificates/` (HP's development root CA private key): the kit's
   Step 3(e)(i) form hashes it (35223 files against 35215 with it pruned; gate finding F4). The gate's wrapper
   (`/private/tmp/b1830-gate/scratch/item1.py`) prunes it with the repository's code unchanged.

4. THE RUNBOOK (`<project>/SETUP_RUNBOOK.md`) gains: the regeneration test and how to regenerate (`Oxpd2Generator.Generate`
   from a small console outside the repository; never edit `Generated/` by hand); the R5 closed-list exception for the
   37 files; the local restore form `-p:NuGetAudit=false` under the closed proxy (the hosted legs keep the audit); that
   test temp folders `oxpd2-contracts-*` accumulate under the system temp folder (D11).

5. THE README (no lane may edit it): the Layout section gains `contracts/oxpd2/` (HP's 37 inputs, the fingerprint
   list, the generator), `src/Datasec.Suite.Adapters.Oxpd2` (in this cut: only its project file, lock file and
   `Generated/`) and `tests/Datasec.Suite.Contracts.Tests`; ONE README pass after the wave, as before.

6. THE BACKLOG gains (each a follow-up, none blocking):
   a. F1: the four public `IReadOnlyList` members that hand out their arrays (`Oxpd2Schema.Properties`,
      `Oxpd2Schema.EnumValues`, `Oxpd2InboundCatalogue.Operations`, `Oxpd2InboundOperation.RequestContentTypes`)
      wrapped read-only, with a reflection cell.
   b. F2: `ReadBoundedAsync` overflow at a caller limit of `int.MaxValue`: long arithmetic or a bound in the limits
      constructor; an N14 row.
   c. F3: an N9 row for string length in Unicode scalar values (astral characters at `maxLength` and one more).
   d. F6: N15 names that an `IOException` from the body stream passes out of a client method, beside
      `HttpRequestException`.
   e. D11: test temp folders removed (or quarantined) after each test.

7. FOR THE MASTER LIST (`OXPD2-1`), open points for the Datasec team or the build, decided by nobody:
   a. **Enum drift on the callbacks (F5, the first):** an enum value HP's inputs do not list makes the whole inbound
      callback refused (42 enum sites in `jobStatistics` alone); a JSON null for an optional property likewise (D9).
      Consequence for a customer: on a firmware newer than the Beta 10 inputs, job statistics or a sign-in prompt
      result could be refused until the inputs are regenerated. Options: a per-site unknown marker (tolerant), or
      regenerate on every beta with a contract diff that fails the build (`03:141`, `03:235`). What a printer does with
      a refused callback is UNMEASURED.
   b. N11's strict reading of `anyOf [ $ref, {} ]` applies today only to 4xx/5xx bodies, which the clients do not parse;
      if a later lane parses error bodies, the strict reading becomes live.
   c. Credential-shaped fields in device answers (F7: HP's `BearerAuthorization...` family, a `functions/solutionToken`
      operation): the logging deny-list and any store must cover them when WP1.2 consumes the clients.
   d. What the real customer gateway answers to a body with no `realm` (the stub answers 500): UNMEASURED.

8. THE TICKET `OXPD2-9` stays open: contract tests against simulator responses wait for hardware; the 1.x WSDL stubs
   are not this cut. Its second half ("whether HP's specification files themselves may be kept in the repository") is
   answered by the ruling in item 2: a records pass may say so on the ticket.

9. THE LANDING: the head was built on main ddbdf800; main is now bb914334 (the secret store). The merge is clean and
   was measured (tree da108e11, total 894); the pull request's checks must be proved to have built the merge with the
   current main (`pr_retrigger.sh --check`) and the code scan must be green before the squash (`landing.txt`).
