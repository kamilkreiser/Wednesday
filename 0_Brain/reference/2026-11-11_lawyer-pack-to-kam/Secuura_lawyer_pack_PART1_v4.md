# PART 1: FOR THE LAWYERS (paste-ready)

## Cover note

Hello,

Two items for the customer contract, sent together.

1. A sentence for the data processing agreement. Our Microsoft 365 integration connects to a customer's own Microsoft 365 account. The customer's documents stay in that account, and the customer is the data controller for them. We would like the agreement to say: "The customer controls, and erases, its own Microsoft 365 documents." Please tell us whether that wording does the job, and how you would change it.

2. Four terms we use in contracts and materials: certification, verification, signing and watermarking. Our working definitions are below. Please tell us where any of them conflicts with how the law or common contract wording uses the same word, and mark any sentence that would be risky for us to rely on. [Remove this bracket once the signing definition is final: the signing definition is still being finished.]

Thank you.

## Definitions

**Certification.** Certification is an umbrella term. It covers up to three things: an attestation, signing, and, if chosen, watermarking. An attestation is a user stating that a document is correct; it is recorded on the blockchain, separately from the file itself. Any change to a certified document, including adding a watermark, produces a new version of the document. Versions are linked to each other, which is the document's lineage. A new version must be certified again. [1]

**Verification.** Verification is a configurable workflow, not one fixed check. [2] Customers set up their own verification workflows using smart contracts, and Secuura does not prescribe what a customer's compliance requires. [2] When a verification runs, the path taken through the workflow is checked against the smart contract and recorded. Simple interactions, such as viewing a document, are not recorded on the blockchain. A third party who verifies a document, for example a recruiter checking a university document, can see the steps taken, such as identity checks and domain matching. The person using the result sees a simple "verified" or not verified; an auditor can see the full detail. [2] A verification is public. It sits outside the document's certified lineage, so checking a document does not create a new version. Where a verification is recorded at all, it is recorded by the Secuura product that performed it, for its own reporting. The Blockchain Manager is not the official record of verification acts. [2]

**Signing.** Signing is one of the three elements of certification (see Certification). [GAP: this draft says no more than that. The external label for what Secuura calls signing, and how it relates to electronic or digital signatures in law, is not settled here.]

**Watermarking.** Watermarking is an optional element of certification. It changes the file by adding a mark to it. Applying a watermark therefore creates a new version of the document, linked to the original in its lineage, and the new version must be certified again. [1]

## Notes to the definitions

[1] The two sentences marked [1] (under Certification and under Watermarking) say that a new version must be certified again. This describes the intended design of the platform. It is not yet built.

[2] The sentences marked [2] (under Verification) describe how verification is designed to work: customer-configured workflows using smart contracts, the steps a third party or auditor can see, how a run is recorded, and that a verification sits outside the document's lineage and is not officially recorded by the Blockchain Manager. This is the intended design of the platform. It is not yet built.

## The sentence for the agreement

"The customer controls, and erases, its own Microsoft 365 documents."

**What Secuura keeps for the Microsoft 365 integration.** When a customer connects its Microsoft 365 account, Secuura reads a document only to work out its hash, a short digital fingerprint of the file, as the file streams through. It does not keep a copy of the document's contents. It does keep: the organisation's connection tokens (the credentials that let the integration reach the customer's account); the names and addresses of the sites it listed; and, for each document the customer syncs, the document's name, its link, a reference to the item in the customer's drive, and its hash. A document's name or link can itself be personal data. Please tell us whether the sentence above should also cover these records, or whether they need their own wording. We are confirming how the connection tokens are protected in storage, what is deleted when an organisation ends its connection, and whether any synced document's hash is ever recorded on a public blockchain. We do not state any of those three as fact here.

---
