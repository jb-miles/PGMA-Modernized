# Error Message Catalog — Gay Adult Film Agents

Generated: 2026-02-05 from 7-day log window (168 hours)
Source: `repairs/progress/consolidated_plex_logs_20260205_153118.txt`
Total error messages clustered: 327 across 45 log files

---

## Agent Inventory

The following agents in this repo produced errors during the analysis window:

| Agent | Total Errors | Agent-Specific Error Types | Infrastructure-Only |
|---|---|---|---|
| AEBN | 99 | 8 | No |
| GEVI | 17 | 9 | No |
| GayAdultFilms | 128 | 1 | No |
| NFOImporter | 3 | 1 | No |
| AVEntertainments | 2 | 0 | Yes |
| AdultFilmDatabase | 2 | 0 | Yes |
| BestExclusivePorn | 2 | 0 | Yes |
| CDUniverse | 2 | 0 | Yes |
| Fagalicious | 2 | 0 | Yes |
| GEVIScenes | 2 | 0 | Yes |
| GayAdult | 4 | 0 | Yes |
| GayAdultScenes | 2 | 0 | Yes |
| GayEmpire | 4 | 0 | Yes |
| GayFetishandBDSM | 2 | 0 | Yes |
| GayHotMovies | 2 | 0 | Yes |
| GayMovie | 2 | 0 | Yes |
| GayRado | 2 | 0 | Yes |
| GayWorld | 4 | 0 | Yes |
| HFGPM | 2 | 0 | Yes |
| HomoActive | 2 | 0 | Yes |
| IAFD | 2 | 0 | Yes |
| QueerClick | 2 | 0 | Yes |
| SimplyAdult | 2 | 0 | Yes |
| WayBig | 2 | 0 | Yes |
| WolffVideo | 2 | 0 | Yes |

Agents with **no errors in this window** (no log entries at all or only INFO/DEBUG): None — all installed agents had at least infrastructure errors from plugin startup.

---

## Category 1: Plex Infrastructure Errors (All Agents)

These errors appear identically in every agent's log and originate from the Plex Framework, not from agent code. They fire once per plugin load (e.g., on PMS restart or plugin reload).

### INFRA-01: Resource Hash HTTP 404

- **Source**: `(networking:197)`
- **Severity**: ERROR
- **Template**: `Error opening URL 'http://127.0.0.1:32400/:/plugins/com.plexapp.system/resourceHashes'`
- **Root cause**: PMS internal API returns 404 when the system plugin isn't ready yet during startup.
- **Impact**: None — the framework handles this gracefully and proceeds.
- **Action**: Ignore. This is a Plex Framework startup race condition.

### INFRA-02: Resource Hash Exception

- **Source**: `(runtime:1299)`
- **Severity**: CRITICAL
- **Template**: `Exception getting hosted resource hashes (most recent call last): ... HTTPError: HTTP Error 404: Not Found`
- **Root cause**: Same as INFRA-01; this is the traceback associated with the HTTP 404.
- **Impact**: None.
- **Action**: Ignore.

---

## Category 2: Agent-Specific Errors

### AEBN (8 unique agent-specific error types)

#### AEBN-01: Search Title Match Failure (Traceback)

- **Source**: `(utils:5551)` in `__init__.py:178`
- **Severity**: ERROR
- **Count**: 44
- **Template**: `AEBN - SEARCH:: ❌ File: __init__.py, Line: 178, Function: _process_function_call -> _search -> search`
- **Description**: The search function found results on AEBN but none matched the expected title. This is the traceback marker.
- **Paired with**: AEBN-02

#### AEBN-02: Search Title Match Failure (Message)

- **Source**: `(utils:5552)`
- **Severity**: ERROR
- **Count**: 43
- **Template**: `AEBN - SEARCH:: Error getting Site Title: < Title Match Failure! >`
- **Description**: Human-readable companion to AEBN-01. The site returned results but the title-matching logic in `matchTitle()` could not find a close enough match.
- **Paired with**: AEBN-01

#### AEBN-03: IAFD Lookup Failure (Traceback)

- **Source**: `(utils:5551)`
- **Severity**: ERROR
- **Count**: 4
- **Template**: `AEBN - UTILS :: ❌ File: , Line: , Function: update -> updateMetadata -> getFilmOnIAFD`
- **Description**: IAFD film lookup failed during metadata update. Empty File/Line fields indicate the error was caught and re-raised by the wrapper.
- **Paired with**: AEBN-04

#### AEBN-04: IAFD Lookup Disabled

