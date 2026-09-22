"""envelope.py — the record encryption envelope (study §4.2). Scheme string unchanged (`…/v1`); Phase 3 adds recipients.

Writer side (a seat, or Kam's browser — common.js is the twin): a fresh 32-byte data key per record; AES-256-GCM over the
UTF-8 plaintext with a 12-byte IV; AAD binds the ciphertext to its CLEAR routing fields (client|kind|id|ts) so a row moved
to another partition or re-labelled fails to decrypt.

PHASE 3 (2026-09-21, design D-2(b), Tuesday's shape adopted by Wednesday, Kam 12:50 "switch to using the live version
only"): the data key is wrapped RSA-OAEP(SHA-256) to EVERY recipient of the record —
    * Kam's KEY RING: every app/keys/kam-*-public.pub (pilot, laptop, ipad, …) so any of his devices reads any row;
    * the ADDRESSED SEAT's existing certificate public key (app/keys/<seat>-seat-public.pub, exported from the .crt):
      partition WED / Secuura -> wednesday-seat; Datasec -> tuesday-seat; ALL (Kam's "both") -> BOTH seats.
      That is what lets a seat read Kam's live-site replies (Phase 2 D-2). No new seat keypair: the seat's own cert key.
  Shape: `wrapped_keys: [{"kid": <sha256(SPKI)[:16]>, "wrapped_key": <b64>}, …]`; the top-level `kid` / `wrapped_key`
  are KEPT for one release and equal the FIRST Kam-ring entry (the pilot key), so a Phase-2 reader still works.
  Reader side selects its entry by kid (kid_of its own public key); a row with no `wrapped_keys` (pre-migration) falls
  back to the top-level pair. The server never sees a private key and has no decrypt path.

Clear fields stay clear on purpose (study §4.4 items 2-3): client, view, ts, kind, id, role, seat, and for cards
status / option KEYS / ruled / ruled_choice.
"""
import base64, glob, hashlib, json, os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SCHEME = "rsa-oaep-sha256+aes-256-gcm/v1"
KEYS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app", "keys")
SEAT_OF_CLIENT = {"WED": ("wednesday",), "Secuura": ("wednesday",), "Datasec": ("tuesday",), "ALL": ("wednesday", "tuesday")}
_OAEP = padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)

def b64(b: bytes) -> str: return base64.b64encode(b).decode()
def unb64(s: str) -> bytes: return base64.b64decode(s)

def load_public(pem_path: str):
    return serialization.load_pem_public_key(open(pem_path, "rb").read())

def load_private(pem_path: str):
    return serialization.load_pem_private_key(open(pem_path, "rb").read(), password=None)

def kid_of(public_key) -> str:
    der = public_key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return hashlib.sha256(der).hexdigest()[:16]

def kid_of_private(private_key) -> str: return kid_of(private_key.public_key())

def aad_for(clear: dict) -> bytes:
    return "|".join(str(clear.get(k, "")) for k in ("client", "kind", "id", "ts")).encode()

# ---------------- recipients ----------------
def kam_ring(keys_dir: str = KEYS_DIR) -> list:
    """Kam's key ring: [(name, public_key)] for every kam-*-public.pub, PILOT FIRST (it fills the legacy top-level pair)."""
    files = sorted(glob.glob(os.path.join(keys_dir, "kam-*-public.pub")))
    files.sort(key=lambda p: (0 if os.path.basename(p) == "kam-pilot-public.pub" else 1, p))
    ring = [(os.path.basename(p)[len("kam-"):-len("-public.pub")], load_public(p)) for p in files]
    if not ring: raise FileNotFoundError(f"no kam-*-public.pub in {keys_dir}")
    return ring

def seat_public(seat: str, keys_dir: str = KEYS_DIR):
    return load_public(os.path.join(keys_dir, f"{seat}-seat-public.pub"))

