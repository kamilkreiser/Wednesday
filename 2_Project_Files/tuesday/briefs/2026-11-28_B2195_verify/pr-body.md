## Why

The agent host, the context-call work and the scan call are built from HP's descriptions of the authentication agent,
the accessories callback and the scan service. Those descriptions were not in the repository: `contracts/oxpd1/hp/`
held the device-side services only. This change adds them, byte for byte, from the same pinned jar as the 23 files
already here. It adds no code.

## What changed

- **Added (12 files, HP's bytes):** from `OXPdLib-1.8.4.jar` of HP's SDK 1.8.4.1 (SHA-256
  `f2bb325f801cc2d6ef8e253abda54280129f5c9090bcc6342eb2a63109c3d341`, the pin in `contracts/oxpd1/README.md`):
  - the whole `authenticationagent` folder: `AuthenticationAgentSoap12Binding.wsdl`, `authenticationagent.wsdl`,
    `authenticationagent.xsd`;
  - the accessories files whose name holds `callback`: `AccessoriesCallbackSoap12Binding.wsdl`,
    `accessoriesCallback.wsdl`;
  - the whole `scan` folder: `ScanSoap12Binding.wsdl`, `scan.wsdl`, `scan.xsd`, `ScanCallbackSoap12Binding.wsdl`,
    `scanCallback.wsdl`;
  - the two schemas they import that were not yet here: `mediadomain.xsd`, `optionsdomain.xsd`.
- **Changed (4 files):** `contracts/oxpd1/inputs.sha256` (23 lines kept byte for byte and in order, 12 added, sorted
  by path: 35); `ContractTests.cs` (C01's count, 23 to 35, one line); `StubDevice.cs` (the binding-port pin, 7 to 11,
  and its message, two lines); `contracts/oxpd1/README.md` (which files are here, and that the stub's table now holds
  the solution-side and callback bindings too).
- Nothing deleted or renamed. No package, lock file, project file, workflow or other code line.

## What proves it

- Each added file equals its jar entry byte for byte, and its SHA-256 equals the digest in the jar's signed manifest
  (the jar's signature block names HP Inc. as signer and verifies over its signature file).
- C01 hashes every listed file and names any unlisted one; C02 is its control. The list without the files reddens C01
  and C02 only; each new file changed by one byte reddens C01 and C02 only; the new bindings without the moved port pin
  redden every stub-backed cell with the port-count message.
- Every binding names one WS-Addressing namespace for its endpoint reference (`http://www.w3.org/2005/08/addressing`;
  the August 2004 namespace is declared in the files and used 0 times), has one `wsdl:service`, and has a soapAction on
  every operation; 106 soapActions, none held twice (also ignoring case). `IsServiceEnabled` stays the only name
  without `Get` that the read form admits. Every import of the 35 files resolves inside the folder, and every schema
  compiles.
- The checks of this pull request: build and the whole solution on linux and windows (the windows leg keeps HP's CRLF
  bytes under `contracts/oxpd1/.gitattributes`), the repository rules, the secret scan, and CodeQL.

## Named limits

- No cell calls the new operations or compiles the new schemas (the schema cell compiles five device-side schemas).
- The stub's binding table now holds solution-side and callback operations as well as the device's; each callback
  binding names the same `wsdl:service` as its device-side sibling (`AccessoriesService`, `ScanService`). The stub keys
  by soapAction, so it would answer a callback action sent to the device-side path. No cell asks for a device-only
  table.
- How a printer calls these services, and which WS-Addressing namespace it sends on the wire, is not measured here:
  the files are descriptions only.
- Two text lines outside this change still say "seven" committed bindings (a test summary and the adapter README).

## Who decides

Every choice of this change (which files, the port pin, the README lines) is the coordinator's. The words that keep
HP's files here are the ones the contracts README already quotes from the project's clarifications (2026-11-21 and
2026-11-23); the first was said of HP's OXPd 2 specification files and is read as covering these descriptions, as for
the 23 already here.

Nothing ran against a printer, a device or a tenant. Nothing is deployed: the repository's only workflow builds,
tests and scans.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
