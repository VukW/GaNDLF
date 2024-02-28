#!usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import argparse
import ast
import sys
import traceback
from typing import Optional

from deprecated import deprecated
import click

from GANDLF import version
from GANDLF.cli import main_run, copyrightMessage
from GANDLF.entrypoints import append_copyright_to_help


def _run(config: str,
         input_data: str,
         train_flag: bool,
         model_dir: str,
         device: str,
         reset_flag: bool,
         resume_flag: bool,
         output_path: Optional[str]
         ):
    if os.path.isdir(input_data):
        # Is this a fine assumption to make?
        # Medperf models receive the data generated by the data preparator mlcube
        # We can therefore ensure the output of that mlcube contains a data.csv file
        filename = "data.csv"
        input_data = os.path.join(input_data, filename)

    if not train_flag:
        # TODO: print a warning if any of these flags is activated. They are not available for train mode
        #  Maybe user misconfigured the command.
        # if inference mode, then no need to check for reset/resume
        reset_flag, resume_flag = False, False

    if reset_flag and resume_flag:
        logging.warning(
            "'reset' and 'resume' are mutually exclusive; 'resume' will be used."
        )
        reset_flag = False

    # TODO: check that is output_path is not passed in training mode;
    #  maybe user misconfigured the command

    logging.debug(f'{config=}')
    logging.debug(f'{input_data=}')
    logging.debug(f'{train_flag=}')
    logging.debug(f'{model_dir=}')
    logging.debug(f'{device=}')
    logging.debug(f'{reset_flag=}')
    logging.debug(f'{resume_flag=}')
    logging.debug(f'{output_path=}')

    try:
        main_run(
            data_csv=input_data,
            config_file=config,
            model_dir=model_dir,
            train_mode=train_flag,
            device=device,
            resume=resume_flag,
            reset=reset_flag,
            output_dir=output_path,
        )
    except Exception:
        # TODO: why so? Why not just default way when exception is printed
        #  and process exits with code 1 automatically?
        sys.exit("ERROR: " + traceback.format_exc())
    print("Finished.")


@click.command()
@click.option('--config', '-c',
              required=True,
              help="The configuration file (contains all the information related to the training/inference session)",
              type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--input-data', '-i',  # TODO: renamed from --inputdata / --data_path
              required=True,
              type=str,
              help="Data CSV file that is used for training/inference; "
                   "can also take comma-separated training-validation pre-split CSVs")
@click.option('--train/--infer', '-t/--infer',
              required=True,  # TODO: what if we make infer as default behavior if no param is passed?
              help="If we run training or inference; for inference, "
                   "there needs to be a compatible model saved in '-modeldir'")
@click.option('--model-dir', '-m',
              type=click.Path(exists=True, file_okay=False, dir_okay=True),
              required=True,
              help="Training: Output directory to save intermediate files and model weights; "
                   "inference: location of previous training session output")
@click.option('--device', '-d',
              default='cuda',
              type=click.Choice(['cuda', 'cpu']),
              required=True,  # FIXME: either keep default value, or set required flag
              help="Device to perform requested session on 'cpu' or 'cuda'; "
                   "for cuda, ensure CUDA_VISIBLE_DEVICES env var is set")
@click.option('--reset', '-rt',
              is_flag=True,
              help="Completely resets the previous run by deleting 'modeldir'")
@click.option('--resume', '-rm',
              is_flag=True,
              help="Resume previous training by only keeping model dict in 'modeldir'")
@click.option('--output-path', '-o',  # TODO: renamed from --outputdir / --output_path
              type=click.Path(),
              help="Location to save the output of the inference session. Not used for training.")
@click.option("--raw-input", "-raw-input",  # TODO: renamed from --rawinput/-rawinput
              is_flag=True,
              hidden=True)
