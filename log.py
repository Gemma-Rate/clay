"""Classes and functions for logging"""
import logging
import functools
import os


def log_setup(logfile_name = 'better_writing_log', logfile_loc = False,
              loglevel = logging.DEBUG):
    """
    Set up logger.
    """
    logger = logging.getLogger("debug-tracking")
    # Make logger object.

    if logfile_loc is False:
        # Place logfile in cwd.
        location = os.getcwd()
    else:
        location = logfile_loc

    file_output = logging.FileHandler(location+'\\'+logfile_name+'.log',
                                      mode='w')
    file_output.setLevel(loglevel)
    logger.addHandler(file_output)
    # Set file output.

    logger.setLevel(loglevel)


def log_function(fun):
    """
    Decorator to add logging to functions.

    Parameters
    ----------
    fun : python function object
        Function input.

    """
    @functools.wraps(fun)
    def wrapper_log_function(*args, **kwargs):
        # Set up a wrapper of the function that takes args and key word
        # args.

        logger = logging.getLogger("debug-tracking")
        try:
            output = fun(*args, **kwargs)
            logger.info('Function {} ran correctly'.format(fun.__name__))
        except Exception as e:
            print(e)
            logger.exception('Exception encountered: {}'.format(e))
            output = None

        return output
    return wrapper_log_function