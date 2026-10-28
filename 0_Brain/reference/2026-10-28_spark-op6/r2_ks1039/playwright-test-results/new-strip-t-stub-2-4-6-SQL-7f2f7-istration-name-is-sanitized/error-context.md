# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: new-strip/t.spec.ts >> stub >> 2.4.6: SQL injection in registration name is sanitized
- Location: 2_Project_Files/local-model/spark/cache/work/op6/w2/new-strip/t.spec.ts:9:7

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: "Robert'); DROP TABLE users; --"
Received: "Robert) DROP TABLE users --"
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | import * as http from 'http';
  3  | const TEST_PASSWORD='x'; let base=''; let srv: http.Server;
  4  | function getBaseUrl(){ return base; }
  5  | function uniqueEmail(){ return 'a+'+Date.now()+'@agentmail.to'; }
  6  | test.beforeAll(async()=>{ srv=http.createServer((rq,rs)=>{ let b=''; rq.on('data',c=>b+=c); rq.on('end',()=>{ const d=JSON.parse(b); let n=d.name; if(true) n=n.replace(/[;']/g,''); rs.writeHead(201,{'content-type':'application/json'}); rs.end(JSON.stringify({success:true,data:{accessToken:'t',user:{id:'u',email:d.email,displayName:n,role:'OWNER'}}})); }); }); await new Promise<void>(r=>srv.listen(0,'127.0.0.1',()=>r())); base='http://127.0.0.1:'+(srv.address() as any).port+'/'; });
  7  | test.afterAll(()=>{ srv.close(); });
  8  | test.describe('stub',()=>{
  9  |   test('2.4.6: SQL injection in registration name is sanitized', async ({ request }) => {
  10 |     const res = await request.post(`${getBaseUrl()}api/auth/register`, {
  11 |       data: {
  12 |         email: uniqueEmail(),
  13 |         password: TEST_PASSWORD,
  14 |         confirmPassword: TEST_PASSWORD,
  15 |         name: "Robert'); DROP TABLE users; --",
  16 |       },
  17 |       failOnStatusCode: false,
  18 |     });
  19 | 
  20 |     const status = res.status();
  21 |     const body = await res.text();
  22 | 
  23 |     // Must not expose SQL errors
  24 |     expect(body.toLowerCase()).not.toContain('sql');
  25 |     expect(body.toLowerCase()).not.toContain('syntax error');
  26 |     // KS-1039: 'drop table' is the INPUT, and a register that stores and returns a display name returns it verbatim, so asserting it is absent from
  27 |     // the body fails on the echo and says nothing about injection. Parameterised SQL means the string is stored as data: the user object the
  28 |     // response carries must hold the exact input, and the call must have succeeded (a rejected call would otherwise skip this check).
  29 |     expect(status).toBe(201);
> 30 |     expect(JSON.parse(body).data.user.displayName).toBe("Robert'); DROP TABLE users; --");
     |                                                    ^ Error: expect(received).toBe(expected) // Object.is equality
  31 |     expect(status).toBeLessThan(500);
  32 |   });
  33 | 
  34 | });
  35 | 
```