@append_copyright_to_help
def new_way(config: str,
            input_data: str,
            train: bool,
            model_dir: str,
            device: str,
            reset: bool,
            resume: bool,
            output_path: str,
            raw_input: bool):
    """Semantic segmentation, regression, and classification for medical images using Deep Learning."""
    _run(config=config,
         input_data=input_data,
         train_flag=train,
         model_dir=model_dir,
         device=device,
         reset_flag=reset,
         resume_flag=resume,
         output_path=output_path)


@deprecated("This is a deprecated way of running GanDLF. Please, use `gandlf run` cli command " +
            "instead of `gandlf_run`. Note that in new CLI tool some params were renamed or changed its behavior:\n" +
            "  --parameters_file to --config\n" +
            "  --inputdata/--data_path to --input-data\n" +
            "  --train changed its behavior: instead of `--train True/False` pass `--train/--infer`\n" +
            "  --modeldir to --model-dir; also, now it is required\n" +
            "  --reset is flag now with default False value if not passed\n" +
            "  --resume is flag now with default False value if not passed\n" +
            "  --outputdir/--output_path to --output-path; in training mode, use --model-dir instead\n" +
            "  --version removed; use `gandlf --version` instead\n" +
            "`gandlf_run` script would be deprecated soon.")
def old_way():
    parser = argparse.ArgumentParser(
        prog="GANDLF",
        formatter_class=argparse.RawTextHelpFormatter,
        description="Semantic segmentation, regression, and classification for medical images using Deep Learning.\n\n"
                    + copyrightMessage,
    )
    parser.add_argument(
        "-c",
        "--config",
        "--parameters_file",
        metavar="",
        type=str,
        required=True,
        help="The configuration file (contains all the information related to the training/inference session)",
    )
    parser.add_argument(
        "-i",
        "--inputdata",
        "--data_path",
        metavar="",
        type=str,
        required=True,
        help="Data CSV file that is used for training/inference; can also take comma-separated training-validation pre-split CSVs",
    )
    parser.add_argument(
        "-t",
        "--train",
        metavar="",
        type=ast.literal_eval,
        required=True,
        help="True: training and False: inference; for inference, there needs to be a compatible model saved in '-modeldir'",
    )
    parser.add_argument(
        "-m",
        "--modeldir",
        metavar="",
        type=str,
        help="Training: Output directory to save intermediate files and model weights; inference: location of previous training session output",
    )
    parser.add_argument(
        "-d",
        "--device",
        default="cuda",
        metavar="",
        type=str,
        required=True,
        help="Device to perform requested session on 'cpu' or 'cuda'; for cuda, ensure CUDA_VISIBLE_DEVICES env var is set",
    )
    parser.add_argument(
        "-rt",
        "--reset",
        metavar="",
        default=False,
        type=ast.literal_eval,
        help="Completely resets the previous run by deleting 'modeldir'",
    )
    parser.add_argument(
        "-rm",
        "--resume",
        metavar="",
        default=False,
        type=ast.literal_eval,
        help="Resume previous training by only keeping model dict in 'modeldir'",
    )
    parser.add_argument(
        "-o",
        "--outputdir",
        "--output_path",
        metavar="",
        type=str,
        help="Location to save the output of the inference session. Not used for training.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s v{}".format(version) + "\n\n" + copyrightMessage,
        help="Show program's version number and exit.",
    )

    # This is a dummy argument that exists to trigger MLCube mounting requirements.
    # Do not remove.
    parser.add_argument("-rawinput", "--rawinput", help=argparse.SUPPRESS)

    args = parser.parse_args()
    if args.modeldir is None and args.outputdir:
        args.modeldir = args.outputdir

    assert args.modeldir is not None, "Missing required parameter: modeldir"

    # config file should always be present
    assert os.path.isfile(args.config), "Configuration file not found!"

    _run(
        config=args.config,
        input_data=args.inputdata,
        train_flag=args.train,
        model_dir=args.modeldir,
        device=args.device,
        reset_flag=args.reset,
        resume_flag=args.resume,
        output_path=args.outputdir
    )


if __name__ == "__main__":
    old_way()
