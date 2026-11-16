//! QA gate (M1 RELAY-IDENTITY): library-level probes of `TlsIdentity::{to_blob, from_blob}`.
//! Written by the independent gate; not part of the branch. Prints a summary with `--nocapture`.

use std::time::Duration;

use coagent_relay::{
    connect_pinned, ClientFrame, IdentityBlobError, Relay, RelayConfig, ServerEvent, ServerFrame,
    TlsIdentity, IDENTITY_BLOB_HEADER, IDENTITY_BLOB_MAX,
};

fn fresh() -> TlsIdentity {
    TlsIdentity::generate(&["127.0.0.1".parse().unwrap()], &[]).unwrap()
}

fn split(blob: &[u8]) -> (Vec<u8>, Vec<u8>) {
    let h = IDENTITY_BLOB_HEADER.len();
    let cl = u32::from_be_bytes(blob[h..h + 4].try_into().unwrap()) as usize;
    let cert = blob[h + 4..h + 4 + cl].to_vec();
    let k0 = h + 4 + cl;
    let kl = u32::from_be_bytes(blob[k0..k0 + 4].try_into().unwrap()) as usize;
    let key = blob[k0 + 4..k0 + 4 + kl].to_vec();
    (cert, key)
}

fn join(cert: &[u8], key: &[u8]) -> Vec<u8> {
    let mut v = IDENTITY_BLOB_HEADER.to_vec();
    v.extend_from_slice(&(cert.len() as u32).to_be_bytes());
    v.extend_from_slice(cert);
    v.extend_from_slice(&(key.len() as u32).to_be_bytes());
    v.extend_from_slice(key);
    v
}

