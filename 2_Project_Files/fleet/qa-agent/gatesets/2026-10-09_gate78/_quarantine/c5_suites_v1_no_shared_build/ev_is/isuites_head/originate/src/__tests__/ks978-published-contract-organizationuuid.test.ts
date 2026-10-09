/**
 * =============================================================================
 * KS-978 — the published contract must describe the organizationUuid bind
 * =============================================================================
 * The defect this exists for: KS-597 made `organizationUuid` an AUTHORIZATION
 * INPUT — a value belonging to another Organisation is refused with 403 — while
 * the published description still read "Accepted and preserved; org attribution
 * wiring lands with the issuer_organization_id population (architecture P1)".
 * KS-597 *is* that P1 wiring. The code and the contract disagreed on `develop`,
 * and the generic `403: commonErrorResponses[403]` named no condition, so the
 * refusal was not in the contract at all.
 *
 * WHY A TEST AND NOT JUST A CORRECTED SENTENCE. `check:openapi` proves the
 * committed yaml matches what the generator emits. It CANNOT prove the
 * generator's own prose is true — that blindness is recorded on KS-811, and it
 * is what let this through. So the properties an integrator depends on are
 * asserted here, where a future edit that quietly drops them goes red.
 *
 * This is a CONTRACT test, not a behaviour test: the 403 itself is correct and
 * is pinned by `ks597-issuer-org-bind.test.ts`.
 * =============================================================================
 */

import { sharedRegistry } from '@secuura/shared';

// Importing for the side effect: it is what registers the paths and schemas on
// the shared registry. Without it every assertion below would read an empty
// registry and could not distinguish "the description is wrong" from "nothing
// was registered" — which is why the first cell checks the route exists at all.
import '../originate.openapi';

type AnyDef = Record<string, any>;

/** The registered `POST /api/documents` route definition. */
function createDocumentRoute(): AnyDef {
  const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
  const route = defs.find(
    (d) => d.type === 'route' && d.route?.method === 'post' && d.route?.path === '/api/documents',
  );
  return route?.route as AnyDef;
}

/** The published description of a request-body property, as a string. */
function requestBodyPropDescription(prop: string): string {
  const route = createDocumentRoute();
  const schema = route?.request?.body?.content?.['application/json']?.schema;
  // zod-to-openapi keeps `.openapi({description})` on the internal metadata.
  const shape = schema?._def?.shape?.() ?? schema?.shape ?? {};
  const field = shape[prop];
  return String(
    field?._def?.openapi?.metadata?.description ??
      field?._def?.openapi?.description ??
      field?.description ??
      '',
  );
}

