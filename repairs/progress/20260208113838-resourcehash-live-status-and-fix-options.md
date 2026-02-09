# Resource Hash Live Status and Fix Options - 2026-02-08 11:38 PST

## Goal
Confirm whether errors are still active and determine whether `resourceHashes` can be truly fixed (not just filtered in reporting).

## Phase Plan And Progress

### Phase 1 - Live status check
- What: Inspect active agent logs and current write activity for repeated error signatures.
- Why this supports the goal: Confirms whether issue is historical or ongoing.
- Output if operating correctly: Current timestamps proving active errors.
- Status: Completed.
- Result:
  - Errors are active now.
  - `resourceHashes` startup errors appear in many active agent logs at `11:37`.
  - Poster write warnings/criticals are also active (example HFGPM at `11:37:52`).

### Phase 2 - Verify source of `resourceHashes` 404
- What: Trace Plex framework code path and system plugin route behavior.
- Why this supports the goal: Determines if fix belongs in agent code or Plex runtime.
- Output if operating correctly: Exact handler + failure mechanism.
- Status: Completed.
- Result:
  - Framework handler route exists: `Framework/handlers/runtime.py` route `/resourceHashes`.
  - Handler returns nothing when hashes are unavailable -> runtime returns `404`.
  - Hashes are obtained via `Framework/components/runtime.py:get_resource_hashes()`.
  - For `com.plexapp.system`, framework fetches `http://resources-cdn.plexapp.com/hashes.json`.
  - If fetch fails, exception is swallowed and cached for 1 hour, leaving `None` and causing repeated local `404` responses.

### Phase 3 - Determine true fixability
- What: Classify fixes by layer (agent vs system/framework).
- Why this supports the goal: Avoids wasting time patching every agent for a system defect.
- Output if operating correctly: Actionable fix options with tradeoffs.
- Status: Completed.
- Result:
  1. **Real fix (preferred): restore successful fetch in `com.plexapp.system` runtime path**
     - Ensure PMS can reach `resources-cdn.plexapp.com` (DNS/firewall/proxy).
     - Then `/resourceHashes` returns JSON and agent startup errors stop naturally.
  2. **Real fix (local patch): patch Plex framework runtime to degrade gracefully**
     - Modify framework so missing hashes returns `{}` or `[]` and HTTP `200`.
     - This is outside repo, gets overwritten by PMS updates, and should be scripted if adopted.
  3. **Agent-level handling only**
     - Catch/ignore startup hash failure noise in agents/reporting.
     - Reduces noise but does not fix root system behavior.

## Conclusion
Yes, errors are continuing. `resourceHashes` can be actually fixed, but not in PGMA agent code alone; the proper fix is at Plex system/framework layer.

## Immediate Next Action
If approved, implement option 2 as a reversible hotfix script plus backup for the Plex framework file, then restart PMS and verify `/resourceHashes` no longer returns `404` from `com.plexapp.system.log`.