def recipients_for(client: str, keys_dir: str = KEYS_DIR, seats=None) -> list:
    """[(name, public_key)] = Kam's whole ring + the seat(s) the partition addresses (SEAT_OF_CLIENT; override with seats=)."""
    out = list(kam_ring(keys_dir))
    for s in (seats if seats is not None else SEAT_OF_CLIENT.get(client, ())):
        out.append((f"{s}-seat", seat_public(s, keys_dir)))
    return out

# ---------------- encrypt ----------------
def wrap(public_key, dk: bytes) -> str: return b64(public_key.encrypt(dk, _OAEP))

def encrypt_text(public_key, plaintext: str, clear: dict, recipients=None) -> dict:
    """`public_key` = the legacy first recipient (fills top-level kid/wrapped_key). `recipients` = [(name, public_key)] wrapped
    into `wrapped_keys` (the first recipient is added automatically if absent). Phase-2 callers passing one key still work."""
    dk = AESGCM.generate_key(bit_length=256)
    iv = os.urandom(12)
    ct = AESGCM(dk).encrypt(iv, plaintext.encode("utf-8"), aad_for(clear))
    env = {"scheme": SCHEME, "kid": kid_of(public_key), "iv": b64(iv), "wrapped_key": wrap(public_key, dk), "ciphertext": b64(ct)}
    if recipients is not None:
        wk, seen = [], set()
        for name, pk in [("_first", public_key)] + list(recipients):
            k = kid_of(pk)
            if k in seen: continue
            seen.add(k); wk.append({"kid": k, "wrapped_key": env["wrapped_key"] if k == env["kid"] else wrap(pk, dk)})
        env["wrapped_keys"] = wk
    return env

def encrypt_record(plaintext: str, clear: dict, keys_dir: str = KEYS_DIR, seats=None) -> dict:
    """Phase 3 default writer: wrap to Kam's whole ring + the partition's seat(s). Every NEW record goes through this."""
    rec = recipients_for(clear["client"], keys_dir, seats)
    return encrypt_text(rec[0][1], plaintext, clear, recipients=rec)

# ---------------- decrypt ----------------
def wrapped_for(env: dict, kid: str):
    """The wrapped data key this kid may open: the matching wrapped_keys entry, else the legacy top-level pair if its kid matches."""
    wk = env.get("wrapped_keys")
    if isinstance(wk, str):
        try: wk = json.loads(wk)
        except Exception: wk = None
    for e in wk or []:
        if isinstance(e, dict) and e.get("kid") == kid: return e["wrapped_key"]
    if env.get("kid") == kid: return env["wrapped_key"]
    return None

def unwrap_data_key(private_key, env: dict) -> bytes:
    """Recover the data key with THIS private key (kid-selected). Bytes only — no text is touched here (Datasec rows may be
    re-wrapped by the migration through this function without their prose ever being decrypted)."""
    if env.get("scheme") != SCHEME:
        raise ValueError(f"unknown scheme {env.get('scheme')!r}")
    w = wrapped_for(env, kid_of_private(private_key))
    if w is None:
        raise KeyError(f"row is not wrapped to kid {kid_of_private(private_key)} (kids: {kids_of(env)})")
    return private_key.decrypt(unb64(w), _OAEP)

def kids_of(env: dict) -> list:
    wk = env.get("wrapped_keys")
    if isinstance(wk, str):
        try: wk = json.loads(wk)
        except Exception: wk = None
    ks = [e.get("kid") for e in (wk or []) if isinstance(e, dict)]
    if env.get("kid") and env["kid"] not in ks: ks.insert(0, env["kid"])
    return ks

def decrypt_text(private_key, env: dict, clear: dict) -> str:
    dk = unwrap_data_key(private_key, env)
    return AESGCM(dk).decrypt(unb64(env["iv"]), unb64(env["ciphertext"]), aad_for(clear)).decode("utf-8")

