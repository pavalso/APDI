"""
This module provides logging functionality for APDI.
"""

import logging


def get_logger() -> logging.Logger:
    """
    Get the logger for APDI.

    Returns:
        logging.Logger: The logger for APDI.
    """
    _logger = logging.getLogger("APDI")
    _logger.setLevel(logging.DEBUG)

    _handler = logging.StreamHandler()
    _handler.setLevel(logging.DEBUG)

    _formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    _handler.setFormatter(_formatter)

    _logger.addHandler(_handler)

    return _logger
