---
date: 2026-08-07
type: commission-capture
for: Secuura platform build (K + S + APIs)
status: captured-verbatim; structuring + agent work in flight
source: "Kam, dictated after the 15:00 meeting with Stuart, 2026-08-07. THE MEETING WAS NOT RECORDED — this dictation is the only record. Preserved verbatim below before any interpretation."
---

# Secuura architecture — Kam's post-meeting brain dump (VERBATIM)

> a couple of thoughts on that meeting and this is a brain dump for us to flesh
> out further and then ultimately to structure into a build for the securer
> platform. There are two or three issues that we are currently grappling with.
> The first is the one I described above where uploading a document with the
> same title could potentially create conflicts within the platform. The second
> issue that we are talking about or trying to solve for is with regards to user
> and document verification and what information is ultimately displayed in the
> connector or platform. bottom line up front on that one we will look at
> workflows and smart contracts smart contracts belong to platform K workflows
> and Stewart's definition of workflow which is essentially just more visual and
> operational layer belong to Platform s. because platform S needs to feed
> certain information into platform K and platform S initially represents how
> most users will interact with the system. We added a third category called
> rules at this stage which are essentially things that belong inside a smart
> contract that platform S will either get from platform K and then feedback
> about a particular document or will define to feed to platform K so that those
> rules and that information can be incorporated into the smart contract. the
> third thing that we are trying to solve for is how to future-proof the
> technology so that we can allow evolution of the way that we control things
> and flexibility client by client into what can be done document by document.
> Ultimately, the way that this might look is as follows. Platform K is the
> blockchain manager or the source of truth. Not immediately, but as we go
> forward, documents that are encrypted or hashed will have an associated smart
> contract. That smart contract defines an undefined amount of parameters about
> that document. The fact that it's undefined is good because we want these
> things to be customized either by client or by document type or particular
> flow or a combination. Once a smart contract has been set, this becomes the
> immutable component that ensures that things cannot be changed or compromised
> in the negative. Things like who gets notified, can the document be deleted,
> can a person add different viewers or different participants to it, etc.
> Also, the smart contract can and should have governance rules which define
> whether that smart contract can be varied and under what terms. Platform S
> will have visual components and a lineage element which you can have a look
> in Platform S and Platform K which defines how that document is treated
> within the platform and as we get forward where we go to full self-sovereign
> documents and that document is outside of our platform how it needs to be
> treated when someone interacts with it. this goes hand in hand with the smart
> contracts but the new little source of truth will be platform K and an
> element stored in the blockchain or the smart contract. the rules need
> further clarification and definition but these allow Platform S to feed
> information into Platform K and to set up different flows that we capture.
> Now tying things back to what we discussed above and the proposed solution
> which needs to be fleshed out. The idea going forward is that when Stuart or
> Platform S provides or uploads a document to Platform K he will need to
> provide the document itself so we will have the title. He will provide
> everything he currently provides as well as a UUID that is generated per
> document and attached to the metadata and a user UUID and an organizational
> UUID. The UUID will not be inside the document but will be held by Platform
> S which is determined or discovered once that user logs in and the
> organizational UUID allows us to layer different workflows, rules and
> contracts so that we have a combination of things that are user defined,
> organization defined or potentially both. As an example a particular
> organization might have a rule that allows the user to control that document
> but also the organization. In terms of how this works for the individual
> user, a good proxy is GitHub, where a user might belong to one or multiple
> organizations and multiple things can be shared within that organization or
> user's repository So when a user is uploading a document and we know that
> they belong to multiple organizations, they can check or select that they
> are going to be uploading things for this organization or another. This is a
> large brain dump but I unfortunately forgot to record the session with Stuart
> So please make sense of the above Ask questions where necessary Interact with
> the SECURA agent And both platform K and platform S Will be relevant and come
> up with a proposed action plan So that the platform can be modified as well
> as the APIs through which Stuart interacts Stuart does not have these notes
> So we would also need to be helpful to his agent so you can incorporate what
> he needs to in platform S

*(Dictation note: one passage about rules/upload appears twice in the original —
a Whisperflow artefact, kept as spoken. "securer"/"SECURA" = Secuura;
"Stewart" = Stuart.)*

