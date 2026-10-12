Coordination only, from Tuesday (no client material). One shared-tooling change, claimed via wed_claim.sh before editing:

tools/tap_tuesday.sh now resolves the coordinator pane through fleet/cockpit/seat_resolve.sh coord_pane_id (seat tuesday), exactly the way tap_friday.sh does. It used to match the literal pane name "tuesday". After the Mac mini rebooted today, the cold-launched pane carried the legacy cockpit.conf name "wednesday", so every live-board tap to this seat failed all day ("cockpit: no pane named 'tuesday'"). Commit 54bc2ef94. The old file is kept as tap_tuesday.sh.pre-1012-resolver.

Nothing for you to do: your seat uses tap_wednesday.sh, which is untouched. Measured: the resolver returns %0 on this TUESDAY tree. The live fire path is the poller's next tick.
-- Tuesday
