# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.0] - 2024-01-01

### Added
- Initial release
- `get_country()` — Nepal national boundary
- `get_province()` — 7 provincial boundaries with optional name filter
- `get_district()` — 77 district boundaries with province and name filters
- `get_municipality()` — 753 municipality boundaries with hierarchical filters
- `get_ward()` — 6 743 ward boundaries with full hierarchical filters
- `get_multiple()` — retrieve several levels in one call
- `info()` — summary statistics for a given level
- `list_levels()` — report feature counts for all levels
- `clear_cache()` — free in-memory cache
- Convenience aliases: `get_prov`, `get_dist`, `get_mun`
- GeoJSON data bundled inside the package (WGS84 / EPSG:4326)
- MIT License
