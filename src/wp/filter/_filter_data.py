import argparse
from typing import List, Optional

from kasperl.api import make_list
from seppl.io import BatchFilter
from seppl.placeholders import placeholder_help, PlaceholderSupporter
from wai.logging import LOGGING_WARNING
from weka.core.classes import from_commandline, to_commandline
from weka.core.dataset import Instances, Instance
from weka.filters import Filter


class FilterData(BatchFilter, PlaceholderSupporter):
    """
    Filters the data coming through.
    """

    def __init__(self, filter_cmdln: str = None, always_initialize: bool = None,
                 load_from: str = None, save_to: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param filter_cmdln: the commandline of the filter to use (classname + options)
        :type filter_cmdln: str
        :param always_initialize: whether to initialize the filter with each data item passing through or only once
        :type always_initialize: bool
        :param load_from: the (optional) file to load the serialized filter from
        :type load_from: str
        :param save_to: the (optional) file to save the initialized filter to
        :type save_to: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.filter_cmdln = filter_cmdln
        self.always_initialize = always_initialize
        self.load_from = load_from
        self.save_to = save_to
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
        parser.add_argument("-f", "--filter", metavar="CMDLINE", type=str, help="The command-line of the filter to use (classname + options).", default=None, required=False)
        parser.add_argument("-a", "--always_initialize", action="store_true", help="Whether to initialize the filter with each data item passing through.")
        parser.add_argument("-L", "--load_from", metavar="FILE", type=str, help="The file to load the serialized filter from. " + placeholder_help(obj=self), default=None, required=False)
        parser.add_argument("-S", "--save_to", metavar="FILE", type=str, help="The file to save the initialized filter to. " + placeholder_help(obj=self), default=None, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.filter_cmdln = ns.filter
        self.always_initialize = ns.always_initialize
        self.load_from = ns.load_from
        self.save_to = ns.save_to

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._first = True
        if self.always_initialize is None:
            self.always_initialize = False

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        data = make_list(data)

        # setting up filter
        if self._first:
            if self.filter_cmdln is not None:
                self.logger().info("Instantiating filter: %s" % self.filter_cmdln)
                self._filter = from_commandline(self.filter_cmdln, classname="weka.filters.Filter")
            elif self.load_from is not None:
                path = self.session.expand_placeholders(self.load_from)
                self.logger().info("Loading filter from: %s" % path)
                self._filter = Filter.deserialize(path)
                self.logger().info("Loaded filter: %s" % to_commandline(self._filter))
            else:
                raise Exception("Either a filter command-line or a serialized file must be specified!")

        # initialize filter
        if self._first or self.always_initialize:
            if isinstance(data[0], Instances):
                self.logger().info("Initializing filter with data: %s" % data[0].relationname)
                self._filter.inputformat(data[0])
            elif isinstance(data[0], Instance):
                self.logger().info("Initializing filter with data: %s" % data[0].dataset.relationname)
                self._filter.inputformat(data[0].dataset)
            else:
                raise Exception("Unhandled data: %s" % str(type(data)))

        # filter data
        result = []
        for item in data:
            result.append(self._filter.filter(item))

        # save filter?
        if self.save_to is not None:
            path = self.session.expand_placeholders(self.save_to)
            self.logger().info("Saving filter to: %s" % path)
            self._filter.serialize(path)

        self._first = False

        return result
