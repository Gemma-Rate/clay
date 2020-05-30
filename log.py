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


def function_profiler(fun):
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


class CodeBlockTimer(object):
    """
    Timer class for small code blocks (as opposed to full functions).

    Public attributes
    -----------------
    elapsed : float
        Elapsed time between timer 'start' and 'stop'.
    uselogger : Boolean
        Write timer output to log file.
    print_sc : Boolean
        Print to screen.
    logger : Logger
        Log object to write to.
    timer_name : str
        Descriptive name of timer (used for multiple objects).
    start : float
        Start of the timer.
    stop : float
        End of the timer.

    Class methods
    -----------------
    start
        Start the timer.
    finish
        Stop the timer.

    """
    def __init__(self, timer_name, uselogger=True, print_sc=True):
        self.runtime = 0.0
        self.uselogger = uselogger
        self.print_sc = print_sc
        self.logger = logging.getLogger("debug-tracking")
        self.timer_name = timer_name

        self.begin = None
        self.end = None

    def start(self):
        """Start the timer."""
        self.begin = time.time()

    def finish(self):
        """Stop the timer."""
        self.end = time.time()
        self.runtime = self.end-self.begin

        if self.uselogger:
            # Write output to file.
            self.logger.info('Timer {} ran in {}s.'.format(self.timer_name, self.runtime))
        if self.print_sc:
            print('Timer {} ran in {}s.'.format(self.timer_name, self.runtime))