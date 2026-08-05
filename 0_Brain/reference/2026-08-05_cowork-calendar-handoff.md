# Calendar access handoff — for "Wednesday" (read-only dashboard)

Prepared by Claude (Cowork), 4 Aug 2026, for Kam.

---

## 1. MECHANISM

**How I (Claude/Cowork) access the calendar:** GUI automation of the macOS
Calendar app (Calendar.app) on the Mac Mini, via the Claude desktop app's
screen-control bridge. Access is granted per-session by Kam clicking an
approval prompt. **I hold NO credentials** — no CalDAV login, no
app-specific password, no API key, no ICS URL. Nothing was ever stored, so
there is nothing secret to hand over in this file.

**Account & calendars:**
- Account: iCloud (Apple ID: kreiser.org@me.com), shown in Calendar.app
  under the "kreiser.org" account group
- Calendar I write to: **"Family"** (shared iCloud calendar, orange)
- Other calendars visible on the Mac (do not touch): KREISER.org,
  Eventbrite, Amelia, plus Birthdays / Australian Holidays / Siri
  Suggestions

**Recommended read-only mechanisms for Wednesday** (pick ONE):

- **Option A — local EventKit / icalBuddy (recommended).** Wednesday runs
  locally on the Mac, so it needs no credentials at all: read events via
  EventKit (Swift/JXA), AppleScript, or the `icalBuddy` CLI. macOS will
  show a one-time "allow calendar access" prompt. Truly read-only, works
  offline, no secrets to manage. If this is used, the .env below is not
  needed except ICAL_CALENDAR_NAMES.

- **Option B — iCloud CalDAV with an app-specific password.** Kam must
  generate the password himself at account.apple.com → Sign-In and
  Security → App-Specific Passwords (name it e.g. "wednesday-dashboard"),
  and paste it straight into Wednesday's local .env — never into a chat.
  Note CalDAV credentials are read-WRITE by nature; Wednesday must
  enforce read-only in its own code.

- **Option C — public ICS subscription link.** In Calendar.app: right-click
  "Family" → Sharing Settings → Public Calendar → copy the webcal:// URL
  (use https:// with the same path). Read-only by design, but anyone with
  the link can read the calendar — household events included — so treat
  the URL itself as a secret.

## 2. .ENV TEMPLATE (values Kam must fill in — I do not possess them)

```env
# Pick ONE mechanism and delete the unused lines.

# --- Option A: local EventKit/icalBuddy (no credentials) ---
ICAL_MECHANISM=eventkit-local
ICAL_CALENDAR_NAMES=Family

# --- Option B: iCloud CalDAV ---
# ICAL_MECHANISM=caldav-icloud
# ICAL_CALDAV_URL=https://caldav.icloud.com
# ICAL_USERNAME=kreiser.org@me.com
# ICAL_APP_PASSWORD=<generate at account.apple.com -> App-Specific Passwords; paste here yourself>
# ICAL_CALENDAR_NAMES=Family

# --- Option C: public ICS subscription ---
# ICAL_MECHANISM=ics-subscription
# ICAL_ICS_URL=<copy from Calendar.app -> Family -> Sharing Settings -> Public Calendar>
# ICAL_CALENDAR_NAMES=Family
```

## 3. OPERATING NOTES FOR WEDNESDAY

**Write cadence:** I write only when Kam asks during a Cowork session —
there is no schedule and no sync daemon. Writes come in short bursts
(e.g. a batch of school-term events) and then nothing for weeks. There is
no locking or conflict protocol, so Wednesday should treat the Family
calendar as strictly read-only.

**Event conventions I use (current set: 12 events, 30 Jul – 4 Sep 2026,
Term 3 school assessments):**
- Titles are prefixed **"Alice: "** followed by the subject and task, e.g.
  "Alice: Maths Cycle Test (Fractions & Decimals)". Parenthetical suffixes
  carry key detail (due time, "ONLINE - bring charged device", etc.).
- Sit-down tests are TIMED events (e.g. 9:00–9:45am); due-dates/submission
  deadlines are ALL-DAY events dated the last school day before the online
  deadline.
- All are single events (no recurrence), Australia/Sydney time, on the
  "Family" calendar, with invitees alice.kreiser@icloud.com and
  thats_you25@hotmail.com, and default alerts (1 hr before for timed,
  day-before 9am for all-day).

**Must NOT modify (to avoid conflicting with my updates):**
- Any event titled "Alice: *" on the Family calendar
- The three "MUSIC - Assmnt" events on 18 Sep 2026 (created from Canvas by
  Amelia — I deliberately left them untouched) and the "End of term 3" event
- Safest rule: Wednesday makes NO writes to the Family calendar at all —
  display only, exactly as Kam intends.

**Security note:** no assistant should ask for or relay the app-specific
password through chat or files like this one. Kam generates it and places
it directly into Wednesday's local .env; revoke it at account.apple.com if
it ever leaks.
