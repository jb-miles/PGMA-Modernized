# Scan Performance Investigation - 2026-02-08 03:51:54

## Goal
Explain why library scans feel extremely slow per video by using raw scanner/server/plugin logs (not aggregated templates), and isolate which phase consumes wall-clock time.

## Phase Plan And Progress

### Phase 1 - Establish the run timeline
- What: Measure actual wall time for `--scan --refresh` jobs from raw `Plex Media Scanner*.log` files.
- Why this supports the goal: Confirms whether the scan stage itself is slow or if delay comes after scan.
- Output if operating correctly: Accurate per-run durations for scan jobs.
- Status: Completed.
- Result:
  - `Plex Media Scanner.2.log`: 44.671s total for scan+refresh invocation.
  - `Plex Media Scanner.log`: 1.401s.
  - `Plex Media Server.log` activity `8f3695af-7a08-4da4-a534-954e018e4427`: 03:40:36.466 -> 03:40:37.926 (1.46s scan activity).

### Phase 2 - Quantify post-scan workload
- What: Measure `--analyze`, `--generate --chapter-thumbs-only`, and `--analyze-deeply` durations.
- Why this supports the goal: Distinguishes scan latency from expensive media analysis jobs that run after scans.
- Output if operating correctly: Duration breakdown by scanner mode.
- Status: Completed.
- Result:
  - `--analyze`: sub-second to ~1.3s per run in sampled logs.
  - `--generate --chapter-thumbs-only`: mostly ~0.05s (forced runs up to ~3.5s).
  - `--analyze-deeply`: major cost center, sampled runs 26.88s to 172.09s each.
  - Total deep-analysis time visible in sampled logs: 563.13s (~9.39 min).

### Phase 3 - Measure agent/plugin search behavior
- What: Read raw `PMS Plugin Logs/com.plexapp.agents.*.log` and compute search routine durations/spans.
- Why this supports the goal: Agent web scraping can create long waits per item even if scan is fast.
- Output if operating correctly: Per-agent timing profile and outliers.
- Status: Completed.
- Result:
  - Measured routine durations (logs that emit both start+finish markers):
    - GEVI avg 18.75s, max 26.32s.
    - GayRado avg 8.57s, max 14.10s.
    - HFGPM avg 9.13s, max 10.60s.
    - GayFetishandBDSM avg 8.72s, max 11.60s.
  - GayWorld is an outlier pattern: it does not emit explicit finish markers in this log file, but thread spans from first search query to last logged activity are long:
    - thread `16f833000`: 297.46s
    - thread `16fc3f000`: 256.87s
    - thread `17004b000`: 244.52s
  - GayWorld repeatedly paginates search queries (`?s=...`, `page/2`, `page/3`, etc.) and iterates many candidate entries per query.

### Phase 4 - Correlate root causes against user symptom
- What: Build expected vs observed behavior and rank likely root causes.
- Why this supports the goal: Produces actionable diagnosis instead of raw log dumps.
- Output if operating correctly: Root-cause ranking with evidence.
- Status: Completed.

## Expected vs Observed

### Expected (fast path)
1. Library scan walks filesystem and updates changed media quickly.
2. Metadata lookups finish in a few seconds per item.
3. Optional post-processing does not dominate perceived scan time.

### Observed (current reality)
1. Scan activity itself is quick (seconds to tens of seconds).
2. Significant time is spent after scan in deep analysis jobs (`--analyze-deeply`) that can take 1-3 minutes each.
3. Multiple metadata agents run per item; some web-search flows (notably GayWorld) span ~4-5 minutes per worker thread due to broad pagination and repeated non-matching candidates.

## Root Cause Ranking
1. **Primary: Deep media analysis backlog after scans**
   - Evidence: repeated `--analyze-deeply --item ...` jobs with long durations (up to 172.09s each) and ~9.39 minutes total in sampled logs.
2. **Secondary: Expensive agent search breadth (especially GayWorld)**
   - Evidence: multi-page search queries and long thread spans (244-297s) in `com.plexapp.agents.GayWorld.log`.
3. **Tertiary: Normal scan time is not the bottleneck**
   - Evidence: scan activity `8f3695af-...` completed in 1.46s; full scanner process examples at 1.4s and 44.7s.

## Decision
The "hour per video" feeling aligns more with **post-scan deep analysis + prolonged metadata-agent search loops**, not with the directory scan phase itself.

## Recommended next verification step
Run one controlled refresh for a single test item while temporarily disabling deep analysis tasks and compare wall-clock time against baseline.
