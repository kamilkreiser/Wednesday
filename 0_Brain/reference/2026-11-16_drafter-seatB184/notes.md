# notes.md: drafter for Seat B 184th (2026-11-16 04:2x to 04:41 AEDT)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatB184_merge.md (49,993 bytes, under the 50 KB cap after trimming; the first draft was 56 KB).
Scripts (session scratchpad, not durable): /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/cb1c74cc-6aba-47b1-a2ff-11511ec82c21/scratchpad/{fetch,api,kfetch,mt,plant2,pairs,gates,dnm,kit,nb,dt,eng,matcher,lin,lin2}.*
Clone: _work/d here (local clone of the 2026-11-15 drafter's clone; origin HTTPS, push URL no_push_drafter_b184). Nothing written under !CODING; GitHub and Linear read-only.

## Measured
- develop 42e242166f892e44b71c9f05d386215e3d7cf06a (PR 2245 squash, 17:12:15Z, ONE parent 701dfdd5b874, tree 7680a03cea6d), unmoved 04:26 to 04:38.
- Partition: K 31st HANDOVER line 7 order list; entry 27 = 2087; 25 rows to 2191. All 25 and all 26 K rows open, unmerged, heads equal queue_table_k31.txt. No removed row.
- Ordinal: `Seat B 184th` 0, `Seat B 183rd` 1 (line 139), `Seat B 182nd` 2, `Seat B 176th` 1.
- Row 1 = 2087, head 954af815c7b7, gate 251 table line 5 GO WITH NOTES (L1 is a title), F1 for Kam (permissions:null stays 201).
- Merge trees (both orders rc 0, same tree, all 25), K-row overlap none, both-sided paths (7 rows), 9 intersecting pairs (clean both orders), planted controls 10/10 positive, 20/20 negative (first plant on blank lines for 2080 and 2127 read rc 0: replaced).
- Re-key counts, matcher (755/764, no-P1 763/764, mutant 764/765, bare 758/759, control 759/759), UUID/hex guards, date-prefix finding (71 tokens), pre-existing b184 (2 hex hits).
- Late ruling from Wednesday (04:35): MERGE WINDOW, ROWS 27-51 DONE wrap, explicit pair sequencing: added to the brief.

## Full table (all 25)
| PR | head40 | merge-base40 | ahead | files | rc1/rc2 | tree (develop,head) |
| 2087 | 954af815c7b71497485c71fd3321f015650ef512 | b27f5fb30f4a912ec2b4b78f5c27281d11e47a87 | 133 | 4 | 0/0 | 38edbb4b6e71be6869eb4467c6048d9f2072d259 |
| 2129 | 902b3161e4350df9468c7459f2c402d291c4a721 | 204e62acdc351e664f9a1ca49a058275e9b3e907 | 103 | 4 | 0/0 | c198fd0019cfacffb281109b937469b7c2ef23d5 |
| 2100 | eb4a08362cfb6ce90ffa094078bd8620caebe5e7 | c0e6e744b7b21f3e1aa28105766764775b50ce6d | 122 | 4 | 0/0 | 703d1afc7328cd4754002acb1dc4cfdde6665b32 |
| 2064 | 6c8856baf1025d8048969a4facc7101ea30cbb7b | 9cdb9321aa8a7957272cd61ef8e0e957175593ad | 145 | 4 | 0/0 | a2bd00b069b3305f969a2466ef06203376b82805 |
| 2158 | 74364b18dcf4e90470a58d3dd4974314b89eae5d | 07d4218e9776a5eced016f16330983c900e94fb3 | 96 | 4 | 0/0 | 44b91ab975729995fe715f40039c49c62ac58728 |
| 2128 | c7e84537d2aeb6b1c11aeaebdff203a7aa6ff181 | 4d6b7bb17fd3be7b3fde8a3babc5d59c91c959b8 | 104 | 4 | 0/0 | 90bf0ff3ab33a1ed0828e77de821f033c76fce00 |
| 2080 | 83ee8509c985b656e2f2b635bc753148a2de3b2b | c5c26b2835df08e7e6addc1aec30939cf5531377 | 147 | 4 | 0/0 | ebec142dbb99cf918bc89ae2543db5f09f1cc9dd |
| 2130 | 11a39402623328f2ee8368284cd397630bca13d5 | 204e62acdc351e664f9a1ca49a058275e9b3e907 | 103 | 4 | 0/0 | 7cf3f4f27ac849afb3b2b91d696325bf9ec8bf1d |
| 2127 | 7dc6ff72cf61de04bb65a0e859cf670e9ff0ac85 | 4d6b7bb17fd3be7b3fde8a3babc5d59c91c959b8 | 104 | 5 | 0/0 | 0f9ab6a1d6149509dfa65dd21283029ad624e1b6 |
| 2162 | 30048d8b295e6be51540b015033aa4bb20ca5fe4 | 0115269abd111ee6acedb06fb0a0c3f8fd86f35a | 95 | 5 | 0/0 | de28733ddf7d60c00ef80bdaaac1556ee7d8ef2f |
| 2067 | 0d08681c616d9459b87387ef9c5ab11f478678e8 | cd773edc2bb8557f3779e69c0154477b5bc9510d | 143 | 6 | 0/0 | 0cb85fcbd7bc4da3e0a022951fbf2a0c97c8fec5 |
| 2085 | 4d4726ca41d99d5eab8c4a5a27b3a4317917beb8 | 35bcfa000b442943667deeee2cf7cec4f56d0cd0 | 142 | 6 | 0/0 | 180d74d0a4531725eed211d042c8ed24f2e64ef7 |
| 2132 | ba0ab4f453497257e9848c16f884ae8900a2f195 | 204e62acdc351e664f9a1ca49a058275e9b3e907 | 103 | 7 | 0/0 | a93d3b3b98824cde8c6ba274d847a40b5f067731 |
| 2138 | fdf80425e9d5c4f99f0a7b5c5c7521b0f7a39ec1 | f98afb113c2ddfb1e39c9f353a6ba4dd64069627 | 100 | 9 | 0/0 | 69cdd1906efa3deceee3e9e5882cfa88606765ca |
| 2161 | 0e50defb7819fe53a92ef6711a8a91e6b2d20f04 | 07d4218e9776a5eced016f16330983c900e94fb3 | 96 | 11 | 0/0 | c505aa1cb1011fb4351c5c5fff6ebad874089b72 |
| 2066 | baf577c78e7f876551e132e407d0982232622de9 | 35bcfa000b442943667deeee2cf7cec4f56d0cd0 | 142 | 14 | 0/0 | 92bbe1ddce5b99ed712bbd061fc967d49e7de65e |
| 2059 | 5d8969b36a24914c24bc6a839f819ec8be3772e9 | c5c26b2835df08e7e6addc1aec30939cf5531377 | 147 | 14 | 0/0 | 0706381310b7f2784ea1795d379ef09c1d3c3df8 |
| 2136 | b907ba03bea2e2fdcd6c1fe7aa0dc73f4c7f1edd | e8d23ce366e292ed6ca13f296cc2cfb2a3796496 | 101 | 3 | 0/0 | dae16112026a0579a9bee057d0251778a9db4790 |
| 2075 | 32aa0d06bc0aceccb790443bbf16384ff0c8e930 | 631ccfb8266a7d044e6577f45f598ccebe4e1773 | 138 | 4 | 0/0 | 6cf2865b4e71b751c9dcf5457eb18ca1ad7deb8c |
| 2135 | e2ada9bf1ea9db6c901a3a33723241e9d38be031 | e8d23ce366e292ed6ca13f296cc2cfb2a3796496 | 101 | 3 | 0/0 | 26b035b1bcde739e02d1ba2414125c0a82b855a7 |
| 2073 | 2684a29d8f576ff74634f07ad6576af5bd00370b | bdbb11b21585d085c25227d009968be342451223 | 140 | 8 | 0/0 | 5a1fcfde1c9e25c87cb178a0082c3f0d3a6a33aa |
| 2131 | 89081fae75e54e78e509d50a81cb0cd82c00eedd | 204e62acdc351e664f9a1ca49a058275e9b3e907 | 103 | 6 | 0/0 | d733c68964fb7a1b4bad85fe152371cd6b860cb4 |
| 2052 | b61674e7b7635a50d51f837849cb9caf1259235d | cfb6c1573ba9c948ebbe898fb2aec283bb9954ab | 128 | 32 | 0/0 | 46a6f80cc11090b2a8112bf0bc9860d35a7aaf65 |
| 2102 | 247e62dc7337a0f87e2b8a20d9c6107e6fcccf14 | fa0592f3b6f595f02fc36af2d8fa936213378fdd | 120 | 5 | 0/0 | d674c5e4e3f5a59a9ba8243fc1a29e5ec4c44909 |
| 2191 | 96ac07b0cd0daf45a8a27580ca0750de8c826f17 | 16a5c67e676eefa3e620c663fee3162941a22fa0 | 78 | 9 | 0/0 | bd87567e3da3bb73e85e9a95669a13796e877755 |

STACKED chain (queue order, one parent each): 2087 38edbb4b6e71, 2129 6cfcd247905a, 2100 d30baa717a20, 2064 cb3eb79fee24, 2158 90df901a5c20, 2128 e673ebfeb214, 2080 1bec188157fe, 2130 6c102b33a79e, 2127 e3bfa4f4417b, 2162 83d1ebd710eb, 2067 934840973d2b, 2085 24b66ccb9acb, 2132 fed25ceb2d3b, 2138 36e88e40032d, 2161 b403c2d7bd2a, 2066 adb2e05d7dfb, 2059 76ff7625fd25, 2136 5d68af9d9a7f, 2075 2d6f1887f3b7, 2135 533b5597e163, 2073 815d0bbc163f, 2131 dd40f77bdd28, 2052 8e2dc383624e, 2102 2b57e5219890, 2191 98967e37fd42

Rows 11 to 25 stacked trees are in the chain line above; the last (2191) is 98967e37fd4221cfce2f67f3c67ed65113fc05b4.

## Planted controls (first ten)
2087 adminConfig.ts line 992(+1)/dev 993; 2129 m365 index.ts 1276; 2100 email.ts 139; 2064 rateLimitEnforce.ts 168; 2158 adminConfig.ts 622(+1); 2128 auth.ts 12(+1); 2080 m365 index.ts 688(+1); 2130 prism index.ts 27; 2127 check-slot-credentials.sh 109(+3); 2162 ks1448 test 163(+1)/dev 172. Each positive rc 1; each negative (next two rows) rc 0.

## Pairs (develop+A then B == develop+B then A, rc 0/0)
2087+2158 28b6af869702; 2129+2080 5d8daa2bfb72; 2127+2052 b1250450f1eb; 2085+2066 b30202584f08; 2138+2161 ad0c166a303d; 2135+2136 3b1b7f7d275f; 2135+2073 8e6de93a5066; 2136+2073 0754cbc233dd; 2073+2131 20a1f5cd9f71.

## Judgement calls (declared)
- "P1" is not defined in the commission for the B lane; I read it as the MINE-regex/case shift (brief item W-2).
- Trimmed the brief from 56 KB to 49,993 bytes by compressing carried prose; no measured figure removed except rows 2-10 full heads (now here: see table above).
- PROVENANCE precedes UNMEASURED, as the commission orders (the template had them reversed).

## UNMEASURED
- Any install, suite, tsc, eslint, jest or vitest run; every cost and leg forecast; whole-suite counts.
- Open-PR census and OUT-list overlap; K 32nd's progress after 04:35; develop movement after 04:38.
- Gate notes beyond the verdict lines; whether gate 245/257/251 items for Kam were ruled; KS-1641 (not found in Linear).
- Matcher and the date-prefix edit on the REAL kit (scratch copies only); evidence count 133 vs 130; launcher preflight; pane contents.
