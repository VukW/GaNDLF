import pytest
from click.testing import CliRunner

from GANDLF.entrypoints.recoverConfig import new_way, old_way, _recover_config
from testing.entrypoints import cli_runner, TestCase, run_test_case, TmpDire, TmpFile, TmpNoEx

# This function is a place where a real logic is executed.
# For tests, we replace it with mock up, and check if this function is called
# with proper args for different cli commands
MOCK_PATH = "GANDLF.entrypoints.recoverConfig.recover_config"
OLD_SCRIPT_NAME = "gandlf_preprocess"

# these files would be either created temporarily for test execution,
# or we ensure they do not exist
test_file_system = [
    TmpDire("model/"),
    TmpFile("model.file"),
    TmpFile("output.yaml"),
    TmpDire("output/"),
    TmpNoEx("output_na.yaml"),
    TmpNoEx("path_na"),
]
test_cases = [
    TestCase(
        should_succeed=True,
        new_way_lines=[
            # full command
            # also checks --mlcube is optional
            "--model-dir model/ --output-file output.yaml",
            # tests short arg aliases
            "-m model/ -o output.yaml",
        ],
        old_way_lines=[
            "--modeldir model/ --outputFile output.yaml",
            "-m model/ -o output.yaml",
        ],
        wrapper_args={
            "model_dir": "model/",
            "mlcube": False,
            "output_file": "output.yaml"
        },
        expected_args={
            "modelDir": "model/",
            "outputFile": "output.yaml",
        }
    ),
    TestCase(
        should_succeed=True,
        new_way_lines=[
            # mlcube way
            "--mlcube --output-file output.yaml",
            # tests short arg aliases
            "-c -o output.yaml",
        ],
        old_way_lines=[
            "--mlcube true -o output.yaml",
            "-c true -o output.yaml",
        ],
        wrapper_args={
            "model_dir": None,
            "mlcube": True,
            "output_file": "output.yaml"
        },
        expected_args={
            "modelDir": "/embedded_model/",
            "outputFile": "output.yaml",
        }
    ),
    TestCase(
        should_succeed=True,
        new_way_lines=[
            # tests model is ignored when mlcube is passed
            "-m model/ -c -o output.yaml",
        ],
        old_way_lines=[
            "-m model/ -c true -o output.yaml",
        ],
        wrapper_args={
            "model_dir": "model/",
            "mlcube": True,
            "output_file": "output.yaml"
        },
        expected_args={
            "modelDir": "/embedded_model/",
            "outputFile": "output.yaml",
        }
    ),
    TestCase(
        should_succeed=True,
        new_way_lines=[
            # tests output may not exist
            "-m model/ -o output_na.yaml",
        ],
        old_way_lines=[
            "-m model/ -o output_na.yaml",
        ],
        wrapper_args={
            "model_dir": "model/",
            "mlcube": False,
            "output_file": "output_na.yaml"
        },
        expected_args={
            "modelDir": "model/",
            "outputFile": "output_na.yaml",
        }
    ),
    TestCase(
        should_succeed=False,
        new_way_lines=[
            # output is required
            "-m model/",
            "-c",
            # model if passed should point to existing dir
            "-m path_na -o output.yaml",
            "-m model.file -o output.yaml",
            # output should point to file, not dir
            "-m model/ -o output/",
        ],
        old_way_lines=[
            # output is required
            "-m model/",  # no check in old way
            "-c",  # no check in old way
            # model if passed should point to existing dir
            # "-m path_na -o output.yaml",  # no check in old way
            # "-m model.file -o output.yaml",  # no check in old way
            # output should point to file, not dir
            # "-m model/ -o output/",  # no check in old way
        ]
    ),
]


@pytest.mark.parametrize("case", test_cases)
def test_case(cli_runner: CliRunner, case: TestCase):
    run_test_case(
        cli_runner=cli_runner,
        file_system_config=test_file_system,
        case=case,
        real_code_function_path=MOCK_PATH,
        new_way=new_way,
        old_way=old_way,
        old_script_name=OLD_SCRIPT_NAME,
        wrapper_func=_recover_config,
        patched_return_value=True
    )
