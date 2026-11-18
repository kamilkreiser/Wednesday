---
date: 2026-11-19
type: reference
source: WED-165 (Kam 2026-11-18 11:29 "is there a way of how to switch accounts from afar?"; 13:53 "can you turn on remote login?"; 13:54 "it will need to wait until Friday")
status: live — setup NOT done; the sign-in paste-back is UNTESTED (test with Kam present, Friday 20 Nov)
---

# Switching Claude accounts on the Mac mini from afar — the steps

**Goal:** Kam, away from home, can switch the account the fleet runs on, from his phone or laptop.

**Measured on the Mac mini, 2026-11-19 06:0x:** macOS 27.2.1 · Claude Code 2.1.327 (has
`claude auth login` / `logout` / `status`) · Screen Sharing ON (port 5900 open) · Remote Login
(SSH, port 22) OFF · Tailscale NOT installed · host name `Kamils-Mac-mini`.
Wednesday cannot do the Mac side: it needs Kam's admin password (`sudo -n` refuses). Never send
that password on the panel or by mail.

## Part 1 — once, at the Mac (Friday, about 10 minutes)

1. **Remote Login on:** System Settings → General → Sharing → Remote Login → on.
   Allow access for: *Only these users* → Kam's account. Leave **"Allow full disk access for
   remote users" OFF**.
2. **Tailscale on the Mac mini:** install from tailscale.com (or the Mac App Store), sign in,
   and set it to start at login. Note the Mac's Tailscale name/IP (`100.x.y.z`).
3. **Tailscale on his phone (and laptop):** install, sign in with the SAME Tailscale account.
   Check the Mac mini shows as connected in the app.
4. **An SSH app on the phone** (e.g. Termius or Blink) pointed at the Mac mini's Tailscale
   address, user `kamil`. Test it on Friday from the phone on mobile data (Wi‑Fi off), so it
   is proven from outside the house.
5. Optional: Screen Sharing over Tailscale (`vnc://<tailscale-ip>` from the laptop) as the
   fallback when a terminal is not enough.

## Part 2 — switching accounts from afar (each time)

The fleet runs in a tmux session called `fleet`; Wednesday is pane 0.

1. Phone → Tailscale on → SSH app → connect to the Mac mini.
2. `tmux attach -t fleet` (detach later with Ctrl‑b then d — never type `exit`, which closes the pane).
3. In Wednesday's pane type `/login`, choose the subscription account, and open the link it
   prints on the phone. Sign in with the NEW account.
4. Paste the code the browser shows back into the pane. **This paste-back over SSH is the
   untested step — Friday's test proves it.**
5. Check: `/status` in the pane names the new account; the statusline usage gauge resets.
6. Seats started after the switch use the new account. Seats already running keep the old
   login until relaunched (to confirm on Friday).

Fallback if `/login` in the pane misbehaves: in a NEW tmux window, `claude auth login`, then
`claude auth status`. Running it logs the machine's Claude out of the old account first —
fine at a switch, never mid-merge.

## Friday test checklist (with Kam present)
- [ ] Part 1 steps 1–4 done; SSH from the phone on mobile data works.
- [ ] `tmux attach -t fleet` from the phone shows Wednesday's pane.
- [ ] `/login` from the phone completes, including the code paste-back.
- [ ] New seats launch on the new account; record what running seats do.
- [ ] Update this file's status line with the result.

## Security notes
- Tailscale keeps SSH off the public internet: never open port 22 on the router.
- Key-based SSH from the phone is better than a password; set it up on Friday if time allows.
- If the phone is lost: remove it in the Tailscale admin console; that cuts its access.
