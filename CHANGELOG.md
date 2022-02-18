# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] - 2021-12-16

### Added

- Filtering option to filter peaks/losses present in more/less thant N percent of samples [#25](https://github.com/mandelbrot-project/memo/issues/25)

### Changed

- actions: add readme web-link checker
- actions: developed test_user_workflow.py

## [0.1.3] - 2021-12-16

### Added

- Documentation

## [0.1.2] - 2021-12-15

### Added

- test for memo_from_unaligned
- test for memo_from_aligned
- test for merged_memo()
- possibility to import "memo ready" feature table

### Changed

- Changed classes.py to avoid erasing when filtering
- Changed .removesuffix to allow support of python <3.9

## [0.1.1] - 2021-12-10

### Changed

- Changed required version of python from >3.8 to >3.7 for TMAP compatibility

## [0.1.0] - 2021-12-06

### Added

- New `MemoMatrix` class, replacing the former `MemoContainer` [#14](https://github.com/matchms/matchms/pull/14)
- First set of unit tests [#12](https://github.com/matchms/matchms/pull/12)
- Continuous integration for testing [#4](https://github.com/matchms/matchms/pull/4)

### Changed

- Code linting [#16](https://github.com/matchms/matchms/pull/16)
- Code linting [#14](https://github.com/matchms/matchms/pull/14)

## [0.0.4] - 2021-11-01

### Added

- This is the initial version of memo from https://github.com/mandelbrot-project/memo


[Unreleased]: https://github.com/mandelbrot-project/memo/compare/0.1.0...HEAD
[0.1.3]: https://github.com/mandelbrot-project/memo/compare/0.1.2...0.1.3
[0.1.2]: https://github.com/mandelbrot-project/memo/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/mandelbrot-project/memo/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/mandelbrot-project/memo/compare/0.0.4...0.1.0
[0.0.4]: https://github.com/mandelbrot-project/memo/releases/tag/0.0.4
