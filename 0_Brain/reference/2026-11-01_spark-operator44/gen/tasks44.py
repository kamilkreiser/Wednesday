TASKS={}
GP='Blockchain/Dev/services/governance/'
G_REF=GP+'src/__tests__/ks1845-process-expired-requires-a-platform-admin.test.ts'
S9="This file is neither `tenant-context.ts` nor `tenant-pool-manager.ts` and is outside services/auth, services/originate, services/anchoring, services/tenant-provisioning and vc-issuer; the S9 brief itself was not re-read by the operator."
def mkold(msg, ret):
    return ("  } catch (err: any) {\n    logger.error('%s', { error: err instanceof Error ? err.message : String(err) });\n    return %s;\n  }\n")%(msg,ret)
def mknew(msg, ret):
    return ("  } catch (err: any) {\n    let reason: string;\n    try {\n      reason = err instanceof Error ? err.message : String(err);\n    } catch {\n      reason = 'unreadable thrown value';\n    }\n    logger.error('%s', { error: reason });\n    return %s;\n  }\n")%(msg,ret)
def mktest(fn, call, msg, okname, okexp, descr):
    return f"""// KS-1868: {descr} must still log its ERROR line and {okname} when the thrown value
// itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws,
// throws on `.message`).
// The db stand-in is a plain function, not a jest.fn(): a spy inspects what it rejects with and
// could itself fail on a revoked Proxy before the code under test saw it.
const mockHolder: {{ toThrow: unknown; error: jest.Mock }} = {{ toThrow: undefined, error: jest.fn() }};

jest.mock('../db', () => ({{
  isDbAvailable: () => true,
  query: () => Promise.reject(mockHolder.toThrow),
}}));
jest.mock('../utils/logger', () => ({{
  logger: {{ info: jest.fn(), warn: jest.fn(), debug: jest.fn(), error: (...a: unknown[]) => mockHolder.error(...a) }},
}}));

const {{ {fn} }} = require('../services/governanceService');

const ERRORS = () => mockHolder.error.mock.calls.filter((c) => String(c[0]).includes('{msg}'));

describe('KS-1868 {descr} reads the thrown value safely', () => {{
  beforeEach(() => {{
    mockHolder.toThrow = undefined;
    mockHolder.error = jest.fn();
  }});

  it('control ks1868 C1 an ordinary Error still logs its message and {okname}', async () => {{
    mockHolder.toThrow = new Error('db down');
    await expect({call}).resolves.{okexp};
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({{ error: 'db down' }});
  }});

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and {okname}', async () => {{
    const {{ proxy, revoke }} = Proxy.revocable({{}}, {{}});
    revoke();
    mockHolder.toThrow = proxy;
    await expect({call}).resolves.{okexp};
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({{ error: 'unreadable thrown value' }});
  }});

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and {okname}', async () => {{
    mockHolder.toThrow = Object.create(Error.prototype, {{
      message: {{
        get() {{
          throw new Error('getter boom');
        }},
      }},
    }});
    await expect({call}).resolves.{okexp};
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({{ error: 'unreadable thrown value' }});
  }});
}});
"""
def add(key, slug, helper, exported, call, msg, ret, okname, okexp, line, consq_ret):
    TASKS[key]=dict(svc='governance', runner_dir='Blockchain/Dev/services/governance', ref=G_REF, s9note=S9, runner='jest', runcmd='',
     dir='ks_1868_o44_%s_governance_%s_unreadable_throw'%(key,slug),
     prod=GP+'src/services/governanceService.ts', test=GP+'src/__tests__/ks1868-%s-unreadable-throw.test.ts'%slug.replace('_','-'),
     old=mkold(msg,ret), new=mknew(msg,ret), tbody=mktest(exported,call,msg,okname,okexp,'`%s`'%helper), where_line=line, fn='`%s`'%helper, file='governanceService.ts',
     shape="a holder object whose name starts with `mock`, `jest.mock(...)` of the db and logger modules, then a `require` of the module under test",
     intro_site="the catch block of the module function `%s` in `services/governanceService.ts`"%helper,
     where_note="The catch block's `instanceof Error` read is on line %d; the catch logs the ERROR line '%s' with `{ error: <message> }` and does NOT rethrow: it then returns %s. The message is only logged, it is never returned to a caller or put in a response. Other catch blocks of the file (the `dbSave*` helpers that rethrow, `dbGetProposal` at line 219 which is a separate held pass, the sibling `dbGet*` readers) are NOT in this brief."%(line,msg,ret),
     whatwrong=("In `governanceService.ts` the catch block of `%s` logs `logger.error('%s', { error: err instanceof Error ? err.message : String(err) })` (the read is on line %d) and then returns %s. "
      "If the database call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. "
      "Either way the catch throws before the ERROR line is logged and before the documented return: `%s` rejects with the hostile value instead of %s. "
      "The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. Nothing else changes: an ordinary Error still logs `{ error: <its message> }`.")%(helper,msg,line,ret,exported,consq_ret),
     consequence="Today a hostile rejection from the database layer makes the catch block itself throw, so nothing is logged and the function rejects instead of returning %s."%ret,
     red1="At the tip `%s` rejects, so the `resolves` assertion fails (and no ERROR line is logged)"%exported,
     dbnote="`../db` and `../utils/logger` are mocked; no database, no app boot and no network.%s"%(" `%s` is not exported, so the test reaches it through the exported `%s`."%(helper,exported) if helper!=exported else ""),
     sibling="Every other catch block of `governanceService.ts` is NOT in this brief")
add('p1','get_all_proposals','dbGetAllProposals','getProposals',"getProposals()",'DB get all proposals failed','[]','resolves an empty list','toEqual([])',255,'treating the list as empty')
add('p2','get_all_participants','dbGetAllParticipants','getParticipants',"getParticipants()",'DB get all participants failed','[]','resolves an empty list','toEqual([])',313,'treating the list as empty')
add('p3','get_active_delegations','dbGetActiveDelegations','revokeDelegation',"revokeDelegation('d-1')",'DB get active delegations failed','[]','resolves undefined (nothing to revoke)','toBeUndefined()',342,'finding no active delegations')
add('p4','get_total_vote_power','getTotalVotePower','getTotalVotePower',"getTotalVotePower()",'DB get total vote power failed','0','resolves 0','toBe(0)',448,'returning 0')
