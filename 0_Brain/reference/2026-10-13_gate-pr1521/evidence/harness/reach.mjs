const m = await import(process.argv[2]);
const shapes = [
  ['connector', undefined], ['connector', []], ['connector', ['documents:read']], ['connector', ['organizations:register']],
  ['Connector', ['organizations:register']], ['CONNECTOR', ['organizations:register']], [' connector', ['organizations:register']],
  ['connector', 'organizations:register'], ['connector', 'x organizations:registerx'], ['connector', {includes: () => true}],
];
for (const [role, scopes] of shapes) {
  const d = m.decideMint({ role, scopes, tenantId: 't' }, {});
  console.log(JSON.stringify({ role, scopes: typeof scopes === 'object' && !Array.isArray(scopes) && scopes ? '{includes}' : scopes, allow: d.allow, via: d.via ?? null }));
}
