Auto import keyword(s), or remove unused imports of golang in sublime text. Also sorts imports when importing.

## Demo

<div align="center">
  <img src="demo.gif" width="800"/>
</div>

Finds imports from:
- Opened project path(if has `go.mod`)
- Go library itself(GOROOT)
- Installed packages(GOMODCACHE)

## Installation

Open command palette `Package Control: Add Repository`:

```
https://github.com/amirHossein5/go-import
```

Then install it using package control by name of `go-import`

## Settings

By default GOROOT and GOMODCACHE are `/usr/lib/go`, `~/go/pkg/mod`.
To edit: `GoImport: Settings`.

## Default key bindings

For modifing key bindings open command palette then `GoImport: Edit key bindings`.

Available Default key bindings:

- `alt+i` -> command: `go_import`
- `alt+e` -> command: `go_import_erase_unused`

## Commands

Available commands:

- `go_import`: Import libs under cursor(s).
- `go_import_erase_unused`: Removes unused imports.

## LICENCE

Licensed under the [MIT license](https://opensource.org/licenses/MIT).
