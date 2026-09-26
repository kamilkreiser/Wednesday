const { toBlockHeight } = await import(process.argv[2]);
const cases = [['null', null], ['undefined', undefined], ["'4242'", '4242'], ["' 42 '", ' 42 '], ["''", ''], ["'abc'", 'abc'], ['0', 0], ["'0'", '0'],
  ["'0x10'", '0x10'], ["'1e3'", '1e3'], ["'-1'", '-1'], ["'4242.5'", '4242.5'], ["'9007199254740993' (MAX_SAFE+2)", '9007199254740993'],
  ['9007199254740993n (BigInt)', 9007199254740993n], ['Infinity', Infinity], ['NaN', NaN], ['true', true], ['{}', {}]];
for (const [k, v] of cases) { const r = toBlockHeight(v); console.log(`${k.padEnd(34)} -> ${typeof r === 'number' ? String(r) : JSON.stringify(r)}`); }
