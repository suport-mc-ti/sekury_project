# Changelog

All notable changes to this project will be documented in this file.

## [3.0.0] - 2026-03-26

### Added
- Unified OG_SEKURY and OG_NETMAPPER into a single project.
- Integrated NETMAPPER submenu into the main CLI application.
- Added one-shot build automation with `build_all.bat`.
- Added NSIS installer support for `SEKURY_NETSUITE_Installer.exe`.
- Added formal project documentation for usage, distribution, and quick start.
- Added MIT license file.

### Changed
- Rebranded the project as SEKURY NETSUITE.
- Consolidated build artifacts under the `SEKURY_NETSUITE` naming scheme.
- Updated documentation and release workflow for the unified project.
- Cleaned the project root from old-version artifacts and deprecated names.

### Fixed
- Fixed invalid banner reference in the main CLI flow.
- Fixed packaging flow so executable, ZIP, and installer can be generated consistently.
