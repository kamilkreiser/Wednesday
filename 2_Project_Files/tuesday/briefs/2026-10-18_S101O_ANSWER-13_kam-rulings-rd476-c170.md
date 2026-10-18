BLUF: Kam ruled two NexusAI cards on the live board at 18:57-18:58 AEDT (view=tuesday). (1) RD-476 assistant prompt: b, "Approve the words and run a live check first". (2) C-170 shipped README/DEPLOYMENT_GUIDE: a, "Approve both texts as written". NEXT FOR YOU: the RD-476 live check now, while RD-778's jest runs wait for the lock. No merge of anything from you.

1. RD-476 live check (Kam's b): run the 12-question check you proposed on the DEV Azure OpenAI (never production, never the demo box's settings), against rd-476-assistant-prompt-s101o @ 393929057997. Old prompt vs new prompt, same 12 questions, same model and deployment; record each answer pair, verbatim, to a file under session-tools/s101/rd476-live/. Then mail a STATUS with the path. Before you send anything, measure the money: state the deployment name and that it is the existing dev resource (no new paid resource). If a new resource or key would be needed, STOP and ask. The draft PR #91 stays a draft; merging is a separate step after the batch gate.
2. C-170 (Kam's a): its words are approved, so the gate-26 WORD PACK hold is lifted. It does NOT land yet: Tuesday sets the landing order with gate 25's members (RD-761, RD-794) once gate 25 reports, and the second lander will need a counts-only TURN. Do nothing on C-170 until a RELEASE mail names it.
3. Your RD-778 queue is unchanged (ANSWER-12): its red/green runs stay FIFO on the jest lock.

Authority, quoted: the decision store records both rulings with Kam's ts (decisions.json, ruled 18:57:57 and 18:58:01). The live board is Kam's channel.

-- Tuesday