# ---------------- files (2026-09-22 file drawer): ONE data key, two AES-GCM payloads ----------------
# The row's `ciphertext` is the META JSON ({name, note, size, sha256, mime}; AAD client|file|id|ts — an ordinary envelope row,
# so decrypt_text / the page's decryptRow open it); the file BYTES are a separate AES-GCM payload under the SAME data key with
# its own `iv_blob` and AAD client|fileblob|id|ts (a blob moved under another row fails to open). Wrapped to the same recipient
# set as a message of that partition (Kam's ring + the addressed seat(s)). common.js is the twin.
def blob_aad(clear: dict) -> bytes:
    return aad_for(dict(clear, kind="fileblob"))

def encrypt_file(data: bytes, meta: dict, clear: dict, keys_dir: str = KEYS_DIR, seats=None) -> tuple:
    """-> (env, ct_bytes). env carries scheme/kid/iv/wrapped_key/ciphertext(meta)/wrapped_keys + iv_blob; ct_bytes is what goes to the blob."""
    assert clear.get("kind") == "file", "clear.kind must be 'file'"
    rec = recipients_for(clear["client"], keys_dir, seats)
    dk = AESGCM.generate_key(bit_length=256)
    iv_m, iv_b = os.urandom(12), os.urandom(12)
    ct_meta = AESGCM(dk).encrypt(iv_m, json.dumps(meta, ensure_ascii=False).encode("utf-8"), aad_for(clear))
    ct_blob = AESGCM(dk).encrypt(iv_b, data, blob_aad(clear))
    wk, seen = [], set()
    for name, pk in rec:
        k = kid_of(pk)
        if k in seen: continue
        seen.add(k); wk.append({"kid": k, "wrapped_key": wrap(pk, dk)})
    env = {"scheme": SCHEME, "kid": wk[0]["kid"], "iv": b64(iv_m), "wrapped_key": wk[0]["wrapped_key"], "ciphertext": b64(ct_meta), "wrapped_keys": wk, "iv_blob": b64(iv_b)}
    return env, ct_blob

def decrypt_file(private_key, env: dict, clear: dict, ct_blob: bytes) -> bytes:
    """The file bytes, with THIS private key (kid-selected). `env` is the file row (carries iv_blob)."""
    dk = unwrap_data_key(private_key, env)
    return AESGCM(dk).decrypt(unb64(env["iv_blob"]), ct_blob, blob_aad(dict(clear, kind="file")))

def rewrap(env: dict, dk: bytes, recipients: list) -> dict:
    """Migration: add wrapped_keys entries for `recipients` [(name, public_key)] to an existing envelope, keeping every entry it
    already has (and the top-level pair). Returns the NEW wrapped_keys list. Idempotent: existing kids are not re-wrapped."""
    have = {e["kid"]: e for e in (json.loads(env["wrapped_keys"]) if isinstance(env.get("wrapped_keys"), str) else env.get("wrapped_keys") or [])}
    if env.get("kid") and env["kid"] not in have: have[env["kid"]] = {"kid": env["kid"], "wrapped_key": env["wrapped_key"]}
    for name, pk in recipients:
        k = kid_of(pk)
        if k not in have: have[k] = {"kid": k, "wrapped_key": wrap(pk, dk)}
    return list(have.values())

