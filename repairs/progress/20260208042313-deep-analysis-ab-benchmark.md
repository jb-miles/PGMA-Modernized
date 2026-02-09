# Deep Analysis A/B Benchmark - 2026-02-08 04:23:13

## Goal
Quantify whether toggling deep-analysis maintenance changes wall-clock time for a controlled single-path refresh on a known item (`ratingKey=471`).

## Phase Plan And Progress

### Phase 1 - Capture controls and baseline
- What: Read active Plex prefs and identify deep-analysis control keys and target item path.
- Why this supports the goal: Ensures both benchmark passes differ only by the intended toggle.
- Output if operating correctly: Confirmed key/value for deep-analysis setting and exact file path used for targeted refresh.
- Status: Completed.
- Result:
  - `ButlerTaskDeepMediaAnalysis` was detected and initially `value="1"`.
  - Target media path resolved from metadata item 471:
    - `/Volumes/internal/porn_movies/(Blue Pictures) - 5 Bros on Whitey Boy (2006).avi`
  - Item-level refresh endpoint `/library/metadata/471/refresh` returned `404` on this PMS build.
  - Section refresh with `path=` returned `200` and was used for test runs.

### Phase 2 - Establish repeatable clean-start conditions
- What: Stop Butler queue and kill active deep-analysis workers before each pass.
- Why this supports the goal: Prevents previously queued maintenance work from contaminating A/B timing.
- Output if operating correctly: Empty activities queue and no active `--analyze-deeply` scanner process at pass start.
- Status: Completed.
- Result:
  - Verified functional stop endpoint on this server build:
    - `DELETE /butler` returns `200`.
  - `pkill -f "Plex Media Scanner.*--analyze-deeply"` used to clear active deep workers.

### Phase 3 - Execute A/B passes
- What: Run two single-path refreshes for the same file, with deep-analysis toggle set `off` then `on`.
- Why this supports the goal: Directly measures whether this setting impacts immediate per-item refresh wall-clock.
- Output if operating correctly: Comparable wall-clock and job traces for both passes with explicit evidence of deep-analysis presence/absence.
- Status: Completed.
- Result:
  - Pass A (`ButlerTaskDeepMediaAnalysis=0`)
    - Refresh request: `GET /library/sections/1/refresh?path=...`
    - Wall-clock to activity queue empty: `1s`
    - Deep-analysis log growth: `0` lines
    - Scanner job observed: `--scan --refresh --section 1 --directory "<target file>"`
  - Pass B (`ButlerTaskDeepMediaAnalysis=1`)
    - Refresh request: same path and section
    - Wall-clock to activity queue empty: `1s`
    - Deep-analysis log growth: `0` lines
    - Scanner job observed: same `--scan --refresh` pattern

### Phase 4 - Restore settings and interpret outcome
- What: Restore original pref value and summarize benchmark implications.
- Why this supports the goal: Leaves environment stable and converts observations into actionable guidance.
- Output if operating correctly: Original setting restored and clear conclusion on observed bottleneck behavior.
- Status: Completed.
- Result:
  - `ButlerTaskDeepMediaAnalysis` restored to original value (`1`).
  - Butler tasks stopped again after benchmark to avoid continued maintenance queue.

## Key Evidence
- Pref toggles accepted (`200`):
  - `PUT /:/prefs?ButlerTaskDeepMediaAnalysis=0`
  - `PUT /:/prefs?ButlerTaskDeepMediaAnalysis=1`
- Targeted refresh accepted (`200`):
  - `GET /library/sections/1/refresh?path=<encoded target file>`
- Server log shows refresh job type for both passes:
  - `Plex Media Scanner --scan --refresh --section 1 --directory "<target file>"`
- No deep-analysis start lines were emitted during either pass.

## Conclusion
For this controlled single-file refresh, toggling `ButlerTaskDeepMediaAnalysis` did **not** change immediate refresh latency (`1s` vs `1s`) and did **not** trigger deep-analysis jobs in either pass.

This supports the earlier diagnosis: the perceived slowdown is dominated by Butler-scheduled deep-analysis backlog and/or broad agent-search workloads, not the direct file-scan step for an individual refresh.

## Practical control found during this run
- On this PMS build, stop maintenance queue with:
  - `DELETE /butler`
- Then kill any already running deep-analysis workers:
  - `pkill -f "Plex Media Scanner.*--analyze-deeply"`
