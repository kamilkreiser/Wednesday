//! QA gate r2 (M1 RELAY-IDENTITY): library probes of the v3 blob. Written by the independent gate;
//! not part of the branch. Run with `--nocapture --test-threads=1` to see the summary lines.

use std::time::{Duration, Instant};

use coagent_relay::{
    connect_pinned, ClientFrame, Fingerprint, IdentityBlobError, IdentityPart, Relay, RelayConfig,
    ServerEvent, ServerFrame, TlsIdentity, IDENTITY_BLOB_HEADER, IDENTITY_BLOB_MAX,
};

fn fresh() -> TlsIdentity {
    TlsIdentity::generate(&["127.0.0.1".parse().unwrap()], &[]).unwrap()
}

/// (cert, key, stored hash) of a v3 blob.
fn split3(blob: &[u8]) -> (Vec<u8>, Vec<u8>, Vec<u8>) {
    let h = IDENTITY_BLOB_HEADER.len();
    let cl = u32::from_be_bytes(blob[h..h + 4].try_into().unwrap()) as usize;
    let cert = blob[h + 4..h + 4 + cl].to_vec();
    let k0 = h + 4 + cl;
    let kl = u32::from_be_bytes(blob[k0..k0 + 4].try_into().unwrap()) as usize;
    let key = blob[k0 + 4..k0 + 4 + kl].to_vec();
    let hash = blob[k0 + 4 + kl..].to_vec();
    (cert, key, hash)
}

fn join3(hdr: &[u8], cert: &[u8], key: &[u8], hash: &[u8]) -> Vec<u8> {
    let mut v = hdr.to_vec();
    v.extend_from_slice(&(cert.len() as u32).to_be_bytes());
    v.extend_from_slice(cert);
    v.extend_from_slice(&(key.len() as u32).to_be_bytes());
    v.extend_from_slice(key);
    v.extend_from_slice(hash);
    v
}

/// What an attacker who can write the file does: edit the certificate, then store its new hash.
fn rehash(hdr: &[u8], cert: &[u8], key: &[u8]) -> Vec<u8> {
    join3(hdr, cert, key, &Fingerprint::of_certificate(cert).0)
}

async fn serves(id: TlsIdentity) -> Result<(), String> {
    let fp = id.fingerprint();
    let mut cfg = RelayConfig::loopback();
    cfg.identity = Some(id);
    let r = Relay::start(cfg).await.map_err(|e| format!("start: {e}"))?;
    let res = async {
        let mut c = connect_pinned(&r.url(), fp, Duration::from_secs(5))
            .await
            .map_err(|e| format!("connect: {e}"))?;
        c.send(&ClientFrame::Ping).await.map_err(|e| format!("{e}"))?;
        match c.recv().await.map_err(|e| format!("{e}"))? {
            ServerEvent::Control(ServerFrame::Pong) => Ok(()),
            o => Err(format!("unexpected {o:?}")),
        }
    }
    .await;
    r.shutdown().await;
    res
}

