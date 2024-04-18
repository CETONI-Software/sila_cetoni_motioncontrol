# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Types of changes

    `Added` for new features.
    `Changed` for changes in existing functionality.
    `Deprecated` for soon-to-be removed features.
    `Removed` for now removed features.
    `Fixed` for any bug fixes.
    `Security` in case of vulnerabilities.
-->

## Unreleased

## v1.10.0

Sync with sila_cetoni v1.10.0 release

### Changed

- All feature implementations use `PropertyUpdater` now

## v1.9.1

Sync with sila_cetoni v1.9.1 release

## v1.9.0

Sync with sila_cetoni v1.9.0 release

### Changed

- Don't set the Command Execution status explicitly - this is done by sila_python

## v1.8.0

Sync with sila_cetoni v1.8.0 release

### Changed

- Bump required sila2 version to v0.10.1
- Increase required Python version to 3.8 because in 3.7 the implementation of `ThreadPoolExecutor` in the standard library does not reuse idle threads leading to an ever increasing number of threads which eventually causes blocking of the server(s) on Raspberry Pis

## v1.7.1

Sync with sila_cetoni v1.7.1 release

### Fixed

- Typo in pyproject.toml

## v1.7.0

Sync with sila_cetoni v1.7.0

### Changed

- Bump required sila2 version to v0.10.0

## v1.6.0

Sync with sila_cetoni v1.6.0

## v1.5.0

Sync with sila_cetoni v1.5.0

## v1.4.0

Sync with sila_cetoni v1.4.0

### Fixed

- Raising of `ValidationError`s works again

## v1.3.0

Sync with sila_cetoni v1.3.0

### Fixed

- Properly call `super().stop()` in the feature implementation classes

## v1.2.0

Sync with sila_cetoni v1.2.0

### Changed

- Use the server name as th name for `ServerConfiguration`

## v1.1.0

### Changed

- Bump sila2 to v0.8.2

## v1.0.0

First release of sila_cetoni

This is the motioncontrol plugin which adds support for controlling CETONI axis system devices via SiLA 2

### Added

- AxisPositionController feature and feature implementation
- AxisSystemControlService feature and feature implementation
- AxisSystemPositionController feature and feature implementation
