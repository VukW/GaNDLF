import os.path
import pytest
from click.testing import CliRunner

from GANDLF.entrypoints.anonymizer import new_way, old_way, _anonymize_images

from testing.entrypoints import cli_runner, TestCase, run_test_case, TempFileSystem

# this function would be replaced with `mock_real_command` replica
MOCK_PATH = "GANDLF.entrypoints.anonymizer.run_anonymizer"
OLD_SCRIPT_NAME = "gandlf_anonymizer"

# these files would be either created temporarily for test execution,
# or we ensure they do not exist
test_file_system = {
    "input/": "dir",
    "config.yaml": {"content": "foo: bar"},
    "output/": "dir",
    "path_na/": "na",
    "output.csv": {"content": "col1,col2\n123,456\n"},
}
test_cases = [
    TestCase(
        should_succeed=True,
        new_way_lines=[
            # full command
            "--input-dir . --config config.yaml --modality rad --output-file output/",
            # tests short arg aliases
            "-i . -c config.yaml -m rad -o  output/",
            # tests modality has default value
            "-i . -c config.yaml -o  output/",
        ],
        old_way_lines=[
            "--inputDir . --config config.yaml --modality rad --outputFile output/",
            "-i . -c config.yaml -m rad -o  output/",
            "-i . -c config.yaml -o output/",
        ],
        wrapper_args={
            "input_dir": ".",
            "output_file": "output/",
            "config_path": "config.yaml",
            "modality": "rad"
        },
        expected_args={
            "input_path": os.path.normpath("."),
            "output_path": os.path.normpath("output/"),
            "parameters": {"foo": "bar"},
            "modality": "rad"
        }
    ),
    TestCase(
        should_succeed=True,
        new_way_lines=[
            # tests that config is optional, and that output may not exist
            "-i . -o path_na",
        ],
        old_way_lines=[
            "-i . -o path_na",
        ],
        wrapper_args={
            "input_dir": ".",
            "output_file": "path_na",
            "config_path": None,
            "modality": "rad"
        },
        expected_args={
            "input_path": os.path.normpath("."),
            "output_path": os.path.normpath("path_na"),
            "parameters": None,
            "modality": "rad"
        }
    ),
    TestCase(
        should_succeed=True,
        new_way_lines=[
            # tests that output may be an existing file
            "-i . -o output.csv",
        ],
        old_way_lines=[
            "-i . -o output.csv",
        ],
        wrapper_args={
            "input_dir": ".",
            "output_file": "output.csv",
            "config_path": None,
            "modality": "rad"
        },
        expected_args={
            "input_path": os.path.normpath("."),
            "output_path": os.path.normpath("output.csv"),
            "parameters": None,
            "modality": "rad"
        }
    ),
    TestCase(
        should_succeed=True,
        new_way_lines=[
            # tests that modality 'histo' is supported also
            "-i . -m histo -o output.csv",
        ],
        old_way_lines=[
            "-i . -m histo -o output.csv",
        ],
        wrapper_args={
            "input_dir": ".",
            "output_file": "output.csv",
            "config_path": None,
            "modality": "histo"
        },
        expected_args={
            "input_path": os.path.normpath("."),
            "output_path": os.path.normpath("output.csv"),
            "parameters": None,
            "modality": "histo"
        }
    ),
    TestCase(
        should_succeed=False,
        new_way_lines=[
            # tests that input should exist
            "-i path_na -o output.csv",
            # tests that input is required
            "-o output.csv",
            # tests that config file, if provided, should exist
            "-i . -c path_na -o output.csv",
            # tests that modality cannot take arbitrary values
            "-i . -m fake_modality -o output.csv",
        ],
        old_way_lines=[
            # "-i path_na -o output.csv", # <- in old way input is not required to exist
            "-o output.csv",
            # "-i . -c path_na -o output.csv",  # <- in old way if config file does not exist, it just skipped silently
            # "-i . -m fake_modality -o output.csv",  # <- in old way there is no such a validation in cli part
        ],
    )
]


@pytest.mark.parametrize("case", test_cases)
def test_case(cli_runner: CliRunner, case: TestCase):
    with TempFileSystem(test_file_system):
        run_test_case(
            cli_runner=cli_runner,
            case=case,
            real_code_function_path=MOCK_PATH,
            new_way=new_way,
            old_way=old_way,
            old_script_name=OLD_SCRIPT_NAME,
            wrapper_func=_anonymize_images
        )
