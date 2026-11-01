# Operator 49, task 1 (KS-1898): test_only brief generator. Reuses spark/gen/mk.py (rd, udiff).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='d7691f35312ea158f043e87a3227e477cccb183d'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
TEST='Blockchain/Dev/services/vc-issuer/src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts'
PROD='Blockchain/Dev/services/vc-issuer/src/routes/credentials.ts'
REF='Blockchain/Dev/services/vc-issuer/src/__tests__/ks1116-presentation-and-credential-reads-bound-to-the-creator.test.ts'
DIR='ks_1898_o49_p1_vcissuer_revoke_byte_identical_logger'
old=mk.rd(TEST); new=old
EDITS=[
# 1: V8b-g body
("""  ])('%s revokes an owner-less row of tenant 1 -> 404 and NO UPDATE', async (_label, caller) => {
    expectNotFound(await revoke(mods, caller, OWNERLESS_T1_ROW));
    expect(updates()).toEqual([]);
  });
""","""  ])('%s revokes an owner-less row of tenant 1 -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged', async (_label, caller) => {
    const refused = await revoke(mods, caller, OWNERLESS_T1_ROW);
    expectNotFound(refused);
    expect(updates()).toEqual([]);
    expectNothingLoggedForTheRefusal();
    expectByteIdentical(refused, await revoke(mods, caller, UNKNOWN_ID));
  });
"""),
# 2: V9 body
("""  ])('%s revokes a pre-054 row with no owner and no tenant -> 404 and NO UPDATE', async (_label, caller) => {
    expectNotFound(await revoke(mods, caller, LEGACY_ROW));
    expect(updates()).toEqual([]);
  });
""","""  ])('%s revokes a pre-054 row with no owner and no tenant -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged', async (_label, caller) => {
    const refused = await revoke(mods, caller, LEGACY_ROW);
    expectNotFound(refused);
    expect(updates()).toEqual([]);
    expectNothingLoggedForTheRefusal();
    expectByteIdentical(refused, await revoke(mods, caller, UNKNOWN_ID));
  });
"""),
# 3: memory owner-less cell, after V5
("""  it('V5 CONTROL: an unknown id -> 404 for the issuer too', async () => {
    expectNotFound(await revoke(mods, ALICE, UNKNOWN_ID));
  });
""","""  it('V5 CONTROL: an unknown id -> 404 for the issuer too', async () => {
    expectNotFound(await revoke(mods, ALICE, UNKNOWN_ID));
  });

  // KS-1898: an owner-less row in MEMORY (stored with the default OWNERLESS owner, as a caller that forgets the owner does).
  it.each([
    ['V14a an OWNER of tenant 1', BOB],
    ['V14b an ORG_ADMIN of tenant 1', ORG_ADMIN],
    ['V14c a SYSTEM_ADMIN of tenant 1', SYSTEM_ADMIN],
    ['V14d a SUPER_ADMIN of tenant 1', SUPER_ADMIN],
  ])('%s revokes an owner-less memory row -> 404 byte-identical to an unknown id; unchanged; reason not logged', async (_label, caller) => {
    const id = 'https://secuura.io/credentials/1851d0b0-0000-4000-8000-000000000014';
    await mods.repo.store(storedCredential(id));
    const before = JSON.stringify(await mods.repo.getById(id));
    Object.values(loggerMock).forEach((fn) => fn.mockClear());

    const refused = await revoke(mods, caller, id);

    expectNotFound(refused);
    expectNothingLoggedForTheRefusal();
    expect(JSON.stringify(await mods.repo.getById(id))).toBe(before);
    expect((await mods.repo.getById(id))?.credentialStatus?.revoked).not.toBe(true);
    expectByteIdentical(refused, await revoke(mods, caller, UNKNOWN_ID));
  });
"""),
]
for o,n in EDITS:
    assert new.count(o)==1,o[:50]; new=new.replace(o,n)
import difflib
def udiff2(path,a,b,n=2):
    A=a.splitlines(keepends=True);B=b.splitlines(keepends=True)
    body=list(difflib.unified_diff(A,B,n=n))[2:]
    return ''.join(['--- a/%s\n'%path,'+++ b/%s\n'%path]+mk.trim(body))
pd=udiff2(TEST,old,new)   # n=2 so V8 and V9 are two hunks (no blank context line)
d=BR+DIR; os.makedirs(d,exist_ok=True)
open(d+'/golden.diff','w',encoding='utf-8').write(pd)
print(pd)
