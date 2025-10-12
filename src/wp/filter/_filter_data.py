import argparse
from typing import List, Optional

from kasperl.api import make_list
from seppl.io import BatchFilter
from wai.logging import LOGGING_WARNING
from weka.core.classes import from_commandline
from weka.core.dataset import Instances, Instance
from weka.filters import Filter


class FilterData(BatchFilter):
    """
    Filters the data coming through.
    """

    def __init__(self, filter_cmdln: str = None, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param filter_cmdln: the commandline of the filter to use (classname + options)
        :type filter_cmdln: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.filter_cmdln = filter_cmdln
        self._filter: Optional[Filter] = None
        self._first = True

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "filter-data"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Filters the data coming through."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [Instances, Instance]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [Instances, Instance]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-f", "--filter", metavar="CMDLINE", type=str, help="The command-line of the filter to use (classname + options).", default=None, required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.filter_cmdln = ns.filter

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self.logger().info("Instantiating filter: %s" % self.filter_cmdln)
        self._filter = from_commandline(self.filter_cmdln, classname="weka.filters.Filter")
        self._first = True

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        data = make_list(data)

        # initialize filter
        if self._first:
            if isinstance(data[0], Instances):
                self._filter.inputformat(data[0])
            elif isinstance(data[0], Instance):
                self._filter.inputformat(data[0].dataset)
            else:
                raise Exception("Unhandled data: %s" % str(type(data)))

        # filter data
        result = []
        for item in data:
            result.append(self._filter.filter(item))

        return result
