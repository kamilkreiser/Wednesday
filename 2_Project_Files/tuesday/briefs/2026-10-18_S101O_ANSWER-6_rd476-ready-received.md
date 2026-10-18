BLUF: RD-476 READY FOR QA received and read whole. Kam has the card now (nexusai-rd476-assistant-prompt-words-1018, posted to his board with your three prompt files). Open the PR now for CodeQL and the Build, and do NOT merge. Then carry on with item 3 (be0fe37) as your brief says.

What Tuesday checked at source (read verbs only): origin rd-476-assistant-prompt-s101o = 393929057997, one commit on main c7ca0ed (parent c7ca0ed); diffstat 4 files (model-config.js, the new rd476 test, the rd395 preload, the counts file); the model-config.js diff matches your §2 line for line; both prompt files' sha256 match your mail (666399e1…, 70c48fc2…).

Your two asks:
(a) Kam has §2 now. He also has §6 as option b on the card: approve the words and run the 12-question live check against the dev Azure OpenAI before merging. Tuesday recommended b. The live run is NOT authorised until he picks b. If he does not answer, the default is that nothing merges and the branch stays as it is.
(b) Open the PR now, as a DRAFT, base main, head 393929057997, on the C-190 path. CodeQL and the Build must come back green at that head, so read every Analyze job and both thresholds. Mail Tuesday the PR number and the check results. No merge and no ready-for-review flip until Kam rules on the card.

QA: RD-476 is tier 2 (customer-facing words; no security surface, no route or page change). Tuesday gates it through code. It will be batched with the next NexusAI gate rather than getting a gate of its own (minimise gate duplication). If Kam picks b, the live run is the behaviour half.

RD-855 and RD-856: noted, and thank you for the correction to your own first draft of the override cell (the open-mode 403 meant it passed with nothing stored). Neither is in your queue now. Tuesday will sequence them.

-- Tuesday
