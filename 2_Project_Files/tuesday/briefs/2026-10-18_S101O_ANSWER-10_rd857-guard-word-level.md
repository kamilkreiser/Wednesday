ANSWER to your QUESTION "RD-857 guard — whole-value match closes engineering only (seed has Melbourne / Sydney HQ)" (04:02Z). SUPERSEDES the "case-insensitive, whole value" clause of ANSWER-9 (03:53Z); the rest of ANSWER-9 stands.

RULED: (b), word-level. The guard fires only when NO user matched the capture, and then treats the capture as a department/location when every word of the capture is a word of one department or location value present in the data, OR every word of one such value is a word of the capture (case-insensitive, whole words, per single value). That closes engineering, melbourne hq and sydney.

Why (b) and not (c): the guard runs only after the user lookup has already failed, so a real user (say "Sydney Smith") is still found as a user first and is never lost. The only behaviour change is that an UNKNOWN name sharing a word with a department or location gets the normal model answer instead of the not-found text, which is acceptable. (c) is fitted to today's seed values; (b) is the general rule.

Cells: add the sydney and melbourne-hq red cells as originally ruled, plus one control your measurement suggests: an unknown single name that shares NO word with any department or location (zebedee) still gets the unchanged not-found text; and one new control: a capture that shares a word with a value but is a real seeded user still reaches the user-activity handler (pick a seeded user if one exists; if none does, say so and skip it).

-- Tuesday
