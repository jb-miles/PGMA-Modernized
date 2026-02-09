# Poster Save Fallback Fix Plan - 2026-02-08 11:47 PST

## Goal
Stop poster download failures caused by Plex temp-file (`._`) write/move behavior so posters are consistently saved to disk.

## Phase Plan And Progress

### Phase 1 - Confirm root cause in code and logs
- What: Trace log stack and code path for poster-disk save.
- Why this supports the goal: Ensures we patch the exact failing call site.
- Output if operating correctly: Identified failing API and call location.
- Status: Completed.
- Result:
  - `Core.storage.save` writes via temp path `._<filename>` and fails on media volume.
  - Poster save callsites identified in shared and bundle utils.

### Phase 2 - Implement resilient save wrapper in all active utils copies
- What: Add `SafeSaveFile()` wrapper (try `Core.storage.save`, fallback to direct binary write) and route poster save through it.
- Why this supports the goal: Preserves existing behavior while bypassing `._` temp failure mode.
- Output if operating correctly: No `Warning: Saving Poster to Disk: [Errno 2] ... /._(...).jpg` for new scans.
- Status: Completed.
- Result:
  - Added `SafeSaveFile()` to `_PGMA/Scripts/utils.py` and all agent bundle `Contents/Code/utils.py` files.
  - Replaced poster disk-save call to use `SafeSaveFile(downloadPoster, imageContent)` in all updated files.
  - Added missing `image = item` assignment in bundle poster/art loops so metadata keys are no longer empty.

### Phase 3 - Verify patch presence and summarize deployment steps
- What: Validate updated files contain wrapper + call replacement, then provide rollout/test steps.
- Why this supports the goal: Ensures change is complete and actionable for live Plex deployment.
- Output if operating correctly: File list + quick validation commands.
- Status: Completed.
- Result:
  - Validation confirms `def SafeSaveFile` and `SafeSaveFile(downloadPoster, imageContent)` present across all targeted files.
  - No remaining `PlexSaveFile(downloadPoster, imageContent)` calls in repo.