if __name__ == "__main__":
    # self-test with throwaway keypairs: positive, wrong-key negative, AAD-relabel negative, multi-recipient positive per key,
    # a non-recipient negative, rewrap idempotency + the legacy single-key path.
    from cryptography.hazmat.primitives.asymmetric import rsa
    k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    clear = {"client": "WED", "kind": "message", "id": "selftest", "ts": "2026-09-21T00:00:00Z"}
    env = encrypt_text(k.public_key(), "synthetic self-test text", clear)
    assert "synthetic" not in json.dumps(env) and "wrapped_keys" not in env
    assert decrypt_text(k, env, clear) == "synthetic self-test text"
    wrong = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    try: decrypt_text(wrong, env, clear); raise SystemExit("NEGATIVE CONTROL FAILED: wrong key decrypted")
    except (ValueError, KeyError): pass
    try: decrypt_text(k, env, dict(clear, client="Datasec")); raise SystemExit("AAD CONTROL FAILED: relabelled row decrypted")
    except Exception as e:
        if "CONTROL" in str(e): raise
    # multi-recipient
    lap = rsa.generate_private_key(public_exponent=65537, key_size=2048); seat = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    env2 = encrypt_text(k.public_key(), "synthetic multi text", clear, recipients=[("laptop", lap.public_key()), ("seat", seat.public_key())])
    assert [e["kid"] for e in env2["wrapped_keys"]] == [kid_of(k.public_key()), kid_of(lap.public_key()), kid_of(seat.public_key())]
    assert env2["wrapped_keys"][0]["wrapped_key"] == env2["wrapped_key"], "top-level pair must equal the first ring entry"
    for who in (k, lap, seat): assert decrypt_text(who, env2, clear) == "synthetic multi text"
    try: decrypt_text(wrong, env2, clear); raise SystemExit("NEGATIVE CONTROL FAILED: non-recipient decrypted the multi envelope")
    except KeyError: pass
    # rewrap: legacy env gains lap; second rewrap adds nothing
    dk = unwrap_data_key(k, env)
    wk1 = rewrap(env, dk, [("laptop", lap.public_key())]); env3 = dict(env, wrapped_keys=wk1)
    assert decrypt_text(lap, env3, clear) == "synthetic self-test text" and decrypt_text(k, env3, clear) == "synthetic self-test text"
    wk2 = rewrap(env3, dk, [("laptop", lap.public_key())]); assert wk2 == wk1, "rewrap must be idempotent"
    # JSON-string wrapped_keys (as Table storage returns it) also decrypts
    assert decrypt_text(lap, dict(env3, wrapped_keys=json.dumps(wk1)), clear) == "synthetic self-test text"
    # files: one data key, meta row + blob; both open with a recipient; the blob refuses a relabelled row and a wrong key
    fclear = {"client": "WED", "kind": "file", "id": "selftest-file", "ts": "2026-09-22T00:00:00Z"}
    import tempfile
    from cryptography.hazmat.primitives import serialization as _ser
    with tempfile.TemporaryDirectory() as td:
        for nm, kk in (("kam-pilot-public.pub", k), ("wednesday-seat-public.pub", seat)):
            open(os.path.join(td, nm), "wb").write(kk.public_key().public_bytes(_ser.Encoding.PEM, _ser.PublicFormat.SubjectPublicKeyInfo))
        data = os.urandom(70000)
        fenv, ct = encrypt_file(data, {"name": "synthetic.bin", "note": "self-test"}, fclear, keys_dir=td)
        assert json.loads(decrypt_text(k, fenv, fclear))["name"] == "synthetic.bin" and json.loads(decrypt_text(seat, fenv, fclear))["note"] == "self-test"
        assert decrypt_file(k, fenv, fclear, ct) == data and decrypt_file(seat, fenv, fclear, ct) == data and len(ct) == len(data) + 16
        try: decrypt_file(wrong, fenv, fclear, ct); raise SystemExit("FILE CONTROL FAILED: wrong key opened the blob")
        except KeyError: pass
        try: decrypt_file(k, fenv, dict(fclear, id="other"), ct); raise SystemExit("FILE AAD CONTROL FAILED: relabelled blob opened")
        except Exception as e:
            if "CONTROL" in str(e): raise
        try: decrypt_file(k, dict(fenv, iv_blob=fenv["iv"]), fclear, ct); raise SystemExit("FILE IV CONTROL FAILED: meta IV opened the blob")
        except Exception as e:
            if "CONTROL" in str(e): raise
    print("envelope self-test PASS (positive, wrong-key negative, AAD-relabel negative, multi-recipient x3, non-recipient negative, rewrap idempotent, json-string wrapped_keys, file meta+blob x2 keys + 3 negatives)")
