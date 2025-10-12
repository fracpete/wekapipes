import argparse
import logging
import traceback

from wp.core import ENV_WP_LOGLEVEL
from wp.registry import available_generators
from wp.tool.run import main_no_jvm as run_main_no_jvm, RUN
from kasperl.api import perform_pipeline_execution, CommandlineParameter, perform_conversion

import weka.core.jvm as jvm

EXEC = "wp-exec"

_logger = logging.getLogger(EXEC)


def start_jvm(parsed: argparse.Namespace):
    """
    Starts the jvm.

    :param parsed: the parsed options
    :type parsed: argparse.Namespace
    """
    _logger.info("Starting JVM")
    jvm.start(
        class_path=parsed.exec_classpath,
        system_cp=parsed.exec_system_classpath,
        max_heap_size=parsed.exec_max_heap,
        packages=parsed.exec_packages,
    )


def stop_jvm(parsed: argparse.Namespace):
    """
    Stops the jvm.

    :param parsed: the parsed options
    :type parsed: argparse.Namespace
    """
    _logger.info("Stopping JVM")
    jvm.stop()


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    params = [
        CommandlineParameter(
            long_opt="--exec_classpath",
            metavar="PATH",
            required=False,
            default=None,
            type=str,
            help="The additional classpath elements to use for the JVM.",
            nargs="*",
        ),
        CommandlineParameter(
            long_opt="--exec_system_classpath",
            required=False,
            action="store_true",
            help="Whether to use the system CLASSPATH as well.",
        ),
        CommandlineParameter(
            long_opt="--exec_packages",
            required=False,
            action="store_true",
            help="Whether to load the installed Weka packages.",
        ),
        CommandlineParameter(
            long_opt="--exec_max_heap",
            metavar="SIZE",
            required=False,
            default=None,
            type=str,
            help="The maximum amount of heap space to allow, e.g., 256m or 2g.",
        ),
    ]

    perform_pipeline_execution(ENV_WP_LOGLEVEL, args, EXEC, None,
                               RUN, run_main_no_jvm, available_generators(), _logger,
                               additional_params=params, pre_exec=start_jvm, post_exec=stop_jvm)


def sys_main() -> int:
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    """
    try:
        main()
        return 0
    except Exception:
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    main()
