From Tuesday (Datasec coordinator seat), Datasec / NexusAI, to SEAT-N128, B1563. ANSWER-1 to your Questions item 1.

## BLUF
YES: file exactly ONE more waiter for the same B1563 chain, with the same tag `b1563-chain`, the same command and the same lock base. That makes two acquisitions in total for this kit. A third needs another answer.

## Why
Run 1 took the lock at 11:14:05 and halted at 11:14:06 on your own instrument (the order of the porcelain string in `lib.sh`), before any jest run, server or inventory drive. You named it in Corrections item 5 and fixed it without touching any code or test file. You checked the fix under bash against old12's real porcelain. Commit A `345cfa2a5b06ae1055a7b08e02959ffb08787709` is unchanged. The cost of run 1 was one second of lock time, so a second acquisition is what HOLD 11's "one acquisition" means to protect: no half-run chain.

## Conditions
1. Before filing: `--plan` on `chain.sh` once more, plus your two guards against old12, so the fixed string is proven on the real tree.
2. The FIFO may now hold other waiters (Datasec/NexusAI-N129 tag `b1567-chain`, Datasec/NexusAI-N130 tag `b1568-chain`). You join at the BACK, never ahead of them. Your hard stop is unchanged (15:30 AEDT). If the FIFO means the chain cannot finish by then, follow the kit's SKIP and HANDOVER rules.
3. Everything else in the kit stands unchanged.

Name this file in ADDENDA READ before you act on it.
