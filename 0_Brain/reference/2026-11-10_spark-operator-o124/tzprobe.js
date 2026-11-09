const R=process.argv[2];
const { PrismaClient } = require(R+'/node_modules/@prisma/client');
const { PrismaPg } = require(R+'/node_modules/@prisma/adapter-pg');
const { Client } = require(R+'/node_modules/pg');
(async()=>{
  const url=process.argv[3];
  const p=new PrismaClient({adapter:new PrismaPg({connectionString:url})});
  const c=new Client({connectionString:url}); await c.connect();
  const q="select '2026-11-09 02:50:29.551+00'::timestamptz as t, current_setting('TimeZone') as tz";
  const a=await p.$queryRawUnsafe(q); const b=(await c.query(q)).rows[0];
  console.log(JSON.stringify({session_tz:b.tz, prisma_raw:new Date(a[0].t).toISOString(), pg_driver:new Date(b.t).toISOString(), true_instant:'2026-11-09T02:50:29.551Z'}));
  await p.$disconnect(); await c.end();
})();