describe('KS-978 — the published contract describes the organizationUuid bind', () => {
  // The discriminator. Every cell below reads through this route object, so if
  // it were absent they would all fail for a reason that has nothing to do with
  // the descriptions. Asserting it separately means a red elsewhere is about
  // the prose, not about the registry being empty.
  it('the POST /api/documents route is registered at all', () => {
    expect(createDocumentRoute()).toBeDefined();
  });

  it('the 403 response NAMES the organizationUuid condition, not just "Forbidden"', () => {
    const description = String(createDocumentRoute()?.responses?.[403]?.description ?? '');
    expect(description).toMatch(/organizationUuid/);
    // Tightened after the KS-978 amendment: a bare /different Organisation/ now
    // matches the `onBehalfOf` clause as well, so it stopped pinning THIS
    // condition. Assert the wording that is specific to the organizationUuid arm.
    expect(description).toMatch(/DIFFERS FROM/);
    // KS-597 option B: the 403 names BOTH identifiers the claim is compared with.
    expect(description).toMatch(/externalRef/);
  });

  // The amendment's own property. The first version of this description named two
  // conditions and read as the COMPLETE set, while the operation answers 403 for
  // several more — vague-and-open replaced by specific-and-closed. Without a cell
  // the re-opening is one careless edit from being lost again.
  it('the 403 description declares itself NOT exhaustive and points at error.code', () => {
    const description = String(createDocumentRoute()?.responses?.[403]?.description ?? '');
    expect(description).toMatch(/not exhaustive/i);
    expect(description).toMatch(/error\.code/);
  });

  it('the 403 description names the conditions that are NOT this route\'s own guard', () => {
    const description = String(createDocumentRoute()?.responses?.[403]?.description ?? '');
    // Gateway enforcement, which an integrator meets on this operation but which
    // originate never throws — the codes live in api-gateway/services/enforcement.ts.
    for (const code of ['DOC_TYPE_DISABLED', 'INSUFFICIENT_VERIFICATION_LEVEL', 'MFA_REQUIRED', 'AUTH_PROVIDER_NOT_ALLOWED']) {
      expect(description).toContain(code);
    }
    expect(description).toMatch(/onBehalfOf/);
    expect(description).toMatch(/documents:write/);
  });

  it('the organizationUuid text names BOTH identifiers it accepts, and says identity, not membership', () => {
    // KS-597 option B (Kam, 2026-09-11): the claim may name the acting
    // Organisation by its K organization id OR by the externalRef it was
    // registered with — a Platform S connector sends the latter. F-2 still holds
    // for everything else: a well-formed uuid belonging to NO Organisation is
    // refused identically, and the contract has to say so.
    const d = requestBodyPropDescription('organizationUuid');
    expect(d).toMatch(/organization id/i);
    expect(d).toMatch(/externalRef/);
    expect(d).toMatch(/identity with the acting Organisation, not membership/i);
    expect(d).toMatch(/no Organisation at all/i);
  });

  it('the organizationUuid description states the refusal rather than "Accepted and preserved"', () => {
    const d = requestBodyPropDescription('organizationUuid');
    expect(d).toMatch(/403/);
    expect(d).toMatch(/bound to the acting organisation/i);
    // The exact sentence that was false once it shipped. It must not come back.
    expect(d).not.toMatch(/Accepted and preserved/i);
  });

  it('it says an org-less caller is NOT refused and NOT attributed', () => {
    const d = requestBodyPropDescription('organizationUuid');
    expect(d).toMatch(/no Organisation/i);
    expect(d).toMatch(/not attributed/i);
  });

  it('it says omitting the field is still valid — a refusal, not a new requirement', () => {
    expect(requestBodyPropDescription('organizationUuid')).toMatch(/omitting/i);
  });

  it('it points a genuine delegation at onBehalfOf', () => {
    expect(requestBodyPropDescription('organizationUuid')).toMatch(/onBehalfOf/);
  });

  // CONTROL. `userUuid` is the neighbour that did NOT change, and its
  // "not yet an authorization input" is STILL TRUE. Without this cell, a change
  // that rewrote every description in the file would pass everything above
  // while destroying the distinction an integrator relies on.
  it('CONTROL: userUuid still says it is NOT an authorization input', () => {
    const d = requestBodyPropDescription('userUuid');
    expect(d).toMatch(/not yet an authorization input/i);
    expect(d).not.toMatch(/403/);
  });
  it('RED KS-1275 ORDERTHROUGHSPEC: the REGISTERED LifecycleEventRequest and LifecycleEventResponse schemas publish action in the declared order of LIFECYCLE_EVENT_ACTIONS', async () => {
    const { LIFECYCLE_EVENT_ACTIONS } = await import('../lifecycleActions');
    const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
    const published = (refId: string) => defs.filter((d) => d.type === 'schema' && d.schema?._def?.openapi?._internal?.refId === refId).map((d) => d.schema.shape.action.options);
    expect([published('LifecycleEventRequest'), published('LifecycleEventResponse')]).toEqual([[[...LIFECYCLE_EVENT_ACTIONS]], [[...LIFECYCLE_EVENT_ACTIONS]]]);
  });
  // KS-1275 replaces #1123's DESCRIPTIONVERBLIST cell, which pinned the SENTENCE: it parsed the
  // published description for the literal list `share/transfer-custody/revoke`. That made the
  // prose load-bearing, which is the drift this ticket exists to end - the list had already gone
  // stale once. These two cells pin the PROPERTY instead, and neither reads the description for a
  // verb name. The description is now required to POINT at the sources of truth, and the
  // exclusion itself is asserted against the registry and the imported enum.

// KS-1321: `description.includes(verb)` could not tell the ordinary English word "version" from the
// route token, because several dedicated-route verbs are ordinary words (anchor, revoke, share,
// verify, version). MEASURED on the three descriptions the ticket names - the "a new version" prose,
// the back-quoted `version` and the slash-delimited /version - the bare `includes` returns
// ["version"] for ALL THREE, so it could only refuse innocent prose and never discriminate.
//
// Two rules, each as wide as it can honestly be:
//   * a HYPHENATED verb (sig-json, sign-cert, sign-wallet, transfer-custody) cannot occur as
//     ordinary prose, so a word-boundary match is enough and nothing is given up.
//   * a SINGLE-WORD verb is an ordinary word, so it counts only in ROUTE-TOKEN form: back-quoted,
//     or slash-DELIMITED on either side, as it appears in a path or in a slash-separated list.
// The `share/` form is in that rule because of a measurement, not by symmetry: with only `/verb`,
// the inline list `share/transfer-custody/revoke` returned ['revoke', 'transfer-custody'] and MISSED
// `share`, the one term with no slash in front of it. The list still reddened the cell, so the guard
// was doing its job - but a slash-separated list makes EVERY term a route token, including the
// first, and a rule that can only see the tail of a list is not describing the shape it refuses.
// Found by an arm of mine whose expected value was wrong; the expectation was the wrong thing to
// correct.
// What this rule still does NOT catch, stated rather than left implied: a single-word verb written
// as bare prose with no delimiter at all ('share must use its own route'). That is inherent to the
// fix this ticket asks for - 'version' in 'a new version' is the same string as the verb, and only
// the delimiter tells them apart. The hyphenated verbs have no such ambiguity and are matched on a
// word boundary.
const namesVerbAsRouteToken = (description: string, verb: string): boolean => {
  const v = verb.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return verb.includes('-')
    ? new RegExp('(^|[^a-z0-9-])' + v + '([^a-z0-9-]|$)', 'i').test(description)
    : new RegExp('`[^`]*/?' + v + '`|/' + v + '(?![a-z0-9-])|(^|[^a-z0-9-])' + v + '/', 'i').test(description);
};
  it('KS-1275 DESCRIPTIONPOINTSATSOURCE: the LifecycleEventRequest action description points at the enum and the vocabulary contract, and names NO verb that has its own route', async () => {
    const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
    const request = defs.find((d) => d.type === 'schema' && d.schema?._def?.openapi?._internal?.refId === 'LifecycleEventRequest');
    const description = String(request?.schema?.shape?.action?._def?.openapi?.metadata?.description ?? '');
    // the verbs that DO have a dedicated route, read from the registry rather than hardcoded
    const dedicatedVerbs = defs
      .filter((d) => d.type === 'route' && d.route?.method === 'post' && /^\/api\/documents\/\{id\}\/[a-z-]+$/.test(String(d.route?.path ?? '')))
      .map((d) => String(d.route?.path).split('/').pop() as string)
      .filter((verb) => verb !== 'lifecycle-events');   // this endpoint itself, not an excluded verb
    expect(dedicatedVerbs.length).toBeGreaterThan(0);   // the guard is not vacuous
    expect([
      /lifecycleActions\.ts/.test(description),
      /docs\/VOCABULARY\.md/.test(description),
      dedicatedVerbs.filter((verb) => namesVerbAsRouteToken(description, verb)),
    ]).toEqual([true, true, []]);
  });
  // KS-1321 done-when, BOTH arms as cells so the widening cannot silently return. Each reads the
  // dedicated-verb set from the registry, as the cell above does, and asserts it non-empty first -
  // an empty set would make both arms trivially true.
  it('KS-1321 ORDINARYWORDSTAYSGREEN: a description using a dedicated verb as an ordinary English word names no route token', async () => {
    const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
    const dedicatedVerbs = defs
      .filter((d) => d.type === 'route' && d.route?.method === 'post' && /^\/api\/documents\/\{id\}\/[a-z-]+$/.test(String(d.route?.path ?? '')))
      .map((d) => String(d.route?.path).split('/').pop() as string)
      .filter((verb) => verb !== 'lifecycle-events');
    const prose = 'The accepted set is this property\'s own enum. A new version of this list is not '
      + 'kept here; the vocabulary contract is docs/VOCABULARY.md and the enum is in lifecycleActions.ts.';
    expect([
      dedicatedVerbs.length > 0,
      dedicatedVerbs.includes('version'),                              // the word under test IS a dedicated verb
      dedicatedVerbs.filter((verb) => prose.includes(verb)),           // what the OLD bare check saw
      dedicatedVerbs.filter((verb) => namesVerbAsRouteToken(prose, verb)),
    ]).toEqual([true, true, ['version'], []]);
  });
  it('KS-1321 ROUTETOKENSTILLREDS: a back-quoted verb, a slash-delimited verb and the historical inline list are each still caught', async () => {
    const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
    const dedicatedVerbs = defs
      .filter((d) => d.type === 'route' && d.route?.method === 'post' && /^\/api\/documents\/\{id\}\/[a-z-]+$/.test(String(d.route?.path ?? '')))
      .map((d) => String(d.route?.path).split('/').pop() as string)
      .filter((verb) => verb !== 'lifecycle-events');
    const backQuoted = 'Send it to the `version` route instead; see docs/VOCABULARY.md.';
    const slashed = 'Send it to POST /api/documents/{id}/version; see docs/VOCABULARY.md.';
    // the exact prose KS-1275 removed, which is the shape this guard exists to refuse
    const inlineList = 'share/transfer-custody/revoke must use their own routes.';
    // A HYPHENATED verb in bare prose, with no slash and no back-quote. This is the only fixture the
    // hyphenated branch is needed for: removing that branch left every other fixture green, so the
    // arm proving it applied and was INERT until this line existed. A hyphenated route token cannot
    // occur as ordinary English, which is why matching it on a word boundary gives nothing up.
    const bareHyphenated = 'A transfer-custody must use its own route.';
    expect([
      dedicatedVerbs.length > 0,
      dedicatedVerbs.filter((verb) => namesVerbAsRouteToken(backQuoted, verb)),
      dedicatedVerbs.filter((verb) => namesVerbAsRouteToken(slashed, verb)),
      dedicatedVerbs.filter((verb) => namesVerbAsRouteToken(inlineList, verb)).sort(),
      dedicatedVerbs.filter((verb) => namesVerbAsRouteToken(bareHyphenated, verb)),
    ]).toEqual([true, ['version'], ['version'], ['revoke', 'share', 'transfer-custody'], ['transfer-custody']]);
  });
  it('KS-1275 EXCLUSIONHOLDS: no verb with a dedicated POST /api/documents/{id}/<verb> route is accepted by LIFECYCLE_EVENT_ACTIONS', async () => {
    const { LIFECYCLE_EVENT_ACTIONS } = await import('../lifecycleActions');
    const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
    const dedicatedVerbs = defs
      .filter((d) => d.type === 'route' && d.route?.method === 'post' && /^\/api\/documents\/\{id\}\/[a-z-]+$/.test(String(d.route?.path ?? '')))
      .map((d) => String(d.route?.path).split('/').pop() as string)
      .filter((verb) => verb !== 'lifecycle-events');
    const accepted = LIFECYCLE_EVENT_ACTIONS as readonly string[];
    // Both sides non-empty first: an empty registry read or an empty enum would make the
    // intersection trivially empty and the cell vacuous.
    expect([dedicatedVerbs.length > 0, accepted.length > 0]).toEqual([true, true]);
    expect(dedicatedVerbs.filter((verb) => accepted.includes(verb))).toEqual([]);
  });
});
