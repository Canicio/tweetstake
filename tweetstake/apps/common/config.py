import logging.config
import coloredlogs
from typing import Dict
from tweetstake.apps.common.util import Constants
from tweetstake.apps.common.decorators import singleton_to_logging


@singleton_to_logging
class Log(object):

    def __init__(self) -> None:
        level_styles: Dict = dict(
            debug=dict(color='white'),
            info=dict(color='cyan'),
            verbose=dict(color='blue'),
            warning=dict(color='yellow'),
            error=dict(color='red'),
            critical=dict(color='red', bold=coloredlogs.CAN_USE_BOLD_FONT)
        )
        self.logger = logging.getLogger('root')
        coloredlogs.install(level='DEBUG', fmt=Constants.FORMAT_LOGGING_BASE, logger=self.logger,
                            level_styles=level_styles)