fn hexs(b: &[u8]) -> String {
    b.iter().map(|x| format!("{x:02x}")).collect()
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

#[test]
fn g01_truncate_at_every_byte_is_refused_without_panic() {
    let id = fresh();
    let blob = id.to_blob().unwrap().as_bytes().to_vec();
    for n in 0..blob.len() {
        assert!(TlsIdentity::from_blob(&blob[..n]).is_err(), "prefix {n} accepted");
    }
    assert!(TlsIdentity::from_blob(&blob).is_ok());
    println!("G01 blob len {} : every prefix refused", blob.len());
}

#[tokio::test(flavor = "multi_thread")]
async fn g02_flip_every_byte() {
    let id = fresh();
    let fp0 = id.fingerprint();
    let blob = id.to_blob().unwrap().as_bytes().to_vec();
    let (cert, _key) = split(&blob);
    let cert_lo = IDENTITY_BLOB_HEADER.len() + 4;
    let cert_hi = cert_lo + cert.len();
    let mut refused = 0;
    let mut same = 0;
    let mut differ: Vec<(usize, u8)> = Vec::new();
    let mut accepted_same_pos: Vec<(usize, u8)> = Vec::new();
    let mut served_fail = Vec::new();
    for pos in 0..blob.len() {
        for mask in [0x01u8, 0x80, 0xff] {
            let mut b = blob.clone();
            b[pos] ^= mask;
            match TlsIdentity::from_blob(&b) {
                Err(_) => refused += 1,
                Ok(m) => {
                    if m.fingerprint() == fp0 {
                        same += 1;
                        accepted_same_pos.push((pos, mask));
                    } else {
                        differ.push((pos, mask));
                    }
                    if let Err(e) = serves(m).await {
                        served_fail.push((pos, mask, e));
                    }
                }
            }
        }
    }
    let in_cert = differ
        .iter()
        .filter(|(p, _)| *p >= cert_lo && *p < cert_hi)
        .count();
    println!(
        "G02 blob len {} cert [{cert_lo},{cert_hi}) : {} mutants : refused {refused}, accepted-same-fp {same}, accepted-DIFFERENT-fp {} (of which inside cert bytes {in_cert}); serve failures {}",
        blob.len(),
        blob.len() * 3,
        differ.len(),
        served_fail.len()
    );
    println!("G02 different-fp positions (pos,mask): {:?}", differ);
    println!("G02 same-fp accepted positions (pos,mask): {:?}", accepted_same_pos);
    println!("G02 serve failures: {:?}", served_fail);
}

#[test]
fn g03_length_extremes_and_variants() {
    let id = fresh();
    let blob = id.to_blob().unwrap().as_bytes().to_vec();
    let (cert, key) = split(&blob);
    let h = IDENTITY_BLOB_HEADER.len();
    let mut out = Vec::new();
    for v in [0u32, 1, 0x7fff_ffff, 0x8000_0000, 0xffff_fffe, 0xffff_ffff, IDENTITY_BLOB_MAX as u32, cert.len() as u32 + 1, cert.len() as u32 - 1] {
        let mut b = blob.clone();
        b[h..h + 4].copy_from_slice(&v.to_be_bytes());
        out.push((format!("certlen={v:#x}"), TlsIdentity::from_blob(&b).err()));
        let mut b = blob.clone();
        let k0 = h + 4 + cert.len();
        b[k0..k0 + 4].copy_from_slice(&v.to_be_bytes());
        out.push((format!("keylen={v:#x}"), TlsIdentity::from_blob(&b).err()));
    }
    let body = &blob[h..];
    let variants: Vec<(&str, Vec<u8>)> = vec![
        ("CRLF header", [b"coagent-relay-identity v1\r\n".as_slice(), body].concat()),
        ("space before NL", [b"coagent-relay-identity v1 \n".as_slice(), body].concat()),
        ("v01", [b"coagent-relay-identity v01\n".as_slice(), body].concat()),
        ("v2", [b"coagent-relay-identity v2\n".as_slice(), body].concat()),
        ("V1 caps", [b"COAGENT-RELAY-IDENTITY V1\n".as_slice(), body].concat()),
        ("leading BOM", [b"\xef\xbb\xbf".as_slice(), &blob].concat()),
        ("leading NL", [b"\n".as_slice(), &blob].concat()),
        ("header only", IDENTITY_BLOB_HEADER.to_vec()),
        ("header without NL", IDENTITY_BLOB_HEADER[..IDENTITY_BLOB_HEADER.len() - 1].to_vec()),
        ("empty", vec![]),
        ("one trailing byte", [blob.as_slice(), b"\0"].concat()),
        ("trailing NL", [blob.as_slice(), b"\n"].concat()),
        ("empty cert", join(&[], &key)),
        ("empty key", join(&cert, &[])),
        ("cert twice in cert part", join(&[cert.clone(), cert.clone()].concat(), &key)),
        ("cert + 1 garbage byte in cert part", join(&[cert.clone(), vec![0]].concat(), &key)),
        ("key + 1 garbage byte in key part", join(&cert, &[key.clone(), vec![0]].concat())),
        ("over cap by one (zeros)", vec![0u8; IDENTITY_BLOB_MAX + 1]),
        ("valid blob padded to cap+1 with trailing", { let mut b = blob.clone(); b.resize(IDENTITY_BLOB_MAX + 1, 0); b }),
        ("valid blob padded to exactly cap", { let mut b = blob.clone(); b.resize(IDENTITY_BLOB_MAX, 0); b }),
    ];
    for (name, b) in variants {
        out.push((name.to_string(), TlsIdentity::from_blob(&b).err()));
    }
    for (n, e) in &out {
        println!("G03 {n:45} -> {e:?}");
        assert!(e.is_some(), "{n} was ACCEPTED");
    }
    // CRLF is UnknownVersion (it starts with the magic); note only.
}

#[test]
fn g04_mismatched_pair_and_kinds() {
    let a = fresh();
    let b = fresh();
    let (ca, _) = split(a.to_blob().unwrap().as_bytes());
    let (_, kb) = split(b.to_blob().unwrap().as_bytes());
    let e = TlsIdentity::from_blob(&join(&ca, &kb)).err();
    println!("G04 cert A + key B -> {e:?}");
    assert_eq!(e, Some(IdentityBlobError::KeyDoesNotMatchCertificate));
    // key B's bytes where the certificate goes, cert where the key goes
    let (cb, kb2) = split(b.to_blob().unwrap().as_bytes());
    println!("G04 swapped parts -> {:?}", TlsIdentity::from_blob(&join(&kb2, &cb)).err());
}

#[test]
fn g05_round_trip_exact_and_no_regeneration() {
    let a = fresh();
    let b1 = a.to_blob().unwrap().as_bytes().to_vec();
    let a2 = TlsIdentity::from_blob(&b1).unwrap();
    let b2 = a2.to_blob().unwrap().as_bytes().to_vec();
    let a3 = TlsIdentity::from_blob(&b2).unwrap();
    assert_eq!(b1, b2);
    assert_eq!(a.fingerprint(), a2.fingerprint());
    assert_eq!(a.fingerprint(), a3.fingerprint());
    // fingerprint is sha256 of the stored cert bytes: compute independently via the Display form
    println!("G05 export/import/export identical ({} bytes), fp stable {}", b1.len(), a3.fingerprint());
}

#[tokio::test(flavor = "multi_thread")]
async fn g06_foreign_key_types_and_certificates() {
    use rcgen::{BasicConstraints, CertificateParams, IsCa, KeyPair, SanType};
    let mk = |alg: Option<&'static rcgen::SignatureAlgorithm>, ca: bool, expired: bool, future: bool| {
        let key = match alg {
            Some(a) => KeyPair::generate_for(a).unwrap(),
            None => KeyPair::generate().unwrap(),
        };
        let mut p = CertificateParams::new(Vec::<String>::new()).unwrap();
        p.subject_alt_names.push(SanType::IpAddress("127.0.0.1".parse().unwrap()));
        if ca {
            p.is_ca = IsCa::Ca(BasicConstraints::Unconstrained);
        }
        if expired {
            p.not_before = rcgen::date_time_ymd(2000, 1, 1);
            p.not_after = rcgen::date_time_ymd(2001, 1, 1);
        }
        if future {
            p.not_before = rcgen::date_time_ymd(2090, 1, 1);
            p.not_after = rcgen::date_time_ymd(2091, 1, 1);
        }
        let c = p.self_signed(&key).unwrap();
        join(c.der().as_ref(), &key.serialize_der())
    };
    let cases: Vec<(&str, Vec<u8>)> = vec![
        ("ed25519", mk(Some(&rcgen::PKCS_ED25519), false, false, false)),
        ("p384", mk(Some(&rcgen::PKCS_ECDSA_P384_SHA384), false, false, false)),
        ("CA cert", mk(None, true, false, false)),
        ("expired cert", mk(None, false, true, false)),
        ("not-yet-valid cert", mk(None, false, false, true)),
    ];
    for (n, b) in cases {
        match TlsIdentity::from_blob(&b) {
            Err(e) => println!("G06 {n:20} -> refused {e:?}"),
            Ok(id) => {
                let s = serves(id).await;
                println!("G06 {n:20} -> ACCEPTED; pinned client: {s:?}");
            }
        }
    }
    // a blob from env (e.g. made with openssl: RSA)
    if let Ok(p) = std::env::var("GATE_EXTRA_BLOBS") {
        for f in p.split(':') {
            let b = std::fs::read(f).unwrap();
            match TlsIdentity::from_blob(&b) {
                Err(e) => println!("G06 file {f} -> refused {e:?}"),
                Ok(id) => {
                    let s = serves(id).await;
                    println!("G06 file {} -> ACCEPTED; pinned client: {s:?}", f.rsplit('/').next().unwrap());
                }
            }
        }
    }
}

#[test]
fn g07_debug_display_never_holds_key() {
    let a = fresh();
    let blob = a.to_blob().unwrap();
    let (_, key) = split(blob.as_bytes());
    let texts = vec![
        format!("{a:?}"),
        format!("{blob:?}"),
        format!("{:?}", TlsIdentity::from_blob(&blob.as_bytes()[..50]).err()),
        format!("{}", IdentityBlobError::KeyDoesNotMatchCertificate),
    ];
    let lower = hexs(&key[key.len() - 16..]);
    let dec = format!("{:?}", &key[key.len() - 8..]);
    let dec_inner = dec.trim_matches(|c| c == '[' || c == ']').to_string();
    for t in &texts {
        assert!(!t.contains(&lower) && !t.to_uppercase().contains(&lower.to_uppercase()) && !t.contains(&dec_inner), "key in {t}");
    }
    // positive control
    let ctl = format!("{:?}", key);
    assert!(ctl.contains(&dec_inner));
    println!("G07 no key in {} Debug/Display forms; control found key", texts.len());
}
