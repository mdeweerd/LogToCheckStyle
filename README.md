# Log2CheckStyle

Convert a log to another format for easy integration with GitHub Actions,
continuous integration pipelines and other purposes.

## Features

- Converts messages to Checkstyle XML format.
- Supports specifying input and output files.
- Allows specifying a root directory to remove from file paths.
- Provides options for GitHub Action integration (annotations).
- Handful as a standalone command-line tool (`logToCs.py`).

## Usage

### Command Line Interface

```bash
logToCs.py [OPTIONS] [INPUT [OUTPUT]]
```

#### OPTIONS

```text
Convert messages to Checkstyle XML format.

positional arguments:
  input                 Input file. Use '-' or omit for stdin.
  output                Output file. Use '-' or omit for stdout.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_NAMED, --in INPUT_NAMED
                        Input filename. Overrides positional input.
  -o OUTPUT_NAMED, --out OUTPUT_NAMED
                        Output filename. Overrides positional output.
  --root ROOT_PATH      Root directory to remove from file paths. Defaults to
                        working directory.
  --github-annotate, --no-github-annotate
                        Annotate when in Github workflow. (default: False)
  --name-only, --no-name-only
                        Report filenames only. (default: False)
```

### GitHub Action

#### Using No Extra Resources:

```yaml
  - name: Convert Raw Log to Checkstyle format (launch action)
    uses: mdeweerd/logToCheckStyle@v2024.3.3
    if: ${{ failure() }}
    with:
      in: ${{ env.RAW_LOG }}
      # Out can be omitted if you do not need the xml output
      out: ${{ env.CS_XML }}
```

The above extracts the notifications from the `RAW_LOG`, writes a file in
CheckStyle format and applies source code annotations for a Github Pull
Request.

For a full example, see
[the precommit github workflow for this project](.github/workflows/pre-commit.yml).

#### Using local resources

Convert the output from an action to CheckStyle xml and convert that to
GitHub Annotations using a different action.

These examples assume that logToCs.py is available as .github/logToCs.py.

##### Example 1:

Use other action to generate the GitHub annotations.

```yaml
  - run: |
      pre-commit run -all-files | tee pre-commit.log
      .github/logToCs.py pre-commit.log pre-commit.xml
  - uses: staabm/annotate-pull-request-from-checkstyle-action@v1
    with:
      files: pre-commit.xml
      notices-as-warnings: true     # optional
```

##### Example 2 (old):

Use cs2pr commands to generate the GitHub annotations.

```yaml
  - run: |
      pre-commit run --all-files | tee pre-commit.log
  - name: Add results to PR
    if: ${{ always() }}
    run: |
      .github/logToCs.py pre-commit.log | cs2pr
```

## Tips

### PHP Codesniffer (AKA php-cs, phpcs)

Use `--report=emacs` (when running with `pre-commit`).

### Edit files that have notices from the CLI.

When running a command on the CLI, it may be helpful to edit only files
with errors.

For instance, codespell reports:

```bash
codespell
./ChangeLog:8244: abadword ==> agoodword
```

And you want to edit the ChangeLog to make the correction.

With the bash function below it is possible to edit the reported files
using `viErrors codespell`.

`logToCs.py` must be in your path.

## Add to .bashrc:

```bash
viErrors() { "$EDITOR" $("$@" |& logToCs.py --name-only) ; }
_viErrors_completion() { COMPREPLY=($(compgen -c -- "${COMP_WORDS[COMP_CWORD]}")); return 0; }
complete -o default -F _viErrors_completion viErrors
```

## or, add in completions directory

Execute the following once and everything code will be loaded when you type
`viErrors....<TAB>`

```bash
_cdir=${BASH_COMPLETION_USER_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/bash-completion}/completions
mkdir -p "${_cdir}"
cat > "${_cdir}/viErrors.bash" << 'EOF'
viErrors() { "$EDITOR" $("$@" |& logToCs.py --name-only) ; }
_viErrors_completion() { COMPREPLY=($(compgen -c -- "${COMP_WORDS[COMP_CWORD]}")); return 0; }
complete -o default -F _viErrors_completion viErrors
EOF
```

## Extending

In the script, patterns can be added to "PATTERNS" to match more messages.

To allow multiline patterns, the python module 'regex' is required.

## Author(s):

- [mdeweerd]

## License

MIT License

[mdeweerd]: https://github.com/mdeweerd
