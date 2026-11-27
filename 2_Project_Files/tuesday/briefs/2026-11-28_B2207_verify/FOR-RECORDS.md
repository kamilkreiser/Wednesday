# FOR RECORDS: gate B2207 (lane L1 slice 1, the OXPd 1.x authentication agent, round 1 of 2)

For the records pass after the landing (no text of the gate goes into a project file by the gate itself).

- **Lane L1 slice 1 DONE when the squash lands:** `Oxpd1AuthenticationAgentEndpoint.AnswerAsync` answers HP's three
  authentication-agent operations (GetPrePromptResult, GetPostPromptResult, SignOutNotification) from one SOAP 1.2
  request, each value checked against HP's committed schema before the host's handler sees it; answers Continued,
  Canceled or Failed (no Succeeded until the user's information is built); the answer in the request's WS-Addressing
  version; every refusal a SOAP fault with a fixed text. Cells G01 to G09 (43 cases) in memory; nine mutants turn them
  red (gate re-run: 9 of 9 MATCH). How an M577 frames these calls is UNMEASURED. (RELAYED from the kit's FOR RECORDS,
  confirmed by the gate's own runs.)
- **Not built:** Succeeded with the user's information (slice 2); the context reserve and release calls (slice 3,
  through lane L1x's class); the HID report event and the HID calls (slice 4); the route, TLS and the caller's
  credential (lanes L3b and AZ-1X); a time bound on the handler.
- **Owed to L3b (the host wiring), from the gate's VERDICT.md:** map ONE POST route to `AnswerAsync` with the request's
  body stream and `Content-Type`; bound the handler to HP's 1 to 5 s; treat a repeated sign-out as done; AND catch an
  `OperationCanceledException` that `AnswerAsync` lets through when the request was NOT aborted (a handler's own
  time-out, F1): answer a Receiver fault, never log the exception's message (it can carry the handler's text).
- **Owed to a later slice of this lane (optional, F2/F4):** drop or set a positive `MaxCharactersFromEntities` (0 is
  "no limit" in .NET; the DTD prohibition is the guard, and the same line sits in the landed `Oxpd1Soap.cs:104`); cells
  for `mustUnderstand="1"`, text beside the operation in the body and a child element inside a value (each refused by
  the code today, MEASURED; no cell pins it).
- **For lane L1d (the first device run):** read the real content type, addressing version, encoding and whether the
  device's `Action` carries white space (refused today).
- Nothing here ran against a device, a printer, a tenant, Azure, a Microsoft host or HP.