/// F2 re-attack: every byte of the WHOLE v3 blob, with four masks; plus 20,000 random two-byte
/// changes. Property: refused, or the same fingerprint; never a different one; never a panic.
#[test]
fn r2_01_every_byte_four_masks_and_random_pairs() {
    let mut worst = Duration::ZERO;
    let mut tot = (0usize, 0usize, 0usize, 0usize); // n, refused, same, different
    let mut different = Vec::new();
    let mut kinds = std::collections::BTreeMap::<String, usize>::new();
    for round in 0..3 {
        let id = fresh();
        let fp = id.fingerprint();
        let blob = id.to_blob().unwrap().as_bytes().to_vec();
        for pos in 0..blob.len() {
            for mask in [0x01u8, 0x80, 0xff, 0x55] {
                let mut b = blob.clone();
                b[pos] ^= mask;
                let t = Instant::now();
                let r = std::panic::catch_unwind(|| TlsIdentity::from_blob(&b));
                worst = worst.max(t.elapsed());
                tot.0 += 1;
                match r {
                    Err(_) => panic!("PANIC at pos {pos} mask {mask:#x}"),
                    Ok(Err(e)) => {
                        tot.1 += 1;
                        *kinds.entry(format!("{e:?}").split([' ', '{', '(']).next().unwrap().to_string()).or_default() += 1;
                    }
                    Ok(Ok(i)) if i.fingerprint() == fp => tot.2 += 1,
                    Ok(Ok(_)) => {
                        tot.3 += 1;
                        different.push((round, pos, mask));
                    }
                }
            }
        }
        // random pairs (deterministic LCG)
        let mut s: u64 = 0x9e3779b97f4a7c15 ^ round as u64;
        let mut next = || {
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            (s >> 33) as usize
        };
        for _ in 0..20_000 {
            let mut b = blob.clone();
            let (p1, p2) = (next() % b.len(), next() % b.len());
            b[p1] ^= (next() % 255 + 1) as u8;
            b[p2] ^= (next() % 255 + 1) as u8;
            tot.0 += 1;
            match TlsIdentity::from_blob(&b) {
                Err(_) => tot.1 += 1,
                Ok(i) if i.fingerprint() == fp => tot.2 += 1,
                Ok(_) => {
                    tot.3 += 1;
                    different.push((round, p1 * 100_000 + p2, 0));
                }
            }
        }
    }
    println!(
        "R2_01 changes={} refused={} same_fp={} DIFFERENT_fp={} worst_import={:?} kinds={kinds:?}",
        tot.0, tot.1, tot.2, tot.3, worst
    );
    assert!(different.is_empty(), "different fingerprints: {:?}", &different[..different.len().min(10)]);
}

/// What the stored hash does NOT protect against: someone who can write the file edits the
/// certificate (here: a byte in its serial, and a byte in its own signature) and stores the new
/// hash. Records whether the edited identity loads and serves a pinned client under a NEW pin.
#[tokio::test(flavor = "multi_thread")]
async fn r2_02_rehashed_edited_certificate() {
    let id = fresh();
    let fp = id.fingerprint();
    let blob = id.to_blob().unwrap().as_bytes().to_vec();
    let (cert, key, hash) = split3(&blob);
    assert_eq!(hash, fp.0.to_vec(), "the stored hash is the pin");
    // serial: rcgen puts the serial early in the TBS; byte 15 is inside it for this generator
    let mut c1 = cert.clone();
    c1[15] ^= 0x01;
    // signature: the last byte of the DER is the last byte of the signature value
    let mut c2 = cert.clone();
    let n = c2.len();
    c2[n - 1] ^= 0x01;
    for (what, c) in [("serial byte 15", c1), ("last signature byte", c2)] {
        let plain = join3(IDENTITY_BLOB_HEADER, &c, &key, &hash);
        let r_plain = TlsIdentity::from_blob(&plain).map(|i| i.fingerprint());
        let re = rehash(IDENTITY_BLOB_HEADER, &c, &key);
        match TlsIdentity::from_blob(&re) {
            Ok(i) => {
                let nfp = i.fingerprint();
                let served = serves(i).await;
                println!("R2_02 {what}: without rehash -> {r_plain:?}; WITH rehash -> LOADED, fingerprint changed={} , serves a client pinned to the new fp: {served:?}", nfp != fp);
            }
            Err(e) => println!("R2_02 {what}: without rehash -> {r_plain:?}; WITH rehash -> refused {e:?}"),
        }
    }
    // whole replacement: another valid identity is simply another valid file
    let other = fresh();
    println!(
        "R2_02 replaced by another identity: loads={}",
        TlsIdentity::from_blob(other.to_blob().unwrap().as_bytes()).is_ok()
    );
}

