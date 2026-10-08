const MARKER = 'slot-literal-ok:';
const lines = ["const p = 6982; // slot-literal-ok:", "const p = 6982; // slot-literal-ok: reason", "const p = 6982;"];
for (const l of lines) console.log(JSON.stringify(l), '->', l.includes(MARKER) ? 'EXEMPTED (the guard returns [] before any pattern)' : 'scanned');
