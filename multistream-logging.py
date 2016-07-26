"""
At work I had this requirement: log messages and warnings to stdout, errors
and above to stderr.
This is one way to achieve this with a logging.Filter-like function.
"""
import sys
import logging


def upper_bound(level):
    """Filter logrecords by level.

    Allow only records with level number LE to level.
    """
    def upper_bound_filter(log_record):
        return int(log_record.levelno <= level)

    return upper_bound_filter

logger = logging.getLogger('default')
logger.setLevel(logging.INFO)

# Handles levels ERROR and up
h1 = logging.StreamHandler(sys.stderr)
h1.setLevel(logging.ERROR)
h1.setFormatter(logging.Formatter("error handler: %(message)s"))

# Handler for a window of levels between INFO and WARNING
h2 = logging.StreamHandler(sys.stdout)
h2.setLevel(logging.INFO)
h2.setFormatter(logging.Formatter("info handler: %(message)s"))
h2.addFilter(upper_bound(logging.WARNING))

# Order in which handlers get added doesn't matter
logger.addHandler(h2)
logger.addHandler(h1)

# test different levels
logger.info("just a message")
logger.warning("beware!")
logger.error('panic! panic!')
logger.error('GÖTTERDÄMERUNG!!!')
