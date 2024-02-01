# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2024-02-01

### Added

- Added support for `"barrier"` `"meta"` instruction in https://github.com/CQCL/phir/pull/56

## [0.2.1] - 2023-12-12

### Fixed

- spec & model: correct values for R2XXYYZZ gate params and args in https://github.com/CQCL/phir/pull/38

## [0.2.0] - 2023-12-06

### Added

- Parallel quantum operations block `qparallel`
- Boolean metadata parameter `strict_parallelism`

### Fixed

- model: require `data_type` in `cvar_define` in https://github.com/CQCL/phir/pull/14

## [0.1.6] - 2023-11-07

### Fixed

- fix(spec): include missing `<=` comparison operator
- fix(model): better validation in https://github.com/CQCL/phir/pull/15
  - pick classical ops from Table I in the spec
  - pick quantum ops from Table II in the spec
  - split QOp into four, validate args/angles

### Changed

- docs: shorten spec file name to `spec.md`
- ci(markdown): add markdownlint, fix minor issues
- style(ruff): use `ruff format` instead of black

## [0.1.5] - 2023-10-23

### Changed

- feat: [include units for duration and angles](https://github.com/CQCL/phir/pull/9)

## [0.1.4] - 2023-10-20

### Changed

- [Better validation for tuples](https://github.com/CQCL/phir/pull/8)

## [0.1.3] - 2023-10-18

### Added

- phir package now comes with type information.

## Fixed

- phir version in the docs site.

## [0.1.2] - 2023-10-17

### Changed

- Add optional "angles" field to quantum operations.

## [0.1.1] - 2023-10-17

### Changed

- Typing improvements to the PHIR model.
- Correct a mistake in PHIR spec example.

## [0.1.0] - 2023-10-16

First release.

### Added

- Pydantic model and JSON schema of the PHIR Specification.
- `phir-cli` for validation against that model and pretty printing on the command line.

[0.1.0]: https://github.com/CQCL/phir/commits/v0.1.0
[0.1.1]: https://github.com/CQCL/phir/compare/v0.1.0...v0.1.1
[0.1.2]: https://github.com/CQCL/phir/compare/v0.1.1...v0.1.2
[0.1.3]: https://github.com/CQCL/phir/compare/v0.1.2...v0.1.3
[0.1.4]: https://github.com/CQCL/phir/compare/v0.1.3...v0.1.4
[0.1.5]: https://github.com/CQCL/phir/compare/v0.1.4...v0.1.5
[0.1.6]: https://github.com/CQCL/phir/compare/v0.1.5...v0.1.6
[0.2.0]: https://github.com/CQCL/phir/compare/v0.1.6...v0.2.0
[0.2.1]: https://github.com/CQCL/phir/compare/v0.2.0...v0.2.1
[0.3.0]: https://github.com/CQCL/phir/compare/v0.2.0...v0.3.0
[unreleased]: https://github.com/CQCL/phir/compare/v0.3.0...HEAD

<!-- markdownlint-configure-file {"MD024": {"siblings_only" : true}, "MD034": false} -->
