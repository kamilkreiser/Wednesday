# OXPd: the M577's lost admin password (Datasec/OXPd), for Kam

**BLUF.** HP says the admin password cannot be recovered: for a lost one, HP tells you to contact HP Support for a complete reset. HP's self-service resets are behind that same admin login, so they don't help. **My recommendation: look for it tomorrow first. If it can't be found, ask HP Support rather than try the forum tricks. Nothing touches the printer meanwhile.**

**HP's words** (checked by me in HP's own guide, "Configuration Guide using the Embedded Web Server (EWS)", https://kaas.hpcloud.hp.com/pdf-public/pdf_878364_en-US-1.pdf, chapter 5):
> "Make note of the password and store it in a safe place. The administrator password cannot be recovered. If the administrator password is lost or forgotten, contact HP Support at support.hp.com for the assistance required to completely reset the printer."

---

**Option 1 (recommended): find it.** Likely places:
- Your password manager.
- Wherever the printer's set-up was noted.
- Whoever installed it.

If it turns up, the first run goes ahead as planned: one read, then one test page.

**Option 2: HP Support.** This is HP's own route. HP doesn't publish what their complete reset erases, so ask them before they do it. Expect it to wipe most of the printer's set-up, so before anything is reset, note:
- Its network address and settings.
- Its scan destinations and address book.

**Not recommended: the start-up menu tricks.** Forum posts describe "Partial Clean", "Cold Reset" and "Clear Password" from the printer's start-up menu.
- These are user reports, not an HP procedure.
- They wipe settings.
- Some users hit a service-code prompt nobody could get past.
- HP's "Reset Svc PWD" start-up option resets a different code, not the admin password.

**What we don't know:** exactly what each reset erases on your firmware, and whether HP Support needs proof of ownership. HP's own document on admin passwords for FutureSmart 4 and 5 wasn't retrieved. I can get it if you want the detail.

**How I checked:** a research agent read HP's guides and support pages, and I re-read the key quote myself in the PDF above. The M577 user guide's "Reset factory settings" path also goes through the Administration menu (HP, https://h10032.www1.hp.com/ctg/Manual/c04647409.pdf; relayed by the agent, not re-read by me).
