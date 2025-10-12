import argparse
from typing import List, Optional

from kasperl.api import make_list, StreamWriter
from seppl.placeholders import InputBasedPlaceholderSupporter, placeholder_list
from wai.logging import LOGGING_WARNING
from weka.core.classes import from_commandline, to_commandline
from weka.core.converters import saver_for_file, Saver
from weka.core.dataset import Instances


class SaveData(StreamWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_file: str = None, use_custom_saver: bool = None, custom_saver: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_file: the file to write to
        :type output_file: str
        :param use_custom_saver: whether to use a custom saver rather than using autodetect
        :type use_custom_saver: bool
        :param custom_saver: the custom saver to use (classname + options)
        :type custom_saver: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file
        self.use_custom_saver = use_custom_saver
        self.custom_saver = custom_saver
        self._saver: Optional[Saver] = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "save-data"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the incoming data to disk."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output_file", metavar="FILE", type=str, help="The file to write the data to; " + placeholder_list(obj=self), required=False)
        parser.add_argument("-u", "--use_custom_saver", action="store_true", help="Whether to use a custom saver instead of using auto-detect based on the file name.")
        parser.add_argument("-c", "--custom_saver", metavar="CMDLINE", type=str, help="The command-line of the saver to use (classname + options).", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output_file
        self.use_custom_saver = ns.use_custom_saver
        self.custom_saver = ns.custom_saver

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.use_custom_saver is None:
            self.use_custom_saver = False
        if self.use_custom_saver:
            if self.custom_saver is None:
                raise Exception("No custom saver specified!")
            self.logger().info("Instantiating custom saver: %s" % self.custom_saver)
            self._saver = from_commandline(self.custom_saver)
        else:
            self._saver = saver_for_file(self.output_file)
            if self._saver is None:
                raise Exception("Failed to determine saver for file: %s" % self.output_file)
            self.logger().info("Auto-detected saver: %s" % to_commandline(self._saver))

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [Instances]

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            output_file = self.session.expand_placeholders(self.output_file)
            self._saver.save_file(item, output_file)