- **Source**: `(utils:5552)`
- **Severity**: ERROR
- **Count**: 1
- **Template**: `AEBN - UTILS :: IAFD Lookup Disabled to prevent 403 Errors.`
- **Description**: IAFD lookups are deliberately disabled because IAFD is returning HTTP 403 Forbidden responses (likely anti-scraping measures). This is a configuration-level disable, not a runtime crash.
- **Paired with**: AEBN-03

#### AEBN-05: No Matching Site Studio

- **Source**: `(utils:5552)`
- **Severity**: ERROR
- **Count**: 2
- **Template**: `AEBN - SEARCH:: Error No Matching Site Studio`
- **Description**: During search, the agent could not match the studio name from the filename/metadata against any studio in the AEBN search results.

#### AEBN-06: Storage Write Exception (Poster)

- **Source**: `(storage:89)`
- **Severity**: CRITICAL
- **Count**: 1
- **Template**: `Exception writing to /Volumes/internal/porn_movies/(...).jpg (most recent call last): ... IOError: [Errno 2] No such file or directory`
- **Description**: Plex Framework failed to save a poster image to disk. The underlying error is an IOError on a macOS resource fork file (`._` prefix), suggesting a filesystem or volume-mount issue.
- **Paired with**: AEBN-07

#### AEBN-07: Poster Save Warning

- **Source**: `(utils:5552)`
- **Severity**: ERROR
- **Count**: 1
- **Template**: `AEBN - UTILS :: Warning: Saving Poster to Disk: [Errno 2] No such file or directory: '...'`
- **Description**: Agent-level warning that poster saving failed. Companion to AEBN-06.
- **Paired with**: AEBN-06

#### AEBN-08: No Scenes/Reviews Found

- **Source**: `(utils:5552)`
- **Severity**: ERROR
- **Count**: 1
- **Template**: `AEBN - UTILS :: Warning: No Scenes / Reviews Found!`
- **Description**: The AEBN detail page for a film contained no scene breakdown or reviews. This may be normal for some titles.

---

### GEVI (9 unique agent-specific error types)

#### GEVI-01: getSiteInfo Failure

- **Source**: `(utils:5551)` in `utils.py:3807`
- **Severity**: ERROR
- **Count**: 4
- **Template**: `GEVI - UTILS :: ⚠ File: utils.py, Line: 3807, Function: getSiteInfo -> _apply -> getSiteInfoGEVI`
- **Description**: The agent failed to retrieve site information from GEVI during metadata collection. Logged as a warning (⚠) rather than a hard error.

#### GEVI-02: Search Failure

- **Source**: `(utils:5551)`
- **Severity**: ERROR
- **Count**: 2
- **Template**: `GEVI - SEARCH:: ⚠ File: , Line: , Function: _process_function_call -> _search -> search`
- **Description**: GEVI search function encountered an issue. Empty File/Line fields indicate the error was caught in the generic wrapper.

#### GEVI-03: Release Date Fallback

- **Source**: `(utils:5552)`
- **Severity**: ERROR
- **Count**: 2
- **Template**: `GEVI - SEARCH:: Warning: Getting Site URL Release Date: Default to Filename Date: 2008-12-31 00:00:00`
- **Description**: Could not extract release date from the GEVI site page; fell back to the date parsed from the filename. Functionally a warning, not data loss.

#### GEVI-04: Cannot Read Model

- **Source**: `(model:205)`
- **Severity**: ERROR
- **Count**: 1
- **Template**: `Cannot read model from .../Metadata/Movies/...bundle/Contents/com.plexapp.agents.GEVI`
- **Description**: Plex could not deserialize the cached metadata model for this agent. Usually caused by a corrupted or empty metadata bundle. May self-heal on next metadata refresh.

#### GEVI-05: No Body Types (Index Error)

- **Source**: `(utils:5552)`
- **Severity**: ERROR
- **Count**: 1
- **Template**: `GEVI - UTILS :: Warning: No Body Types: list index out of range`
- **Description**: The GEVI page for a performer did not contain body type data where the parser expected it. An `IndexError` was caught and logged.

#### GEVI-06: No Types (Index Error)

- **Source**: `(utils:5552)`
- **Severity**: ERROR
- **Count**: 1
- **Template**: `GEVI - UTILS :: Warning: No Types: list index out of range`
- **Description**: Similar to GEVI-05; a performer type field was missing from the GEVI page HTML.

#### GEVI-07: IAFD Lookup Disabled

- **Source**: `(utils:5552)`
- **Severity**: ERROR
- **Count**: 1
- **Template**: `GEVI - UTILS :: IAFD Lookup Disabled to prevent 403 Errors.`
- **Description**: Same as AEBN-04. IAFD lookups are disabled project-wide.

#### GEVI-08: Storage Write Exception (Poster)

