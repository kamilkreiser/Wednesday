# Instructions for the Claude desktop agent: fix Kam's TRMNL "Kam view" screen

You are helping Kam Kreiser with his TRMNL e-ink display. Use the browser; Kam will log you in to trmnl.com. Work only inside trmnl.com.

## What is already known to work (do not redo these)
- A private plugin named **Kam view** exists, Strategy **Webhook**, framework 3.4.0, refresh 15 minutes.
- Data is arriving. Every 15 minutes a job on Kam's Mac POSTs to the plugin's webhook. TRMNL accepted the last pushes (HTTP 200), and reading the plugin's data back from TRMNL showed it stored (last checked 14:49 on Fri 9 Oct).
- The stored data has these top-level variables: `action_counts, actions, actions_more, actions_total, agents, cal_more, cal_total, cal_warn, days, updated`.
- So the problem is almost certainly in **how the plugin is displayed**: the markup, the playlist, or the device.

## Do NOT do these (they break the link to Kam's Mac)
- Do **not** delete or recreate the plugin, and do not regenerate its webhook URL. If you believe you must, stop and tell Kam first. A new URL has to be put into a file on his Mac before anything reaches the screen again.
- Do not change Strategy away from Webhook. Do not turn on polling.
- Do not delete other plugins, devices or playlists.

## Check these in order, and stop at the first one that fixes it
1. **The plugin preview.** Open the Kam view plugin's settings page. Look for its preview / "Force refresh" / "Your Variables" area.
   - "Your Variables" (or similar) should list the variables above (`updated`, `days`, `agents`, `actions`, …). If it is EMPTY, tell Kam, and do not change anything else: that means the data is not reaching THIS plugin.
   - If the preview shows a blank or an error, go to step 2.
2. **The markup.** Click **Edit Markup**, open the **Full** tab. It must contain the markup at the bottom of this file, exactly.
   - If the Full tab is empty, or holds something else, replace its whole content with the markup below and **Save**.
   - Leave the Half / Quadrant tabs alone.
   - Then re-check the preview. It should show meetings on the left (Today / Tomorrow) and, on the right, three agent gauges (Wednesday, Tuesday, Friday) above a short "Needs you" list.
   - If the preview shows a Liquid error, copy the error text exactly and give it to Kam.
3. **The playlist.** Open the device's **Playlist**. The Kam view plugin must be in it as a **full-screen** item (not a mashup), and enabled.
   - If it is missing, add it. If it is there but is not the next item, use the device's "Force Refresh" / "Show now" option if one exists, rather than reordering anything else.
4. **The device.** On the device page, check it is online and when it last refreshed. The device only fetches a new screen on its own refresh cycle, so after a fix the screen can take up to its refresh interval to change.

## When you finish, tell Kam (short)
- Which step was wrong and what you changed (or "nothing changed").
- What the preview shows now.
- Any error text, copied exactly.
- If the plugin's webhook URL CHANGED for any reason, say so clearly: Wednesday must update it on the Mac.

## The markup for the Full tab (paste it exactly, all of it)

```liquid
<!--
  TRMNL private plugin "Kam view" — FULL layout tab (paste into Edit Markup > Full).
  Framework 3.4 classes only; every string is pre-formatted by build_payload.py, so this
  template uses plain Liquid (for / if / size) and no TRMNL-specific filters.
  The platform supplies <div class="view view--full"> around this markup
  (https://trmnl.com/framework/docs/3.4/view — "You don't specify the view").
  Left half: meetings (3 calendars). Right half: agent weekly-usage gauges, then the
  "needs you" table (open decision cards, one row each).
-->
<div class="layout layout--top layout--left layout--stretch">
  <div class="grid grid--cols-2 stretch-x" style="min-width:0">

    <!-- ── LEFT: running list of meetings ─────────────────────────────── -->
    <div class="flex flex--col flex--top flex--stretch-x gap--small" style="min-width:0;overflow:hidden">
      <span class="title title--small">Meetings · next 7 days</span>
      {% if days.size == 0 %}
        <span class="description">Nothing in the next 7 days.</span>
      {% else %}
      <!-- Row budget is enforced in build_payload.py (--max-rows counts day headings too),
           so the overflow engine never has to cut a list and orphan a heading. -->
      <table class="table table--small" style="table-layout:fixed;width:100%">
        <colgroup><col style="width:58px"><col style="width:20px"><col></colgroup>
        <tbody>
        {% for day in days %}
          <tr><td colspan="3"><span class="label label--small label--underline">{{ day.label }}</span></td></tr>
          {% for e in day.events %}
          <tr>
            <td><span class="label label--small{% if e.now %} label--inverted{% endif %}">{{ e.time }}</span></td>
            <td><span class="label label--small">{{ e.src }}</span></td>
            <td><span class="label" data-clamp="1">{{ e.title }}</span></td>
          </tr>
          {% endfor %}
        {% endfor %}
        </tbody>
      </table>
      {% endif %}
      {% if cal_more > 0 %}
        <span class="label label--small shrink-0">+{{ cal_more }} more in the next 7 days</span>
      {% endif %}
      {% for w in cal_warn %}
        <span class="label label--small label--inverted shrink-0">! {{ w }}</span>
      {% endfor %}
    </div>

    <!-- ── RIGHT: agent gauges (top) + needs-you table (below) ────────── -->
    <div class="flex flex--col flex--top flex--stretch-x gap--small" style="min-width:0;overflow:hidden">
      <span class="title title--small">Agents · weekly plan used</span>
      {% for a in agents %}
        <div class="progress-bar progress-bar--small shrink-0">
          <div class="content">
            <span class="label label--small">{{ a.name }}{% if a.stale %} ({{ a.age }} old){% endif %}</span>
            <span class="value value--xxsmall">{% if a.pct == nil %}–{% else %}{{ a.pct }}%{% endif %}</span>
          </div>
          <div class="track">
            <div class="fill" style="width: {% if a.pct == nil %}0{% else %}{{ a.pct }}{% endif %}%"></div>
          </div>
        </div>
      {% endfor %}

      <div class="flex flex--col flex--top flex--stretch-x gap--small" data-overflow="true" data-overflow-counter="true" data-overflow-max-height="250">
        <span class="title title--small">Needs you ({{ actions_total }}) · W {{ action_counts.Wednesday }} · T {{ action_counts.Tuesday }} · F {{ action_counts.Friday }}</span>
        {% if actions.size == 0 %}
          <span class="description">Nothing is waiting on you.</span>
        {% endif %}
        {% for x in actions %}
          <div class="item">
            <div class="meta"></div>
            <div class="content">
              <span class="title title--small" data-clamp="2">{{ x.title }}</span>
              <span class="description" data-clamp="1">If ignored: {{ x.dflt }}</span>
              <div class="flex gap--small">
                <span class="label label--small label--underline">{{ x.seat }}</span>
                <span class="label label--small">since {{ x.since }}</span>
              </div>
            </div>
          </div>
        {% endfor %}
        {% if actions_more > 0 %}
          <span class="label label--small">+{{ actions_more }} more on the cockpit</span>
        {% endif %}
      </div>
    </div>

  </div>
</div>
<div class="title_bar">
  <span class="title">Kam</span>
  <span class="instance">updated {{ updated }}</span>
</div>
```
