--- comment 5826263176 by linear[bot] at 2026-09-25T03:37:37Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1266/four-originate-unit-test-files-make-a-real-dns-lookup-and-tcp-connect">KS-1266 Four originate unit test files make a real DNS lookup and TCP connect to anchoring:4005 (the default ANCHORING_SERVICE_URL)</a></summary>
<p>

## BLUF

`ks1213`**,** `ks444`**,** `ks445` **and** `ks543` **in** `services/originate/src/__tests__/` **reach the network. They do a DNS lookup of** `anchoring` **and a TCP connect to** `:4005`**, because they leave** `ANCHORING_SERVICE_URL` **at its default.** The unit suite is not hermetic, and its result depends on the host's resolver.

## Recommendation

In each file, point `ANCHORING_SERVICE_URL` at a loopback port that is refused, or mock `fetch` for the anchoring call. **Don't use port 1:** it is on the Fetch-spec bad-port list, and undici refuses it before opening a socket (the gate's N43-6). `127.0.0.1:2` gives a real `ECONNREFUSED`.

## Detail

* Measured per file by the batch gate, each file run alone at develop AND at #1043's head (`evidence/perfile_net.out`). The ks1228 file contacts nothing non-loopback.
* Found by the batch gate `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-batch1042-1045-tier1-r1/report.md` (finding N43-5). Pre-existing hygiene.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1266-keep-seven-originate-unit-files-off-the-network-and-correct-20ffffd56796">Review in Linear</a></p>

