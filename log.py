"""Classes and functions for logging"""
import logging
import functools
import os
import time


def log_setup(logfile_name = 'clay_log', logfile_loc = False,
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


def profiler(fun):
    """
    Decorator to add time profiling to functions.

    Parameters
    ----------
    fun : python function object
        Function input.
    """

    @functools.wraps(fun)
    def wrapper_profile_function(*args, **kwargs):
    # Set up a wrapper of the function that takes args and key word
    # args.
        logger = logging.getLogger("debug-tracking")
        start = time.time()
        output = fun(*args, **kwargs)
        end = time.time()

        runtime = end-start
        print('Function {} ran in {}s.'.format(fun.__name__, runtime))

        logger.info('Function {} ran in {}s.'.format(fun.__name__, runtime))

        return output
    return wrapper_profile_function
