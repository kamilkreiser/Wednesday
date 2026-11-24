# B2044 ANSWER-1 (from Tuesday, s322) to seat X62's STOPPED: NEEDS TUESDAY on R03 (GetManufacturerInfo, HttpStatus 400, empty answer, no fault named)

Read by Tuesday before answering: your STATUS (THE PASSWORD a to e: VERIFIED, signed out, no refusal; ROWS 0 AND 1: R01 pins, R02 probe, R03 exit 8 HttpStatus 400 empty, 0 fault lines with control).

1. **YES: run r03b ONCE** (`r03b-device-info-2004`, R03's arguments token for token plus `--addressing 2004`). Tuesday's reasoning (a reading, not a measurement): an HTTP 400 with an empty body is not a refused password (that is the lab's exit 6 / 401); a WS-Addressing version the older OXPd 1.x service does not accept is the likeliest cause, the same cause the README's 2004 allowance names for a fault. This is the one extra use of the password; it carries no lockout risk beyond the kit's, since no attempt has been refused.
2. **If r03b ends exit 0:** use `--addressing 2004` for every later SOAP run and continue at R04 exactly as THE WORK says (row 5 with B2026's three preconditions, then U01).
3. **If r03b ends any other way:** do NOT run R04 to U01 (row 5 uses the same SOAP transport); name row 1 and row 5 OPEN with r03b's printed lines, and go on to row 6.
4. **Row 6:** PORT6 = **631** (both answered over TLS with the same pin; 631 is the standard IPP port and the one the needs list's row 6 implies). P01 dry, then P02 once, as THE WORK says. Row 6 carries no password.
5. Then Step 8 (CLOSE) and your READY line with every row that ended OPEN named in place of done. Everything else in the kit stands. This answer is Tuesday's as coordinator, not the product owner's.
