The OXPd 1.x CA store writes (first-run step 3), built and tested against stubs only, before any run against a
device. One commit, `be650e1b`, on `main` `baa32eae` (behind 0, ahead 1). Eleven files: two added, nine changed, all
under `src/Datasec.Suite.Adapters.Oxpd1/`, `src/Datasec.Suite.Lab/Commands/Oxpd1/` and the two matching test folders.
No package, no lock file, no project file, no `Datasec.Suite.slnx` line, no workflow, no file under `contracts/`.

## Why

- First-run step 3 needs a lab write for HP's CertificateManagement `ImportCertificate` and its delete
  (`RemoveCertificate`), with a dry run, a read of the store before and an undo. HP's descriptions (committed under
  `contracts/oxpd1/hp/`) say an import of a certificate already in the store "will succeed ... but will have no
  effect", so a remove sent as its undo would take out a certificate that was there before: the store is read first.

## What changed

- **The client.** The closed write catalogue gains `ImportCaCertificate` and `RemoveCaCertificate` (two rows of the
  committed binding, HTTP Basic `admin`). `Oxpd1CaCertificate` takes ONE DER X.509 certificate of 1 to 10240 bytes
  (HP's schema) whose one basic constraints extension names an authority; its id is the first 16 bytes of its SHA-256
  as a version-8 UUID, carried in the call's agent id so the undo list keys it unchanged. An import's undo is the
  remove of the same certificate. `ReadCaStoreAsync` makes `ExportCertificates` (admin) through one new internal send,
  `SendAdminReadAsync`, and answers only when the response, the result and every entry (base64 of PEM text holding one
  `CERTIFICATE` block, or of DER, loading as exactly one certificate) are in HP's shape. The read catalogue and its
  read-only rule are unchanged.
- **The lab.** `oxpd1 write --write ImportCaCertificate|RemoveCaCertificate --certificate <file>`: ONE CA certificate,
  PEM or DER, at most 64 KiB, a file holding the words `PRIVATE KEY` refused first, a leaf refused; each a usage error
  (exit 2) before any folder or connection. An executed import reads the store first: listed is exit 0 with nothing
  written and no undo; refused is exit 6; any other end, or an entry it cannot read, is exit 8 with nothing written. An
  answered import or remove reads the store after and prints whether the certificate is there (the exit code does not
  change). The undo list's import line names `RemoveCaCertificate sha256 <hex>`; `undo-owed` owes the remove of an
  import until an answered remove of the same id on the same host.
- **Text.** Both READMEs: the three CertificateManagement rows, the certificate's rules, the store read's shape, the
  verb's options, order, exit codes and undo, and the Limits.

## What proves it

- Red first: 21 cases fail by assertion on a permissive first shape (adapter `Total: 86, Failed: 11`; lab
  `Total: 274, Failed: 10`). Green: 2297 / 0 / 2293 / 4 locally; the branch's push run 45569238645: linux 2293
  succeeded, windows 2276 succeeded, rules 677 files, `Ran 117 tests`, secret scan clean.
- 12 mutants, each red on exactly its cells, none surviving (a leaf taken; no size bound; no undo for an import; an
  unreadable entry skipped; the store's shape not checked; a second PEM block taken in an entry and in the file; the
  store read sent as `guest`; a key file taken; the import's undo not owed; a listed certificate imported again; no
  read after).
- Against stubs on 127.0.0.1: an import not in the store (read, import, read after: three requests, `admin` each);
  one already there (one request, nothing written); a store read refused, faulted or holding an entry that is not a
  certificate (nothing written); an import that faults (owed) or is refused (not owed); a remove; the eight file and
  option refusals (no folder, 0 connections); the undo list across hosts and ids.

## Still open

- Nothing here has run against a device. Whether the M577 takes the development root in its OXPd CA store (HP: "The
  use of self-signed certificates with the OXPd CA Certificate store is not recommended/supported"), how it exports an
  entry, and whether it then uses the CA are not measured; the device run of step 3 is a separate step after this lands.
- Named limits: an entry exported in another form than its DER bytes is not found by the SHA-256 compare; a
  certificate added by anyone else between the read before and the import is not seen; a fault's subcode is not read;
  an answered import that the read after does not list is reported, not acted on.
- Known, not changed here: `undo-owed` keys a write by host and id whatever its kind, so an answered unregister typed
  with a certificate's id clears an owed import, and a later register of that id replaces it in the list; the file's
  64 KiB bound is checked on the path's own size, so a link or a pipe can deliver more; the words check finds a PEM
  private key, not a bare base64 one after the certificate (only the certificate's DER is ever sent, and no key byte
  is printed); the store reader takes a non-ASCII space beside the entries; the client's record file holds the
  certificates' base64 (public certificates, as it holds any answer); a CA is taken on its basic constraints alone
  (its key usage and dates are not read); the store reader refuses several schema-valid PEM forms (a leading newline,
  text before the first line, another label), which stops an import with nothing written.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (the order with the next write lane;
the store read as the writer's own, with the read catalogue unchanged; every entry one certificate or no answer; an
import of a listed certificate writing nothing; the read after reported only; PEM or DER with the key words refused
first; the derived id in the existing column; the dry run's envelope printed whole; no local CodeQL). No choice in
this change is the product owner's.

Nothing is deployed; nothing was sent to any printer or device.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
