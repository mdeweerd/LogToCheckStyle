#!/usr/bin/python3
"""
Convert a log to CheckStyle format.

Url: https://github.com/mdeweerd/LogToCheckStyle

The log can then be used for generating annotations in a github action.

Note: this script is very young and "quick and dirty".
      Patterns can be added to "PATTERNS" to match more messages.

# Examples

Assumes that logToCs.py is available as .github/logToCs.py.

## Example 1:


```yaml
      - run: |
          pre-commit run -all-files | tee pre-commit.log
          .github/logToCs.py pre-commit.log pre-commit.xml
      - uses: staabm/annotate-pull-request-from-checkstyle-action@v1
        with:
          files: pre-commit.xml
          notices-as-warnings: true # optional
```

## Example 2:


```yaml
      - run: |
          pre-commit run --all-files | tee pre-commit.log
      - name: Add results to PR
        if: ${{ always() }}
        run: |
          .github/logToCs.py pre-commit.log | cs2pr
```

Author(s):
  - https://github.com/mdeweerd

License: MIT License

"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET


def convert_to_checkstyle(messages):
    root = ET.Element("checkstyle")
    for message in messages:
        fields = parse_message(message)
        if fields:
            add_error_entry(root, **fields)
    return ET.tostring(root, encoding="utf-8").decode("utf-8")


ANY_REGEX = r".*?"
FILE_REGEX = r"\s*(?P<file_name>\S.*?)\s*?"
LINE_REGEX = r"\s*(?P<line>\d+?)\s*?"
COLUMN_REGEX = r"\s*(?P<column>\d+?)\s*?"
SEVERITY_REGEX = r"\s*(?P<severity>error|warning|notice)\s*?"
MSG_REGEX = r"\s*(?P<message>.+?)\s*?"
# cpplint confidence index
CONFIDENCE_REGEX = r"\s*\[(?P<confidence>\d+)\]\s*?"


# List of message patterns, add more specific patterns earlier in the list
# Creating patterns by using constants makes them easier to define and read.
PATTERNS = [
    re.compile(f"^{FILE_REGEX}:{LINE_REGEX}:{COLUMN_REGEX}:{MSG_REGEX}$"),
    # Cpplint default output:
    #           '%s:%s:  %s  [%s] [%d]\n'
    #   % (filename, linenum, message, category, confidence)
    re.compile(f"^{FILE_REGEX}:{LINE_REGEX}:{MSG_REGEX}{CONFIDENCE_REGEX}$"),
    # re.compile(f"^{ANY_REGEX}:{LINE_REGEX}:{MSG_REGEX}$"),
]

# Severities available in CodeSniffer report format
SEVERITY_NOTICE = "notice"
SEVERITY_WARNING = "warning"
SEVERITY_ERROR = "error"


def parse_message(message):
    """
    Parse message until it matches a pattern.

    Returns the fields in a dict.
    """
    for pattern in PATTERNS:
        m = pattern.match(message)
        if not m:
            continue
        result = m.groupdict()
        if len(result) == 0:
            continue

        if "confidence" in result:
            # Convert confidence level of cpplint
            # to warning, etc.
            confidence = int(result["confidence"])
            del result["confidence"]

            if confidence <= 1:
                severity = SEVERITY_NOTICE
            elif confidence >= 5:
                severity = SEVERITY_ERROR
            else:
                severity = SEVERITY_WARNING
            result["severity"] = severity

        if "severity" not in result:
            result["severity"] = SEVERITY_ERROR
        else:
            result["severity"] = result["severity"].lower()

        return result

    # Nothing matched
    return None


def add_error_entry(
    root,
    severity,
    file_name,
    line=None,
    column=None,
    message=None,
    source=None,
):
    file_element = find_or_create_file_element(root, file_name)
    error_element = ET.SubElement(file_element, "error")
    error_element.set("severity", severity)
    if line:
        error_element.set("line", line)
    if column:
        error_element.set("column", column)
    if message:
        error_element.set("message", message)
    if source:
        # To verify if this is a valid attribute
        error_element.set("source", source)


def find_or_create_file_element(root, file_name):
    for file_element in root.findall("file"):
        if file_element.get("name") == file_name:
            return file_element
    file_element = ET.SubElement(root, "file")
    file_element.set("name", file_name)
    return file_element


def main():
    parser = argparse.ArgumentParser(
        description="Convert messages to Checkstyle XML format."
    )
    parser.add_argument(
        "input", help="Input file. Use '-' for stdin.", nargs="?", default="-"
    )
    parser.add_argument(
        "output",
        help="Output file. Use '-' for stdout.",
        nargs="?",
        default="-",
    )
    parser.add_argument(
        "-i",
        "--input-named",
        help="Named input file. Overrides positional input.",
    )
    parser.add_argument(
        "-o",
        "--output-named",
        help="Named output file. Overrides positional output.",
    )

    args = parser.parse_args()

    if args.input == "-" and args.input_named:
        with open(args.input_named) as input_file:
            messages = input_file.readlines()
    elif args.input != "-":
        with open(args.input) as input_file:
            messages = input_file.readlines()
    else:
        messages = sys.stdin.readlines()

    checkstyle_xml = convert_to_checkstyle(messages)

    if args.output == "-" and args.output_named:
        with open(args.output_named, "w") as output_file:
            output_file.write(checkstyle_xml)
    elif args.output != "-":
        with open(args.output, "w") as output_file:
            output_file.write(checkstyle_xml)
    else:
        print(checkstyle_xml)


if __name__ == "__main__":
    main()