- **Source**: `(storage:89)`
- **Severity**: CRITICAL
- **Count**: 1
- **Template**: `Exception writing to /Volumes/internal/porn_movies/(...).jpg`
- **Description**: Same root cause as AEBN-06. macOS resource fork (`._` file) IOError.

#### GEVI-09: Poster Save Warning

- **Source**: `(utils:5552)`
- **Severity**: ERROR
- **Count**: 1
- **Template**: `GEVI - UTILS :: Warning: Saving Poster to Disk: [Errno 2] No such file or directory`
- **Description**: Same pattern as AEBN-07. Agent-level companion to GEVI-08.

---

### GayAdultFilms (1 unique agent-specific error type)

#### GAF-01: Cannot Read Model

- **Source**: `(model:205)`
- **Severity**: ERROR
- **Count**: 122
- **Template**: `Cannot read model from .../Metadata/Movies/...bundle/Contents/com.plexapp.agents.GayAdultFilms`
- **Description**: By far the highest-count error for any single agent. Plex cannot deserialize the cached metadata model for 122 distinct items. This suggests widespread metadata corruption or an agent that wrote incomplete/invalid metadata at some point. This is the **most impactful error** in the entire log window.

---

### NFOImporter (1 unique agent-specific error type)

#### NFO-01: Function 'Start' Not Found

- **Source**: `(sandbox:298)`
- **Severity**: ERROR
- **Count**: 1
- **Template**: `Function named 'Start' couldn't be found in the current environment`
- **Description**: The Plex plugin sandbox could not find a `Start()` function in the NFOImporter plugin. This likely means the plugin's `__init__.py` doesn't define a `Start()` entry point, or the plugin failed to load entirely. This error also appeared for `localmedia` (a built-in agent).

---

## Category 3: Cross-Cutting Error Patterns

These patterns appear across multiple agents and share a common root cause:

### CROSS-01: IAFD 403 Disabled

- **Agents affected**: AEBN, GEVI (and all agents that use `getFilmOnIAFD`)
- **Pattern**: IAFD lookups deliberately disabled due to HTTP 403 from iafd.com
- **Error IDs**: AEBN-03, AEBN-04, GEVI-07
- **Status**: Intentionally disabled via configuration. Re-enable requires IAFD to lift rate limiting or adding request throttling/headers.

### CROSS-02: Poster Storage IOError

- **Agents affected**: AEBN, GEVI
- **Pattern**: macOS resource fork (`._` prefix) file causes `IOError: [Errno 2]` during poster save
- **Error IDs**: AEBN-06, AEBN-07, GEVI-08, GEVI-09
- **Root cause**: The Plex Framework's `storage.py` uses `shutil.move()` which fails when macOS creates `._` resource fork files on certain volumes (especially network/external drives).
- **Status**: Framework-level issue, not directly fixable in agent code.

### CROSS-03: Title/Studio Match Failures (AEBN)

- **Agents affected**: AEBN
- **Pattern**: Search returns results but title/studio matching logic fails
- **Error IDs**: AEBN-01, AEBN-02, AEBN-05
- **Total count**: 89 (largest agent-specific error volume)
- **Status**: Active — title matching improvements were recently implemented but may need further tuning.

### CROSS-04: Model Corruption

- **Agents affected**: GayAdultFilms, GEVI
- **Pattern**: `Cannot read model from .../Contents/com.plexapp.agents.<Agent>`
- **Error IDs**: GAF-01, GEVI-04
- **Total count**: 123
- **Status**: Likely requires metadata cache cleanup (Plex "Empty Trash" or manual bundle deletion).

---

## Summary Statistics

| Category | Error Count | % of Total |
|---|---|---|
| Infrastructure (INFRA-01/02) | 72 | 22% |
| Title/Studio Match (CROSS-03) | 89 | 27% |
| Model Corruption (CROSS-04) | 123 | 38% |
| IAFD Disabled (CROSS-01) | 6 | 2% |
| Poster Storage (CROSS-02) | 4 | 1% |
| Parser Warnings (GEVI-01..06) | 11 | 3% |
| Other (AEBN-08, NFO-01) | 2 | <1% |
| Non-PGMAM agents | 20 | 6% |
| **Total** | **327** | **100%** |

### Top Issues by Impact

1. **Model Corruption (38%)** — 123 GayAdultFilms entries can't load metadata. Highest count, affects end-user experience.
2. **Title Match Failures (27%)** — 89 AEBN searches fail to match. Prevents metadata from being applied.
3. **Infrastructure Noise (22%)** — Benign startup errors, safe to ignore.
4. **GEVI Parser Gaps (3%)** — Minor data gaps (missing body types, dates). Low severity.
5. **IAFD Disabled (2%)** — Intentional, pending IAFD access resolution.
6. **Poster Storage (1%)** — Filesystem/volume issue, not agent code.
