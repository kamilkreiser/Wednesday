# B747 ADDENDUM-1 - main moved after your stamp: #223 and #221 LANDED (read before your REFUSE pins)

From Tuesday s182 (the Datasec coordinator seat), Datasec / HPSM-POC. Written after your stamp (15:48) and before your Step 0. It resolves one conflict inside your kit and changes nothing else.

## What happened (measured by Tuesday 15:58, gh api under the project config)
On the product owner's live-board word ("Skip ci on all of these" 15:52:31, then "Option 2" 15:57:36), Tuesday landed two PRs after turning off main's include-administrators setting for 12 seconds. The setting was restored at 15:58:08; protection now reads enforce_admins true with 5 required contexts.
- **#221** squash `ebff49d5` (merged 04:58:03Z), parent `1523cd2d`: one path, `infra/tests/test_ci_workflow.py`.
- **#223** squash `58a863a07ac97e5ebc0baf3836d6ba1856592520` (merged 04:58:07Z), parent `ebff49d5`: five paths, `ActionPlanEndpoints.cs`, `ReportingEndpoints.cs`, `Requests.cs`, the Assessment `README.md`, `Hpsmpoc343ControlCharacterTests.cs`.
- Main is now `58a863a07ac97e5ebc0baf3836d6ba1856592520`. `compare 1523cd2d...main` reads ahead 2, those 6 paths.
- Tuesday read every one of those 6 blobs on the new main equal to its gated head's blob (`22d5c13c` for #221, `bcb359f8` for #223).

## The conflict, and the ruling
Your REFUSE line on main moving would read NOT GATED, because four moved paths are among your six. Your stacked-head rule (3) says "#223 landed during your gate = NOT a refuse". **Rule (3) governs.** This is exactly the case it was written for.
1. Apply rule (3): prove by program that each of #223's five paths on main `58a863a0` has the blob it has at `bcb359f8`, and that `infra/tests/test_ci_workflow.py` is the only other moved path (#221's; none of your six). Then keep judging the SAME delta `bcb359f8..66bf9aa8` and redo the merge prediction on main `58a863a0`.
2. NOT GATED applies only if a moved path is NOT explained by those two squashes (a blob that differs from `bcb359f8` or `22d5c13c`, or any other path among your guarded list).
3. Your "#223 open and unmoved" field in the verdict line reads "#223 LANDED 58a863a0, blobs equal y/n" instead.
4. FOR TUESDAY: the re-land predicate is now concrete. The three commits are cherry-picked onto main `58a863a0`; write the exact byte-equality commands against that sha.

Everything else in your kit stands.
