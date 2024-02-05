#!/bin/python3
"""
Test log files in IN path versus expected outputs.
"""
import os
import subprocess
import sys
from glob import glob

import pytest


# Function to get the list of test files in the 'IN' directory
def get_test_files(in_directory="IN"):
    """
    Read all test input files from given directory
    """
    return glob(os.path.join(in_directory, "*.log"))


# Function to run the program and capture stdout to a file
def run_program(input_file, xml_file, output_file):
    """
    Run our program under test
    """
    # Set the environment variable before running the subprocess
    os.environ["GITHUB_ACTIONS"] = "true"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(script_dir, "..", "logToCs.py")

    command = [script, input_file, xml_file]
    print(" ".join(command))
    with open(output_file, "wb") as out_file:
        subprocess.run(command, stdout=out_file, check=True)


# Function to compare the program output with expected output
def test_program_output():
    """
    Test our program using the files in directory `IN`
    """
    # pylint: disable=too-many-locals
    script_dir = os.path.dirname(os.path.abspath(__file__))
    in_directory = os.path.join(script_dir, "IN")
    out_directory = os.path.join(script_dir, "OUT")
    os.makedirs(out_directory, exist_ok=True)

    for input_file in get_test_files(in_directory):
        log_file = input_file
        expected_xml_file = input_file.replace(".log", ".xml")
        expected_txt_file = input_file.replace(".log", ".txt")

        xml_file = os.path.join(
            out_directory, os.path.basename(expected_xml_file)
        )
        txt_file = os.path.join(
            out_directory, os.path.basename(expected_txt_file)
        )

        file_paths = [
            [expected_xml_file, xml_file],
            [expected_txt_file, txt_file],
        ]

        # Run the program and capture stdout to a file
        run_program(log_file, xml_file, txt_file)

        for expected_fn, actual_fn in file_paths:
            # Read the actual and expected outputs
            with open(actual_fn, "rb") as actual_file:
                actual_output = actual_file.read()

            with open(expected_fn, "rb") as expected_file:
                expected_output = expected_file.read()

            # Compare the actual and expected outputs
            assert (
                actual_output == expected_output
            ), f"Contents for {actual_fn} does not match {expected_fn}"
            print(
                "Comparison successful for files: "
                f"{actual_fn} and {expected_fn}"
            )
            # captured = capsys.readouterr()
            # print(captured.out)


# pylint: disable=unused-argument
def pytest_sessionfinish(session, exitstatus):
    """
    Cleanup after tests
    """
    # os.remove('temp_output.txt')


if __name__ == "__main__":
    # Run the tests using pytest
    # test_program_output()
    exit_code = pytest.main([__file__])
    sys.exit(exit_code)
