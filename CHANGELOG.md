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
