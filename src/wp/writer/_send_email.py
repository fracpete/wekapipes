import os
from email.mime.multipart import MIMEMultipart

from kasperl.writer import SendEmail as KSendEmail


class SendEmail(KSendEmail):

    def _attach_item(self, message: MIMEMultipart, item) -> bool:
        """
        Attaches the file to the message.

        :param message: the message to attach to
        :type message: MIMEMultipart
        :param item: the path of the file to attach
        :return: whether data type has handled
        :rtype: bool
        """
        if isinstance(item, str):
            self.logger().info("Reading data from: %s" % item)
            with open(item, "rb") as fp:
                data = fp.read()
            self._attach_data(message, data, os.path.basename(item))
            return True
        else:
            return False
