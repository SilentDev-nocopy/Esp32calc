# Resiris

A PC-side development environment and interpreter for the Resiris programming language.

The current prototype runs `.resy` source files through the Resiris tokenizer, parser, AST and interpreter.

## Requirements

You need:

- Python 3

For the `.resy` file integration, these are optional:

- VS Code / Code - OSS / VSCodium
- `xdg-mime`
- `update-mime-database`
- `update-desktop-database`

## How to use

Download or clone this repository, then open a terminal in the project folder.

To run a specific Resiris program:

```bash
python3 -m resiris program.resy
```

You can also use the project launcher:

```bash
./resiris program.resy
```

If you run Resiris without a file, it does not automatically open `main.resy`. Instead, it prints a short usage message:

```bash
resiris
```

## Using `resiris` as a terminal command

If you want to start Resiris by simply typing:

```bash
resiris
```

Run this from inside the project folder:

```bash
./install_reseris
```

The installer creates the `resiris` symlink in `~/.local/bin`. It also installs the `.resy` Linux file-manager integration and the existing Seti-based VS Code extension from `pre_packaging`.

Then you can run Resiris from any terminal:

```bash
resiris program.resy
```

Running only:

```bash
resiris
```

shows the short Resiris usage screen. It does not run `main.resy` automatically.

## Error output

When a Resiris source file contains a normal tokenizer, parser or runtime error, the CLI prints only the Resiris error. Python traceback output is not shown.

For example:

```text
UnknownVariableError: sor 1, oszlop 1: x: ismeretlen név
```

The internal Python call stack is kept out of normal Resiris error output.

## Removing it

To remove the installed terminal command, `.resy` Linux integration and VS Code extension, run:

```bash
./uninstall_reseris.sh
```

The project files themselves are not deleted.
