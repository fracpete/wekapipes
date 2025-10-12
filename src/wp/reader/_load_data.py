import argparse
from typing import List, Iterable, Union, Optional

from seppl.io import locate_files
from wai.logging import LOGGING_WARNING

from seppl.placeholders import PlaceholderSupporter, placeholder_list
from kasperl.api import Reader
from weka.core.dataset import Instances, Instance
from weka.core.classes import from_commandline, to_commandline
from weka.core.converters import Loader, loader_for_file


class LoadData(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 resume_from: str = None, use_custom_loader: bool = None, custom_loader: str = None,
                 class_index: str = None, incremental: bool = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param resume_from: the file to resume from (glob)
        :type resume_from: str
        :param use_custom_loader: whether to use a custom loader instead of using automatic detection
        :param custom_loader: bool
        :param custom_loader: the custom loader command-line to use
        :type custom_loader: str
        :param class_index: the class index to use (e.g. 1, first, 3, last), ignored if None
        :type class_index: str
        :param incremental: whether to load the data row by row or in one goe
        :type incremental: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.resume_from = resume_from
        self.use_custom_loader = use_custom_loader
        self.custom_loader = custom_loader
        self.class_index = class_index
        self.incremental = incremental
        self._inputs = None
        self._current_input: Optional[Loader] = None
        self._loader = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "load-data"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the dataset and forwards it. Optionally, a custom loader definition can be supplied."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the data file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the data files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--resume_from", type=str, help="Glob expression matching the file to resume from, e.g., '*/012345.arff'", required=False)
        parser.add_argument("-u", "--use_custom_loader", action="store_true", help="Whether to use the supplied custom loader rather than auto-detection.")
        parser.add_argument("-L", "--custom_loader", metavar="CMDLINE", type=str, default=None, help="The command-line of the custom loader to use (classname + options).", required=False)
        parser.add_argument("-c", "--class_index", type=str, default=None, help="The class index to use on the data, e.g., 1, first, 3, last.", required=False)
        parser.add_argument("--incremental", action="store_true", help="Whether to load the data row by row rather than in one go.")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.source = ns.input
        self.source_list = ns.input_list
        self.resume_from = ns.resume_from
        self.use_custom_loader = ns.use_custom_loader
        self.custom_loader = ns.custom_loader
        self.class_index = ns.class_index
        self.incremental = ns.incremental

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        if self.incremental:
            return [Instance]
        else:
            return [Instances]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.use_custom_loader is None:
            self.use_custom_loader = False
        if self.use_custom_loader:
            if self.custom_loader is None:
                raise Exception("No custom loader command-lined specified!")
            self.logger().info("Instantiating custom loader: %s" % self.custom_loader)
            self._loader = from_commandline(self.custom_loader, classname="weka.core.converters.Loader")
        if self.incremental is None:
            self.incremental = False
        self._inputs = None

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        if self._inputs is None:
            self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, resume_from=self.resume_from)
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))
        if not self.use_custom_loader:
            self._loader = loader_for_file(self._current_input)
            if self._loader is None:
                raise Exception("Failed to determine loader for file: %s" % self._current_input)
            self.logger().info("Auto-detected loader: %s" % to_commandline(self._loader))
        if self.incremental:
            self._loader.load_file(self._current_input, incremental=True, class_index=self.class_index)
            for inst in self._loader:
                yield inst
        else:
            data = self._loader.load_file(self._current_input, incremental=False, class_index=self.class_index)
            yield data

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return (self._inputs is not None) and len(self._inputs) == 0
