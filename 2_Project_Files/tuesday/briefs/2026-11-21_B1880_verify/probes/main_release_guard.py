"""Release guard: judges a release artefact folder before anything is packaged from it.

usage: python3 -I build/release_guard.py <artefact folder> [--denylist <file>]

It walks every file under the folder and every member of every ZIP-format file it meets (a file
whose first four bytes are PK 03 04), nested to depth 3.

  G1  No file of a release artefact is HP's OXPd2Lib assembly or a build against it.
      Fires on a base name equal to OXPd2Lib.dll ignoring case, and on a file that starts with the
      two bytes MZ and holds the string OXPd2Lib (ignoring case) in ASCII or UTF-16LE.
  G2  No certificate of a release artefact is on the deny-list, and no file carries the development
      CA's file name. Fires on a base name starting ExtSDKRootCA ignoring case; on a PEM CERTIFICATE
      block whose DER bytes have a listed SHA-256; and on a DER certificate with a listed SHA-256
      anywhere inside a file (the whole file, or embedded in a larger one).
  G3  A file the guard cannot read, or a ZIP it cannot open, is a finding, never a skip. The same
      holds for a folder link it will not follow, a ZIP nested deeper than it reads, a ZIP member
      too large to read and a PEM block that does not decode.

Exit 0 and "GUARD: clean (<n> files)" when no rule fires (n counts the files on disk);
exit 1 and one line "GUARD: <rule> <path>" per finding;
exit 2 on a folder that does not exist or holds 0 files (an empty artefact is never clean), and
on a deny-list that is missing or holds a line that is no fingerprint.

The guard does not open tar, gzip or other archive formats: it is run on the publish folder,
before packaging.
"""
import base64
import binascii
import hashlib
import io
import os
import re
import stat
import sys
import zipfile

LIB = b"oxpd2lib"
LIB_UTF16 = "oxpd2lib".encode("utf-16-le")
LIB_FILE_NAME = "oxpd2lib.dll"
CA_NAME_PREFIX = "extsdkrootca"
ZIP_MAGIC = b"PK\x03\x04"
MAX_ZIP_DEPTH = 3
MAX_MEMBER_BYTES = 1 << 30
PEM_BLOCK = re.compile(rb"-----BEGIN CERTIFICATE-----(.*?)-----END CERTIFICATE-----", re.DOTALL)
FINGERPRINT = re.compile(r"[0-9a-f]{64}")
DEFAULT_DENYLIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "denylist", "dev_ca_sha256.txt")


class DenylistError(Exception):
    pass


def load_denylist(path):
    try:
        with open(path, "r", encoding="ascii") as handle:
            raw_lines = handle.read().splitlines()
    except (OSError, UnicodeError) as error:
        raise DenylistError("bad deny-list %s: %s" % (path, error.__class__.__name__))
    fingerprints = set()
    for number, raw in enumerate(raw_lines, 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if not FINGERPRINT.fullmatch(line):
            raise DenylistError("bad deny-list line %d of %s (want 64 lower-case hex characters)" % (number, path))
        fingerprints.add(line)
    return fingerprints


def embedded_der_fingerprints(data):
    """SHA-256 of every byte run that is framed like a DER certificate (30 82 <2 length bytes>)."""
    start = data.find(b"\x30\x82")
    while start != -1:
        if start + 4 <= len(data):
            end = start + 4 + int.from_bytes(data[start + 2:start + 4], "big")
            if end <= len(data):
                yield hashlib.sha256(data[start:end]).hexdigest()
        start = data.find(b"\x30\x82", start + 1)


class Guard:
    def __init__(self, denylist):
        self.denylist = denylist
        self.findings = []
        self.files = 0

    def find(self, rule, path):
        finding = (rule, path)
        if finding not in self.findings:
            self.findings.append(finding)

    def judge(self, path, data, depth):
        base = path.rsplit("!", 1)[-1].rsplit("/", 1)[-1].lower()
        lowered = data.lower()

        if base == LIB_FILE_NAME:
            self.find("G1", path)
        if data[:2] == b"MZ" and (LIB in lowered or LIB_UTF16 in lowered):
            self.find("G1", path)

        if base.startswith(CA_NAME_PREFIX):
            self.find("G2", path)
        for match in PEM_BLOCK.finditer(data):
            try:
                der = base64.b64decode(b"".join(match.group(1).split()), validate=True)
            except (binascii.Error, ValueError):
                self.find("G3", path)
                continue
            if hashlib.sha256(der).hexdigest() in self.denylist:
                self.find("G2", path)
        if self.denylist:
            for fingerprint in embedded_der_fingerprints(data):
                if fingerprint in self.denylist:
                    self.find("G2", path)
                    break

        if data[:4] == ZIP_MAGIC:
            self.judge_zip(path, data, depth)

    def judge_zip(self, path, data, depth):
        if depth >= MAX_ZIP_DEPTH:
            self.find("G3", path)
            return
        try:
            archive = zipfile.ZipFile(io.BytesIO(data))
            members = archive.infolist()
        except Exception:  # any failure to open is the finding: an archive that cannot be judged
            self.find("G3", path)
            return
        with archive:
            for member in members:
                if member.is_dir():
                    continue
                member_path = path + "!" + member.filename
                if member.file_size > MAX_MEMBER_BYTES:
                    self.find("G3", member_path)
                    continue
                try:
                    member_data = archive.read(member)
                except Exception:  # encrypted, damaged or unsupported: cannot be judged
                    self.find("G3", member_path)
                    continue
                self.judge(member_path, member_data, depth + 1)

    def walk(self, folder):
        for current, folders, names in os.walk(folder, followlinks=False):
            folders.sort()
            for name in sorted(folders):
                if os.path.islink(os.path.join(current, name)):
                    self.find("G3", self.relative(folder, os.path.join(current, name)))
            for name in sorted(names):
                full = os.path.join(current, name)
                path = self.relative(folder, full)
                self.files += 1
                try:
                    if not stat.S_ISREG(os.stat(full).st_mode):
                        raise OSError("not a regular file")
                    with open(full, "rb") as handle:
                        data = handle.read()
                except OSError:
                    self.find("G3", path)
                    continue
                self.judge(path, data, 0)

    @staticmethod
    def relative(folder, full):
        return os.path.relpath(full, folder).replace(os.sep, "/")


def main(argv):
    args = list(argv)
    denylist_path = DEFAULT_DENYLIST
    if "--denylist" in args:
        at = args.index("--denylist")
        if at + 1 >= len(args):
            print("usage: release_guard.py <artefact folder> [--denylist <file>]")
            return 2
        denylist_path = args[at + 1]
        del args[at:at + 2]
    if len(args) != 1:
        print("usage: release_guard.py <artefact folder> [--denylist <file>]")
        return 2
    folder = args[0]

    if not os.path.isdir(folder):
        print("GUARD: no such folder %s" % folder)
        return 2
    try:
        denylist = load_denylist(denylist_path)
    except DenylistError as error:
        print("GUARD: %s" % error)
        return 2

    guard = Guard(denylist)
    guard.walk(folder)
    if guard.files == 0:
        print("GUARD: 0 files under %s (an empty artefact is never clean)" % folder)
        return 2
    if not denylist:
        print("GUARD-WARN: development CA deny-list holds 0 fingerprints (owed)")
    if guard.findings:
        for rule, path in guard.findings:
            print("GUARD: %s %s" % (rule, path))
        return 1
    print("GUARD: clean (%d files)" % guard.files)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
