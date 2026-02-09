# Refresh Trigger vs Root Cause - 2026-02-08 11:35 PST

## Goal
Verify whether normal library refresh is itself failing, or whether refresh is only exposing existing agent-level errors.

## Phase Plan And Progress

### Phase 1 - Validate refresh pipeline health in current burst
- What: Check Plex server request/response results for metadata tree + agent update calls during the observed burst window.
- Why this supports the goal: If refresh internals are healthy (`200` on `/tree` and `/system/agents/update`), refresh is not the root error source.
- Output if operating correctly: Concrete status codes for core refresh-related endpoints.
- Status: Completed.
- Result:
  - Repeated `GET /library/metadata/640/tree`, `641/tree`, `642/tree`, `643/tree`, `644/tree`, `645/tree` all completed `200`.
  - Repeated `GET /system/agents/update?...` completed `200`.
  - Evidence: `/Users/jbmiles/Library/Logs/Plex Media Server/Plex Media Server.log` lines around `1270-1617`, `2111-2174`, `2983-3112`.

### Phase 2 - Identify actual high-volume error signatures
- What: Extract dominant ERROR/CRITICAL signatures from active plugin logs.
- Why this supports the goal: Distinguishes true defect classes from normal refresh traffic.
- Output if operating correctly: Ranked, line-backed root causes.
- Status: Completed.
- Result:
  1. Framework startup noise on each agent start:
     - `/:/plugins/com.plexapp.system/resourceHashes` -> `404` -> runtime critical.
     - Example: `/Users/jbmiles/Library/Logs/Plex Media Server/PMS Plugin Logs/com.plexapp.agents.GayAdultFilms.log` lines `18-20`.
  2. GayRado parse loop (high-volume search failures):
     - `Error matching Site Entry Contents` repeatedly from `_search -> search` (`__init__.py`, line 257).
     - Example: `/Users/jbmiles/Library/Logs/Plex Media Server/PMS Plugin Logs/com.plexapp.agents.GayRado.log` lines `311-396`.
  3. Poster-to-disk write failures (real data-path issue):
     - `CRITICAL (storage:89)` and `IOError: [Errno 2]` while writing poster files with `._(...)` target names.
     - Example: `/Users/jbmiles/Library/Logs/Plex Media Server/PMS Plugin Logs/com.plexapp.agents.GEVI.log` lines `1645-1668`.

### Phase 3 - Reconcile with earlier spike hypothesis
- What: Compare this run with previous burst diagnosis.
- Why this supports the goal: Explains why refresh can correlate with errors without being causal.
- Output if operating correctly: Single causal statement.
- Status: Completed.
- Result:
  - Refresh is the execution trigger that fans out work to selected agents.
  - Error spikes occur when that fan-out hits existing scraper/parser/storage defects.
  - In this active window, refresh endpoints are healthy; failures are agent-level behavior.

## Conclusion
A normal refresh is not inherently broken. It is currently exposing three independent issues: recurring framework `resourceHashes` startup noise, GayRado candidate parsing errors, and poster-save path failures (`._...jpg`).

## Recommended Next Step
Prioritize fixes in this order:
1. Poster-save path sanitizer/guard (reduces CRITICAL write failures).
2. GayRado candidate parser hardening (largest search-error volume).
3. Suppress or reclassify `resourceHashes` startup critical noise in diagnostics.
