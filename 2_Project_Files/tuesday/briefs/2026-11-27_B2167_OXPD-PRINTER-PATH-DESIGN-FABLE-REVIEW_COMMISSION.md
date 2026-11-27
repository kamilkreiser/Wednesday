# B2167 COMMISSION (one in-session READ-ONLY reviewer on the newest FABLE, flagged by Kam) -- Datasec/OXPd: adversarial review of the Azure mock client environment and printer-path design

Commissioned by Tuesday (s334). Model: Fable, on Kam's live-board words of 2026-11-27 (stamped 18:13:30): "the printer sitting here is a good example. clients will have more complex networks but their printers will always be in their office. let me know the best design for this. it needs to be seamless and security aligned. use fable if need be" (the flag the 2026-11-21 model rule requires).

## Review this, whole
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2165_OXPD-AZURE-MOCK-CLIENT-ENV.md` (designer B2165, Opus). Its sources: `2026-11-27_B2163_OXPD-CLIENT-DEPLOYMENT-MIRROR.md`, the design `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Design/02_architecture.md` (sections 4, 6, 7, 8), CLARIFICATIONS, and the Microsoft pages it cites (open them yourself).

## Answer, each with sources; a claim you cannot source is UNMEASURED
1. **Does the recommended "OXPd Site Connector" over Azure Relay actually carry OXPd's traffic both ways?** OXPd 1.x: device-initiated SOAP callbacks to the server's agents and server-initiated calls into the device on its fixed port 7627, no address translation (02:249, C2:154), exact certificate CN match (02:635-636). OXPd 2 REST. IPPS 631 for Universal Print. Check Azure Relay Hybrid Connections' real protocol limits (WebSocket/HTTP vs raw TCP, `azbridge`'s support status, latency, connection limits, message size), and whether the printer will accept 1.x calls from the connector's address (the design's own S14b unknown). Is "encryption from printer to server without a stop" true, or does TLS terminate at the connector?
2. **Security alignment:** what can a compromised connector reach; can it be scoped to enrolled printers and ports only; the Relay SAS/Entra auth model and secret rotation; the two-tier CA with the root key in Key Vault; least privilege for the agent login; logging and audit; does the design open any inbound path on the office network.
3. **Seamless for a client:** what the client's IT must do to deploy the connector from the Marketplace route, and is that realistic against how Workpath customers deploy today (B2163 item 7).
4. **Is a site-to-site VPN or another pattern actually better** for Kam's goals (seamless, security-aligned, mirrors clients)? Say plainly if the designer's recommendation is wrong.
5. **Cost and the lab build:** check the AUD figures against the retail prices API (or mark UNMEASURED), the A$50/month card threshold, and whether the lab build (azbridge on the Mac) mirrors the product closely enough to be worth testing.
6. **Errors:** every factual error, unsupported claim or contradiction with a Kam ruling (P-4 a with its note; K11b c "full mimic of target environment now"; q05, q14, q22; the mirror-a-client rule).

## Output
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2167_OXPD-PRINTER-PATH-FABLE-REVIEW.md`: VERDICT first (AGREE / AGREE WITH CHANGES / DISAGREE), then findings ranked by severity, each with its source, then a 5-line plain-English summary Tuesday can give Kam.

## Fences
READ-ONLY everywhere except that one output and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s334/d2167/`. No Azure write (read-only `az` under `AZURE_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/.azure'` only if needed), no write in the OXPd project, Jira, GitHub, cards or mail. Never read `Source_Documents/`, `4_Credentials/` or key folders. Never type `cd`; never delete. Every clock printed by `date`. Return 10 lines, first the VERDICT.
