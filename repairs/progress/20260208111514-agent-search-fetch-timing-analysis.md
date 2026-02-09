# Agent Search Fetch And Timing Analysis - 2026-02-08 11:15:14

## Goal
Measure how many search fetches are typically executed when candidates are found, and identify searches that do not finish within a reasonable time.

## Phase Plan And Progress

### Phase 1 - Collect raw search lifecycle events
- What: Parse live PMS plugin logs (`com.plexapp.agents.*.log*`) for search lifecycle markers.
- Why this supports the goal: We need start/finish markers and query/candidate lines to compute fetch counts and durations.
- Output if operating correctly: Structured session rows with start time, search queries, candidate processing count, and finish status.
- Status: Completed.
- Result:
  - Parsed non-imdb agent logs across active + rotated files.
  - Search lifecycle markers used:
    - `SEARCH:: Search Query:`
    - `SEARCH:: Next Page Search Query:`
    - `SEARCH:: Titles Found`
    - `SEARCH:: Processing`
    - `Finished Search Routine`
    - `Error: Search Query did not pull any results`

### Phase 2 - Quantify fetches when candidates are found
- What: Compute aggregate and per-agent fetch metrics for sessions where candidates were found (`Titles Found > 0`).
- Why this supports the goal: Gives a direct baseline for “normal” search breadth before adding hard limits.
- Output if operating correctly: Average query count and candidate-processing count for successful candidate-return sessions.
- Status: Completed.
- Result:
  - Total parsed sessions: `111`
  - Finished sessions: `93`
  - Sessions with candidates found: `43`
  - Overall when candidates are found:
    - Average search-query fetches per session: `1.07`
    - Average candidate rows processed per session: `5.47`
    - Average `Titles Found` count per session: `5.56`

#### Per-agent (candidate-found sessions)
- `GEVI`: sessions `9`, avg query fetches `1.11`, avg processed rows `1.44`, avg titles found `1.67`, avg duration `18.85s`
- `GayFetishandBDSM`: sessions `3`, avg query fetches `1.33`, avg processed rows `3.33`, avg titles found `3.33`, avg duration `12.19s`
- `GayMovie`: sessions `6`, avg query fetches `1.17`, avg processed rows `6.17`, avg titles found `5.17`, avg duration `12.07s`
- `GayRado`: sessions `10`, avg query fetches `1.00`, avg processed rows `14.70`, avg titles found `14.70`, avg duration `7.32s`
- `GayWorld`: sessions `5`, avg query fetches `1.00`, avg processed rows `1.40`, avg titles found `1.80`, avg duration `21.10s`
- `HFGPM`: sessions `10`, avg query fetches `1.00`, avg processed rows `2.10`, avg titles found `2.70`, avg duration `10.30s`

### Phase 3 - Detect unreasonably long or unfinished searches
- What: Flag sessions that either finished slowly (`>= 60s`) or remained open without a finish marker.
- Why this supports the goal: Identifies timeout and hanging behavior candidates for hardening.
- Output if operating correctly: Count of long finished sessions and list of open sessions with observed run time.
- Status: Completed.
- Result:
  - Finished sessions >= 60s in current parsed window: `0`
  - Open sessions without `Finished Search Routine`: `18`
  - Open sessions > 30s (notable):
    - `GayWorld` thread `16fae3000`: `94.31s`, `2` query fetches, `10` processed rows, `8` titles found
    - `GayWorld` thread `16d9fb000`: `41.90s`, `2` query fetches, `0` processed rows, `0` titles found
    - `GayFetishandBDSM` thread `171993000`: `35.71s`, `2` query fetches, `0` processed rows, `0` titles found
  - For `GayFetishandBDSM` sampled case, log shows repeated search-query failures with no finish marker:
    - `Error: Search Query did not pull any results: < No Film Titles >`

## Interpretation
- In this current log window, candidate-found searches are usually shallow (`~1` search query fetch) and finish in tens of seconds or less.
- The main concern is not long completed runs in this slice; it is sessions that fail/no-result and do not consistently emit the normal finish marker.
- Combined with earlier historical evidence (multi-minute GayWorld spans), this supports adding explicit guardrails:
  - search wall-clock timeout budget,
  - max search pages,
  - max detail fetches total,
  - guaranteed search routine close/finalization on errors.
