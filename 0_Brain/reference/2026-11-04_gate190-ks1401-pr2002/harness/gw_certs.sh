#!/bin/bash
# Gateway shape: certifications.tenant_id is NOT NULL after CORE; plant A,A,B and read the head matrix; base control on a fresh gateway base.
. /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002/harness/lib.sh
P g_1 -c "INSERT INTO certifications (id,certification_type,tenant_id) VALUES (gen_random_uuid(),'fx','$TA'),(gen_random_uuid(),'fx','$TA'),(gen_random_uuid(),'fx','$TB')"
echo "g_1 (head, after 058) $(matrix g_1 | grep certif)"
echo "certifications.tenant_id nullable: $(S g_1 "SELECT is_nullable FROM information_schema.columns WHERE table_schema='public' AND table_name='certifications' AND column_name='tenant_id'")"
