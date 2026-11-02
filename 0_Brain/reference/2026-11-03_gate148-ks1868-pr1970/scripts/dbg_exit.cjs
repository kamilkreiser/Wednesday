const oe = process.exit; process.exit = (c) => { require('fs').writeSync(2, 'EXIT CALLED ' + c + '\n' + new Error().stack + '\n'); oe(c); };
process.on('exit', (c) => require('fs').writeSync(2, 'on exit ' + c + '\n'));
