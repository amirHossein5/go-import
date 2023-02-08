## CHANGE LOG

## [v0.3.1](https://github.com/amirHossein5/go-import/compare/v0.3.0...v0.3.1)

## Fixed

- Separate standard library imports from another places with a new line.
- Find list of words when navigating path recursively. 
- Search for modules from current working directory every time before checking cached files.
- Creating cache file inside of `tmp` folder not in sublime's zip file.
- Fix Messing up imported keywords which contains `-` or any non word character.
- Don't suggest import paths which has `vendor/` directory.

## [v0.3.0](https://github.com/amirHossein5/go-import/compare/v0.2.1...v0.3.0)

### Added

- Cache paths of GOROOT and GOMODCACHE to import faster.
- Show quick panel for multi name imports.
- Sorting imports when importing.
- Add Settings file for setting GOROOT and GOMODCACHE for other OS.

## Fixed

- Fix to not consider import line itself when erasing unused imports.
- Being unable to import when no project is open.

## [v0.2.1](https://github.com/amirHossein5/go-import/compare/v0.1.0...v0.2.1)

### Added

- Find libraries inside opened project.
- Find installed libraries.

### Improved

- Get/Filter import keywords regex.

## v0.1.0
init
