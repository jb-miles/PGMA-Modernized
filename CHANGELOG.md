# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Changed

#### Age Gate/Cookie Handling
- **AEBN**: Added `ageGated=1` cookie to bypass age verification gate
  - Disabled caching on search requests (`cacheTime=0`)
  - Added age-gate detection logging for troubleshooting
- **GayEmpire**: Added `ageConfirmed=true` cookie to bypass age verification gate
  - Disabled caching on search and detail requests (`cacheTime=0`)
- **GayHotMovies**: Added `ageConfirmed=true` cookie to bypass age verification gate
  - Disabled caching on search requests (`cacheTime=0`)
  - Added age-gate detection logging for troubleshooting
- **GayFetishandBDSM**: Added `SITE_LANGUAGE` constant for localization handling
- **WolffVideo**: Added custom `getHTMLElementFromURL()` function to bypass SSL certificate issues
  - WolffVideo.com has an expired SSL certificate that requires verification bypass

#### Default Preferences - Reduced Collection Creation
Changed default preferences to create fewer collections by default for cleaner library organization:

**Disabled by default:**
- System Collections (IAFD, Compilation, Stacked) - `systemcollection: false`
- Genre Collections - `genrecollection: "No"`
- Country Collections - `countrycollection: "No"`
- Director Collections - `directorcollection: false`
- Cast Collections - `castcollection: false`

**Enabled by default:**
- Studio Collections - `studiocollection: true`
- Series Collections - `seriescollection: true`

#### IAFD Enrichment
- Disabled IAFD duration matching by default (`prefMATCHIAFDDURATION: false`)
- Reduces dependency on IAFD enrichment for improved reliability

### Notes
These changes were made across multiple commits over the past few weeks but are being documented here retroactively. Future changes will be documented in a more timely manner.

---

## [Previous Releases]

*No previous releases documented in this changelog.*
