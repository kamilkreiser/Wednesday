"""envelope.py — the record encryption envelope (study §4.2), pilot scheme v1.

Writer side (a seat): a fresh 32-byte data key per record; AES-256-GCM over the
UTF-8 plaintext with a 12-byte IV; the data key wrapped with Kam's RSA-OAEP
(SHA-256) PUBLIC key. Additional authenticated data (AAD) binds the ciphertext to
its CLEAR routing fields (client|kind|id|ts) so a row moved to another partition
or re-labelled fails to decrypt.

Reader side: Kam's browser (WebCrypto) — see app/static/index.html — or, for the
offline probe, `decrypt_text` below with the private PEM. The server never sees a
private key and has no decrypt path.

Clear fields stay clear on purpose (study §4.4 items 2-3): client, view, ts, kind,
id, role, seat, and for cards status / option KEYS / ruled / ruled_choice.
"""
import base64, hashlib, json, os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SCHEME = "rsa-oaep-sha256+aes-256-gcm/v1"

def b64(b: bytes) -> str: return base64.b64encode(b).decode()
def unb64(s: str) -> bytes: return base64.b64decode(s)

def load_public(pem_path: str):
    return serialization.load_pem_public_key(open(pem_path, "rb").read())

def load_private(pem_path: str):
    return serialization.load_pem_private_key(open(pem_path, "rb").read(), password=None)

def kid_of(public_key) -> str:
    der = public_key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return hashlib.sha256(der).hexdigest()[:16]

def aad_for(clear: dict) -> bytes:
    return "|".join(str(clear.get(k, "")) for k in ("client", "kind", "id", "ts")).encode()

def encrypt_text(public_key, plaintext: str, clear: dict) -> dict:
    dk = AESGCM.generate_key(bit_length=256)
    iv = os.urandom(12)
    ct = AESGCM(dk).encrypt(iv, plaintext.encode("utf-8"), aad_for(clear))
    wrapped = public_key.encrypt(dk, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return {"scheme": SCHEME, "kid": kid_of(public_key), "iv": b64(iv), "wrapped_key": b64(wrapped), "ciphertext": b64(ct)}

def decrypt_text(private_key, env: dict, clear: dict) -> str:
    if env.get("scheme") != SCHEME:
        raise ValueError(f"unknown scheme {env.get('scheme')!r}")
    dk = private_key.decrypt(unb64(env["wrapped_key"]), padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return AESGCM(dk).decrypt(unb64(env["iv"]), unb64(env["ciphertext"]), aad_for(clear)).decode("utf-8")

if __name__ == "__main__":
    # self-test with a throwaway keypair: positive + negative control
    from cryptography.hazmat.primitives.asymmetric import rsa
    k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    clear = {"client": "WED", "kind": "message", "id": "selftest", "ts": "2026-09-21T00:00:00Z"}
    env = encrypt_text(k.public_key(), "synthetic self-test text", clear)
    assert "synthetic" not in json.dumps(env)
    assert decrypt_text(k, env, clear) == "synthetic self-test text"
    wrong = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    try:
        decrypt_text(wrong, env, clear); raise SystemExit("NEGATIVE CONTROL FAILED: wrong key decrypted")
    except ValueError:
        pass
    try:
        decrypt_text(k, env, dict(clear, client="Datasec")); raise SystemExit("AAD CONTROL FAILED: relabelled row decrypted")
    except Exception as e:
        if "CONTROL" in str(e): raise
    print("envelope self-test PASS (positive, wrong-key negative, AAD-relabel negative)")