/// Version-line variants and v1/v2 forms of the CURRENT body and of a round-1-shaped body.
#[test]
fn r2_03_version_lines() {
    let id = fresh();
    let blob = id.to_blob().unwrap().as_bytes().to_vec();
    let (cert, key, hash) = split3(&blob);
    let body3 = &blob[IDENTITY_BLOB_HEADER.len()..];
    let mut v1_old = b"coagent-relay-identity v1\n".to_vec(); // round-1 layout: no hash
    v1_old.extend_from_slice(&join3(b"", &cert, &key, b""));
    let mut out = Vec::new();
    let cases: Vec<(&str, Vec<u8>)> = vec![
        ("v1 + round-1 body (no hash)", v1_old),
        ("v1 + v3 body", [b"coagent-relay-identity v1\n".as_ref(), body3].concat()),
        ("v2 + v3 body", [b"coagent-relay-identity v2\n".as_ref(), body3].concat()),
        ("v3 CRLF", [b"coagent-relay-identity v3\r\n".as_ref(), body3].concat()),
        ("v3 + space", [b"coagent-relay-identity v3 \n".as_ref(), body3].concat()),
        ("v03", [b"coagent-relay-identity v03\n".as_ref(), body3].concat()),
        ("V3 upper", [b"coagent-relay-identity V3\n".as_ref(), body3].concat()),
        ("v4", [b"coagent-relay-identity v4\n".as_ref(), body3].concat()),
        ("v30", [b"coagent-relay-identity v30\n".as_ref(), body3].concat()),
        ("leading space", [b" coagent-relay-identity v3\n".as_ref(), body3].concat()),
        ("header only", IDENTITY_BLOB_HEADER.to_vec()),
        ("header w/o newline", IDENTITY_BLOB_HEADER[..IDENTITY_BLOB_HEADER.len() - 1].to_vec()),
        ("empty", vec![]),
        ("valid", blob.clone()),
        ("hash 31 bytes", join3(IDENTITY_BLOB_HEADER, &cert, &key, &hash[..31])),
        ("hash 33 bytes", join3(IDENTITY_BLOB_HEADER, &cert, &key, &[&hash[..], &[0u8]].concat())),
        ("hash all zero", join3(IDENTITY_BLOB_HEADER, &cert, &key, &[0u8; 32])),
        ("no hash", join3(IDENTITY_BLOB_HEADER, &cert, &key, b"")),
    ];
    for (name, b) in cases {
        let r = TlsIdentity::from_blob(&b);
        let s = match &r {
            Ok(i) => format!("ACCEPTED same_fp={}", i.fingerprint() == id.fingerprint()),
            Err(e) => format!("refused {e:?}"),
        };
        println!("R2_03 {name:28} -> {s}");
        out.push((name, r.is_ok()));
    }
    for (name, ok) in out {
        assert_eq!(ok, name == "valid", "{name}");
    }
}

/// Length fields at u32 extremes, in both length positions; must refuse fast, without panic.
#[test]
fn r2_04_length_extremes() {
    let id = fresh();
    let blob = id.to_blob().unwrap().as_bytes().to_vec();
    let (cert, _key, _) = split3(&blob);
    let h = IDENTITY_BLOB_HEADER.len();
    let k0 = h + 4 + cert.len();
    for (where_, off) in [("cert len", h), ("key len", k0)] {
        for v in [0u32, 1, 0x7fff_ffff, 0x8000_0000, 0xffff_fffe, 0xffff_ffff, IDENTITY_BLOB_MAX as u32, blob.len() as u32] {
            let mut b = blob.clone();
            b[off..off + 4].copy_from_slice(&v.to_be_bytes());
            let t = Instant::now();
            let r = std::panic::catch_unwind(|| TlsIdentity::from_blob(&b));
            let el = t.elapsed();
            let s = match r {
                Err(_) => "PANIC".to_string(),
                Ok(Ok(_)) => "ACCEPTED".to_string(),
                Ok(Err(e)) => format!("refused {e:?}"),
            };
            println!("R2_04 {where_} = {v:#010x}: {s} ({el:?})");
            assert!(s.starts_with("refused"), "{where_} {v:#x}: {s}");
        }
    }
    // a key length that consumes exactly everything (so no hash is left): Truncated(CertificateHash)?
    let (cert, key, _) = split3(&blob);
    let mut b = join3(IDENTITY_BLOB_HEADER, &cert, &key, b"");
    let r = TlsIdentity::from_blob(&b);
    println!("R2_04 no room for the hash: {r:?}", r = r.as_ref().map(|_| ()).map_err(|e| format!("{e:?}")));
    assert!(matches!(r, Err(IdentityBlobError::Truncated { part: IdentityPart::CertificateHash })));
    b.truncate(0);
}
