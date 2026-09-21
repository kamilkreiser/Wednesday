// Step 5b — run the VIEWER'S OWN WebCrypto decrypt (functions lifted verbatim from app/static/index.html) in Node's
// globalThis.crypto.subtle against a real raw Table row + the pilot private PEM. Same API calls the browser makes
// (importKey pkcs8 RSA-OAEP/SHA-256 non-extractable, RSA-OAEP decrypt, AES-GCM decrypt with additionalData).
// NOT the browser itself: Safari/Chrome are proven only when Kam signs in and loads the key (ACTIONS FOR KAM).
import fs from 'node:fs';
const [,, rowPath, pemPath, expected] = process.argv;
const html = fs.readFileSync(new URL('../app/static/index.html', import.meta.url), 'utf8');
const pick = (name) => { const m = html.match(new RegExp(`^(?:function ${name}\\(|const ${name}=).*$`, 'm')); if (!m) throw new Error('cannot find '+name+' in index.html'); return m[0]; };  // each helper is one line in the page
// pull the exact source lines of the four helpers out of the page and evaluate them here
const src = [pick('pemToDer'), pick('unb64'), pick('AAD')].join('\n') + `
async function importPem(text){ if(!/BEGIN PRIVATE KEY/.test(text)) throw new Error('need PKCS8'); return crypto.subtle.importKey('pkcs8',pemToDer(text),{name:'RSA-OAEP',hash:'SHA-256'},false,['decrypt']); }
async function decryptRow(PRIV,r){
  if(r.scheme!=='rsa-oaep-sha256+aes-256-gcm/v1') throw new Error('scheme '+r.scheme);
  const dk=await crypto.subtle.decrypt({name:'RSA-OAEP'},PRIV,unb64(r.wrapped_key));
  const k=await crypto.subtle.importKey('raw',dk,{name:'AES-GCM'},false,['decrypt']);
  const pt=await crypto.subtle.decrypt({name:'AES-GCM',iv:unb64(r.iv),additionalData:AAD(r)},k,unb64(r.ciphertext));
  return new TextDecoder().decode(pt);
}
return {importPem, decryptRow};`;
const {importPem, decryptRow} = new Function(src)();
const row = JSON.parse(fs.readFileSync(rowPath,'utf8')).items[0];
row.client = row.PartitionKey;
const PRIV = await importPem(fs.readFileSync(pemPath,'utf8'));
console.log('key imported: extractable =', PRIV.extractable, '(must be false), algorithm =', PRIV.algorithm.name, PRIV.algorithm.hash.name, PRIV.algorithm.modulusLength);
const pt = await decryptRow(PRIV, row);
console.log(pt === expected ? 'PASS  WebCrypto decrypt == expected synthetic text: '+JSON.stringify(pt) : 'FAIL  got '+JSON.stringify(pt));
try { await decryptRow(PRIV, {...row, client:'Datasec'}); console.log('FAIL  relabelled row decrypted'); } catch(e){ console.log('PASS  relabelled row (AAD) refused:', e.name||e.message); }
const wrong = await crypto.subtle.generateKey({name:'RSA-OAEP',modulusLength:4096,publicExponent:new Uint8Array([1,0,1]),hash:'SHA-256'},false,['decrypt']);
try { await decryptRow(wrong.privateKey, row); console.log('FAIL  wrong key decrypted'); } catch(e){ console.log('PASS  wrong key refused:', e.name||e.message); }