---

# Structured reading (Wednesday's interpretation — verify against Kam)

## The three problems being solved

1. **Document identity collisions** — same title or same bytes from different
   uploaders confuse the platform (Stuart's S/K finding, decision-pack item 7).
2. **User & document verification display** — what the connector/platform
   actually shows about a document and its people.
3. **Future-proofing** — control must evolve per client, per document type, per
   flow, without re-architecture.

## The three-layer model agreed with Stuart

| Layer | Owner | What it is |
|---|---|---|
| **Smart contracts** | **Platform K** | The immutable component per document: notification rules, deletability, who may add viewers/participants — plus **governance rules defining whether and how the contract itself may be varied** |
| **Workflows** | **Platform S** | Stuart's definition: the visual and operational layer; how most users actually interact |
| **Rules** | **The bridge (new category)** | Parameters that live inside a smart contract; S either receives them from K (feedback about a document) or defines them and feeds them to K for incorporation |

K is the source of truth ("not immediately, but as we go forward"). S carries
visual components and a **lineage element** visible in both platforms — extending
eventually to **self-sovereign documents** that live outside the platform but
carry treatment rules with them, anchored back to K.

## The identity model (the proposed solution to problem 1)

On upload to K, Platform S supplies, alongside everything it sends today:
- **a per-document UUID** — generated by the workflow, carried in the
  **registration metadata, NOT stamped inside the file** (Kam: "The UUID will
  not be inside the document but will be held by Platform S") — which sidesteps
  the changes-the-hash problem entirely;
- **a user UUID** — discovered at login;
- **an organisational UUID** — enabling layered control: user-defined rules,
  org-defined rules, or both (e.g. an org rule granting control to both the
  user and the org).

**Mental model: GitHub.** A user belongs to one or many orgs; at upload they
select which org (or their personal space) the document belongs to.

## What this appears to settle (flagged to Kam as questions, not assumed)

- **Decision-pack item 7 (what does a duplicate upload mean)** — under this
  model, two uploads of identical bytes are **two registrations with two
  document UUIDs**. Hash stops being the identity key; the UUID is. That is
  effectively option (c) "keep both deliberately", made coherent.
- **My UUID-in-metadata answer from earlier today** — Kam's design takes the
  path I recommended: identity in registration metadata, not stamped into the
  artefact.

## Commission

Make sense of it · ask questions where necessary · work with the Secuura agent
across BOTH platforms' concerns · produce a proposed action plan covering
Platform K modifications and the APIs Stuart uses · prepare material for
Stuart's agent so Platform S can incorporate its side (**Stuart does not have
these notes**; delivery to him goes through Kam under v1.3).

---

# KAM'S CLARIFICATION — 2026-08-07, supersedes my reading above

Verbatim: *"There will be multiple UUIDs. The document UUID (generated for every
single document) will be stored in the document metadata. The user UUID and the
company UUID will be generated for each and stored in platform S and most likely
platform K."*

**So my earlier reading was WRONG and is corrected here:** the document UUID IS
stamped into the file's metadata — this is Stuart's option 4, chosen
deliberately. User and org UUIDs live platform-side (S, most likely K too),
never in the file.

**The consequence that must now be a design decision, not an accident:** stamping
changes the bytes, so the hash of the stamped file differs from the hash of what
the user originally submitted. The clean resolution is ordering: **stamp FIRST,
then hash and register the STAMPED artefact, and return the stamped file to the
user as the canonical copy.** Then the file the user holds matches the registered
hash, and independent verification works. The problem only bites if K hashes the
pre-stamp bytes or the user keeps only their unstamped original. Watermarking
already sets this precedent if it produces the canonical copy today.

Sub-questions this raises (routed to the agent as part of the commission):
- confirm where in the current pipeline the hash is computed relative to any
  byte-modifying step (this was already question 1 of the five);
- formats with no metadata container (plain text, CSV) cannot carry the doc
  UUID — fallback needed: registration-metadata-only for those, or restrict
  supported formats;
- the stamped UUID remains a lookup hint, never proof — it is strippable and
  forgeable; identity evidence stays the hash + registry.
