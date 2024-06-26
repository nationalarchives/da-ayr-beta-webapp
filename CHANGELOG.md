# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

It is part of the [TRE template repository](https://github.com/nationalarchives/da-tre-template)

## [1.1.0] - 2023-04-08

### Added

- Add ability to serve static assets from cloudfront with flask-s3

### Changed

- Bump moto from 5.0.3 to 5.0.4
- Bump pillow from 10.2.0 to 10.3.0
- configure playwright e2e tests to run on multiple browsers

### Fixed

- browse consignment date validation issues fixed
- visual regression tests viewports fixed

## [1.0.1] - 2023-03-28

### Fixed

- removing all search terms in search results route now returns you to the top level browse route as expected
- removed extra padding on search results summary and no results found pages

## [1.0.0] - 2023-03-27

### Added

- All features for AYR Webapp Beta MVP release including the following routes:
  - `search`
  - `search_results_summary`
  - `search_transferring_body`
  - `record`
  - `download_record`
  - `sign_out`
  - `browse`
  - `browse_transferring_body`
  - `browse_series`
  - `browse_consignment`
  - `static`
  - `index`
  - `sign_in`
  - `signed_out`
  - `callback`
  - `accessibility`
  - `cookies`
  - `privacy`
  - `how_to_use`
  - `terms_of_use`

## [0.0.1] - 2023-01-31

### Added

- The keep a change log CHANGELOG

### Fixed

- Minor typos
