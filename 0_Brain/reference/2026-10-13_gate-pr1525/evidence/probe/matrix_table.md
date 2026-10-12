| cell | who | base_st1 | head_st2 | base_mt1 | head_mt1 |
|---|---|---|---|---|---|
| SETUP |  | role=secuura_app su=False bp=False tenantManager=False | role=secuura_app su=False bp=False tenantManager=False | role=secuura_app su=False bp=False tenantManager=True | role=secuura_app su=False bp=False tenantManager=True |
| docB-by-ext | userA | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| docB-by-pkey | userA | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored |
| docB-by-ext | orgAdminA | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| docB-by-pkey | orgAdminA | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored |
| docB-by-ext | connA | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| docB-by-pkey | connA | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored |
| docB-by-ext | superAdminUpper | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| docB-by-pkey | superAdminUpper | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored |
| docB-by-ext connA+onBehalfOf(userA email) | connA | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| docB-by-ext connA+onBehalfOf(userB email, other org) | connA | 403 saved=0 row=same st=anchored | 403 saved=0 row=same st=anchored | 403 saved=0 row=same st=anchored | 403 saved=0 row=same st=anchored |
| docB-by-ext | sysAdmin | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified |
| docB-by-ext | sysAdminLower | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified |
| docB-by-ext | superAdminLower | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified |
| docB-by-pkey | sysAdmin | 201 saved=1 row=same st=anchored | 201 saved=1 row=same st=anchored | 201 saved=1 row=same st=anchored | 201 saved=1 row=same st=anchored |
| own-by-ext | userB | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified |
| own-by-pkey | userB | 201 saved=1 row=same st=anchored | 201 saved=1 row=same st=anchored | 201 saved=1 row=same st=anchored | 201 saved=1 row=same st=anchored |
| recipient-doc (recipientEmail upper) | recipient | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified |
| recipient-doc by non-recipient userA | userA | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| oboDoc by creating connector connB (real provenance) | connB | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified |
| oboDoc by other connector connA | connA | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| oboDoc by its resolved owner userB | userB | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified |
| oboUnknown-email doc by creating connector connB | connB | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified |
| ownerless by its creating connector connB (DECISION) | connB | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| ownerless by stranger userA | userA | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| ORACLE |  | ext[201, 1] uuid[201, 1] conn[201, 1] notYours[201, 1] notYoursConn[201, 1] identical=False | ext[403, 0] uuid[403, 0] conn[403, 0] notYours[403, 0] notYoursConn[403, 0] identical=True | ext[201, 1] uuid[201, 1] conn[201, 1] notYours[201, 1] notYoursConn[201, 1] identical=False | ext[403, 0] uuid[403, 0] conn[403, 0] notYours[403, 0] notYoursConn[403, 0] identical=True |
| documentId as ARRAY [ext] | userA | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored |
| documentId + parentDocumentId="" (empty) | userA | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| documentId + parentDocumentId=own docA | userA | 201 saved=1 row=same st=anchored | 201 saved=1 row=same st=anchored | 201 saved=1 row=same st=anchored | 201 saved=1 row=same st=anchored |
| documentId + parentDocumentId=null | userA | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored |
| documentId + parentDocumentId=0 (number) | userA | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored |
| documentId + parentDocumentId=false | userA | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored | 400 saved=0 row=same st=anchored |
| documentId upper-cased ext | userA | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored |
| documentId with trailing space | userA | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored | 201 saved=1 row=same st=anchored | 403 saved=0 row=same st=anchored |
| ITEM1 register documentUuid = another doc pkey (via route) |  | {"status": 409, "id": null} | {"status": 409, "id": null} | {"status": 409, "id": null} | {"status": 409, "id": null} |
| ITEM1 constructed: userA names its OWN pkey which is B-doc external_id |  | 201 bChanged=True aChanged=False | 403 bChanged=False aChanged=False | 201 bChanged=True aChanged=False | 403 bChanged=False aChanged=False |
| ITEM2 provenance row in T2 names T-doc, connA certifies | connA | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| ITEM2 control: same row in T, connA certifies | connA | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified |
| ITEM2 provenance names userA as connector, userA (human role) certifies | userA | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored | 201 saved=1 row=CHANGED st=certified | 403 saved=0 row=same st=anchored |
| ITEM2 stale provenance: connA created U, U deleted, userB re-registers U, connA certifies | connA | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified | 201 saved=1 row=CHANGED st=certified |
| ITEM4 owner flipped to B mid-flight (constructed via SQL, simulating transfer-custody) |  | 201 landedOnBsDoc=True | 201 landedOnBsDoc=True | 201 landedOnBsDoc=True | 201 landedOnBsDoc=True |
| ITEM5 lineage under B by userA |  | 201 derived=1 verifyCertBefore=False after=Org B Official Registrar anon=Org B Official Registrar bRowChanged=False | 201 derived=1 verifyCertBefore=False after=Org B Official Registrar anon=Org B Official Registrar bRowChanged=False | 201 derived=1 verifyCertBefore=False after=Org B Official Registrar anon=Org B Official Registrar bRowChanged=False | 201 derived=1 verifyCertBefore=False after=Org B Official Registrar anon=Org B Official Registrar bRowChanged=False |
| ITEM5b documentId=B doc + parentDocumentId=A own |  | 201 bRowChanged=False | 201 bRowChanged=False | 201 bRowChanged=False | 201 bRowChanged=False |
| ITEM5c parent = A OWN doc, data.contentHash = B bytes |  | 201 certBefore=None certAfterBy=Org B Official Registrar | 201 certBefore=None certAfterBy=Org B Official Registrar | 201 certBefore=None certAfterBy=Org B Official Registrar | 201 certBefore=None certAfterBy=Org B Official Registrar |
| ITEM3 |  | {"skipped": "PROBE_TIMING_N=0"} | {"skipped": "PROBE_TIMING_N=0"} | {"skipped": "PROBE_TIMING_N=0"} | {"skipped": "PROBE_TIMING_N=0"} |
