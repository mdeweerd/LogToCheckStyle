# Convert a log to CheckStyle format.

Url: https://github.com/mdeweerd/LogToCheckStyle

The log can then be used for generating annotations in a github action.

Note: this script is very young and "quick and dirty". Patterns can be
added to "PATTERNS" to match more messages.

To allow multiline patterns, the python module 'regex' is required.

## OPTIONS

```text
positional arguments:
  input                 Input file. Use '-' for stdin.
  output                Output file. Use '-' for stdout.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_NAMED, --in INPUT_NAMED
                        Input filename. Overrides positional input.
  -o OUTPUT_NAMED, --out OUTPUT_NAMED
                        Output filename. Overrides positional output.
  --root ROOT_PATH      Root directory to remove from file paths.
                        Defaults to working directory.
```

## Run as a github action (no extra resources)

This runs `logToCs.py` which outputs "github action commands" that result
in source code annotations.

For an example, see
[a github action for this project](.github/workflows/pre-commit.yml).

```yaml
  - name: Convert Raw Log to Checkstyle format (launch action)
    uses: mdeweerd/logToCheckStyle@v2024.2.2
    if: ${{ failure() }}
    with:
      in: ${{ env.RAW_LOG }}
      # Out can be omitted if you do not need the xml output
      out: ${{ env.CS_XML }}
```

## Run as a github action (local resources)

Assumes that logToCs.py is available as .github/logToCs.py.

### Example 1 (old):

This is the older method of running `logToCs.py`. It is no longer needed to
use `staabm/annotate-pull-request-from-checkstyle-action`, in fact, when
`GITHUB_ACTIONS` is `true`, `logToCs.py` will write the appropriate
commands to stdout resulting in code annotations.

```yaml
  - run: |
      pre-commit run -all-files | tee pre-commit.log
      .github/logToCs.py pre-commit.log pre-commit.xml
  - uses: staabm/annotate-pull-request-from-checkstyle-action@v1
    with:
      files: pre-commit.xml
      notices-as-warnings: true     # optional
```

### Example 2 (old):

Also old, `logToCs.py` now handles annotation by itself.

```yaml
  - run: |
      pre-commit run --all-files | tee pre-commit.log
  - name: Add results to PR
    if: ${{ always() }}
    run: |
      .github/logToCs.py pre-commit.log | cs2pr
```

## Hints

- `phpcs`: Use `--report=emacs` (when running with `pre-commit`).

## Author(s):

- https://github.com/mdeweerd

## License

MIT License
