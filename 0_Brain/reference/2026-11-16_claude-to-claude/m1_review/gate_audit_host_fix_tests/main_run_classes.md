| Record | (random) x278; none hit x57; CreateTemp anchors x35; Rename anchors x35 | Ok(Recorded) | member true | fresh landed true | retry - | 532 |
| Record | (random) x64; CreateTemp store x35; Rename store x35; Write store x33 | Err(Audit(Store)) | member true | fresh landed false | retry Ok(Recorded) | 199 |
| Record | SyncDir store x6 | Err(LandedUnknown) | member false | fresh landed true | retry - | 6 |
| RecordFor | (random) x259; none hit x57; CreateTemp anchors x35; Rename anchors x35 | Ok(Recorded) | member true | fresh landed true | retry - | 513 |
| RecordFor | (random) x72; CreateTemp store x35; Rename store x35; Write store x33 | Err(Audit(Store)) | member true | fresh landed false | retry Ok(Recorded) | 207 |
| RecordFor | SyncDir store x6; (random) x1 | Err(LandedUnknown) | member false | fresh landed true | retry - | 7 |
| Checkpoint | (random) x257; none hit x57; CreateTemp anchors x35; Rename anchors x35 | Ok(Checkpoint) | member true | fresh landed true | retry - | 511 |
| Checkpoint | (random) x85; CreateTemp store x35; Rename store x35; Write store x33 | Err(Audit(Store)) | member true | fresh landed false | retry Ok(Checkpoint) | 220 |
| Checkpoint | SyncDir store x6; (random) x2 | Err(LandedUnknown) | member false | fresh landed true | retry - | 8 |
| Receive | (random) x242; none hit x57; CreateTemp anchors x35; Rename anchors x35 | Ok(Received) | member true | fresh landed true | retry - | 467 |
| Receive | (random) x66; CreateTemp store x35; Rename store x35; Write store x33 | Err(Audit(Store)) | member true | fresh landed false | retry Ok(Received) | 201 |
| Receive | SyncDir store x19; (random) x16; CreateTemp anchors + SyncDir store x2; Rename anchors + SyncDir store x2 | Err(Reopened{landed:true}) | member true | fresh landed true | retry - | 45 |
| Receive | SyncDir store x6; (random) x1 | Err(LandedUnknown) | member false | fresh landed true | retry - | 7 |
| Release | (random) x175; none hit x97; SyncDir anchors x65; Unlink anchors x48 | Ok(Released) | member true | fresh landed true | retry - | 601 |
| Release | (random) x137; CreateTemp anchors x49; Link archive x49; Rename anchors x49 | Err(Dir(Io)) | member true | fresh landed false | retry Ok(Released) | 613 |
| Release | Unlink store x82; SyncDir store x44; (random) x34; SyncDir anchors + Unlink store x9 | Err(Audit(Store)) | member true | fresh landed false | retry Ok(Released) | 225 |
| Release | SyncDir store x17; (random) x5; SyncDir store + Unlink store x3 | Err(LandedUnknown) | member false | fresh landed false | retry Ok(Released) | 25 |
| Release | SyncDir store x3 | Err(LandedUnknown) | member false | fresh landed true | retry - | 3 |
| ReleaseTomb | (random) x215; SyncDir store x115; Unlink store x115; none hit x91 | Ok(Released) | member true | fresh landed true | retry - | 985 |
| ReleaseTomb | (random) x102; CreateTemp anchors x56; Link archive x56; Rename anchors x56 | Err(Dir(Io)) | member true | fresh landed false | retry Ok(Released) | 648 |
| ReleaseTomb | CreateTemp store x43; Rename store x43; (random) x33; Write store x30 | Err(Audit(Store)) | member true | fresh landed false | retry Ok(Released) | 230 |
| ReleaseTomb | (random) x2; CreateTemp store + SyncDir store x1; Rename store + SyncDir store x1; SyncDir store + SyncFile store x1 | Err(LandedUnknown) | member false | fresh landed false | retry Ok(Released) | 6 |
| ReleaseTomb | SyncDir store x29; SyncDir store + Unlink store x4; (random) x3 | Err(LandedUnknown) | member false | fresh landed true | retry - | 36 |
| Seal | (random) x182; Unlink store x143; SyncDir anchors x99; SyncDir store x91 | Ok(SealReport seg 1) | member true | fresh landed true | retry - | 1196 |
| Seal | (random) x91; CreateTemp anchors x67; Rename anchors x67; SyncDir anchors x67 | Err(Dir(Io)) | member true | fresh landed false | retry Ok(SealReport seg 1) | 747 |
| Seal | CreateTemp store x52; Rename store x49; (random) x40; Write store x30 | Err(SealCommitFailed{segment_now:0}) | member true | fresh landed false | retry Ok(SealReport seg 1) | 276 |
| Seal | SyncDir store x28; SyncDir anchors + SyncDir store x4; (random) x4; CreateTemp anchors + SyncDir store x3 | Err(SealCommitFailed{segment_now:1}) | member true | fresh landed true | retry - | 50 |
| Seal | SyncDir store x6; CreateTemp store + SyncDir store x1; Rename store + SyncDir store x1; SyncDir store + SyncFile store x1 | Err(LandedUnknown) | member false | fresh landed false | retry Ok(SealReport seg 1) | 11 |
| Seal | CreateTemp store x66; Rename store x66; Write store x64; SyncFile store x63 | Err(Audit(NothingToSeal)) | member true | fresh landed false | retry Ok(SealReport seg 1) | 291 |
| Seal | SyncDir store x22 | Err(LandedUnknown) | member false | fresh landed true | retry - | 22 |
| Seal | SyncDir store x12; (random) x1 | Ok(SealReport seg 1) | member false | fresh landed true | retry - | 13 |
