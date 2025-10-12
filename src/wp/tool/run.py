import traceback
from typing import List

from wp.core import ENV_WP_LOGLEVEL
from wp.help import generate_plugin_usage
from wp.registry import available_readers, available_filters, available_writers, REGISTRY
from seppl import Session
from kasperl.api import perform_conversion, CommandlineParameter

import weka.core.jvm as jvm


RUN = "wp-run"
DESCRIPTION = "Tool for running Weka pipelines."


def start_jvm(session: Session):
    """
    Starts the jvm.

    :param session: the current session object
    :type session: Session
    """
    session.logger.info("Starting JVM")
    jvm.start(
        class_path=session.options.classpath,
        system_cp=session.options.system_classpath,
        max_heap_size=session.options.max_heap,
        packages=session.options.packages,
    )


def stop_jvm(session: Session):
    """
    Stops the jvm.

    :param session: the current session object
    :type session: Session
    """
    session.logger.info("Stopping JVM")
    jvm.stop()


def additional_params() -> List[CommandlineParameter]:
    """
    Returns the list of parameters to use.

    :return: the list of parameters
    :rtype: list
    """
    return [
        CommandlineParameter(
            short_opt="-c",
            long_opt="--classpath",
            metavar="PATH",
            required=False,
            default=None,
            type=str,
            help="The additional classpath elements to use for the JVM.",
            nargs="*",
        ),
        CommandlineParameter(
            short_opt="-s",
            long_opt="--system_classpath",
            required=False,
            action="store_true",
            help="Whether to use the system CLASSPATH as well.",
        ),
        CommandlineParameter(
            short_opt="-p",
            long_opt="--packages",
            required=False,
            action="store_true",
            help="Whether to load the installed Weka packages.",
        ),
        CommandlineParameter(
            short_opt="-M",
            long_opt="--max_heap",
            metavar="SIZE",
            required=False,
            default=None,
            type=str,
            help="The maximum amount of heap space to allow, e.g., 256m or 2g.",
        ),
    ]


def main(args=None):
    perform_conversion(
        ENV_WP_LOGLEVEL, args, RUN, DESCRIPTION,
        available_readers(), available_filters(), available_writers(),
        aliases=REGISTRY.all_aliases, require_reader=True, require_writer=False,
        generate_plugin_usage=generate_plugin_usage, additional_params=additional_params(),
        pre_initialize=start_jvm, post_finalize=stop_jvm)


def main_no_jvm(args=None):
    perform_conversion(
        ENV_WP_LOGLEVEL, args, RUN, DESCRIPTION,
        available_readers(), available_filters(), available_writers(),
        aliases=REGISTRY.all_aliases, require_reader=True, require_writer=False,
        generate_plugin_usage=generate_plugin_usage, additional_params=additional_params(),
        pre_initialize=None, post_finalize=None)


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
