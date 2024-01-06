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

## Examples

Assumes that logToCs.py is available as .github/logToCs.py.

### Example 1:

```yaml
  - run: |
      pre-commit run -all-files | tee pre-commit.log
      .github/logToCs.py pre-commit.log pre-commit.xml
  - uses: staabm/annotate-pull-request-from-checkstyle-action@v1
    with:
      files: pre-commit.xml
      notices-as-warnings: true     # optional
```

### Example 2:

```yaml
  - run: |
      pre-commit run --all-files | tee pre-commit.log
  - name: Add results to PR
    if: ${{ always() }}
    run: |
      .github/logToCs.py pre-commit.log | cs2pr
```

## Author(s):

- https://github.com/mdeweerd

## License

MIT License
